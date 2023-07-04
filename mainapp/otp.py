from django.conf import settings
import http.client,requests,random


def phone_otp(phone_number,otp):
    try:
        url = f'https://2factor.in/API/V1/e2496452-1a3b-11ee-addf-0200cd936042/SMS/+91{phone_number}/{otp}/OTP1'
        response = requests.get(url)
    
    except Exception as e:
        return None