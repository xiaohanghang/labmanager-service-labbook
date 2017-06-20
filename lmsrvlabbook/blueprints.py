from flask import Blueprint
from flask_graphql import GraphQLView
import graphene

from .api import LabbookQueries, LabbookMutations

from lmcommon.configuration import Configuration

# Load config data for the LabManager instance
config = Configuration()

# Create Blueprint
labbook_service = Blueprint('simple_page', __name__)

# Add route
labbook_service.add_url_rule('/labbook/',
                             view_func=GraphQLView.as_view('graphql',
                                                           schema=graphene.Schema(query=LabbookQueries,
                                                                                  mutation=LabbookMutations),
                                                           graphiql=config.config["flask"]["DEBUG"]))
