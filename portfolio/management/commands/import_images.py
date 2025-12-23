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
                if 'live_performance.jpg' in filename.lower():
                    description = "The Black Swing team delivering a captivating live performance."
                    title = "Live Performance"
                elif 'live_performance_trio' in filename.lower():
                    title = "Harmonizing Brass"
                    description = "Our trio delivering soulful melodies and impeccable harmony at a recent private gala."
                elif 'live_performance_sax_solo' in filename.lower():
                    title = "Saxophone Serenade"
                    description = "Capturing the deep, resonant essence of jazz with every note. Pure passion on stage."
                elif 'live_performance_quartet' in filename.lower():
                    title = "The Full Swing Experience"
                    description = "Bringing energy, elegance, and the timeless spirit of swing to life. A night to remember."
                elif 'post_performance_team_1' in filename.lower():
                    title = "Post-Show Glow"
                    description = "The team taking a moment to celebrate a successful performance. Sharp suits, great vibes."
                elif 'post_performance_team_2' in filename.lower():
                    title = "Ready for the Next Gig"
                    description = "Instruments packed, spirits high. The Black Swing team is always ready to bring the music to you."

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
                     # Simplified: If no member has this image, create one.
                    
                    role = 'other'
                    bio = 'Band member'

                    if 'ben_griffin' in filename.lower():
                        name = "Ben Griffin"
                        role = "saxophone"
                        bio = "The soul of the saxophone, bringing smooth jazz lines and energetic solos to every performance."
                    elif 'benson_mose' in filename.lower():
                        name = "Benson Mose"
                        role = "trumpet"
                        bio = "Master of the high notes, adding brilliance, power, and a touch of gold to the brass section."
                    elif 'morgan_gitonga' in filename.lower():
                        name = "Morgan Gitonga"
                        role = "trumpet"
                        bio = "A virtuoso of the trumpet, delivering sharp, precise, and soaring melodies that define the Black Swing sound."
                    elif 'denzel_ccoga' in filename.lower():
                        name = "Denzel Ccoga"
                        role = "clarinet"
                        bio = "Weaving intricate melodies with grace and precision, bridging classical technique with the spontaneous spirit of jazz."

                    self.stdout.write(f"Adding team member image: {name}")
                    TeamMember.objects.get_or_create(
                        name=name,
                        defaults={
                            'role': role,
                            'image': relative_path,
                            'bio': bio
                        }
                    )
