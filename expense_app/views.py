import json
from decimal import Decimal
from django.views.generic import TemplateView, View
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Sum

from datetime import datetime
from django.utils.timezone import make_aware
from django.db import transaction
from django.urls import reverse, reverse_lazy

from .models import User, Income, Expense, Goal, Category
from .forms import ExpenseCreateForm, IncomeForm, GoalForm


class HomePageView(TemplateView):
    template_name = "expense/index.html"

    def get(self, request, *args, **kwargs):
        # check if user has income
        if request.user.has_income:
            return redirect(reverse("dashboard"))
        return super().get(request, *args, **kwargs)

    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Wrap in a try-except block to handle potential errors
        data = request.POST.copy()
        amount = data.pop("amount")
        
        try:
            decimal_amount = float(amount[0])
            # Validate form inputs
            income_form = IncomeForm({"amount": decimal_amount})
            goal_form = GoalForm(request.POST)
        
            if income_form.is_valid() and goal_form.is_valid():
                # Create income and goal within the atomic transaction
                income = income_form.save(commit=False)
                income.user = request.user
                income.save()

                goal = goal_form.save(commit=False)
                goal.user = request.user
                goal.save()

                # Redirect to the dashboard
                return redirect(reverse_lazy("dashboard"))
            else:
                # If validation fails, handle it
                return self.form_invalid(income_form, goal_form)

        except ValidationError as e:
            transaction.set_rollback(True)  # Explicitly rollback on error
            return self.form_invalid(income_form, goal_form)

    def form_invalid(self, income_form, goal_form):
        # Handle the case where the form is invalid, perhaps re-render the form with errors
        context = self.get_context_data(income_form=income_form, goal_form=goal_form)
        return self.render_to_response(context)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "expense/dashboard.html"

    def get(self, request, *args, **kwargs):
        if not request.user.has_income:
            return redirect(reverse("home"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        # random goal
        goal = Goal.objects.filter(user = self.request.user).order_by("-created_at").first()
        all_user_expenses = Expense.objects.filter(user = self.request.user).order_by("-created_at")
        total_expenses = all_user_expenses.aggregate(Sum('amount'))['amount__sum'] or 0.00
        categories = Category.objects.all().distinct()
        income = Income.current_income(self.request.user)

        # expense creation form
        expense_creation_form = ExpenseCreateForm()

        # avalable income = current - total expenses
        available_income = float(income.amount) - float(total_expenses)

        context = super().get_context_data(*args, **kwargs)
        context['goal'] = goal
        context['expenses'] = all_user_expenses[:5] #return the latest five
        context['categories'] = categories
        context['spent_amount'] = total_expenses
        context['available_amount'] = available_income
        context['income'] = income.amount
        context['form'] = expense_creation_form

        return context
    

class ExpenseCreateView(LoginRequiredMixin, View):
    model = Expense
    
    form_class = ExpenseCreateForm

    def get_user(self, id):
        # The reason this method exist is becaus of the SimpleLazyObject that i'm getting
        return User.objects.get(id=id)

    def post(self, request, *args, **kwargs):
        user = request.user
        userObj = self.get_user(user.id)
        
        # Get all expenses for the user and calculate total
        all_user_expenses = Expense.objects.filter(user=userObj).order_by("-created_at")
        total_expenses = all_user_expenses.aggregate(Sum('amount'))['amount__sum'] or 0.00
        
        # Get current income for the user
        income = Income.current_income(userObj)
        # Available income = current income - total expenses
        available_income = float(income.amount) - float(total_expenses)
        
        dashboard_data = {
            "income": float(income.amount),
            "available_income": float(available_income)
        }

        # Parse request body data and add the user to it
        data = json.loads(request.body)
        data.update({"user": userObj})

        # Handle form submission
        form = self.form_class(data=data)
        if form.is_valid():
            data = form.save()
            dashboard_data['new'] = data.serialized_fields()
            return JsonResponse({"message": "Expense has been added successfully", "data": json.dumps(dashboard_data)}, status=201)

        return JsonResponse({"error": form.errors})


class ExpenseUpdateView(LoginRequiredMixin, View):
    pass


class ResetExpenses(LoginRequiredMixin, View):
    def get_user(self, id):
        # The reason this method exist is becaus of the SimpleLazyObject that i'm getting
        return User.objects.get(id=id)
    

    def post(self, request, *args, **kwargs):
        # will delete all expenses from the 1st of the current month to now
        user = request.user
        userObj = self.get_user(user.id)
        
        # Get the first day of the current month
        now = make_aware(datetime.now())
        first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Filter expenses from the first day of the current month until now
        userExpenses = Expense.objects.filter(
            user=userObj,
            created_at__gte=first_day_of_month,
            created_at__lte=now
        )
        
        # Delete the expenses
        deleted, _ = userExpenses.delete()

        return JsonResponse({
            'status': 'success',
            'message': f'{deleted} expenses deleted successfully.',
            'data': None
        }, status=200)





