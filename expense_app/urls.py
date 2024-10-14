from django.urls import path
from .views import HomePageView, DashboardView, ExpenseCreateView


urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("expense/", ExpenseCreateView.as_view(), name="expense_create"),
    path("", HomePageView.as_view(), name="home"),
]