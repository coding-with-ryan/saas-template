from ._anvil_designer import ChangeEmailTemplate
from anvil import *
import anvil.server

class ChangeEmail(ChangeEmailTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def save_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('change_email', self.email_text_box.text)
    self.raise_event("x-close-alert", value=self.email_text_box.text)
