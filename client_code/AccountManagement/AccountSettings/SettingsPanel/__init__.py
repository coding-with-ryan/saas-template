from ._anvil_designer import SettingsPanelTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class SettingsPanel(SettingsPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    user = anvil.users.get_user()
    self.name.text = user["name"] if user["name"] else "-"
    self.email.text = user["email"]
    
  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if alert(DeleteAccountAlert(), buttons=None, large=True):
      anvil.server.call('delete_user')
    else:
      print("Deletion cancelled")
