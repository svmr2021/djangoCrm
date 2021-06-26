from django.urls import path
from .api import *

urlpatterns = [
    path('list/', LeadListApi.as_view(), name='list-view'),
    path('list/<int:id>/', LeadDetailApi.as_view(), name='detail-view'),
    path('auth/', UserAuthentication.as_view(), name='auth-view'),

]
