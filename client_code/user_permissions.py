import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import Notification



def check_permissions(func):
  def wrapper(self, *args, **kargs):
    try:
      func(self)
    except anvil.server.PermissionDenied:
      Notification("Please upgrade your subscription to use this functionality.", title="Please upgrade your subscription", timeout=3).show()
    except anvil.users.AuthenticationFailed:
      Notification("Please log in to use this functionality.", title="Please log in", timeout=3).show()
  return wrapper