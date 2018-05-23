# Copyright (c) 2017 FlashX, LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import shutil
import os
import base64

from flask import Flask, jsonify, request
import flask
from flask_cors import CORS, cross_origin
import redis
import blueprint

from lmcommon.configuration import Configuration
from lmcommon.logging import LMLogger
from lmcommon.environment import RepositoryManager
from lmcommon.auth.identity import AuthenticationError, get_identity_manager
from lmcommon.labbook.lock import reset_all_locks
from lmcommon.labbook import LabBook
from lmcommon.portmap.portmap import reset_all_ports


logger = LMLogger.get_logger()

# Create Flask app
app = Flask("lmsrvlabbook")

# Load configuration class into the flask application
random_bytes = os.urandom(32)
app.config["SECRET_KEY"] = base64.b64encode(random_bytes).decode('utf-8')
app.config["LABMGR_CONFIG"] = config = Configuration()
app.config["LABMGR_ID_MGR"] = get_identity_manager(Configuration())

if config.config["flask"]["allow_cors"]:
    # Allow CORS
    CORS(app)

# Set Debug mode
app.config['DEBUG'] = config.config["flask"]["DEBUG"]

# Register LabBook service
app.register_blueprint(blueprint.complete_labbook_service)


# Set auth error handler
@app.errorhandler(AuthenticationError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# Set Unauth'd route for API health-check
@app.route("/ping/")
@cross_origin(headers=["Content-Type", "Authorization"])
def ping():
    """Unauthorized endpoint for validating the API is up"""
    return jsonify(config.config['build_info'])


@app.route('/savehook/<jupyter_token>')
def savehook(jupyter_token):
    redis_conn = redis.Redis(db=1)
    lb_key = None
    rkeys = [k for k in redis_conn.scan_iter('*-jupyter-token')]
    for k in rkeys:
        if redis_conn.get(k) == jupyter_token:
            lb_key = k.replace('-jupyter-token')
            break

    if lb_key is None:
        logger.error('Received Jupyter save hook, but no LabBook matched')
        return

    lb = LabBook()
    lb.from_key(lb_key)
    changed_file = request.args.get('filename')
    logger.info(f"Received Jupyter save hook on {changed_file or '<unknown file>'}")
    with lb.lock_labbook():
        lb._sweep_uncommitted_changes()


# TEMPORARY KLUDGE
# Due to GitPython implementation, resources leak. This block deletes all GitPython instances at the end of the request
# Future work will remove GitPython, at which point this block should be removed.
@app.after_request
def cleanup_git(response):
    loader = getattr(flask.request, 'labbook_loader', None)
    if loader:
        for key in loader.__dict__["_promise_cache"]:
            lb = loader.__dict__["_promise_cache"][key].value
            lb.git.repo.__del__()
    return response
# TEMPORARY KLUDGE


logger.info("Cloning/Updating environment repositories.")

erm = RepositoryManager()
update_successful = erm.update_repositories()
if update_successful:
    logger.info("Indexing environment repositories.")
    erm.index_repositories()
    logger.info("Environment repositories updated and ready.")

else:
    logger.info("Unable to update environment repositories at startup, most likely due to lack of internet access.")

# Empty container-container share dir as it is ephemeral
share_dir = os.path.join(os.path.sep, 'mnt', 'share')
logger.info("Emptying container-container share folder: {}.".format(share_dir))
try:
    for item in os.listdir(share_dir):
        item_path = os.path.join(share_dir, item)
        if os.path.isfile(item_path):
            os.unlink(item_path)
        else:
            shutil.rmtree(item_path)
except Exception as e:
    logger.error(f"Failed to empty share folder: {e}.")
    raise

post_save_hook_code = """
import subprocess, os
def post_save_hook(os_path, model, contents_manager, **kwargs):
    token = open('/opt/jupyter_token').read()
    subprocess.run(f'wget https://localhost:10000/savehook/{token}?file={os.path.basename(os_path)}')
"""
os.makedirs(os.path.join(share_dir, 'jupyterhooks'))
with open(os.path.join(share_dir, 'jupyterhooks', '__init__.py'), 'w') as initpy:
    initpy.write(post_save_hook_code)


# Reset distributed lock, if desired
if config.config["lock"]["reset_on_start"]:
    logger.info("Resetting ALL distributed locks")
    reset_all_locks(config.config['lock'])
    # also reset portmap
    logger.info("Resetting ALL assigned ports")
    reset_all_ports(config)


def main(debug=False) -> None:
    try:
        # Run app on 0.0.0.0, assuming not an issue since it should be in a container
        # Please note: Debug mode must explicitly be set to False when running integration
        # tests, due to properties of Flask werkzeug dynamic package reloading.
        if debug:
            # This is to support integration tests, which will call main
            # with debug=False in order to avoid runtime reloading of Python code
            # which causes the interpreter to crash.
            app.run(host="0.0.0.0", port=10001, debug=debug)
        else:
            # If debug arg is not explicitly given then it is loaded from config
            app.run(host="0.0.0.0", port=10001)
    except Exception as e:
        logger.exception(e)
        raise


if __name__ == '__main__':
    main()
