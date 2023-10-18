from ._anvil_designer import AccountSettingsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .AccountPanel import AccountPanel
from .SubscriptionPanel import SubscriptionPanel

class AccountSettings(AccountSettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.settings_main_panel.add_component(AccountPanel())

  def account_tab_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.settings_main_panel.clear()
    self.settings_main_panel.add_component(AccountPanel())

  def subscription_tab_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.settings_main_panel.clear()
    self.settings_main_panel.add_component(SubscriptionPanel())

  # TEMPLATE EXPLANATION ONLY - DELETE DELETE ROWS 30-33 WHEN YOU'RE READY
  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    Notification("Welcome to your app's account management page. Try changing your name.", title="Template Explanation", timeout=None, style="warning").show()





