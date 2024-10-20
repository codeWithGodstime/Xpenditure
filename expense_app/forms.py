from django import forms
from decimal import Decimal, InvalidOperation
from .models import Expense, Income, Goal


class ExpenseCreateForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["description", "is_fixed", "category",  "amount", "user"]

    
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['estimated_amount', 'description']
    
    def clean_estimated_amount(self):
        estimated_amount = self.cleaned_data.get('estimated_amount')
        try:
            if float(estimated_amount) < 0:
                raise forms.ValidationError("Estimated amount cannot be negative.")
        except Exception as e:
            print(e)
        return estimated_amount


class IncomeForm(forms.ModelForm):
    amount = forms.DecimalField(
        max_digits=16,
        decimal_places=2,
        widget=forms.TextInput(attrs={'placeholder': 'Enter amount'})
    )
    class Meta:
        model = Income
        fields = ['amount']
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        try:
            # Attempt to convert to Decimal
            decimal_amount = Decimal(amount)
            if decimal_amount <= 0:
                raise forms.ValidationError("Income amount must be greater than zero.")
        except InvalidOperation:
            # If conversion to Decimal fails
            raise forms.ValidationError("Enter a valid number for the income amount.")
        
        return decimal_amount