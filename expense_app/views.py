import json
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum

from .models import User, Income, Expense, Goal, Category
from .forms import ExpenseCreateForm

class HomePageView(TemplateView):
    template_name = "expense/index.html"


class DashboardView(TemplateView, LoginRequiredMixin):
    template_name = "expense/dashboard.html"

    def get_context_data(self, **kwargs):
        # random goal
        goal = Goal.objects.filter(user = self.request.user).order_by("-created_at").first()
        all_user_expenses = Expense.objects.filter(user = self.request.user).order_by("-created_at")
        total_expenses = all_user_expenses.aggregate(Sum('amount'))
        categories = Category.objects.all().distinct()
        income = Income.current_income(self.request.user)

        # expense creation form
        expense_creation_form = ExpenseCreateForm()

        # avalable income = current - total expenses
        available_income = income.amount - total_expenses.get("amount__sum") 

        context = super().get_context_data(**kwargs)
        context['goal'] = goal
        context['expenses'] = all_user_expenses[:5] #return the latest five
        context['categories'] = categories
        context['spent_amount'] = total_expenses.get("amount__sum")
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
        
        data = json.loads(request.body)
        data.update({"user": userObj})

        print(type(data), data)
        form = self.form_class(data=data)
        # print(form)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Expense has been added successfully"})

        return JsonResponse({"error": form.errors})




