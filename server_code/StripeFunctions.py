import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import stripe
import json

import datetime

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = anvil.secrets.get_secret('stripe_test_api_key')

PRICES = {"personal" : "price_X", "pro" : "price_X"}

# DO I NEED TO GET THE PRICE IDs? 

@anvil.server.http_endpoint('/stripe/stripe_customer_created')
def stripe_customer_created():
  # Get the Stripe Customer ID
  payload_json = json.loads(anvil.server.request.body.get_bytes())

  # Make sure the event is in a format we expect
  try:
    event = stripe.Event.construct_from(
      payload_json, stripe.api_key
    )
  except ValueError as e:
    # Invalid payload
    return anvil.server.HttpResponse(400)
  
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
  print("user row updated: ", datetime.datetime.now())


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
  stripe_customer_id = payload_json.get("data").get("object").get("customer")

  stripe_customer = stripe.Customer.retrieve(
      stripe_customer_id
    )
  stripe_customer_email = stripe_customer["email"]
  user = app_tables.users.get(email=stripe_customer_email)

  # Check the subscription objects status: https://stripe.com/docs/api/subscriptions/object#subscription_object-status
  subscription_status = payload_json.get("data").get("object").get("status")
  # If the subscription status is "Active"
  if subscription_status == "active":
    price_id_of_plan = payload_json.get("data").get("object").get("items").get("data")[0].get("price").get("id")
    # Check the price/plan and update the user record in the DB accordingly
    if price_id_of_plan == PRICES["personal"]:
      print("Checking subscription for Personal Plan: ", datetime.datetime.now())
      user["subscription"] = "personal"
    elif price_id_of_plan == PRICES["pro"]:
      print("Checking subscription for Pro Plan: ", datetime.datetime.now())
      user["subscription"] = "pro"

    if payload_json.get("data").get("object").get("cancel_subscription_at_period_end"):
      user["cancel_subscription_at_period_end"] = True
    else:
      user["cancel_subscription_at_period_end"] = False
      
  elif subscription_status == "past_due":
    anvil.email.send(from_name = "My SaaS app", 
                 to = "",
                 subject = "Subscription Past Due",
                 text = f"""
                 A user's subscription payment has failed.
                 Email: {user["email"]}
                 Stripe Customer ID: {stripe_customer_id}                 
                 """
                 )
    user["subscription"] = "expired"
  else:
    user["subscription"] = "expired"

  anvil.server.HttpResponse(200)

@anvil.server.callable(require_user=True)
def cancel_subscription():
  user = anvil.users.get_user()
  # Need to raise an exception here if the subscription isn't cancelled
  
  try:
    stripe_customer_record = stripe.Customer.retrieve(
      user["stripe_id"],
      expand=["subscriptions"]
    )
    subscription_id = stripe_customer_record.get("subscriptions").get("data")[0].get("id")
    stripe_subsription = stripe.Subscription.delete(
      subscription_id,
    )
    # x = 1/0
  except Exception as e:
    print("Error when cancelling subscription: ", e, "\nUser ID: ", user.get_id())
  

@anvil.server.callable(require_user=True)
def delete_stripe_customer(stripe_id):
  # Need to raise an exception here if the subscription isn't deleted
  try:
    stripe.Customer.delete(stripe_id)
  except Exception as e:
    print("Error when deleting user: ", e, "\nUser ID: ", user.get_id())