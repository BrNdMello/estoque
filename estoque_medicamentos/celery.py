import os
from celery import Celery

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque_medicamentos.settings')

app = Celery('estoque_medicamentos')

# Configurações do Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descobrir tarefas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

