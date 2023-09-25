import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import stripe
import json


# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = anvil.secrets.get_secret('stripe_test_api_key')

PRICES = {"Personal" : "price_1Ns3AAAp4vQdl4epHiqlYaIc", "Pro" : "price_1Ns3DHAp4vQdl4ep3xtVZZ54"}

@anvil.server.http_endpoint('/stripe/stripe_customer_created')
def stripe_customer_created():
  # Get the Stripe Customer ID
  payload_json = json.loads(anvil.server.request.body.get_bytes())
  stripe_customer_id = payload_json.get("data").get("object").get("id")

  # Get the Anvil user's row ID and transform it to work with Stripes API
  stripe_customer_email = payload_json.get("data").get("object").get("email")
  user_row = app_tables.users.get(email=stripe_customer_email)
  user_row_id = user_row.get_id()
  transformed_user_row_id = user_row_id[1:-1].replace(",", "_")

  # Update the customer record, so the row_id is always available
  stripe.Customer.modify(
    stripe_customer_id,
    metadata={"anvil_user_row_id": transformed_user_row_id},
  )

  # Update the user record in the Anvil app to include the Stripe Customer ID
  user_row.update(stripe_id=stripe_customer_id)


@anvil.server.http_endpoint('/stripe/stripe_subscription_updated')
def stripe_subscription_updated():
  # Here we want to look for "customer.subscription.updated" because this event is what shows whether a subscription is valid or not. Events like "customer.subscription.created" are similar but are called before a charge is attempted and is usually followed by "customer.subscription.updated".

  payload_json = json.loads(anvil.server.request.body.get_bytes())

  # Make sure the event is in a format we expect
  try:
    event = stripe.Event.construct_from(
      payload_json, stripe.api_key
    )
  except ValueError as e:
    # Invalid payload
    return anvil.server.HttpResponse(400)
  
  # Need to get the users record from the DB based on the subscription objects "customer" field
  print(payload_json)
  stripe_customer_id = payload_json.get("data").get("object").get("customer")
  user = app_tables.users.get(stripe_id=stripe_customer_id)

  # Check the subscription objects status: https://stripe.com/docs/api/subscriptions/object#subscription_object-status
  subscription_status = payload_json.get("data").get("object").get("status")
  # If the subscription status is "Active"
  print(subscription_status)
  print(user)
  if subscription_status == "active":
    print("active")
    price_id_of_plan = payload_json.get("data").get("object").get("items").get("plan").get("id")
    # Check the price/plan and update the user record in the DB accordingly
    if price_id_of_plan == PRICES["Personal"]:
      user["subscription"] = "Personal"
    elif price_id_of_plan == PRICES["Pro"]:
      user["subscription"] = "Pro"
  else:
    user["subscription"] = "Expired"

  anvil.server.HttpResponse(200)











###############
##############
##############
def cancel_subscription(subscription_id):
    pass

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
  user_row = app_tables.users.get_by_id(user_row_id)
  payment_status = payload_data_json.get("payment_status")