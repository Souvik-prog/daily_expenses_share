from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expenses.urls')),  # Include the urls from the 'expenses' app
]