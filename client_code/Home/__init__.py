from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

from ..user_permissions import catch_permission_errors
from ..AccountManagement.DeleteAccountAlert import DeleteAccountAlert as DeleteAccountAlert



class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  # Catch_permission_errors catches excpetions that are thrown by a user not being subscribed and gives them a notification to upgrade
  @catch_permission_errors
  # This function is a simple example function to show you functionality that is gated behind a paywall
  def calculate_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.number_1_textbox.text and self.number_2_textbox.text:
      percentage = anvil.server.call('calculate_percentage_of', self.number_1_textbox.text, self.number_2_textbox.text)
      self.original_number_1.text, self.percentage_label.text, self.original_number_2.text = self.number_1_textbox.text, str(percentage) + "%", self.number_2_textbox.text
      self.answer_rich_text.visible = True
    else:
      Notification("Please enter two numbers.")

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('cancel_subscription')

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    if alert(DeleteAccountAlert(), buttons=None, large=True):
      anvil.server.call('delete_user')
    else:
      print("Deletion cancelled")


    
    
    


