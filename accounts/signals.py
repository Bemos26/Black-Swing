from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MemberProfile
from portfolio.models import TeamMember

@receiver(post_save, sender=MemberProfile)
def sync_member_to_team(sender, instance, created, **kwargs):
    """
    Syncs approved MemberProfiles to the TeamMember model for public display.
    """
    if instance.is_approved:
        # Determine display name
        full_name = f"{instance.user.first_name} {instance.user.last_name}".strip()
        if not full_name:
            full_name = instance.user.username
            
        # Check if team member already exists (msg match by name is heuristic but simple for now)
        # Ideally we'd link them via FK, but for now we match by name or update if existing.
        # Since we don't have a direct link, we'll try get_or_create by name.
        
        team_member, _ = TeamMember.objects.get_or_create(
            name=full_name,
            defaults={
                'role': instance.role,
                'bio': instance.bio,
                'is_active': True,
                'order': 50 # Default order for auto-added members
            }
        )
        
        # Always update fields to match current profile state
        team_member.role = instance.role
        team_member.bio = instance.bio
        team_member.is_active = True
        
        # Sync Image
        if instance.image:
            # We copy the image file reference. 
            # Note: This points to the same file on disk (or object storage).
            team_member.image = instance.image
            
        team_member.save()
        print(f"Synced {full_name} to TeamMember list.")
