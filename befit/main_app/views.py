from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import  LoginRequiredMixin
from .models import Gym,Session,Subscription, SubscriptionPackage, Profile, Trainer, Registration
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from django.utils import timezone
from datetime import timedelta

from django.contrib import messages 

from django.utils import timezone




# List View - To display all subscription packages
class SubscriptionPackageListView(ListView):
    model = SubscriptionPackage
    template_name = 'main_app/subscriptions_list.html'
    context_object_name = 'packages'

# Create View - To create a new subscription package
class SubscriptionPackageCreateView(CreateView):
    model = SubscriptionPackage
    template_name = 'main_app/subscription_package_form.html'
    fields = ['name', 'description', 'duration_days', 'price', 'user_type']
    success_url = reverse_lazy('subscription_package_list')  # Redirect to the list page after creation

# Update View - To update an existing subscription package
class SubscriptionPackageUpdateView(UpdateView):
    model = SubscriptionPackage
    template_name = 'main_app/subscription_package_form.html'
    fields = ['name', 'description', 'duration_days', 'price', 'user_type']
    success_url = reverse_lazy('subscription_package_list')  # Redirect to the list page after updating

# Delete View - To delete a subscription package
class SubscriptionPackageDeleteView(DeleteView):
    model = SubscriptionPackage
    template_name = 'main_app/subscription_package_confirm_delete.html'
    success_url = reverse_lazy('subscription_package_list')  # Redirect to the list page after deletion


@login_required
def subscribe_to_package(request, package_id):
    # Get the user's profile to check their type
    user_profile = Profile.objects.get(user=request.user)
    
    # Check if the user already has an active subscription
    active_subscription = Subscription.objects.filter(user=request.user, status='Active').first()

    if active_subscription:
        # Check if the current active subscription has expired
        today = timezone.now().date()
        if active_subscription.endDate < today:  # If the active subscription has expired
            active_subscription.status = 'Inactive'  # Change the status to 'Inactive'
            active_subscription.save()

     

        # Notify the user that they already have an active subscription
        messages.warning(request, "You already have an active subscription. Please wait for it to expire before subscribing to a new one.")
        
        # Filter packages based on user type (RU or GO)
        if user_profile.type == 'GO':  # Gym owner
            packages = SubscriptionPackage.objects.filter(user_type='GO')
        else:  # Regular user
            packages = SubscriptionPackage.objects.filter(user_type='NU')
        
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

    active_subscription = Subscription.objects.filter(user=request.user, status='Active').exists()

    if active_subscription:
        # Notify the user that they already have an active subscription
        messages.warning(request, "You already have an active subscription. Please wait for it to expire before subscribing to a new one.")

    if user_profile.type == 'GO':  # Gym owner
        # Show only gym owner packages
        packages = SubscriptionPackage.objects.filter(user_type='GO')
    else:  # Regular user
        # Show only regular user packages
        packages = SubscriptionPackage.objects.filter(user_type='NU')

    return render(request, 'main_app/subscription_package_list.html', {'packages': packages})



def register_for_session(request, session_id):
    # Retrieve the session
    session = Session.objects.filter(id=session_id).first()

    # If the session doesn't exist, redirect to the session list
    if not session:
        messages.error(request, "Session does not exist.")
        return redirect('session_list')

    # Check if the user has an active subscription
    user_subscription = Subscription.objects.filter(user=request.user, status='Active').first()

    if not user_subscription:
        # If not subscribed, notify the user to subscribe first
        messages.warning(request, "You must subscribe to a package first before registering for a session.")
        return redirect('subscription_package_list')

    # Check if the user is already registered for the session
    if Registration.objects.filter(user=request.user, session=session).exists():
        # If already registered, inform the user
        messages.info(request, "You are already registered for this session.")
        return redirect('session_list')
    
    # Check if there are available seats for the session
    if session.seats <= 0:
        # If no seats are available, inform the user
        messages.warning(request, "Sorry, no seats are available for this session.")
        return redirect('session_list')

    # Create a new registration
    Registration.objects.create(
        session=session,
        user=request.user,
        date_registered=timezone.now().date()
    )

    # Decrease the available seats by 1
    session.seats -= 1
    session.save()

    # Notify the user that the registration was successful
    messages.success(request, "You have successfully registered for the session.")

    # Redirect the user to the list of their registrations
    return redirect('view_my_registrations')



@login_required
def view_my_registrations(request):
    user_profile = request.user.profile  # Get the logged-in user's profile

    if user_profile.type == 'GO':  # Gym Owner
        # Get the gym associated with the logged-in user (Owner)
        gym = Gym.objects.filter(user=request.user).first()

        if gym:
            # Filter registrations for sessions associated with this gym
            registrations = Registration.objects.filter(session__gym=gym)
        else:
            registrations = []
            messages.warning(request, "No gym associated with your account.")
    else:  # Regular User
        # Regular users can only see their own registrations
        registrations = Registration.objects.filter(user=request.user)

    return render(request, 'main_app/my_registrations.html', {'registrations': registrations})



# # subscription view
# @login_required
# def view_my_subscriptions(request):
#     subscriptions = Subscription.objects.filter(user=request.user)  # Filter subscriptions by the logged-in user
#     return render(request, 'main_app/my_subscriptions.html', {'subscriptions': subscriptions})




