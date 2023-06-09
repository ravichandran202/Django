# Generated by Django 4.1.7 on 2023-04-15 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("register", "0004_feedback_alter_teamregister_person3_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="teamregister",
            name="user",
            field=models.ForeignKey(
                blank=True,
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
