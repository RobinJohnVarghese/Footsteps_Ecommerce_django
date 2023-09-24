import random
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(1111, 9999))

def send_otp_email(email, otp):
    subject = 'OTP for Sign Up/Sign In'
    message = f'Your OTP is: {otp}'
    from_email = 'robinvarghesjohn@gmail.com'  # Replace with your email address
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)