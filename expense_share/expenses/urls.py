from django.urls import path
from . import views
#from .views import register_user, login_user
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    #path('auth/register/', register_user, name='register_user'),
    #path('auth/login/', login_user, name='login_user'),
    #path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/create/', views.create_user, name='create_user'), # Create an user
    path('expenses/add/', views.add_expense, name='add_expense'), # Add Expense
    path('expenses/user/<str:email>/', views.user_expenses, name='user_expenses'), # Endpoint to retireve expense of each user
    path('expenses/overall/', views.overall_expenses, name='overall_expenses'), # Endpoint to retrieve overall expenses
    path('expenses/balance_sheet/', views.download_balance_sheet, name='download_balance_sheet'), # Download balance sheet
]