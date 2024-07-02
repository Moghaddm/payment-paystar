from .models import Payment
from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    amount = serializers.IntegerField(max_value=50_000_000)


class CallbackSerializer(serializers.Serializer):
    ref_num = serializers.CharField()
    card_number = serializers.CharField()
    tracking_code = serializers.CharField()
