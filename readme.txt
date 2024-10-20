Run the following commands in the terminal:

~ pip install Django
~ pip install django djangorestframework
~ django-admin startproject expense_share
~ cd expense_share
~ python manage.py startapp expenses
~ python manage.py makemigrations
~ python manage.py migrate
~ python manage.py runserver

API Endpoints:

~ /users/create/: Create a user
~ /expenses/add/: Add expense
~ /expenses/user/<email>/: Get expenses for a user
~ /expenses/overall/: Get overall expenses
~ /expenses/balance_sheet/: Download balance sheet as CSV file