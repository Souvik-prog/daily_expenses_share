from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validate_mobile_number(value):
    if len(value) != 10:
        raise ValidationError('Mobile number must be exactly 10 digits.')

# Create user and superuser (admin)    
class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            mobile=mobile
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile, password=None):
        user = self.create_user(email, name, mobile, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# User model to store user details
# email: Stores the email of an user (Must be unique)
# name: Name of the user
# mobile: Mobile Number of user
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    mobile = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$', 
                message='Mobile number must be exactly 10 digits'
            )
        ]
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    def __str__(self):
        return self.email

# Expense model to store expense details
class Expense(models.Model):
    # Split choices can be equal, exact or percentage
    SPLIT_CHOICES = (
        ('equal', 'Equal'),
        ('exact', 'Exact'),
        ('percentage', 'Percentage'),
    )

    description = models.CharField(max_length=255) # Type of expense: Say ('Lunch', 'Shopping' or 'Dinner)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Total amount spent
    payer = models.ForeignKey(User, related_name="expenses_paid", on_delete=models.CASCADE) # Payer (Foreign Key to User model): Refers to an user in User model
    split_method = models.CharField(max_length=10, choices=SPLIT_CHOICES) # split_method based on choices mentioned above
    date_created = models.DateTimeField(auto_now_add=True) # Creation data

    def __str__(self):
        return f'{self.description} - {self.amount} by {self.payer.name}'

class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, related_name="participants", on_delete=models.CASCADE) # Refers to expense table
    user = models.ForeignKey(User, related_name="expenses", on_delete=models.CASCADE) # refers to user table
    amount = models.DecimalField(max_digits=10, decimal_places=2) # amount for each participant
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # percentage share of each user