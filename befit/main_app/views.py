from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import  LoginRequiredMixin
from .models import Gym,Session
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy


from .models import Profile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm


# from .models import Class
class ProfileCreate(CreateView):
    model = Profile
    fields = ['age', 'gender', 'type', 'weight', 'height', 'image']

    def get_success_url(self):
        # Check the 'type' field of the form instance to determine the redirect URL
        if self.object.type == 'GO':
            return '/gyms/create/'
        else:
            return '/gyms/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.is_valid():
            form.instance.isSubscribed = True
            form.instance.save()
            return super().form_valid(form)




class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['age','weight','height', 'image']
    success_url = '/profile/'

# Create your views here.


class GymCreate(LoginRequiredMixin, CreateView):
    # fields = __all__: if no relationship
    model = Gym
    fields = ['gym', 'location', 'phoneNumber', 'description']
   

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super().form_valid(form)
    

class GymUpdate(LoginRequiredMixin, UpdateView):
    # fields = __all__: if no relationship
    model = Gym 
    fields = [ 'location', 'phoneNumber', 'description']



class GymDelete(LoginRequiredMixin, DeleteView):
    # fields = __all__: if no relationship
    model = Gym
    success_url = '/gyms/'



class SessionList(LoginRequiredMixin, ListView):
    model = Session
    template_name = 'session/index.html'  # Ensure this is the correct template
    
    def get_queryset(self):
        # Check if the user is a Gym Owner (GO) or Normal User (NU)
        if self.request.user.profile.type == 'NU':
            # If Normal User, get all sessions
            return Session.objects.all()
        else:
            # If Gym Owner, get only sessions related to the gym owned by the user
            return Session.objects.filter(user=self.request.user)


class SessionDetail(LoginRequiredMixin, DetailView):
    model = Session


class SessionCreate(LoginRequiredMixin, CreateView):
    model = Session
    fields = ['name','location', 'time','date','trainer','price', 'avalibility']

    def form_valid(self, form):
        # Set the user to the currently authenticated user
        form.instance.user = self.request.user
        return super().form_valid(form)

    # Redirect the user after successful form submission
    success_url = '/session/'



class SessionUpdate(LoginRequiredMixin, UpdateView):
    model = Session
    fields = ['location', 'time','date','trainer','price']


class SessionDelete(LoginRequiredMixin, DeleteView):
    model = Session
    success_url = '/session/'




def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')


# change this to gym_index
@login_required
def class_index(request): 
    if request.user.profile.type == 'NU':
        gyms = Gym.objects.all()
    else:
        gyms = Gym.objects.filter(user=request.user)
    return render(request,'gyms/index.html' , {'gyms' : gyms})


@login_required
def gyms_detail(request, gym_id):
    gym = Gym.objects.get(id=gym_id)
    # feeding_form = FeedingForm
    # toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
    return render(request,'gyms/detail.html', {'gym' : gym })



def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('profile_create')
    else:
      error_message = 'Invalid Signup- Please try again later.'

  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


  # profile view
@login_required
def profile(request):
    return render(request, 'profile.html')