import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import datetime

# The has_subscription takes a list object and checks whether the user's subscription is valid for the decorated function
# See Utils to see it in use
def has_subscription(subscription):
  return lambda user: user["subscription"] in subscription


# Here are some example of functions you may need if you are using your own payment workflow
# Anvil comes with send http request with either the Python requests module or Anvil's http module:
# https://anvil.works/docs/http-apis/making-http-requests
@anvil.server.callable
def process_payment(user_id, amount):
    # Process a payment for a user
    # Implement your payment processing logic here
    pass

@anvil.server.callable
def process_payment(user_id, amount):
    # Process a payment for a user and update their subscription status
    user = app_tables.users.get(user_id=user_id)
    
    # Implement your payment processing logic here
    # Example: Check if the payment is successful and update the user's subscription status
    if payment_successful(user_id, amount):
        user['is_subscribed'] = True
        user['last_payment_date'] = datetime.now()
        user['subscription_status'] = 'Active'
        user['subscription_amount'] = amount
        user.save()
        return True
    else:
        return False

def payment_successful(user_id, amount):
    # Simulate a successful payment for demonstration purposes
    # Replace this with your actual payment processing logic
    return True