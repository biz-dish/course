# Generated by Django 4.1 on 2022-10-05 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0033_room_delete_pv'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='user2',
            new_name='user_tar',
        ),
        migrations.RemoveField(
            model_name='room',
            name='message',
        ),
        migrations.RemoveField(
            model_name='room',
            name='user1',
        ),
        migrations.AddField(
            model_name='room',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
