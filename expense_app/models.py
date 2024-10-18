import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModelMixin(models.Model):
    id = models.CharField(max_length=300, unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModelMixin):
    name = models.CharField(max_length=299)

    def __str__(self):
        return self.name
    

class Income(BaseModelMixin):
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def current_income(cls, user):
        """return the current income for the user"""
        print(cls.objects.filter(user=user).order_by("-created_at").first())
        return cls.objects.filter(user=user).order_by("-created_at").first()


class Expense(BaseModelMixin):
    description = models.CharField(max_length=700)
    is_fixed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)

    def serialized_fields(self):
        return {
            "description": self.description,
            "is_fixed": self.is_fixed,
            "user": self.user.username,
            "category": self.category.name,
            "amount": float(self.amount)
        }

    def __str__(self):
        return self.description[:30]

class Goal(BaseModelMixin):

    STATUS = (
        ("COMPLETE", "COMPLETE"),
        ("ACTIVE", "ACTIVE")
    )

    estimated_amount = models.DecimalField(max_digits=16, null=True, blank=True, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS, default="ACTIVE")
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
