# Generated by Django 5.0.3 on 2024-10-17 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_app', '0003_goal_description_alter_goal_estimated_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=16),
        ),
        migrations.AlterField(
            model_name='goal',
            name='estimated_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=16, null=True),
        ),
        migrations.AlterField(
            model_name='income',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=16),
        ),
    ]
