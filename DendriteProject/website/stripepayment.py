import stripe
from flask import request, jsonify
from flask_stripe import StripeWebhook

# My stripe secret key
stripe.api_key = "sk_test_51OSJyoSEQFnizz7cAWRTpeWkiropSU4vP947ectUgPOI6PNHUGvMC1bq4gYIUA0VMsCZZ9EYO542ZC7slHtAVSEO00aLTECWE"

# Create a stripe webhook object
stripe_webhook = StripeWebhook(app)

# Define a route that creates a checkout session for the pro license
@app.route("/check", methods=["POST"])
def create_checkout_session():
  # Get the current user
  user = get_current_user()
  # Create a stripe customer object for the user if not exists
  if not user.stripe_customer_id:
    customer = stripe.Customer.create(email=user.email)
    user.stripe_customer_id = customer.id
    db.session.commit()
  # Create a stripe checkout session object for the pro license
  session = stripe.checkout.Session.create(
    customer=user.stripe_customer_id,
    payment_method_types=["card"],
    line_items=[{
      "price": "SDF39GS93",#pro license price id
      "quantity": 1
    }],
    mode="subscription",
    success_url="https://success.com",
    cancel_url="https://cancel.com"
  )
  # Return the session id as a json response
  return jsonify({"id": session.id})

# Define a webhook handler that updates the user's pro license status after payment
@stripe_webhook.event("checkout.session.completed")
def checkout_session_completed(event):
  # Get the session object from the event data
  session = event.data.object
  # Get the customer id and subscription id from the session object
  customer_id = session.customer
  subscription_id = session.subscription
  # Query the database for the user that matches the customer id
  user = User.query.filter_by(stripe_customer_id=customer_id).first()
  # Update the user's pro license status and subscription id
  user.pro = True
  user.stripe_subscription_id = subscription_id
  db.session.commit()
  # Return a 200 response
  return "", 200
