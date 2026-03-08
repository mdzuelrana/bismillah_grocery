from django.core.mail import send_mail
from django.conf import settings

def send_activation_email(user, uid, token):
    frontend_url = "https://bismillah-grocery.vercel.app"
    activation_path = f"/activate/{uid}/{token}"
    activation_link = f"{frontend_url}{activation_path}"

    subject = "Activate Your GroceryStore Account"
    message = (
        f"Hi {user.username},\n\n"
        f"Click here to activate your account:\n{activation_link}\n\n"
        "Thank you!"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])