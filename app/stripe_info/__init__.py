from app import app
import os
import stripe

stripe_keys = {
  'secret_key': "sk_test_s8zCASFgKidV07WleXsXxrzj",       ##app.config['STRIPE_SECRET_KEY'],
  'publishable_key': "pk_test_yS1w7tqtVE0gHbgHdjY957To"   ##app.config['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']