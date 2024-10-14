from django.contrib import admin
from .models import Income, Expense, Goal, Category


admin.site.register([Income, Expense, Goal, Category])