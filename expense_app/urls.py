from django.urls import path
from .views import HomePageView, DashboardView, ExpenseCreateView, ResetExpenses


urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("expense/", ExpenseCreateView.as_view(), name="expense_create"),
    path("reset/", ResetExpenses.as_view(), name="reset_expense"),
    path("", HomePageView.as_view(), name="home"),
]