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
  if payload_json.get("type") == "checkout.session.completed":
    # Get the user row ID we sent to Stripe earlier and reconstitute it to work with Anvil's user table
    user_row_id = "[" + payload_data_json.get("client_reference_id").replace(",", "_") + "]"
    user_row = app_tables.users.get_by_id(user_row_id)
    payment_status = payload_data_json.get("payment_status")
    print(user_row_id, payment_status)
  elif payload_json.get("type") == "payment_intent.created":
    pass 

@anvil.server.http_endpoint('/stripe/stripe_customer_created')
def stripe_customer_created():
  payload_json = json.loads(anvil.server.request.body.get_bytes())
  stripe_customer_id = payload_json.get("object").get("id")
  user_row_id = "[" + payload_data_json.get("client_reference_id").replace(",", "_") + "]"
  stripe.Customer.modify(
    stripe_customer_id,
    metadata={"anvil_user_row_id": user_row_id},
  )

@anvil.server.http_endpoint('/stripe/stripe_scubscription_updated')
def stripe_subscription_updated():
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
    # If Personal plan is selected Personal plan ID: price_1Ns3AAAp4vQdl4epHiqlYaIc
    if price_id == "price_1Ns3AAAp4vQdl4epHiqlYaIc":
      user_row["subscription"] = "Personal"
    elif price_id == "price_1Ns3AbAp4vQdl4epxcEN5RUz":
      user_row["subscription"] = "Pro"
  else:
    # Unexpected event type
    print('Unhandled event type {}'.format(event['type']))

  return jsonify(success=True)





    
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'customer.subscription.created':
      subscription = event['data']['object']
    elif event['type'] == 'customer.subscription.updated':
      subscription = event['data']['object']
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)

    
    
  

 
  