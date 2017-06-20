import graphene
from graphene import resolve_only_args

from .objects import Labbook

from lmcommon.labbook import LabBook


class LabbookQueries(graphene.ObjectType):
    """Entry point for all LabBook queries"""
    labbook = graphene.Field(Labbook, name=graphene.String())
    labbooks = graphene.Field(graphene.List(graphene.String), username=graphene.String())
    users = graphene.Field(graphene.List(graphene.String))

    # TODO: @randal - what is resolve only args?
    @resolve_only_args
    def resolve_labbook(self, name):
        lb = LabBook()

        # TODO: Lookup name based on logged in user
        lb.from_name("default", name)

        return Labbook(name=lb.name, id=lb.id, description=lb.description, username=lb.username)

    @resolve_only_args
    def resolve_labbooks(self, username):
        lb = LabBook()

        # TODO: Lookup name based on logged in user
        labbooks = lb.list_local_labbooks(username=username)

        return labbooks[username]

    @resolve_only_args
    def resolve_users(self):
        lb = LabBook()

        # TODO: Lookup name based on logged in user
        labbooks = lb.list_local_labbooks()

        return labbooks.keys()


