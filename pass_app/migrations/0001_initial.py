# Generated by Django 4.2.7 on 2024-04-10 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255, verbose_name='Barcode message')),
                ('format', models.CharField(choices=[('PKBarcodeFormatPDF417', 'PDF417'), ('PKBarcodeFormatQR', 'QR'), ('PKBarcodeFormatAztec', 'Aztec'), ('PKBarcodeFormatCode128', 'Code128')], default='PKBarcodeFormatPDF417', max_length=50, verbose_name='Barcode format')),
                ('alt_text', models.CharField(blank=True, max_length=255, verbose_name='Text')),
                ('message_encoding', models.CharField(default='iso-8859-1', max_length=50, verbose_name='Encoding')),
            ],
            options={
                'verbose_name': 'Barcode',
                'verbose_name_plural': 'Barcodes',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, verbose_name='Key')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('label', models.CharField(blank=True, max_length=255, verbose_name='Label')),
                ('change_message', models.CharField(blank=True, max_length=255, verbose_name='Change Message')),
                ('text_alignment', models.CharField(choices=[('PKTextAlignmentLeft', 'Left'), ('PKTextAlignmentCenter', 'Center'), ('PKTextAlignmentRight', 'Right'), ('PKTextAlignmentJustified', 'Justified'), ('PKTextAlignmentNatural', 'Natural')], default='PKTextAlignmentLeft', max_length=50, verbose_name='Text Alignment')),
            ],
            options={
                'verbose_name': 'Field',
                'verbose_name_plural': 'Fields',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longtitude')),
                ('altitude', models.FloatField(blank=True, default=0.0, verbose_name='Altitude')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='PassInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_name', models.CharField(choices=[('coupon', 'Coupon'), ('eventTicket', 'Event'), ('generic', 'Generic'), ('storeCard', 'Storecard')], verbose_name='Name pass')),
                ('auxiliaryFields', models.ManyToManyField(blank=True, related_name='auxiliary_fields', to='pass_app.field')),
                ('backFields', models.ManyToManyField(blank=True, related_name='back_fields', to='pass_app.field')),
                ('headerFields', models.ManyToManyField(blank=True, related_name='header_fields', to='pass_app.field')),
                ('primaryFields', models.ManyToManyField(blank=True, related_name='primary_fields', to='pass_app.field')),
                ('secondaryFields', models.ManyToManyField(blank=True, related_name='secondary_fields', to='pass_app.field')),
            ],
            options={
                'verbose_name': 'Pass Info',
            },
        ),
        migrations.CreateModel(
            name='Pass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formatVersion', models.IntegerField(default=1, verbose_name='Format Version')),
                ('description', models.TextField(verbose_name='Description')),
                ('passTypeIdentifier', models.CharField(max_length=255, verbose_name='Pass Type Identifier')),
                ('serialNumber', models.CharField(max_length=255, verbose_name='Serial Number')),
                ('teamIdentifier', models.CharField(max_length=255, verbose_name='Team Identifier')),
                ('organizationName', models.CharField(max_length=255, verbose_name='Organization Name')),
                ('webServiceURL', models.URLField(blank=True, null=True, verbose_name='Web Service URL')),
                ('authenticationToken', models.CharField(blank=True, max_length=255, null=True, verbose_name='Authentication Token')),
                ('suppressStripShine', models.BooleanField(blank=True, null=True, verbose_name='Suppress Strip Shine')),
                ('relevantDate', models.DateTimeField(blank=True, null=True, verbose_name='Relevant Date')),
                ('logoText', models.CharField(blank=True, max_length=255, null=True, verbose_name='Logo Text')),
                ('foregroundColor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Foreground Color')),
                ('backgroundColor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Background Color')),
                ('labelColor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Label Color')),
                ('expirationDate', models.DateTimeField(blank=True, null=True, verbose_name='Expire Date')),
                ('barcode', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='barcodes', to='pass_app.barcode')),
                ('locations', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='pass_app.location')),
                ('pass_information', models.ManyToManyField(related_name='passes', to='pass_app.passinformation')),
            ],
            options={
                'verbose_name': 'Pass',
                'verbose_name_plural': 'Passes',
            },
        ),
    ]
