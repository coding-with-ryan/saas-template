import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from .Subscriptions import has_subscription

@anvil.server.callable(require_user=has_subscription(["Personal", "Pro"]))
def calculate_percentage_of():
    percentage = (self.number_1_textbox.text / self.number_2_textbox.text) * 100
    self.percentage_label.text, self.original_number_1.text, self.original_number_2.text = str(percentage) + "%", self.number_1_textbox.text, self.number_2_textbox.text
    self.answer_rich_text.visible = True
    return percentage