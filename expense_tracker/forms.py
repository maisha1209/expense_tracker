from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Budget, Category, BudgetCategoryAmount
from .models import SavingsGoal

#class SignUpForm(UserCreationForm):
 #   email = forms.EmailField(required=True)

 #   class Meta:
 #       model = User
 #       fields = ["username", "email", "password1", "password2"]

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['date', 'user']
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['description', 'user']

class BudgetCategoryAmountForm(forms.ModelForm):
    class Meta:
        model = BudgetCategoryAmount
        fields = ['amount']




class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['goal_name', 'target_amount', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }