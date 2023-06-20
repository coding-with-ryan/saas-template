from ._anvil_designer import MainTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ..Home import Home

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.content_panel.add_component(Home(), full_width_row=True)

    if anvil.users.get_user():
      self.create_account_button.visible = False

  def create_account_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.login_with_form()

  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.login_with_form()

  def sign_out_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()



  

