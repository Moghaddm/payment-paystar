from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.shortcuts import render
from rest_framework.response import Response
from pay_star import serializers
from rest_framework import status
from pay_star.serializers import PaymentSerializer, CallbackSerializer
from django.contrib.auth import get_user_model
from .models import Payment
import json
import requests
import hashlib
import hmac

# Create your views here.


User = get_user_model()


class PaymentView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data

            amount = validated_data.get('amount')
            phone_number = validated_data.get('phone_number')
            url = "https://core.paystar.ir/api/pardakht/create"
            gateway_id = 'PgNWX5LST77Hs9FgJ3u9'
            header = {
                "Accept": "application/json",
                "Authorization": "Bearer " + gateway_id
            }
            sign_key = '1234'
            order_id = '45245'
            callback = 'http://127.0.0.1:8000/api/payment/callback'
            sign_data = f"{amount}#{order_id}#{callback}"
            sign = hmac.new(sign_key.encode(), sign_data.encode(), hashlib.sha512).hexdigest()

            user = User.objects.filter(phone_number=phone_number).first()
            if user is None:
                return Response(data='there is no any user for creating its transaction.',
                                status=status.HTTP_404_NOT_FOUND)

            data = {
                'amount': amount,
                'order_id': order_id,
                'callback': callback,
                'sign': sign,
                'phone': phone_number,
                'mail': user.email,
                'description': 'just simple transaction and for testing',
                'national_code': user.national_code,
            }

            response = requests.post(url, headers=header, json=data)
            output = json.dumps(response.json(), indent=4, ensure_ascii=False)
            output_dict = json.loads(output)

            if output_dict['status'] == 'unauthenticated':
                return Response(output, status=status.HTTP_400_BAD_REQUEST)

            ref_num = output_dict['data']['ref_num']
            Payment.objects.create(amount=amount, user=user, ref_num=ref_num)

            print(output_dict)

            return Response(output_dict['data']['token'], status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CallbackView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CallbackSerializer

    def post(self, request, *args, **kwargs):
        url = "https://core.paystar.ir/api/pardakht/verify"
        gateway_id = 'PgNWX5LST77Hs9FgJ3u9'
        header = {
            "Accept": "application/json",
            "Authorization": "Bearer " + gateway_id
        }
        sign_key = '1234'
        amount = 10000.0
        ref_num = request.data.get('ref_num')
        card_number = request.data.get('card_number')
        tracking_code = request.data.get('tracking_code')

        sign_data = f"{amount}#{ref_num}#{card_number}#{tracking_code}"
        sign = hmac.new(sign_key.encode(), sign_data.encode(), hashlib.sha512).hexdigest()

        data = {
            'amount': amount,
            'ref_num': ref_num,
            'sign': sign,
        }
        response = requests.post(url, headers=header, json=data)
        output = json.dumps(response.json(), indent=4, ensure_ascii=False)
        output_dict = json.loads(output)

        return Response(
            f'transaction occurred successfully. with {ref_num} reference number and {output_dict['data']['price']} price.')
