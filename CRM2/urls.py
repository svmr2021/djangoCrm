from django.contrib import admin
from django.urls import path, include
from leads import urls
import leads
import agents
from agents import urls
from leads import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include(leads.urls, namespace='leads')),
    path('agents/', include(agents.urls, namespace='agents')),

    path('', views.LandingPage.as_view(), name='landing-page'),
    path('login/', LoginView.as_view(), name='login-page'),
    path('logout/', LogoutView.as_view(), name='logout-page'),
    path('signup/', views.LeadSignUp.as_view(), name='signup-page'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('reset-password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
