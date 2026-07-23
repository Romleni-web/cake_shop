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
        if not token:
            print("DEBUG: Failed to get M-Pesa OAuth Token")
            return {"ResponseCode": "1", "CustomerMessage": "Failed to authenticate with Safaricom"}

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
            "TransactionDesc": f"Payment for Order {order_id}"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        # In production, use: https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest
        if os.getenv('DEBUG') == 'False':
            url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        print(f"DEBUG: Sending STK Push request to {url} with callback {self.callback_url}")
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            print(f"DEBUG: Safaricom STK Push Status: {response.status_code}")
            return response.json()
        except Exception as e:
            print(f"DEBUG: STK Push Request Exception: {e}")
            return {"ResponseCode": "1", "CustomerMessage": str(e)}
