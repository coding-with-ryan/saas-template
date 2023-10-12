from ._anvil_designer import AccountPanelTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .ChangeName import ChangeName
from .ChangeEmail import ChangeEmail

from .DeleteAccountAlert import DeleteAccountAlert

class AccountPanel(AccountPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.user = anvil.users.get_user(allow_remembered=True)
    self.name.text = self.user["name"] if self.user["name"] else "-"
    self.email.text = self.user["email"]
    
  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if alert(DeleteAccountAlert(), buttons=None, large=True):
      anvil.server.call('delete_user')
      anvil.users.logout()
      print("closed alert")
      # Close Account Settings page
      self.parent.parent.parent.raise_event("x-close-alert", value=True)
      open_form('LoginPage')
      
      

  def change_name_click(self, **event_args):
    """This method is called when the link is clicked"""
    new_name = alert(ChangeName(item=anvil.users.get_user()["name"]), title="Change name", buttons=None, dismissible=True)
    if new_name:
      anvil.server.call('change_name', new_name)
      self.name.text = new_name
      self.refresh_data_bindings()

    # TEMPLATE EXPLANATION ONLY - DELETE WHEN YOU'RE READY
    Notification("Now, you've seen how the template edits user information, let's click the subscriptions tab and then click cancel subscription.", title="Template Explanation", timeout=None, style="warning").show()

  def change_email_button_click(self, **event_args):
    """This method is called when the link is clicked"""
    new_email = alert(ChangeEmail(item=anvil.users.get_user()["email"]), title="Change email", buttons=None, dismissible=True)
    if new_email:
      anvil.server.call('change_email', new_email)
      self.email.text = new_email
      self.refresh_data_bindings()

  def reset_password_button_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.users.send_password_reset_email(self.user["email"])
    alert("A password reset email has been sent to your inbox.", title="Password reset email sent")



