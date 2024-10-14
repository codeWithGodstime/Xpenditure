# Generated by Django 5.0.3 on 2024-10-14 00:15

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=300, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('estimated_amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('status', models.CharField(choices=[('COMPLETE', 'COMPLETE'), ('ACTIVE', 'ACTIVE')], default='ACTIVE', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
