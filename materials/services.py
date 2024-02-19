import stripe

from config.settings import STRIPE_KEY

stripe.api_key = STRIPE_KEY


def creating_a_purchase(product: str, price: int):
    subscription_product = stripe.Product.create(
        name=product,
    )

    subscription_price = stripe.Price.create(
        unit_amount=price,
        currency="rub",
        recurring={"interval": "month"},
        product=subscription_product['id'],
    )

    subscription_session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[{"price": subscription_price['id'], "quantity": 1}],
        mode="payment",
    )

    return subscription_session




