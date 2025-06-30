import time

def send_notification(email: str):
    print(f'Sending confirmation email to {email}')
    time.sleep(2)
    print(f"Confirmation email sent to {email}")