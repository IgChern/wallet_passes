# Generated by Django 4.2.7 on 2024-04-09 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pass_app', '0002_alter_passinformation_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pass',
            options={'verbose_name': 'Pass', 'verbose_name_plural': 'Passes'},
        ),
    ]
