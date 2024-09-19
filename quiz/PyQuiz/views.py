from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import  UserUpdateForm, profileUpdateForm, UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView, LogoutView, SignupView
from allauth.utils import get_form_class, get_request_param
from allauth.account.views import _ajax_response
from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from .import app_settings
from django.shortcuts import resolve_url
from allauth.account.adapter import get_adapter, DefaultAccountAdapter
from django.views.generic import UpdateView, CreateView
from allauth.account.utils import (
    complete_signup,
    get_login_redirect_url,
    get_next_redirect_url,
    # logout_on_password_change,
    passthrough_next_redirect_url,
    perform_login,
    sync_user_email_addresses,
    url_str_to_user_pk,
)

# from django.http import HttpResponse
# from .models import Quiz

# Create your views here.


def register(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("*** FORM data from Regiter view ELSE FALSE *** ", form.is_valid())
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!!")
        return redirect("users_login")
        
    else:
        form = UserRegisterForm()
        return render(request, "singup.html", {"form": UserRegisterForm() })
        
@login_required
def profile(request):
    if request.method== "POST":
        u_form = UserUpdateForm(request.POST, instance= request.user)
        p_form = profileUpdateForm(request.POST,
                                   request.FILES,
                                   instance= request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Account updated successfully!!")
            return redirect("users_logout")  # user_profile
    else:
        u_form = UserUpdateForm(instance= request.user)
        p_form = profileUpdateForm(instance=request.user.profile)
            
    context = {
            "u_form": u_form,
            "p_form": p_form
        }
        
    return render(request, "PyQuiz/profile.html", context)
    

class UserLoginView(LoginView):
    form_class = UserLoginForm
    print("**** LOGIN VIEW **** :", form_class)
    template_name = "PyQuiz/login.html"
    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        print("loginview *****", self.request)
        print("\n")
        print("loginview  users_ singup *****", self.redirect_field_name)
        
        signup_url = passthrough_next_redirect_url(self.request,
                                                   reverse("users_signup"), # users_signup
                                                   self.redirect_field_name
                                                   )
        redirect_field_value = get_request_param(self.request,
                                                 self.redirect_field_name)
        print("\n")
        print("loginview  users_ singup redirect_field_value *****", redirect_field_value)
        
        site = get_current_site(self.request)
        
        ret.update({
            "signup_url": signup_url,
            "site" : site,
            "redirect_field_name": self.redirect_field_name,
            "redirect_field_value" : redirect_field_value
        })
        # print("**** LOGIN VIEW **** :", ret)
        return ret
        
class UserLogoutView(LogoutView):
    template_name = "PyQuiz/logout.html"
    
    def get(self, *args, **kwargs):
        print("***** at start argument ******", **kwargs)
        if app_settings.LOGOUT_ON_GET:
            return self.post(*args, **kwargs) 
        # if not self.request.user.is_authenticated:
        if  not self.request.user.is_authenticated:
            print("Error here", self.get_redirect_url())
            response = redirect(self.get_redirect_url())
            # print("***Response from UserLogoutView:********* ", self.get_redirect_url())
            return _ajax_response(self.request, response)
        if self.request.user.is_authenticated:
            self.logout()
        ctx = self.get_context_data()
        response = self.render_to_response(ctx)
        return _ajax_response(self.request, response)
    
    def post(self, *args, **kwargs):
        url = self.get_redirect_url()
        if self.request.user.is_authenticated:
            self.logout()
        response = redirect(url)
        return _ajax_response(self.request, response)
    
    def get_redirect_url(self):
        return (
            get_next_redirect_url(
                self.request,
                self.redirect_field_name or get_adapter(self.request).get_logout_redirect_url(self.request)
            )
        )
    
class UserSignupView(SignupView):
    form_class = UserRegisterForm
    template_name = "PyQuiz/singup.html"
    
    def get(self, *args, **kwargs):
        output = super().get(*args, **kwargs)
        return output
    
    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        print("****** RET Value: ", ret)
        form = ret["form"]
        email = self.request.session.get("account_verified_email")
        if email:
            email_keys = ["email"]
            if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
                email_keys.append("email2")
                for email_key in email_keys:
                    form.fields[email_keys].initial = email
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("users_login"),
                                                  self.redirect_field_name
                                                  )
        print("SINGUP *****: ", login_url)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = get_request_param(self.request,
                                                 redirect_field_name)
        ret.update({"login_url": login_url,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        ret.update({"login_url": login_url,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret
    
    def post(self, request, *args, **kwargs):
        output = super().post(request, *args, **kwargs)
        return output

class UserProfileView(UpdateView):
    template_name = "PyQuiz/profile.html"
    print("I'm at UserProfileview class section")
    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)
        
        print("I'm at UserProfileview def section")
        
        context = {
            "u_form": u_form,
            "p_form": p_form
        }
        
        return render(request, "PyQUiz/profile.html", context)
    
    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = profileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile
            
        )
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Account Update Successfully!!!")
            
        return redirect("PyQuiz_profile")
    
