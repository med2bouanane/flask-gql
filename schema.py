import graphene
import requests
from graphene.types.resolver import dict_resolver
import json
from flask.json import jsonify

## USER
class User(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver
    id = graphene.Int()
    name = graphene.String()
    email = graphene.String()
    password = graphene.String()


class Query(graphene.ObjectType):

    users = graphene.List(User)

    def resolve_users(self, args):
        response = requests.get('http://localhost:3001/users').json()
        return response


class Token(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver
    access_token = graphene.String()


"""
## TOKEN
class Token(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver
    access_token = graphene.String()

class Query(graphene.ObjectType):
    token = graphene.Field(Token)
    def resolve_users(self, args):
        response = requests.post('http://localhost:3001/auth/login').json()
        return response"""


## MUTATION
class Login(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    # output
    class Meta:
        default_resolver = dict_resolver
    access_token = graphene.String()

    def mutate(self, info, email, password):
        user = {"email":email, "password":password}
        body_str = json.dumps(user)
        body_json = json.loads(body_str)
        response = requests.post('http://localhost:3001/auth/login', json=user).json() #Login(user=user)
        return response#jsonify(response)

class Mutation(graphene.ObjectType):
    login = Login.Field()

schema = graphene.Schema(query=Query, types=[User], mutation=Mutation)
