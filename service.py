import graphene
from flask import Flask

from lmsrvlabbook.blueprints import labbook_service

from lmcommon.configuration import Configuration

# Load config data for the LabManager instance
config = Configuration()

app = Flask("lmsrvlabbook")
app.config['DEBUG'] = config.config["flask"]["DEBUG"]

# Register service
app.register_blueprint(labbook_service)

if __name__ == '__main__':
    app.run()
