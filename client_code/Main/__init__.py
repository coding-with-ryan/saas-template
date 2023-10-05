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
    self.content_panel.add_component(Home(), full_width_row=True)
    self.check_login_buttons()

  def pricing_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(StripePricing(), large=True)

  def check_login_buttons(self):
    if anvil.users.get_user():
      if anvil.users.get_user()["subscription"] == "Free":
        self.upgrade_button.visible = True
      else:
        self.upgrade_button.visible = False
    else:
      self.upgrade_button.visible = False

  def upgrade_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(StripePricing(), large=True)

  def account_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(AccountPage(), title=anvil.users.get_user()["email"], dismissible=True, buttons=None)





    





  

