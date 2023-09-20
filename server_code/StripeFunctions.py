import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import stripe
import json


# Initialize Stripe with your secret key
stripe.api_key = anvil.secrets.get_secret('stripe_test_api_key')

def create_subscription(customer_email, payment_method_id, plan_id):
    try:
        # Create a customer
        customer = stripe.Customer.create(
            email=customer_email,
            payment_method=payment_method_id,
            invoice_settings={
                'default_payment_method': payment_method_id
            }
        )

        # Subscribe the customer to a plan
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    'price': plan_id,
                },
            ],
        )

        return subscription

    except stripe.error.StripeError as e:
        return str(e)

def cancel_subscription(subscription_id):
    try:
        # Cancel the subscription
        canceled_subscription = stripe.Subscription.update(
            subscription_id,
            cancel_at_period_end=True
        )

        return canceled_subscription

    except stripe.error.StripeError as e:
        return str(e)

def check_subscription_status(subscription_id):
    try:
        # Retrieve the subscription
        subscription = stripe.Subscription.retrieve(subscription_id)
        return subscription.status

    except stripe.error.StripeError as e:
        return str(e)

@anvil.server.http_endpoint('/stripe/stripe_checkout_completed')
def stripe_checkout_completed():

  # This should work but there's a bug that Ian has fixed that I'm waiting to propogate on the Anvil servers
  # payload_json = anvil.server.request.body_json
  # We'll use this as a workaround for now:
  payload_json = json.loads(anvil.server.request.body.get_bytes())
  payload_data_json = payload_json.get("data").get("object")

  # Get the user row ID we sent to Stripe earlier and reconstitute it to work with Anvil's user table
  user_row_id = "[" + payload_data_json.get("client_reference_id").replace(",", "_") + "]"
  print(user_row_id)

  payment_status = payload_data_json.get("paymeny_status")
  print(payment_status)
  
  return user_row_id, payment_status
 
  