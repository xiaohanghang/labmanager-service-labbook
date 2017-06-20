import graphene


class Labbook(graphene.ObjectType):
    """The LabBook type that represents a LabBook instance on disk"""
    # A unique identifier for the LabBook
    id = graphene.ID()

    # The name of the LabBook. Must be unique to what exists locally and unique in a user's library when pushing
    # Only A-Za-z0-9- allowed
    name = graphene.String()

    # A short description of the LabBook limited to 140 UTF-8 characters
    description = graphene.String()

    # The username of the owner - To be replaced with a proper User interface
    username = graphene.String()


class Labbooks(graphene.ObjectType):
    """The LabBook type that represents a LabBook instance on disk"""
    labbook_names = graphene.List(graphene.String)


class Users(graphene.ObjectType):
    """The LabBook type that represents a LabBook instance on disk"""
    usernames = graphene.List(graphene.String)
