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
  
  # Need to get the users record from the DB based on the subscription objects "customer" field
  payload_json = json.loads(anvil.server.request.body.get_bytes())
  stripe_customer_id = payload_json.get("object").get("customer")
  user = app_tables.users.get(stripe_customer_id=stripe_customer_id)

  # Check the subscription objects status: https://stripe.com/docs/api/subscriptions/object#subscription_object-status
  subscription_status = payload_json.get("object").get("status")
  # If the subscription status is "Active"
  if subscription_status == "Active":
    price_id_of_plan = payload_json.get("object").get("items").get("plan").get("id")
    # Check the price/plan and update the user record in the DB accordingly
    if price_id_of_plan == PRICES["Personal"]:
      user["subscription"] = "Personal"
    elif price_id_of_plan == PRICES["Pro"]:
      user["subscription"] = "Pro"
  else:
    user["subscription"] = "Expired"
  
  
  event = None
  payload = anvil.server.request.body
  payload_json = anvil.server.request.body_json
  sig_header = request.headers["STRIPE_SIGNATURE"]
  endpoint_secret = "we_1NsnudAp4vQdl4epdWPQpKUL"

  price_id = payload_json.get("object").get("items").get("data")[0].get("price").get("id")
  
  
  try:
    event = json.loads(anvil.server.request.body.get_bytes())
  except:
      print("⚠️  Webhook error while parsing basic request." + str(e))
      return jsonify(success=False)
  if endpoint_secret:
    # Only verify the event if there is an endpoint secret defined
    # Otherwise use the basic event deserialized with json
    sig_header = request.headers.get("stripe-signature")
    try:
      event = stripe.Webhook.construct_event(
          payload, sig_header, endpoint_secret
      )
    except stripe.error.SignatureVerificationError as e:
      print("⚠️  Webhook signature verification failed" + str(e))
      return jsonify(success=False)

  # Handle the event
  if event and (event.get("type") == "customer.subscription.created" or event.get("type") == "customer.subscription.updated"):
    # GOT TO FIND OUT WHICH USER TO UPDATE FROM THE EVENT DATA subscription.created or . updated -> customer -> customer.metadata.anvil_user_row_id -> (anvil) get_user -> updated subscription column
    event.get("type")
    user_row = app_tables.users.get_by_id(user_row_id)
    stripe_customer_id = payload_json.get("object").get("id") or payload_json.get("object").get("customer")
    if stripe_customer_id:
      app_tables.users.get_by_id()
    else:
      print("⚠️  No customer ID")
  else:
    # Unexpected event type
    print('Unhandled event type {}'.format(event['type']))

  return jsonify(success=True)


# # If Personal plan is selected Personal plan ID: price_1Ns3AAAp4vQdl4epHiqlYaIc
# if price_id == "price_1Ns3AAAp4vQdl4epHiqlYaIc":
#   user_row["subscription"] = "Personal"
#   print("User row subscription: ", user_row['subscription'])
# elif price_id == "price_1Ns3AbAp4vQdl4epxcEN5RUz":
#   user_row["subscription"] = "Pro"
#   print("User row subscription: ", user_row['subscription'])











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
  if payload_json.get("type") == "checkout.session.completed":
    # Get the user row ID we sent to Stripe earlier and reconstitute it to work with Anvil's user table
    user_row_id = "[" + payload_data_json.get("client_reference_id").replace(",", "_") + "]"
    user_row = app_tables.users.get_by_id(user_row_id)
    payment_status = payload_data_json.get("payment_status")
    print(user_row_id, payment_status)
  elif payload_json.get("type") == "payment_intent.created":
    pass 