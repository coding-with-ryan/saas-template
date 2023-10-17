from ._anvil_designer import SubscriptionPanelTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class SubscriptionPanel(SubscriptionPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Replace this URL with your own
    self.manage_subscription.url = ""

    # Any code you write here will run before the form opens.
    user = anvil.users.get_user(allow_remembered=True)
    if not user["subscription"] or user["subscription"] == "expired":
      self.cancel_subscription.visible = False
