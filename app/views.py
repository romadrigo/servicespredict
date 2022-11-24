from asyncio.windows_events import NULL
import json
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
import json
import numpy as np
from tablib import Dataset
from datetime import date
# Create your views here.



# from django.conf import settings
# User = settings.AUTH_USER_MODEL               