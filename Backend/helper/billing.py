
import stripe
from decouple import config
from api.models import djUser

DJANGO_DEBUG=config("DJANGO_DEBUG", default=False, cast=bool)
STRIPE_SECRET_KEY =  config("STRIPE_SECRET_KEY", default="", cast=str)

if "sk_test" in STRIPE_SECRET_KEY and not DJANGO_DEBUG:
    raise ValueError("Invalid stripe key for prod")


stripe.api_key = STRIPE_SECRET_KEY


#def create_customer(
       # name="",
      #  email="",
       # raw=False):
#
   # response = stripe.Customer.create(
    #  name=name,
      #email=email,

   # )

  #  if raw:
   #     return response
 #   stripe_id = response.id
  #  return stripe_id

def create_stripe_customer(user):
    customer = stripe.Customer.create(
        email=user.email,
        name=user.get_name(),
    )

    djUser.objects.create(
        user=user,
        stripe_customer_id=customer.id,
    )
    
    return customer

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
        cancel_url = '',
        price_stripe_id='',
        raw=True):

        if not success_url.endswith("?session_id={CHECKOUT_SESSION_ID}"):
            success_url = f"{success_url}" + "?session_id={CHECKOUT_SESSION_ID}"

        response = stripe.checkout.create(
            customer = customer_id,
            success_url=success_url,
            cancel_url=cancel_url,
            line_items=[{"price": price_stripe_id, "quantity": 1}],
            mode="payment",
        ) 

        if raw:
            return response
        return response.url 


#setattr(_user_sub_obj, 'is_active', True) this is built in python function it means 
#Set the attributed name on object to the given value 
#this equals _user_sub_obj.is_active = True 
#for k, v in update_sub_options.items():
#   setattr(_user_sub_obj, k, v)
#sets things dynamically, based on the keys and values in the dictionary  