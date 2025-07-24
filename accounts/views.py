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


# Set up logging
logger = logging.getLogger(__name__)


def empty(request):
    return render(request,'page.html')

def home(request):
    return render(request,'index.html')



def connect(request):
    return render(request,'connect_wallet.html')
