import os
from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import Project, TeamMember
from django.core.files import File

class Command(BaseCommand):
    help = 'Imports images from media directories into the database'

    def handle(self, *args, **options):
        self.import_portfolio()
        self.import_team()

    def import_portfolio(self):
        images_dir = os.path.join(settings.MEDIA_ROOT, 'portfolio_images')
        if not os.path.exists(images_dir):
            self.stdout.write(self.style.WARNING(f"Directory not found: {images_dir}"))
            return

        for filename in os.listdir(images_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Check if exists
                # We interpret the title from filename
                title = filename.rsplit('.', 1)[0].replace('_', ' ').title()
                
                # Special case for the image provided by user
                description = ""
                if 'live_performance' in filename.lower():
                    description = "The Black Swing team delivering a captivating live performance."
                    title = "Live Performance"

                # Check if a project with this image path already exists to avoid duplicates
                # This is a bit tricky since ImageField stores relative path.
                relative_path = f'portfolio_images/{filename}'
                
                if not Project.objects.filter(image=relative_path).exists():
                    self.stdout.write(f"Adding project: {title}")
                    project = Project(
                        title=title,
                        description=description,
                        category='live', # Default category
                        image=relative_path
                    )
                    project.save()
                else:
                    self.stdout.write(f"Skipping existing: {filename}")

    def import_team(self):
        images_dir = os.path.join(settings.MEDIA_ROOT, 'team_images')
        if not os.path.exists(images_dir):
            return

        for filename in os.listdir(images_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                name = filename.rsplit('.', 1)[0].replace('_', ' ').title()
                relative_path = f'team_images/{filename}'
                
                if not TeamMember.objects.filter(image=relative_path).exists():
                     # Try to find a member with this name to update, or create new?
                     # Ideally we just update the image of existing member if name matches, or create new.
                     # Let's simple create new if not exists, but names might collide.
                     # Simplified: If no member has this image, create one.
                    self.stdout.write(f"Adding team member image: {name}")
                    TeamMember.objects.get_or_create(
                        name=name,
                        defaults={
                            'role': 'other',
                            'image': relative_path,
                            'bio': 'Band member'
                        }
                    )
