#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque_medicamentos.settings')
django.setup()

from django.contrib.auth import authenticate

user = authenticate(username='admin', password='admin123')
print('auth_ok=', bool(user))


