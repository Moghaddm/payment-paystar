from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.shortcuts import render
from rest_framework.response import Response
from pay_star import serializers
from rest_framework import status
from pay_star.serializers import PaymentSerializer
from django.contrib.auth import get_user_model
import json
import requests
import hashlib
import hmac

# Create your views here.


User = get_user_model()


class PaymentView(CreateAPIView):

    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            print(serializer.validated_data)

            amount = serializer.validated_data['amount']
            phone_number = serializer.validated_data['phone_number']
            url = "https://core.paystar.ir/api/pardakht/create"
            gateway_id = 'PgNWX5LST77Hs9FgJ3u9'
            header = {
                "Accept": "application/json",
                "Authorization": "Bearer " + gateway_id
            }
            sign_key = '1234'
            order_id = '45245'
            callback = 'http://127.0.0.1:8000/pay-star/callback'
            sign_data = f"{amount}#{order_id}#{callback}"
            sign = hmac.new(sign_key.encode(), sign_data.encode(), hashlib.sha512).hexdigest()

            user = User.objects.filter(phone_number=phone_number).first()
            if user is None:
                return Response(data='there is no any user for creating its transaction.',
                                status=status.HTTP_404_NOT_FOUND)
            print(user.mail)

            data = {
                'amount': amount,
                'order_id': order_id,
                'callback': callback,
                'sign': sign,
                'name': 'Mohammad Mahdi Moghaddam',
                'phone': phone_number,
                'mail': user.email,
                'description': 'just simple transaction and for testing',
                # 'wallet_hashid': 'wallet123',
                'national_code': user.national_code,
                # 'card_number': '1234567890123456'
            }

            response = requests.post(url, headers=header, json=data)
            output = json.dumps(response.json(), indent=4, ensure_ascii=False)
            print(output)

            return Response(output, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CallbackView(APIView):
    def get(self, request):
        url = "https://core.paystar.ir/api/pardakht/verify"
        gateway_id = 'PgNWX5LST77Hs9FgJ3u9'
        header = {
            "Accept": "application/json",
            "Authorization": "Bearer " + gateway_id
        }
        sign_key = '1234'
        amount = 10000.0
        ref_num = 'your_ref_num'
        card_number = 'your_card_number'
        tracking_code = 'your_tracking_code'

        sign_data = f"{amount}#{ref_num}#{card_number}#{tracking_code}"
        sign = hmac.new(sign_key.encode(), sign_data.encode(), hashlib.sha512).hexdigest()

        data = {
            'amount': amount,
            'ref_num': ref_num,
            'sign': sign,
        }
        response = requests.post(url, headers=header, json=data)
        output = json.dumps(response.json(), indent=4, ensure_ascii=False)

        return Response()
