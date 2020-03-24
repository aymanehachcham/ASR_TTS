from django.contrib.auth.models import User

def run():
    current_user = User.objects.filter(username='administrator').first()
    if not current_user:
        User.objects.create_superuser('administrator', '', '123456789')
