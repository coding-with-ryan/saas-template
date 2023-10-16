from ._anvil_designer import LoginPageTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class LoginPage(LoginPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

    anvil.js.get_dom_node(self.TEMPLATE_EXPLANATION_rich_text).classList.add("anvil-designer-only")

  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.login_with_form(allow_cancel=True, show_signup_option=True, allow_remembered=True)
    if user:
      open_form('Main')

      # TEMPLATE EXPLANATION ONLY - DELETE WHEN YOU'RE READY
      Notification("Welcome to your SaaS product's main page. For this template, we've created a very simple calculator that requires a subscription to use. Try using the calculator.", title="Template Explanation", timeout=None, style="warning").show()
      
  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    if anvil.users.get_user():
      self.outlined_card_1.visible = False
      open_form('Main')
    else:
      # Stops the glitch in rendering components if we're only going to open the main form anyway
      self.outlined_card_1.visible = True
      
      # TEMPLATE EXPLANATION ONLY - DELETE WHEN YOU'RE READY
      Notification("Here's your SaaS app's login page. To start click login and then signup for an account.", title="Template Explanation", timeout=None, style="warning").show()
    

      
    

