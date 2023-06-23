from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  # def calculate_button_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   if self.number_1_textbox.text and self.number_2_textbox.text:
  #     try:
  #       percentage = anvil.server.call('calculate_percentage_of', self.number_1_textbox.text, self.number_2_textbox.text)
  #       self.original_number_1.text, self.percentage_label.text, self.original_number_2.text = self.number_1_textbox.text, str(percentage) + "%", self.number_2_textbox.text
  #       self.answer_rich_text.visible = True
  #     except anvil.server.PermissionDenied:
  #       Notification("Please upgrade").show()
  #     except anvil.users.AuthenticationFailed:
  #       Notification("Please login").show()
  #   else:
  #     Notification("Please enter two numbers.")

  def calculate_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.number_1_textbox.text and self.number_2_textbox.text:
      
      percentage = anvil.server.call('calculate_percentage_of', self.number_1_textbox.text, self.number_2_textbox.text)
      self.original_number_1.text, self.percentage_label.text, self.original_number_2.text = self.number_1_textbox.text, str(percentage) + "%", self.number_2_textbox.text
      self.answer_rich_text.visible = True
    else:
      Notification("Please enter two numbers.")
    
    
    


