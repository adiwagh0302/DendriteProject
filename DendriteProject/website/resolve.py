from ariadne import scalar
from sqlalchemy_utils import ImageType

# Define a custom scalar type for images
@scalar(ImageType)
def serialize_image(value):
  # Convert the image value to a base64 encoded string
  return value.encode("base64")

# Define a query resolver that returns all the todos for the current user
def resolve_todos(obj, info):
  # Get the current user from the keycloak token
  user = info.context["user"]
  # Query the database for the todos that belong to the user
  todos = Todo.query.filter_by(user_id=user.id).all()
  # Return the todos as a list
  return todos

# Define a mutation resolver that creates a new todo for the current user
def resolve_create_todo(obj, info, title, description, time, image=None):
  # Get the current user from the keycloak token
  user = info.context["user"]
  # Check if the user has a pro license
  if image and not user.pro:
    # Raise an error if the user tries to upload an image without a pro license
    raise Exception("You need a pro license to upload images in your todos")
  # Create a new todo object with the given arguments
  todo = Todo(title=title, description=description, time=time, image=image, user_id=user.id)
  # Add the todo to the database session
  db.session.add(todo)
  # Commit the changes to the database
  db.session.commit()
  # Return the todo object
  return todo

# Define a mutation resolver that updates an existing todo for the current user
def resolve_update_todo(obj, info, id, title=None, description=None, time=None, image=None):
  # Get the current user from the keycloak token
  user = info.context["user"]
  # Check if the user has a pro license
  if image and not user.pro:
    # Raise an error if the user tries to upload an image without a pro license
    raise Exception("You need a pro license to upload images in your todos")
  # Query the database for the todo that matches the id and belongs to the user
  todo = Todo.query.filter_by(id=id, user_id=user.id).first()
  # Raise an error if the todo is not found
  if not todo:
    raise Exception("Todo not found")
  # Update the todo attributes with the given arguments
  if title:
    todo.title = title
  if description:
    todo.description = description
  if time:
    todo.time = time
  if image:
    todo.image = image
  # Commit the changes to the database
  db.session.commit()
  # Return the todo object
  return todo

# Define a mutation resolver that deletes an existing todo for the current user
def resolve_delete_todo(obj, info, id):
  # Get the current user from the keycloak token
  user = info.context["user"]
  # Query the database for the todo that matches the id and belongs to the user
  todo = Todo.query.filter_by(id=id, user_id=user.id).first()
  # Raise an error if the todo is not found
  if not todo:
    raise Exception("Todo not found")
  # Delete the todo from the database session
  db.session.delete(todo)
  # Commit the changes to the database
  db.session.commit()
  # Return True to indicate success
  return True

# Create a schema object from the type definitions and resolvers
schema = make_executable_schema(type_defs, resolvers)
