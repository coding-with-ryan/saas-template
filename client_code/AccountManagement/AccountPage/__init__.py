from ._anvil_designer import AccountPageTemplate
from anvil import *
import anvil.server
import anvil.users

from ..AccountSettings import AccountSettings

class AccountPage(AccountPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def settings_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event("x-close-alert")
    alert(AccountSettings(), title=anvil.users.get_user()["email"], dismissible=True, buttons=None, large=True)

  def logout_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('LoginPage')
    self.raise_event("x-close-alert")


