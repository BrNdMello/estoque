#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque_medicamentos.settings')
django.setup()

from accounts.models import User

def main():
    user, _ = User.objects.get_or_create(username='admin', defaults={
        'email': 'admin@example.com',
        'first_name': 'Administrador',
        'last_name': 'Sistema',
        'nivel_acesso': 'admin',
        'is_superuser': True,
        'is_staff': True,
        'is_active': True,
    })
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    user.set_password('admin123')
    user.save()
    print('OK: senha do admin redefinida para admin123')

if __name__ == '__main__':
    main()
