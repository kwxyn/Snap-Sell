from django import forms
from .models import Post, PostPicture
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','desc', 'type', 'assetType', 'location', 'contact1', 'contact2', 'price']

        widgets = {
            'desc' : forms.Textarea(attrs={'class' : 'form-control', 'style' : 'resize:none;', 'placeholder' : 'More details..'}),
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Title'}),
            'location' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Location'}),
            'contact1' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'xxx-xxx-xxxx'}),
            'contact2' : forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'example@example.com'}),
            'type' : forms.Select(attrs={'class' : 'form-control'}),
            'assetType' : forms.Select(attrs={'class' : 'form-control'}),
            'price' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : '$$$'}),
        }

        labels = {
            'desc' : 'Description',
            'title' : 'Post Title',
            'location' : 'Location',
            'contact1' : 'Contact No',
            'contact2' : 'Email',
            'type' : 'Post Type',
            'assetType' : 'Product',
            'price' : 'price'
        }

class PostPictureForm(forms.ModelForm):
    class Meta:
        model = PostPicture
        fields = ['picture']

        widgets = {
            'picture' : forms.FileInput(attrs={'class' : 'custom-file-input'})
        }

