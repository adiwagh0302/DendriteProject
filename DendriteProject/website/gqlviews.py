from flask import Flask
from flask_graphql import GraphQLView
from flask_keycloak import Keycloak
from flask_jwt_extended import JWTManager

gqlviews = Blueprint('views', __name__)


# Configure the app with keycloak and jwt settings
app.config["KEYCLOAK_SERVER_URL"] = "https://keycloakserver.com"
app.config["KEYCLOAK_REALM"] = "myrealm"
app.config["KEYCLOAK_CLIENT_ID"] = "clientid"
app.config["KEYCLOAK_CLIENT_SECRET"] = "client secret"
app.config["JWT_SECRET_KEY"] = "your jwt secret key"

# Initialize keycloak and jwt extensions
keycloak = Keycloak(app)
jwt = JWTManager(app)

# Define a function that returns the current user from the keycloak token
def get_current_user():
  # Get the token identity from the jwt
  token_identity = get_jwt_identity()
  # Get the user info from the keycloak client
  user_info = keycloak.client.userinfo(token_identity)
  # Query the database for the user that matches the user info
  user = User.query.filter_by(email=user_info["email"]).first()
  # Return the user object
  return user

# Define a function that adds the current user to the graphql context
def context_factory():
  # Get the current user
  user = get_current_user()
  # Return a dictionary with the user as the context
  return {"user": user}

# Register a graphql view with the schema object and the context factory
app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, context=context_factory, graphiql=True))
