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
from flask import Flask
from flask_cors import CORS, cross_origin
import getpass
import shutil
import os

import blueprint

from lmcommon.configuration import Configuration
from lmcommon.logging import LMLogger
from lmcommon.environment import RepositoryManager

# Load config data for the LabManager instance
config = Configuration()

# Create Flask app and configure
app = Flask("lmsrvlabbook")

if config.config["flask"]["allow_cors"]:
    # Allow CORS
    CORS(app)

# Set Debug mode
app.config['DEBUG'] = config.config["flask"]["DEBUG"]

# Register service
app.register_blueprint(blueprint.complete_labbook_service)

# Setup local environment repositories
lmlog = LMLogger()
lmlog.logger.info("Cloning/Updating environment repositories.")

erm = RepositoryManager()
erm.update_repositories()
lmlog.logger.info("Indexing environment repositories.")
erm.index_repositories()
lmlog.logger.info("Environment repositories ready.")

# Empty container-container share dir as it is ephemeral
share_dir = os.path.join(os.path.sep, 'mnt', 'share')
lmlog.logger.info("Emptying container-container share folder: {}.".format(share_dir))
try:
    for item in os.listdir(share_dir):
        item_path = os.path.join(share_dir, item)
        if os.path.isfile(item_path):
            os.unlink(item_path)
        else:
            shutil.rmtree(item_path)
except Exception as e:
    lmlog.logger.error("Failed to empty share folder: {}.".format(e))
    raise

lmlog.logger.info("LabManager Ready")

if __name__ == '__main__':
    if getpass.getuser() == "giguser":
        app.run(host="0.0.0.0")
    else:
        app.run()
