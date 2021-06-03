from django.shortcuts import render, redirect
from .forms import PostForm, PostPictureForm
from django.http import JsonResponse
from .models import Post, PostPicture, AssetType
from django.views import View
from django.forms import formset_factory

from .serializers import PostSerializer, AssetTypeSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
# Create your views here.

class PostAPI(APIView):

    def get(self, request):
        search_title = request.GET.get('search_title')
        search_location = request.GET.get('search_location')
        posts = Post.objects.filter(title__icontains=search_title, location__icontains=search_location)

        search_assetType = request.GET.get('search_assetType')
        if search_assetType != '-1':
            posts = posts.filter(assetType=AssetType.objects.get(id=search_assetType))

        search_type = request.GET.get('search_type')
        if search_type != '-1':
            posts = posts.filter(type=search_type)

        search_is_active = request.GET.get('search_is_active')
        if search_is_active != '-1':
            posts = posts.filter(is_active=bool(int(search_is_active)))

        posts = posts.order_by('-is_active', '-create_at') # sort by create_at & is_active desc

        assetTypes = AssetType.objects.all()

        serializer_posts = PostSerializer(posts, many=True)
        serializer_assetTypes = AssetTypeSerializer(assetTypes, many=True)

        return Response([serializer_posts.data, serializer_assetTypes.data], status=status.HTTP_200_OK)

    def patch(self, request):
        post_id = request.data.get('post_id')
        post = Post.objects.get(id=post_id)

        post.is_active = False
        post.take_information = request.data.get('message')
        post.save()

        return Response({'post_id' : post_id}, status=status.HTTP_200_OK)

class IndexView(View):
    template_name = 'index.html'
    def get(self, request):
        buyings = Post.objects.filter(type='buying')
        sellings = Post.objects.filter(type='selling')
        active = len(sellings.filter(is_active=True))

        return render(request, self.template_name, {
            'buyings' : buyings,
            'sellings' : sellings,
            'active' : active,
            'closed' : len(sellings) - active,
            'all' : len(sellings) + len(buyings)
        })


class CreateView(View):
    template_name = 'create.html'
    PictureFormSet = formset_factory(PostPictureForm, extra=0)
    def get(self, request):
        form = PostForm()
        formset = self.PictureFormSet()
        return render(request, self.template_name, {
            'form' : form,
            'formset' : formset
        })

    def post(self, request):
        form = PostForm(request.POST)
        formset = self.PictureFormSet(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.user = request.user
            else:
                post.key = request.POST.get('key')
                # validate key
                if (len(post.key) < 6):
                    return render(request, self.template_name, {
                        'form' : form,
                        'formset' : self.PictureFormSet(),
                        'key_error' : 'Please enter a key that is 6 or more characters.'
                    })
                # check if key is used
                for i in Post.objects.all():
                    if i.key == post.key:
                        return render(request, self.template_name, {
                            'form' : form,
                            'formset' : self.PictureFormSet(),
                            'key_error' : 'This key is already in the system.'
                        })
            post.save()
            if request.POST.get('form-TOTAL_FORMS') != '0':
                for picture in formset:
                    if picture.is_valid():
                        picture = picture.save(commit=False)
                        picture.post = post
                        picture.save()
            return redirect('detail', post_id=post.id)
        else:
            return render(request, self.template_name, {
                'form' : form,
                'formset' : self.PictureFormSet()
            })

class DetailView(View):
    template_name = 'detail.html'
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        return render(request, self.template_name, {
            'post' : post
        })

    #def post(self, request, post_id):

class EditPostView(View):
    template_name = 'edit_post.html'
    PictureFormSet = formset_factory(PostPictureForm, extra=0)

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        form = PostForm(instance=post)

        if request.user.is_authenticated:
            if request.user != post.user: # If you log in and go to the edit page that you haven't created.
                return redirect('index')
        elif post.key == None: # If you are not logged in and edit a post created by someone who is logged in.
            return redirect('index')


        formset = self.PictureFormSet()


        return render(request, self.template_name, {
            'form' : form,
            'post': post,
            'pictures' : post.postpicture_set.all(),
            'formset' : formset,
            'anonymous' : True if post.user == None else False,
        })

    def post(self, request, post_id):

        post = Post.objects.get(id=post_id)
        form = PostForm(request.POST, instance=post)

        formset = self.PictureFormSet(request.POST, request.FILES)

        if form.is_valid():

            post = form.save(commit=False)

            if post.user == None and request.POST.get('key') != post.key:
                return render(request, self.template_name, {
                    'form' : form,
                    'post': post,
                    'pictures' : post.postpicture_set.all(),
                    'formset' : formset,
                    'anonymous' : True if post.user == None else False,
                    'key_error' : 'Invalid key'
                })

            post.save()

            # If delete image (JS will set value of input: hidden to 0)
            for picture in post.postpicture_set.all():
                value = request.POST.get(f'{picture.id}')
                if value == '0':
                    picture.delete()

            if request.POST.get('form-TOTAL_FORMS') != '0':
                for picture in formset:
                    if picture.is_valid():
                        picture = picture.save(commit=False)
                        picture.post = post
                        picture.save()

            return render(request, self.template_name, {
                'form' : form,
                'post': post,
                'pictures' : post.postpicture_set.all(),
                'formset' : formset,
                'anonymous' : True if post.user == None else False,
                'success' : 'The post information was successfully edited.'
            })
        else:
            return render(request, self.template_name, {
                'form' : form,
                'post': post,
                'pictures' : post.postpicture_set.all(),
                'formset' : formset,
                'anonymous' : True if post.user == None else False,
            })



def delete_view(request, post_id):
    post = Post.objects.get(id=post_id)

    if post.key == None and post.user != request.user: # If post doesn't have a key and request is not the one who created it.
        return redirect('index')
    elif post.key != None:
        key = request.GET.get('key')
        if post.key != key: # If the key sent from get is invalid
            return redirect('index')

    post.delete()
    return redirect('my_posts')
