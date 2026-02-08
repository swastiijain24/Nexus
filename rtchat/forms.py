from attr import field
from django import forms

from rtchat.models import GroupChat, GroupMessage

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model=GroupMessage
        fields=['body']
        widgets= {
            'body': forms.TextInput(attrs={'placeholder': 'Message...'})
        }
    
class NewGrpChat(forms.ModelForm):
    class Meta:
        model = GroupChat
        fields=['groupchat_name']
        widgets= {
            'groupchat_name': forms.TextInput(attrs={'placeholder': 'Add a Group name'})
        }

class EditGrpChat(forms.ModelForm):
    class Meta:
        model = GroupChat
        fields=['groupchat_name', 'group_members']
        widgets= {
            'groupchat_name': forms.TextInput(attrs={'placeholder': 'Add a Group name'})
        }