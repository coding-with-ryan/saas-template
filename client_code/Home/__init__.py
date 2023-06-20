from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.features_repeating_panel.items = ({"name": "feature 1"}, {"name": "feature 2"}, {"name": "feature 3"})

  def features_data_grid_show(self, **event_args):
    """This method is called when the data grid is shown on the screen"""
    pass


