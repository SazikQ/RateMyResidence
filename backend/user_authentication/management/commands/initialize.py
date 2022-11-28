from django.core.management.base import BaseCommand
from backend.user_profile.models import *


class Command(BaseCommand):
    """
    initializes residences and reviews

    Create a superuser if none exist
    Example:
        manage.py createsuperuser_if_none_exists --user=admin --password=changeme
    """

    def add_arguments(self, parser):
        parser.add_argument("--user", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--email", default="admin@example.com")

    def handle(self, *args, **options):

        if not Residence.objects.filter(name="Cary Quad").exists():
            cary_quad, created = Residence.objects.get_or_create(name="Cary Quad")
            cary_location, created = Location.objects.get_or_create(streetName="W Stadium Ave", streetNum="1016", zipcode="47906")
            cary_quad.location = cary_location
            cary_quad.save()
            self.stdout.write(f'cary quad was created')

            hilltop, created = Residence.objects.get_or_create(name="Hilltop Apartments")
            hilltop_location, created = Location.objects.get_or_create(streetName="Hilltop Dr", streetNum="235", zipcode="47906")
            hilltop.location = hilltop_location
            hilltop.save()
            self.stdout.write(f'hilltop apartment was created')

            first_street, created = Residence.objects.get_or_create(name="First Street Towers")
            first_location, created = Location.objects.get_or_create(streetName="1st Street", streetNum="1250", zipcode="47906")
            first_street.location = first_location
            first_street.save()
            self.stdout.write(f'first street was created')

            mcc, created = Residence.objects.get_or_create(name="McCutcheon Hall")
            mcc_location, created = Location.objects.get_or_create(streetName="Mccutcheon Dr", streetNum="400", zipcode="47906")
            mcc.location = mcc_location
            mcc.save()
            self.stdout.write(f'McCutcheon Hall was created')

            earhart, created = Residence.objects.get_or_create(name="Earhart Hall")
            earhart_location, created = Location.objects.get_or_create(streetName="1st Street", streetNum="1275", zipcode="47906")
            earhart.location = earhart_location
            earhart.save()
            self.stdout.write(f'earhart was created')

            mer, created = Residence.objects.get_or_create(name="Meredith Hall")
            mer_location, created = Location.objects.get_or_create(streetName="N Martin Jischke Dr", streetNum="201", zipcode="47906")
            mer.location = mer_location
            mer.save()
            self.stdout.write(f'Meredith Hall was created')
        else:
            self.stdout.write(f'residences already exist')


        if User.objects.filter(username='admin').exists():
            self.stdout.write(f'Superuser already exists')
            return
        username = options["user"]
        password = options["password"]
        email = options["email"]
        User.objects.create_superuser(username=username, password=password, email=email)
        self.stdout.write(f'Superuser "{username}" was created')




