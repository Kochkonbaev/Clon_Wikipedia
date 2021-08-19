from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.template import RequestContext
from .forms import LoginForm, RegistrationForm

User = get_user_model()

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'account/dashboard.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')            
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('all_news'))
        context = {'form': form}
        return render('account/dashboard.html', context, context_instance = RequestContext(request))

class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('all_news'))
        form = RegistrationForm(request.POST or None)
        context = {'form': form}
        return render(request, 'account/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email = form.cleaned_data['email']
            new_user.password = form.cleaned_data['password']
            new_user.confirm_password = form.cleaned_data['confirm_password']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(email=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('all_news'))
        context = {'form': form}
        return render(request, 'account/registration.html', context)

# class Dashboard(LoginView):
#     def dashboard(request):
#         return render(request, 'account/dashboard.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('dashboard'))



