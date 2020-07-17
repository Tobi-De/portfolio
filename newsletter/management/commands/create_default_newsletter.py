from django.core.management.base import BaseCommand

from ...models import Newsletter


class Command(BaseCommand):
    help = "This command is there to create the default newsletter."

    def add_arguments(self, parser):
        parser.add_argument("-t", "--title", type=str, help="title for the newslette")
        parser.add_argument("-d", "--description", type=str, help="description for the newslette")

    def handle(self, *args, **options):
        title = options["title"] if options["title"] else "default"
        description = options["description"] if options["description"] else "default newsletter"
        if not Newsletter.objects.filter(title=title).exists():
            Newsletter.objects.create(title=title, description=description)
