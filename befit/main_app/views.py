from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import  LoginRequiredMixin
from .models import Gym,Session
from .forms import RegistrationForm
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy


# from .models import Class

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

#--------------------------------------------------------------------------------------------------

class SessionList(LoginRequiredMixin, ListView):
    model = Session

class SessionDetail(LoginRequiredMixin, DetailView):
    model = Session


class SessionCreate(LoginRequiredMixin, CreateView):
    model = Session
    fields = ['name','location', 'time','date','trainer','price']

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

#-------------------------------------------------------------------------------------------------------




def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

@login_required
def class_index(request): 
    gyms = Gym.objects.all()
    return render(request,'gyms/index.html' , {'gyms' : gyms})


@login_required
def gyms_detail(request, gym_id):
    gym = Gym.objects.get(id=gym_id)
    Registration_form = RegistrationForm()
    # toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
    return render(request,'gyms/detail.html', {'gym' : gym, 'Registration_form' : Registration_form})


@login_required
def Regist(request, session_id):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        new_Regist = form.save(commit=False)
        new_Regist.session_id = session_id
        new_Regist.save()
        return redirect('detail', session_id = session_id)



def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid Signup- Please try again later.'

  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)