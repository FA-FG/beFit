from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import  LoginRequiredMixin

from .models import Profile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm


# from .models import Class
class ProfileCreate(CreateView):
  model = Profile
  
  fields = ['age', 'gender', 'weight', 'height', 'image']

  def form_valid(self,form):
    form.instance.user = self.request.user
    if form.is_valid:
      form.instance.isSubscribed = True

      form.instance.save()

      return super().form_valid(form)

    else:
      print(form.errors)  # Print out form errors for debugging



# Create your views here.


def home(request):
    return render(request,'home.html')

def about(request):
    # return HttpResponse('<h1>this is about </h1>')
    return render(request,'about.html')

@login_required
def class_index(request): 

    return render(request,'classes/index.html')



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


  # profile view
@login_required
def profile(request):
    return render(request, 'profile.html')