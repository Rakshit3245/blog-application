from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(CreateView):
    model = get_user_model()
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Account created for {username}!')
        return response

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change')
    template_name = 'users/password_change.html'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['u_form'] = UserUpdateForm(instance=self.request.user)
        context['p_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        return context

    def post(self, request,pk, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)


        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile',pk=pk)

        return self.render_to_response(self.get_context_data(u_form=u_form, p_form=p_form))

class LogoutView(TemplateView):
    template_name = 'users/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})

# @login_required
# def logoutview(request):
#     logout(request)
#     return render(request, 'users/logout.html', {})


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST,
#                                    request.FILES,
#                                    instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#
#         context = {
#             'u_form': u_form,
#             'p_form': p_form
#         }
#         return render(request, 'users/profile.html', context)
