
import stripe
from decouple import config

DJANGO_DEBUG=config("DJANGO_DEBUG", default=False, cast=bool)
STRIPE_SECRET_KEY =  config("STRIPE_SECRET_KEY", default="", cast=str)

if "sk_test" in STRIPE_SECRET_KEY and not DJANGO_DEBUG:
    raise ValueError("Invalid stripe key for prod")


stripe.api_key = STRIPE_SECRET_KEY


def create_customer(
        name="",
        email="",
        raw=False):

    response = stripe.Customer.create(
      name=name,
      email=email,

    )

    if raw:
        return response
    stripe_id = response.id
    return stripe_id

def create_product(name="",
        metadata={},
        raw=False):

    response = stripe.Customer.create(
      name=name,
      metadata=metadata,

    )

    if raw:
        return response
    stripe_id = response.id
    return stripe_id

#helper function below 

def create_price( currency="usd",
            unit_amount="9999",
            interval="month",
            
            product=None,
            metadata={},
        raw=False):
    if product is None:
        return None

    response = stripe.Customer.create(
         stripe.Price.create(
                currency=currency,
                unit_amount=unit_amount,
                recurring={"interval": interval},
                product=product,
                metadata=metadata
            )
    )

    if raw:
        return response
    stripe_id = response.id
    return stripe_id

def start_checkout_session(customer_id,
        success_url = "",
        line_items=[{"price": "price(does it need a key?", "Quantity":1 }],
        mode="payment",

        response = stripe.checkout.create
)
