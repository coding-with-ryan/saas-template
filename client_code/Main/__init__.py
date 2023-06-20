from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server
from ..Home import Home

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.content_panel.add_component(Home(), full_width_row=True)
