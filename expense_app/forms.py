from django import forms

from .models import Expense


class ExpenseCreateForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["description", "is_fixed", "category",  "amount", "user"]