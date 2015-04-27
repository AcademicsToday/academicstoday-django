from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from landpage.models import LandpageTeamMember
from landpage.models import LandpagePartner

class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py setup_academicstoday
    """
    help = 'Picks the top 9 courses with the highest student enrollment.'
    
    def handle(self, *args, **options):
        """
            Function will create the objects necessary for some of the UI
            elements in the landpage.
        """
        LandpageTeamMember.objects.all().delete()
        LandpageTeamMember.objects.create(
            id=1,
            full_name="Bartlomiej Mika",
            role="Lead Developer",
            twitter_url="https://twitter.com/BartlomiejMika",
            facebook_url="https://www.facebook.com/bartlomiej.mika",
            image_filename="bartlomiejmika.png",
            linkedin_url="https://www.linkedin.com/pub/bartlomiej-mika/3b/568/a9a",
            email="bartlomiej.mika@gmail.com",
        )
        LandpageTeamMember.objects.create(
            id=2,
            full_name="Michael Murray",
            role="Lead Designer",
            twitter_url="https://twitter.com/iamnotchad",
            facebook_url="https://www.facebook.com/michael.murray.75033149",
            image_filename="michaelmurray.png",
            github_url="https://github.com/Michael-Murray",
            email="m_poet5@hotmail.com",
        )
        LandpageTeamMember.objects.create(
            id=3,
            full_name="Sebastion Rydzewski",
            role="Developer",
            twitter_url="https://twitter.com/@srydzewski_AT",
            google_url="https://plus.google.com/u/0/108001172254765225648/posts",
            image_filename="sebastionrydzewski.png",
            linkedin_url="http://ca.linkedin.com/pub/sebastian-rydzewski/5b/108/160",
            email="srydzewski.AT@gmail.com",
        )

        LandpagePartner.objects.all().delete()
        LandpagePartner.objects.create(
            id=1,
            image_filename="duplexsoft.png",
            title="Duplexsoft",
            url="www.duplexsoft.com"
        )
        LandpagePartner.objects.create(
            id=2,
            image_filename="eurasiasoft.png",
            title="Eurasiasoft",
            url="www.eurasiasoft.com"
        )
