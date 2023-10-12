from ._anvil_designer import AccountSettingsTemplate
from anvil import *
import anvil.server
import anvil.users

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




