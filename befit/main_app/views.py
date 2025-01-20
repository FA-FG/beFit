from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import  LoginRequiredMixin
from .models import Gym,Session,Subscription, SubscriptionPackage, Profile
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from django.utils import timezone
from datetime import timedelta

from django.contrib import messages  # Import messages framework

from django.contrib import messages  # Import messages framework

@login_required
def subscribe_to_package(request, package_id):
    # Get the user's profile to check their type
    user_profile = Profile.objects.get(user=request.user)
    
    # Check if the user already has an active subscription
    active_subscription = Subscription.objects.filter(user=request.user, status='Active').exists()

    if active_subscription:
        # Notify the user that they already have an active subscription
        messages.warning(request, "You already have an active subscription. Please wait for it to expire before subscribing to a new one.")
        
        # Filter packages based on user type (RU or GO)
        if user_profile.type == 'GO':  # Gym owner
            packages = SubscriptionPackage.objects.filter(user_type='GO')
        else:  # Regular user
            packages = SubscriptionPackage.objects.filter(user_type='RU')
        
        # Render the page with the filtered packages and the message
        return render(request, 'main_app/subscription_package_list.html', {'packages': packages})
    
    # If no active subscription, proceed with subscription creation
    package = SubscriptionPackage.objects.get(id=package_id)  # Get the selected package
    
    # Calculate the subscription's end date based on the package duration
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=package.duration_days)
    
    # Create the subscription for the logged-in user
    Subscription.objects.create(
        package=package,
        startDate=start_date,
        endDate=end_date,
        user=request.user,
        status="Active"
    )
    
    # Notify the user of successful subscription
    messages.success(request, f"Successfully subscribed to {package.name}!")
    
    # After successful subscription, show the list of subscriptions
    return redirect('view_my_subscriptions')  # Redirect to the list of subscriptions


@login_required
def subscription_package_list(request):
    user_profile = Profile.objects.get(user=request.user)  # Get the logged-in user's profile

    if user_profile.type == 'GO':  # Gym owner
        # Show only gym owner packages
        packages = SubscriptionPackage.objects.filter(user_type='GO')
    else:  # Regular user
        # Show only regular user packages
        packages = SubscriptionPackage.objects.filter(user_type='RU')

    return render(request, 'main_app/subscription_package_list.html', {'packages': packages})


@login_required
def view_my_subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user)  # Filter subscriptions by the logged-in user
    return render(request, 'main_app/my_subscriptions.html', {'subscriptions': subscriptions})



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


    def form_valid(self, form):
        profile = form.save(commit=False)

        # get the password
        password = self.request.POST.get('password', None)

        if password: #if there is a password
            user = profile.user  # Get the User
            user.set_password(password)  # change the pw to the new one + hash it
            user.save()

        profile.save()  # SaveProfile
        return redirect(self.success_url)  # Redirect to /profile/




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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.get_object()  # This gets the session object from the view's context

        
        user = session.user
        profile = user.profile  

        if profile.type == 'GO': # if gym owner
            gym = Gym.objects.filter(user=user).first()  # Get the gym associated with the user (gym owner)
            
            if gym:
                # Filter trainers that belong to the gym
                trainers = Trainer.objects.filter(gym=gym).exclude(id__in = session.trainers.all().values_list('id'))
            else:
                trainers = []  # no trainers
        else:
            trainers = []  # If the user is not a gym owner, no trainers should be listed

        context['trainers'] = trainers
        return context



class SessionCreate(LoginRequiredMixin, CreateView):
    model = Session
    fields = ['name','location', 'time','date','price', 'avalibility']

    def form_valid(self, form):
        # Set the user to the currently authenticated user
        form.instance.user = self.request.user
        return super().form_valid(form)

    # Redirect the user after successful form submission
    success_url = '/session/'



class SessionUpdate(LoginRequiredMixin, UpdateView):
    model = Session
    fields = ['location', 'time','date','price']
    


class SessionDelete(LoginRequiredMixin, DeleteView):
    model = Session
    success_url = '/session/'



# trainer
class TrainerDetail(LoginRequiredMixin, DetailView):
    model = Trainer
    fields = "__all__"

class TrainerCreate(LoginRequiredMixin, CreateView):
    model = Trainer
    fields = ['name', 'age', 'image', 'specialties', 'description']

    def form_valid(self, form):
        form.instance.gym = Gym.objects.get(user=self.request.user)
        return super().form_valid(form)
    
    def get_success_url(self):
        return f'/gyms/{self.object.gym.id}/'


class TrainerUpdate(LoginRequiredMixin, UpdateView):
    model = Trainer
    fields = ['name', 'age', 'image', 'specialties', 'description']
    
    def get_success_url(self):
        gym_id = self.object.gym.id 
        return f'/gyms/{gym_id}/'

class TrainerDelete(LoginRequiredMixin, DeleteView):
    model = Trainer
    success_url = '/trainer/'

    def get_success_url(self):
        gym_id = self.object.gym.id 
        return f'/gyms/{gym_id}/'


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
    
    profile = request.user.profile

    trainers = Trainer.objects.filter(gym=gym)

    

    return render(request,'gyms/detail.html', {'gym' : gym, 'trainers': trainers, 'profile': profile })



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


# added assoc and unassoc between trainer and session

def assoc_trainer(request, session_id, trainer_id):
    session = Session.objects.get(id=session_id)
    trainer = Trainer.objects.get(id=trainer_id)
    session.trainers.add(trainer)
    
    return redirect('session_detail', pk=session_id) 

def unassoc_trainer(request, session_id, trainer_id):
    session = Session.objects.get(id=session_id)
    trainer = Trainer.objects.get(id=trainer_id)
    session.trainers.remove(trainer)
    
    return redirect('session_detail', pk=session_id) 


