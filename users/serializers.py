from rest_framework import serializers

from materials.services import creating_a_purchase
from users.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    subscription_url = serializers.SerializerMethodField(read_only=True)

    def get_subscription_url(self, instance):
        response = creating_a_purchase(
            product=instance.course.title,
            price=instance.course.price * 100
        )

        return response['url']

    class Meta:
        model = Payment
        fields = '__all__'
