from ._anvil_designer import MainTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ..Home import Home
from ..StripePricing import StripePricing

from ..AccountManagement.AccountPage import AccountPage as AccountPage

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
    self.user = anvil.users.get_user()
    self.content_panel.add_component(Home(), full_width_row=True)
    self.check_upgrade_button()
    

  def pricing_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(StripePricing(), large=True)

  def check_upgrade_button(self):
    if self.user:
      if self.user["subscription"] == "Free" or not self.user["subscription"]:
        self.upgrade_button.visible = True
      else:
        self.upgrade_button.visible = False
    else:
      self.upgrade_button.visible = False

  def upgrade_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(StripePricing(), large=True)
    # TEMPLATE EXPLANATION ONLY - DELETE WHEN YOU'RE READY
    Notification("With a subscription set up, you can now use the calculator. Check the Users module in the template's server modules and the client code user_permissions module to see how the user permissions work.", title="Template Explanation", timeout=None, style="warning").show()
    
  def account_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(AccountPage(), title=self.user["email"], dismissible=True, buttons=None)






    





  

