from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from .models import User, Expense, ExpenseParticipant
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.shortcuts import get_object_or_404
import csv
from django.db.models import Sum

"""@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    user = User.objects.create_user(
        email=data['email'],
        name=data['name'],
        mobile=data['mobile'],
        password=data['password']
    )
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)"""
    
@api_view(['POST'])
# The view is invoked on /users/create
# On successful creation of user: "User created successfully"
def create_user(request):
    data = request.data
    # Check user details
    try:
        user = User.objects.create_user(
            email=data['email'],
            name=data['name'],
            mobile=data['mobile'],
            password=data['password']
        )
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_expense(request):
    data = request.data
    # Check expense details
    try:
        payer = get_object_or_404(User, email=data['payer_email'])
        amount = Decimal(data['amount'])
        # Amount must be greater than 0
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        split_method = data['split_method'] # Read the split method entered
        participants = data['participants'] # Read the participants included in expense
        
        # percentage validation
        if split_method == 'percentage':
            total_percentage = sum([p['percentage'] for p in participants])
            # If total percentage is not 100 display error message
            if total_percentage != 100:
                return Response({'error': 'Total percentages must equal 100'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the expense object
        expense = Expense.objects.create(
            description=data['description'],
            amount=amount,
            payer=payer,
            split_method=split_method
        )

        # Add participants to the expense object
        for participant_data in participants:
            user = get_object_or_404(User, email=participant_data['email'])  # Check if the user exists

            # Handle the amount splitting methods
            if split_method == 'equal':
                participant_amount = amount / len(participants)
            elif split_method == 'exact':
                participant_amount = Decimal(participant_data['amount'])
            elif split_method == 'percentage':
                participant_amount = amount * (Decimal(participant_data['percentage']) / 100)

            # Create ExpenseParticipant object
            ExpenseParticipant.objects.create(
                expense=expense,
                user=user,
                amount=participant_amount
            )

        return Response({'message': 'Expense added successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
# Get user expenses
def user_expenses(request, email):
    user = User.objects.get(email=email)
    expenses = ExpenseParticipant.objects.filter(user=user).select_related('expense')
    expense_data = [{'description': p.expense.description, 'amount': p.amount} for p in expenses]

    return Response({'expenses': expense_data}, status=status.HTTP_200_OK)

@api_view(['GET'])
# Get overall expenses
def overall_expenses(request):
    expenses = Expense.objects.all()
    expense_data = [{'description': e.description, 'amount': e.amount, 'payer': e.payer.email} for e in expenses]
    return JsonResponse({'expenses': expense_data}, status=200)

@api_view(['GET'])
# Download balance sheet view
# The balance sheet contains "Overall Expenses", "Expense of each user" also "Share of each user in each expense"
def download_balance_sheet(request):
    # Get all users and their individual expenses
    users = User.objects.all()
    expenses = Expense.objects.all()

    # Create a CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

    writer = csv.writer(response)

    # Header
    writer.writerow(['User', 'Mobile', 'Total Expenses', 'Description', 'Amount', 'Payer'])

    # Loop through each user
    for user in users:
        total_user_expense = ExpenseParticipant.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

        # Write each user's total expenses
        writer.writerow([user.name, user.mobile, total_user_expense])

        # Loop through individual expenses associated with this user
        for participant in ExpenseParticipant.objects.filter(user=user):
            writer.writerow([
                '',  # Empty because this row is for the expense breakdown
                '',
                '',  # Empty, we're showing details
                participant.expense.description,
                participant.amount,
                participant.expense.payer.email
            ])

    # Overall expense summary
    writer.writerow([''])
    writer.writerow(['Overall Expenses Summary'])

    for expense in expenses:
        writer.writerow([
            expense.description,
            expense.amount,
            expense.payer.email
        ])

    return response