@login_required
def view_my_subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user)  # Filter subscriptions by the logged-in user
    today = timezone.now().date()

    # Check for expired subscriptions and update their status
    for subscription in subscriptions:
        if subscription.endDate < today and subscription.status == 'Active':  # If the subscription has expired
            subscription.status = 'Inactive'  # Change the status to Inactive
            subscription.save()

    return render(request, 'main_app/my_subscriptions.html', {'subscriptions': subscriptions})


class ProfileCreate(CreateView):
    model = Profile
    fields = ['age', 'gender', 'type', 'weight', 'height', 'image']

    def get_success_url(self):
        # Check the 'type' field of the form instance to determine the redirect URL
        if self.object.type == 'GO':
            return '/gyms/create/'
        else:
            return '/'

    def form_valid(self, form):
        age = form.instance.age
        weight = form.instance.weight
        height = form.instance.height

        if age < 0:
            form.add_error('age', 'Age cannot be less than 0.')
            return self.form_invalid(form)

        if weight < 0:
            form.add_error('weight', 'Weight cannot be less than 0.')
            return self.form_invalid(form)

        if height < 0:
            form.add_error('height', 'Height cannot be less than 0.')
            return self.form_invalid(form)

        # If validation passes, set additional fields
        form.instance.user = self.request.user
        form.instance.isSubscribed = True

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



# class SessionList(LoginRequiredMixin, ListView):
#     model = Session
#     template_name = 'session/index.html'  # Ensure this is the correct template
    
#     def get_queryset(self):
#         # Check if the user is a Gym Owner (GO) or Normal User (NU)
#         if self.request.user.profile.type == 'NU':
#             # If Normal User, get all sessions
#             return Session.objects.all()
#         else:
#             # If Gym Owner, get only sessions related to the gym owned by the user
#             return Session.objects.filter(user=self.request.user)


class SessionList(LoginRequiredMixin, ListView):
    model = Session
    template_name = 'session/index.html'  # Ensure this is the correct template
    
    def get_queryset(self):
        # If the user is a Normal User (NU), filter sessions based on Gym Owner's active subscription
        if self.request.user.profile.type == 'NU':
            # Get the gyms owned by Gym Owners (GO)
            gyms = Gym.objects.filter(user__profile__type='GO')
            
            # Filter sessions related to gyms that have active subscriptions for the Gym Owner (GO)
            active_gym_owners = [gym.user for gym in gyms if self._has_active_subscription(gym.user)]
            
            # Only show sessions that belong to gyms with an active Gym Owner's subscription
            return Session.objects.filter(gym__user__in=active_gym_owners)
        
        # If the user is a Gym Owner (GO), show all sessions for the gym owned by the user
        return Session.objects.filter(user=self.request.user)

    def _has_active_subscription(self, gym_owner):
        """Helper method to check if the Gym Owner has an active subscription"""
        return Subscription.objects.filter(user=gym_owner, status="Active").exists()






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
    fields = ['name','location', 'time','date','seats','price']
    

    def form_valid(self, form):
        seats = form.instance.seats
        price = form.instance.price

        if seats <= 0:
            form.add_error('seats', 'seats cannot be less than 0.')
            return self.form_invalid(form)

        if price < 0:
            form.add_error('price', 'Price cannot be less than 0.')
            return self.form_invalid(form)

        form.instance.user = self.request.user
        form.instance.gym = Gym.objects.get(user=self.request.user)
        return super().form_valid(form)

    # Redirect the user after successful form submission
    success_url = '/session/'





class SessionUpdate(LoginRequiredMixin, UpdateView):
    model = Session
    fields = ['location', 'time','date','seats','price']
    


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
        age = form.instance.age

        if age <= 0:
            form.add_error('age', 'Age cannot be less than or equal 0.')
            return self.form_invalid(form)

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



class RegisterUpdate(LoginRequiredMixin, UpdateView):
    model = Registration
    fields = ['status','comment']
    
    
    template_name = 'main_app/registration_form.html'  # Update this line to match your actual template name

    def form_valid(self, form):
        form.save()
        return redirect('view_my_registrations')



def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')


# change this to gym_index
# @login_required
# def class_index(request): 

#     if request.user.profile.type == 'NU':
#         gyms = Gym.objects.all()
#     else:
#         gyms = Gym.objects.filter(user=request.user)
#     return render(request,'gyms/index.html' , {'gyms' : gyms})

@login_required
def class_index(request):
    if request.user.profile.type == 'NU':
        # Get the gyms where the Gym Owner has an active subscription
        gyms_with_active_subscription = []
        
        # Loop through all gyms owned by Gym Owners and check if they have an active subscription
        for gym in Gym.objects.filter(user__profile__type='GO'):
            if _has_active_subscription(gym.user):
                gyms_with_active_subscription.append(gym)
        
        gyms = gyms_with_active_subscription
    else:
        # Gym Owners can see all their gyms
        gyms = Gym.objects.filter(user=request.user)

    return render(request, 'gyms/index.html', {'gyms': gyms})

def _has_active_subscription(gym_owner):
    """Helper method to check if the Gym Owner has an active subscription"""
    return Subscription.objects.filter(user=gym_owner, status="Active").exists()



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
