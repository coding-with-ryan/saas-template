from ._anvil_designer import APP_READMETemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class APP_README(APP_READMETemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # TEMPLATE EXPLANATION ONLY - THIS FORM IS ONLY HERE TO GET YOU STARTED WITH THE TEMPLATE. IT CAN BE DELETED WHEN YOU'RE READY.