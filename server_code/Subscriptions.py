import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from functools import partial

@anvil.server.callable
def process_payment(user_id, amount):
    # Process a payment for a user
    # Implement your payment processing logic here
    pass


# user_permission_check = check_user_subscription("THE USER SUB")(pro_feature)

def has_subscription(subscription):
  return lambda user: user["subscription"] == subscription

@anvil.server.callable(require_user=has_subscription("Pro"))
def only_if_pro():
  print("Only if you're pro")
  
# new_pro_feature = check_user_subscription("THE USER SUB")(pro_feature)

@anvil.server.callable
def process_payment(user_id, amount):
    # Process a payment for a user and update their subscription status
    user = app_tables.users.get(user_id=user_id)
    
    # Implement your payment processing logic here
    # Example: Check if the payment is successful and update the user's subscription status
    if payment_successful(user_id, amount):
        user['is_subscribed'] = True
        user['last_payment_date'] = anvil.server.now_utc()
        user['subscription_status'] = 'Active'
        user['subscription_amount'] = amount
        user.save()
        return True
    else:
        return False

# Additional server-side functions for your SaaS product

def payment_successful(user_id, amount):
    # Simulate a successful payment for demonstration purposes
    # Replace this with your actual payment processing logic
    return True