# Generated by Django 4.2.7 on 2024-04-09 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pass_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pass',
            name='pass_information',
        ),
        migrations.AddField(
            model_name='pass',
            name='pass_information',
            field=models.ManyToManyField(related_name='passes', to='pass_app.passinformation'),
        ),
    ]