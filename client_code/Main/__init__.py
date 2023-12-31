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
from ..user_permissions import PRODUCT_NAMES

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
    self.user = anvil.users.get_user()
    self.content_panel.add_component(Home(), full_width_row=True)
    self.check_upgrade_button()

    # TEMPLATE EXPLANATION ONLY - DELETE ROWS 23-24 WHEN YOU'RE READY
    self.TEMPLATE_EXPLANATION()
      
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
    
  def account_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(AccountPage(), title=self.user["email"], dismissible=True, buttons=None)

  # TEMPLATE EXPLANATION ONLY - DELETE ROWS 47-55 WHEN YOU'RE READY    
  def TEMPLATE_EXPLANATION(self):
    if anvil.users.get_user()["subscription"] in PRODUCT_NAMES and not anvil.users.get_user()["cancel_subscription_at_period_end"]:
      Notification("With your subscription set up, you can now use the calculator. Check the Users module in the template's server modules and the client code user_permissions module to see how the user permissions work.", title="Template Explanation", timeout=None, style="warning").show()
    elif anvil.users.get_user()["cancel_subscription_at_period_end"]:
      Notification("You've cancelled your subscription and, once it expires, your user records subscription status will be updated.", title="Template Explanation", timeout=None, style="warning").show()
      Notification("That's the tour of the app template complete. Now it's time for you to begin adding your own Stripe account details and finding out how to make the app your own. .", title="Template Explanation", timeout=None, style="warning").show()
    else:
      Notification("This is your SaaS product's main page. For this template, we've created a very simple calculator that requires a subscription to use. Try using the calculator.", title="Template Explanation", timeout=None, style="warning").show()