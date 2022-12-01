from django.core.management.base import BaseCommand
from backend.user_profile.models import *
from django.core.files.base import File


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
            cary_quad.distance = 20
            cary_quad.university = True
            cary_quad.website = "https://www.housing.purdue.edu/my-housing/options/residence-halls/cary-quad.html"
            cary_quad.tags.add('no-air-condition')
            cary_quad.save()

            cary_quad_photo = ResidenceImage()
            cary_quad_photo.belonged_residence = cary_quad
            cary_quad_photo.photo = "residence_media/cary_quad.jpeg"
            cary_quad_photo.save()

            self.stdout.write(f'cary quad was created')

            hilltop, created = Residence.objects.get_or_create(name="Hilltop Apartments")
            hilltop_location, created = Location.objects.get_or_create(streetName="Hilltop Dr", streetNum="235", zipcode="47906")
            hilltop.location = hilltop_location
            hilltop.distance = 21
            hilltop.university = True
            hilltop.website = "https://www.housing.purdue.edu/my-housing/options/apartments/hilltop.html"
            hilltop.tags.add('quiet')
            hilltop.save()

            hilltop_photo = ResidenceImage()
            hilltop_photo.belonged_residence = hilltop
            hilltop_photo.photo = "residence_media/hilltop.jpg"
            hilltop_photo.save()

            self.stdout.write(f'hilltop apartment was created')

            first_street, created = Residence.objects.get_or_create(name="First Street Towers")
            first_location, created = Location.objects.get_or_create(streetName="1st Street", streetNum="1250", zipcode="47906")
            first_street.location = first_location
            first_street.distance = 22
            first_street.university = True
            first_street.website = "https://www.housing.purdue.edu/my-housing/options/residence-halls/first-street.html"
            first_street.tags.add('close-to-class')
            first_street.save()

            first_street_photo = ResidenceImage()
            first_street_photo.belonged_residence = first_street
            first_street_photo.photo = "residence_media/first-street-towers.jpg"
            first_street_photo.save()

            self.stdout.write(f'first street was created')

            mcc, created = Residence.objects.get_or_create(name="McCutcheon Hall")
            mcc_location, created = Location.objects.get_or_create(streetName="Mccutcheon Dr", streetNum="400", zipcode="47906")
            mcc.location = mcc_location
            mcc.distance = 23
            mcc.university = True
            mcc.website = "https://www.housing.purdue.edu/my-housing/options/residence-halls/mccutcheon.html"
            mcc.tags.add('with-AC')
            mcc.save()

            mcc_photo = ResidenceImage()
            mcc_photo.belonged_residence = mcc
            mcc_photo.photo = "residence_media/mcc.jpg"
            mcc_photo.save()

            self.stdout.write(f'McCutcheon Hall was created')

            earhart, created = Residence.objects.get_or_create(name="Earhart Hall")
            earhart_location, created = Location.objects.get_or_create(streetName="1st Street", streetNum="1275", zipcode="47906")
            earhart.location = earhart_location
            earhart.distance = 24
            earhart.university = True
            earhart.website = "https://www.housing.purdue.edu/my-housing/options/residence-halls/earhart.html"
            earhart.tags.add('with-dining-court')
            earhart.save()

            earhart_photo = ResidenceImage()
            earhart_photo.belonged_residence = earhart
            earhart_photo.photo = "residence_media/earhart.jpg"
            earhart_photo.save()

            self.stdout.write(f'earhart was created')

            mer, created = Residence.objects.get_or_create(name="Meredith Hall")
            mer_location, created = Location.objects.get_or_create(streetName="N Martin Jischke Dr", streetNum="201", zipcode="47906")
            mer.location = mer_location
            mer.distance = 25
            mer.university = True
            mer.website = "https://www.housing.purdue.edu/my-housing/options/residence-halls/meredith.html"
            mer.tags.add('female-only')
            mer.save()

            mer_photo = ResidenceImage()
            mer_photo.belonged_residence = mer
            mer_photo.photo = "residence_media/meredith.jpg"
            mer_photo.save()

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




