import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import stripe

# Initialize Stripe with your secret key
stripe.api_key = anvil.secrets.get_secret('stripe_live_key')

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

@anvil.server.http_endpoint('/stripe/subscrription_change/list',  methods=["POST", "HEAD"])
def register_subscription_change():
  if anvil.server.request.method == "HEAD":
    return {}