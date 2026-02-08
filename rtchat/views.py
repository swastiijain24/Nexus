from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from rtchat.forms import ChatMessageForm, EditGrpChat, NewGrpChat
from rtchat.models import GroupChat, UserChannel
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.
def chat_view(request, chatroom_name='public-chat'):
    chat_group, created = GroupChat.objects.get_or_create(groupname=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:50]
    form = ChatMessageForm()

    other_user= None
    if chat_group.is_private == True:
        if request.user not in chat_group.group_members.all():
            raise Http404()
        
        for member in chat_group.group_members.all():
            if other_user != request.user:
                other_user=member
                break
            
    if chat_group.groupchat_name:
        if request.user not in chat_group.group_members.all():
            chat_group.group_members.add(request.user)
    
    if request.htmx:
        form = ChatMessageForm(request.POST) #making a new one 
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message':message,
                'user':request.user,
            }
            return render(request, 'rtchat/chat_message.html', context)
    
    context = {
        'chat_messages':chat_messages,
        'form':form,
        'other_user':other_user,
        'chatroom_name':chatroom_name,
        'chat_group':chat_group,
    }
    return render(request, 'rtchat/chat.html', context)

@login_required
def get_or_create_chat(request, username):
    if request.user.username == username:
        return redirect('home')
    
    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.group_members.all():
                return redirect('chat', chatroom.groupname)
    
    chatroom = GroupChat.objects.create(is_private=True)
    chatroom.group_members.add(request.user, other_user)
    return redirect('chat', chatroom.groupname)

@login_required
def create_newgrpchat(request):
    form = NewGrpChat()
    if request.method == 'POST':
        form = NewGrpChat(request.POST)
        if form.is_valid():
            newgrpchat = form.save(commit=False) #means before saving in the database
            newgrpchat.admin = request.user
            newgrpchat.save()
            newgrpchat.group_members.add(request.user)
            return redirect('chat', newgrpchat.groupname)

    context ={
        'form':form
    }

    return render(request, 'rtchat/new-grpchat.html', context)

def edit_group(request, chatroom_name):
    chat_group = GroupChat.objects.get(groupname=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    
    form = EditGrpChat(instance=chat_group)

    if request.method == 'POST':
        form = EditGrpChat(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()

            remove_members = request.POST.getlist('remove_members')
            for member_id in remove_members:
                member = User.objects.get(id=member_id)
                chat_group.group_members.remove(member)
                channel_layer = get_channel_layer()
                user_channels = UserChannel.objects.filter(member=member, group=chat_group)
                for user_channel in user_channels:
                    async_to_sync(channel_layer.group_discard)(
                        chatroom_name,
                        user_channel.channel
                    )
                    user_channel.delete()
            
            return redirect('edit_group', chatroom_name)

    context = {
        'form': form,
        'chat_group': chat_group,
    }
    return render(request, 'rtchat/edit_group.html', context)

def delete_chatroom(request, chatroom_name):
    return render(request, 'rtchat/delete_chatroom.html')