from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Message
from .forms import MessageForm

User = get_user_model()

@login_required
def teacher_chat_view(request):
    if not request.user.is_member:
        return redirect('dashboard_redirect')
    
    # Assuming valid admin exists (superuser) - Get the first one or a specific one "admin"
    # For simplicity, we chat with the first superuser found or specific system account
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if not admin_user:
        messages.error(request, "System administrator not found.")
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = admin_user
            msg.save()
            return redirect('teacher_chat')
    else:
        form = MessageForm()

    # Get conversation
    chat_messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=admin_user)) |
        (Q(sender=admin_user) & Q(recipient=request.user))
    ).order_by('created_at')

    # Mark received messages as read
    Message.objects.filter(sender=admin_user, recipient=request.user, is_read=False).update(is_read=True)

    context = {
        'chat_messages': chat_messages,
        'form': form,
        'chat_partner': admin_user
    }
    return render(request, 'messaging/teacher_chat.html', context)

@login_required
def admin_inbox_view(request):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    # Find all users who have exchanged messages with admin
    # This is a bit complex in pure Django ORM to get unique list annotated with last message
    # Simplified approach: Get all teachers, iterate and find last message
    
    from accounts.models import MemberProfile
    teachers = MemberProfile.objects.all().select_related('user')
    
    conversations = []
    for teacher_profile in teachers:
        teacher = teacher_profile.user
        last_msg = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient=teacher)) |
            (Q(sender=teacher) & Q(recipient=request.user))
        ).last()
        
        unread_count = Message.objects.filter(sender=teacher, recipient=request.user, is_read=False).count()
        
        # Only show if there's a conversation or if we want to show all teachers regardless
        # Let's show all teachers so admin can initiate
        conversations.append({
            'teacher': teacher,
            'last_message': last_msg,
            'unread_count': unread_count
        })
    
    # Sort by last message date (desc)
    conversations.sort(key=lambda x: x['last_message'].created_at if x['last_message'] else x['teacher'].date_joined, reverse=True)
    
    return render(request, 'messaging/admin_inbox.html', {'conversations': conversations})

@login_required
def admin_chat_detail_view(request, user_id):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    teacher = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = teacher
            msg.save()
            return redirect('admin_chat_detail', user_id=user_id)
    else:
        form = MessageForm()
        
    chat_messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=teacher)) |
        (Q(sender=teacher) & Q(recipient=request.user))
    ).order_by('created_at')
    
    # Mark read
    Message.objects.filter(sender=teacher, recipient=request.user, is_read=False).update(is_read=True)
    
    context = {
        'chat_messages': chat_messages,
        'form': form,
        'chat_partner': teacher
    }
    return render(request, 'messaging/admin_chat_detail.html', context)
