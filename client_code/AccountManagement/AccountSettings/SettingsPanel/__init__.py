from ._anvil_designer import SettingsPanelTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .ChangeName import ChangeName
from ... import USER

class SettingsPanel(SettingsPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.name.text = USER["name"] if USER["name"] else "-"
    self.email.text = USER["email"]
    
  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if alert(DeleteAccountAlert(), buttons=None, large=True):
      anvil.server.call('delete_user')
    else:
      print("Deletion cancelled")

  def change_name_click(self, **event_args):
    """This method is called when the link is clicked"""
    if alert(ChangeName(), title="Change name", buttons=None, dismissible=True):
      self.refresh_data_bindings()
      print("data bindings refreshed")

