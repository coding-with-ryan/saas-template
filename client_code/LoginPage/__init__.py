from ._anvil_designer import LoginPageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class LoginPage(LoginPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    

  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.login_with_form(allow_cancel=True, show_signup_option=True, allow_remembered=True)
    if user:
      open_form('Main')

      # TEMPLATE EXPLANATION ONLY - DELETE WHEN YOU'RE READY
      alert("Welcome to your SaaS product's main page. For this template, we've created a very simple calculator that requires a subscription to use. Try using the calculator.", large=True)

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    if anvil.users.get_user():
      open_form('Main')
    else:
      # Stops the glitch in rendering components if we're only going to open the main form anyway
      self.outlined_card_1.visible = True

      
    

