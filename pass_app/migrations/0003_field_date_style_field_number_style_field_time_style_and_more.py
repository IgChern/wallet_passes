# Generated by Django 4.2.7 on 2024-04-10 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pass_app', '0002_remove_passinformation_json_name_pass_json_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='date_style',
            field=models.CharField(blank=True, choices=[('PKDateStyleNone', 'None'), ('PKDateStyleShort', 'Short'), ('PKDateStyleMedium', 'Medium'), ('PKDateStyleLong', 'Long'), ('PKDateStyleFull', 'Full')], max_length=50, null=True, verbose_name='Date Style '),
        ),
        migrations.AddField(
            model_name='field',
            name='number_style',
            field=models.CharField(blank=True, choices=[('PKNumberStyleDecimal', 'Decimal'), ('PKNumberStylePercent', 'Percent'), ('PKNumberStyleScientific', 'Scientific'), ('PKNumberStyleSpellOut', 'Spell Out')], max_length=50, null=True, verbose_name='Number Style '),
        ),
        migrations.AddField(
            model_name='field',
            name='time_style',
            field=models.CharField(blank=True, choices=[('PKDateStyleNone', 'None'), ('PKDateStyleShort', 'Short'), ('PKDateStyleMedium', 'Medium'), ('PKDateStyleLong', 'Long'), ('PKDateStyleFull', 'Full')], max_length=50, null=True, verbose_name='Time Style '),
        ),
        migrations.AlterField(
            model_name='field',
            name='label',
            field=models.CharField(max_length=255, null=True, verbose_name='Label'),
        ),
        migrations.AlterField(
            model_name='field',
            name='text_alignment',
            field=models.CharField(blank=True, choices=[('PKTextAlignmentLeft', 'Left'), ('PKTextAlignmentCenter', 'Center'), ('PKTextAlignmentRight', 'Right'), ('PKTextAlignmentJustified', 'Justified'), ('PKTextAlignmentNatural', 'Natural')], max_length=50, null=True, verbose_name='Text Alignment'),
        ),
    ]