from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, MyPasswordChangeForm, EditProfileForm
from .models import UserProfile
from posts.models import Post
from django.contrib.auth.models import User
from django.views import View

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class SignupView(View):
    template_name = 'signup.html'
    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {
            'form' : form,
           
        })

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            try:
                picture = request.FILES['picture']
            except:
                picture = None

            userprofile = UserProfile.objects.create(
                user=user,
                
            )

            if picture != None:
                userprofile.avatar = picture
                userprofile.save()

            # login
            login(request, user)
            return redirect('index')
        else:
            return render(request, self.template_name, {
                'form' : form
            })

class LoginView(View):
    template_name = 'login.html'
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        next_url = request.GET.get('next') # if have next send it to save in input:hidden
        return render(request, 'login.html', {
            'next_url' : next_url
        })

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        next_url = request.POST.get('next_url')
        if user:
            login(request, user)
            if next_url != 'None':
                return redirect(next_url)
            else:
                return redirect('index')

        return render(request, 'login.html', {
            'next_url' : next_url,
            'error' : 'Invaild Username or Password'
        })


class MyPostView(View):
    template_name = 'my_posts.html'

    def get(self, request):
        if request.user.is_authenticated:
            posts = Post.objects.filter(user=request.user).order_by('-is_active', '-create_at')
            sellings = Post.objects.filter(user=request.user, type='selling')
            buyings = Post.objects.filter(user=request.user, type='buy')
        else:
            posts = "key"
            sellings = []
            buyings = []
        return render(request, self.template_name, {
            'posts' : posts,
            'sellings' : sellings,
            'buyings' : buyings,
            'closed' : len(Post.objects.filter(is_active=False))
        })

    def post(self, request):
        key = request.POST.get('key')
        try:
            post = Post.objects.get(key=key)
            return render(request, self.template_name, {
                'posts' : [post],
                'key' : key
            })
        except:
            return render(request, self.template_name, {
                'posts' : 'key',
                'key_error' : 'There is no post in the system.'
            })

class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(user=user)
        sellings = Post.objects.filter(user=user, type='selling')
        buyings = Post.objects.filter(user=user, type='buying')
        closed = 0
        for post in posts:
            if post.is_active == False:
                closed += 1
        context = {
            'user' : user,
            'posts' : posts,
            'closed' : closed,
            'active' : len(posts) - closed,
            'sellings' : sellings,
            'buyings' : buyings
        }
        return render(request, self.template_name, context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    template_name = 'change_password.html'

    def get(self, request):
        user = request.user
        form = MyPasswordChangeForm(user=user)

        return render(request, self.template_name, {
            'user' : user,
            'form' : form
        })

    def post(self, request):
        user = request.user
        form = MyPasswordChangeForm(data=request.POST, user=user)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, self.template_name, {
                'user' : user,
                'form' : form
            })

@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    template_name = 'edit_profile.html'

    def get(self, request):
        user = request.user
        form = EditProfileForm(instance=user)


        return render(request, self.template_name, {
            'user' : user,
            'form' : form,
           
        })

    def post(self, request):
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        form = EditProfileForm(request.POST,instance=user)

        userprofile.save()

        try:
            picture = request.FILES['picture']
        except:
            picture = None

        if picture != None:
            userprofile.avatar = picture
            userprofile.save()

        if form.is_valid():
            form.save()
            return render(request, self.template_name, {
                'user' : user,
                'form' : form,
                'success' : 'Profile edited'
            })
        else:
            return render(request, self.template_name, {
                'user' : user,
                'form' : form,
            })
