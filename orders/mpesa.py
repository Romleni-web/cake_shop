import requests
import base64
from datetime import datetime
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()

class MpesaClient:
    def __init__(self):
        self.consumer_key = os.getenv('MPESA_CONSUMER_KEY')
        self.consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
        self.shortcode = os.getenv('MPESA_SHORTCODE')
        self.passkey = os.getenv('MPESA_PASSKEY')
        self.callback_url = os.getenv('MPESA_CALLBACK_URL')
        self.base_url = "https://sandbox.safaricom.co.ke"

    def get_token(self):
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(url, auth=(self.consumer_key, self.consumer_secret))
        return response.json().get('access_token')

    def stk_push(self, phone_number, amount, order_id):
        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}"}
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{self.shortcode}{self.passkey}{timestamp}".encode()).decode()

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": f"Order{order_id}",
            "TransactionDesc": "Payment for Melanin Cake House Order"
        }

        url = f"{self.base_url}/mpesa/stkpush/v1/query" # Note: Correcting URL to process in actual usage
        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"

        response = requests.post(url, json=payload, headers=headers)
        return response.json()
