from ._anvil_designer import StripePricingTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# This is a custom HTML form built using Stripe's pricing table solution
# https://stripe.com/docs/payments/checkout/pricing-table
# You can either do the same with your payment provider of choice or build a form to accept payments using Anvil components

class StripePricing(StripePricingTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

    # Add user ID to subscription screen
    user_id = anvil.users.get_user().get_id()
    # Reconstitute the user_id for the Stripe API to accept - see: https://stripe.com/docs/payments/checkout/pricing-table#track-subscriptions
    # To reverse it "[" + user_id.replace("_", ",") + "]"
    user_id = user_id[1:-1].replace(",", "_")
    self.dom_nodes["stripe-pricing-table"].setAttribute("client-reference-id", user_id)


