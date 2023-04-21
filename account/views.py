from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, UpdateView
from .forms import LoginForm, UserRegisterationForm, VerifyCodeForm
from .models import CustomUser,  OtpCode, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
import random


class CustomLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account:profile')
        else:
            form = LoginForm()
            return render(request, 'account/index.html', {'form': form})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('account:profile')
        else:
            form = LoginForm()
            return render(request, 'account/index.html', {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'
    login_url = '/account/'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user.pk)
        return context


class UserRegisterView(View):
    from_class = UserRegisterationForm

    def get(self, request):
        form = self.from_class
        return render(request, 'account/register.html', {'form': form})
    
    def post(self, request):
        form = self.from_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            OtpCode.objects.create(
                phone_number=form.cleaned_data['phone_number'],
                code=random_code
                )
            request.session['user_registeration_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password2'],

            }
            messages.success(request, 'send confirm code to your email', 'success')
            return redirect('account:verify')
        return redirect('account:index')


class VerifyRegisterCode(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'account/verify.html', {'form': form})
    
    def post(self, request):
        user_session = request.session['user_registeration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                CustomUser.objects.create_user(
                    email=user_session['email'],
                    password=user_session['password'],
                    phone_number=user_session['phone_number'],
                )
                code_instance.delete()
                messages.success(request, 'Registered Successfully', 'success')
                return redirect('account:index')
            else:
                messages.error(request, 'Wrong Code', 'error')
                return redirect('account:verify')
        return redirect('account:index')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('account:index')


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'account/profile_edit.html'
    fields = ['first_name', 'last_name', 'avatar', 'address', 'job_title', 'website', 'github', 'twitter', 'linkedin']
    success_url = '/account/profile/'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user.pk)


class PasswordChange(PasswordChangeView):
    template_name = 'account/password_change_form.html'
    success_url = reverse_lazy('account:profile')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed.')
        return super().form_valid(form)
