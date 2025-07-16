from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Create an API token for a user (for n8n automation)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username to create token for',
            default='admin'
        )
        parser.add_argument(
            '--create-user',
            action='store_true',
            help='Create user if it doesn\'t exist'
        )

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"Found user: {username}")
        except User.DoesNotExist:
            if options['create_user']:
                password = 'api_user_password_123!'
                user = User.objects.create_user(
                    username=username,
                    password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {username} with password: {password}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'User {username} does not exist. Use --create-user to create it.')
                )
                return

        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created new API token for {username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Token already exists for {username}')
            )
        
        self.stdout.write(f'\n' + '='*50)
        self.stdout.write(f'API Token: {token.key}')
        self.stdout.write(f'User: {username}')
        self.stdout.write(f'='*50)
        self.stdout.write(f'\nAPI Endpoints you can use:')
        self.stdout.write(f'• Base URL: http://127.0.0.1:8000/api/v1/blog/')
        self.stdout.write(f'• Create Post: POST /api/v1/blog/create-post/')
        self.stdout.write(f'• List Posts: GET /api/v1/blog/posts/')
        self.stdout.write(f'• Bulk Create: POST /api/v1/blog/bulk-create/')
        self.stdout.write(f'• Health Check: GET /api/v1/blog/health/')
        self.stdout.write(f'\nAuthentication Header:')
        self.stdout.write(f'Authorization: Token {token.key}')
        self.stdout.write(f'\n' + '='*50) 