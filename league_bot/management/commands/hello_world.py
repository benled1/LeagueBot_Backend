from django.core.management.base import BaseCommand
from league_bot.models import Test

class Command(BaseCommand):
    help="This is the hellow_world command"

    def handle(self, *args, **kwargs):
        test_object = Test.objects.create(
            first_attr = "This is first attribute."
        )
        self.stdout.write(self.style.SUCCESS(f"{test_object.first_attr}"))

    
