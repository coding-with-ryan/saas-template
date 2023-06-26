import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# def bar(greeting):
#     def wrapper(f):
#         def func(*args, **kargs):
#             print(greeting)
#             return f(*args, **kargs)
#         return func
#     return wrapper

# @bar("New Greeting")
# def foo(name):
#     print(f"Hello, {name}")
#     return name

# # foo = bar("New Greeting")(foo)

# print(foo("Ryan"))
# # foo("Meredydd")


def check_permissions():
  def wrapper(f):
    def func(*args, **kargs):
      try:
        f()
      except anvil.server.PermissionDenied:
        Notification("Please upgrade your subscription").show()
      except anvil.users.AuthenticationFailed:
        Notification("Please login").show()
      return f(*args, **kargs)
    return func
  return wrapper