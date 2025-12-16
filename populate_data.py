import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'black_swing.settings')
django.setup()

from django.core.files import File
from portfolio.models import Project, TeamMember

def populate_data():
    # Clear existing data to avoid duplicates (optional, comment out if safer)
    # Project.objects.all().delete()
    # TeamMember.objects.all().delete()

    # Portfolio Items
    portfolio_items = [
        {'title': 'Live Performance - Event 1', 'category': 'live', 'image_path': 'static/img/masonry-portfolio/event_1.jpg'},
        {'title': 'Live Performance - Event 2', 'category': 'live', 'image_path': 'static/img/masonry-portfolio/event_2.jpg'},
        {'title': 'Live Performance - Event 3', 'category': 'live', 'image_path': 'static/img/masonry-portfolio/event_3.jpg'},
        {'title': 'Live Performance - Event 4', 'category': 'live', 'image_path': 'static/img/masonry-portfolio/event_4.jpg'},
    ]

    for item in portfolio_items:
        if not Project.objects.filter(title=item['title']).exists():
            project = Project(
                title=item['title'],
                category=item['category'],
                description="Black Swing Live Event Performance"
            )
            # We can only save the image if the file exists. 
            # In development, static files are in static/.
            # ImageField usually serves from MEDIA_ROOT.
            # We will manually save the file reference or copy it.
            # For simplicity in this script, we assume specific paths.
            
            # NOTE: ImageField saves to MEDIA_ROOT. Linking to STATIC isn't standard for ImageField.
            # We'll just skip image file creation in this script to avoid path complexity issues
            # and let the user add them via dashboard OR we try to open it.
            # trying to open:
            if os.path.exists(item['image_path']):
                with open(item['image_path'], 'rb') as f:
                    project.image.save(os.path.basename(item['image_path']), File(f), save=False)
                project.save()
                print(f"Added project: {project.title}")
            else:
                print(f"Image not found: {item['image_path']}")

    # Team Members
    team_members = [
        {'name': 'Denzel Ccoga', 'role': 'clarinet', 'image': 'static/img/team/denzel_ccoga.jpg', 'order': 1},
        {'name': 'Benson Mose', 'role': 'trumpet', 'image': 'static/img/team/benson_mose.jpg', 'order': 2},
        {'name': 'BenGriffins', 'role': 'saxophone', 'image': 'static/img/team/bengriffins.jpg', 'order': 3},
        {'name': 'Micah Mose', 'role': 'piano', 'image': None, 'order': 4},
        {'name': 'Morgan Gitonga', 'role': 'trumpet', 'image': 'static/img/team/morgan_gitonga.jpg', 'order': 5},
        {'name': 'Nick', 'role': 'saxophone', 'image': 'static/img/team/nick.jpg', 'order': 6},
        {'name': 'Killion Lemi', 'role': 'bass', 'image': None, 'order': 7},
    ]

    for member in team_members:
        if not TeamMember.objects.filter(name=member['name']).exists():
            tm = TeamMember(
                name=member['name'],
                role=member['role'],
                order=member['order'],
                bio=f"Professional {member['role']} player."
            )
            if member['image'] and os.path.exists(member['image']):
                with open(member['image'], 'rb') as f:
                    tm.image.save(os.path.basename(member['image']), File(f), save=False)
            tm.save()
            print(f"Added team member: {member['name']}")

if __name__ == '__main__':
    populate_data()
