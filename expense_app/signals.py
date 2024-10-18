from django.db.models.signals import post_save
from django.dispatch import receiver
from expense_app.models import Income
from accounts.models import User

@receiver(post_save, sender=User)  # Connect to the built-in post_save signal
def create_default_income_for_user(sender, instance, created, **kwargs):
    # This function will be called automatically after Order model instance is saved
    if created:
        income = Income.objects.create(user=instance)
        income.save()
        print("Income created")