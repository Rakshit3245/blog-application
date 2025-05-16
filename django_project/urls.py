from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from users.forms import EmailValidationOnForgotPassword
from users.views import ChangePasswordView


urlpatterns = [
    path('', include("blog.urls")),

    path('admin/', admin.site.urls),

    path("register/",
         user_views.RegisterView.as_view(template_name="users/register.html"),
         name='register'),

    path("profile/<int:pk>",
         user_views.ProfileUpdateView.as_view(template_name="users/profile.html"),
         name='profile'),

    path("login",
         auth_views.LoginView.as_view(template_name="users/login.html"),
         name='login'),

    path("logout/",
         user_views.LogoutView.as_view(template_name="users/logout.html"),
         name='logout'),

    path("password-reset/",
         auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword,
         template_name ="users/password_reset.html"),
         name='password_reset'),

    path("password-reset/done/",
         auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name='password_reset_done'),

    path("password-reset-confirm/<uidb64>/<token>",
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
         name='password_reset_confirm'),

    path("password-reset-complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),

    path("password-change/done/",
         auth_views.PasswordResetDoneView.as_view(template_name="users/password_change_done.html"),
         name='password_change_done'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

