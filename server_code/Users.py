import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server




@anvil.server.callable(require_user=True)
def change_name(name):
  user = anvil.users.get_user()
  user["name"] = name

@anvil.server.callable(require_user=True)
def change_email(email):
  user = anvil.users.get_user()
  user["email"] = email

@anvil.server.callable(require_user=True)
def delete_user():
  user = anvil.users.get_user()
  # Need to raise an exception here if the subscription isn't deleted
  if user["stripe_id"]:
    pass
  try:
    stripe.Customer.delete(user["stripe_id"])
    user.delete()