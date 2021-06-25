from django.urls import path
from leads import views

app_name = 'leads'
urlpatterns = [
    path('', views.LeadList.as_view(), name='list-view'),
    path('<int:pk>/category', views.CategoryUpdateView.as_view(), name='category_update-view'),
    path('detail/<int:pk>/', views.LeadDetail.as_view(), name='detail-view'),
    path('create/', views.LeadCreate.as_view(), name='create-view'),
    path('update/<int:pk>/', views.LeadUpdate.as_view(), name='update-view'),
    path('delete/<int:pk>/', views.LeadDelete.as_view(), name='delete-view'),
    path('assign-agent/<int:pk>', views.AssignAgent.as_view(), name='assign_agent-view'),
    path('categories/', views.CategoryListView.as_view(), name='category_list-view'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail-view'),
]
