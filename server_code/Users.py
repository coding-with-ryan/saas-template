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