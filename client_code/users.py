import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def bar(greeting):
    def wrapper(f):
        def func(*args, **kargs):
            print(greeting)
            return f(*args, **kargs)
        return func
    return wrapper

@bar("New Greeting")
def foo(name):
    print(f"Hello, {name}")
    return name

# foo = bar("New Greeting")(foo)

print(foo("Ryan"))
# foo("Meredydd")

def check_permissions():
  def wrapper(f):
    def func(*args, **kargs):
      try:
        f()
        
      return f(*args, **kargs)
    return func
  return wrapper


try:
  percentage = anvil.server.call('calculate_percentage_of', self.number_1_textbox.text, self.number_2_textbox.text)
  self.original_number_1.text, self.percentage_label.text, self.original_number_2.text = self.number_1_textbox.text, str(percentage) + "%", self.number_2_textbox.text
  self.answer_rich_text.visible = True
except anvil.server.PermissionDenied:
  Notification("Please upgrade").show()
except anvil.users.AuthenticationFailed:
  Notification("Please login").show()