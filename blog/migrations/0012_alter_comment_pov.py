# Generated by Django 4.1 on 2022-09-05 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_comment_pov'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pov',
            field=models.TextField(null=True, verbose_name='Point of view'),
        ),
    ]