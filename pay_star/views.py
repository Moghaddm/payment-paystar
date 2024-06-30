from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from pay_star import serializers
from rest_framework import status
from pay_star.serializers import PaymentSerializer
import json
import requests
import hashlib
import hmac

# Create your views here.

class PaymentView(APIView):
    def post(self,request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            phone_number = serializer.validated_data['phone_number']
            
            url = "https://core.paystar.ir/api/pardakht/create"
            gateway_id = 'your_gateway_id'
            header = {
                "Accept": "application/json",
                "Authorization" : "Bearer " + gateway_id
            }

            sign_key = 'your_sign_key'
            amount = 10000.0
            order_id = '45245'
            callback = 'http://127.0.0.1:8000/pay-star/callback'

            sign_data = f"{amount}#{order_id}#{callback}"
            sign = hmac.new(sign_key.encode(), sign_data.encode(), hashlib.sha512).hexdigest()

            data = {
                'amount': amount,
                'order_id': order_id,
                'callback': 'https://example.com/callback',
                'sign': sign,
                'name': 'علی مرادی',
                'phone': '09345678910',
                'mail': 'john@example.com',
                'description': 'توضیحات تراکنش ',
                'wallet_hashid': 'wallet123',
                'national_code': '0234567891',
                'card_number': '1234567890123456'
            }
            response = requests.post(url, headers=header, json=data)
            output = json.dumps(response.json(), indent=4, ensure_ascii=False)
                        
            return Response(output,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CallbackView(APIView):
    def get(self,request):
        
        url = "https://core.paystar.ir/api/pardakht/verify"
        gateway_id = 'your_gateway_id'
        header = {
            "Accept": "application/json",
            "Authorization" : "Bearer " + gateway_id
        }

        sign_key = 'your_sign_key'
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
            