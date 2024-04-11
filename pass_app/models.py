from django.db import models
from django.utils.translation import gettext_lazy as _


class PassChoice(models.TextChoices):
    COUPON = 'coupon', 'Coupon'
    EVENTTICKET = 'eventTicket', 'Event'
    GENERIC = 'generic', 'Generic'
    STORECARD = 'storeCard', 'Storecard'


class Alignment(models.TextChoices):
    LEFT = "PKTextAlignmentLeft", "Left"
    CENTER = "PKTextAlignmentCenter", "Center"
    RIGHT = "PKTextAlignmentRight", "Right"
    JUSTIFIED = "PKTextAlignmentJustified", "Justified"
    NATURAL = "PKTextAlignmentNatural", "Natural"


class BarcodeFormat(models.TextChoices):
    PDF417 = "PKBarcodeFormatPDF417", "PDF417"
    QR = "PKBarcodeFormatQR", "QR"
    AZTEC = "PKBarcodeFormatAztec", "Aztec"
    # is not supported with apple watch
    CODE128 = 'PKBarcodeFormatCode128', 'Code128'


class DateStyle(models.TextChoices):
    NONE = "PKDateStyleNone", "None"
    SHORT = "PKDateStyleShort", "Short"
    MEDIUM = "PKDateStyleMedium", "Medium"
    LONG = "PKDateStyleLong", "Long"
    FULL = "PKDateStyleFull", "Full"


class NumberStyle(models.TextChoices):
    DECIMAL = "PKNumberStyleDecimal", "Decimal"
    PERCENT = "PKNumberStylePercent", "Percent"
    SCIENTIFIC = "PKNumberStyleScientific", "Scientific"
    SPELLOUT = "PKNumberStyleSpellOut", "Spell Out"


class Field(models.Model):
    key = models.CharField(_('Key'), max_length=255)
    value = models.CharField(_('Value'), max_length=255)
    label = models.CharField(_('Label'), max_length=255, null=True)
    change_message = models.CharField(
        _('Change Message'), max_length=255, blank=True, null=True)
    text_alignment = models.CharField(
        _('Text Alignment'), max_length=50, choices=Alignment.choices, null=True, blank=True)
    number_style = models.CharField(
        _('Number Style '), max_length=50, choices=NumberStyle.choices, null=True, blank=True)
    time_style = models.CharField(
        _('Time Style '), max_length=50, choices=DateStyle.choices, null=True, blank=True)
    date_style = models.CharField(
        _('Date Style '), max_length=50, choices=DateStyle.choices, null=True, blank=True)

    def get_dict_field(self) -> dict:
        data = {
            'key': self.key,
            'value': self.value,
            'label': self.label,
            'change_message': self.change_message,
            'textAlignment': self.text_alignment,
            'numberStyle': self.number_style,
            'timeStyle': self.time_style,
            'dateStyle': self.date_style
        }

        return {key: value for key, value in data.items() if value is not None}

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _('Field')
        verbose_name_plural = _('Fields')


class Barcode(models.Model):
    message = models.CharField(_('Barcode message'), max_length=255)
    format = models.CharField(_('Barcode format'),
                              max_length=50, choices=BarcodeFormat.choices, default=BarcodeFormat.PDF417)
    alt_text = models.CharField(
        _('Text'), max_length=255, blank=True, null=True)
    message_encoding = models.CharField(
        _('Encoding'), max_length=50, default='iso-8859-1')

    def get_dict_barcode(self):
        data = {
            'message': self.message,
            'format': self.format,
            'message_encoding': self.message_encoding,
            'alt_text': self.alt_text
        }
        return {key: value for key, value in data.items() if value is not None}

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = _('Barcode')
        verbose_name_plural = _('Barcodes')


class Location(models.Model):
    latitude = models.FloatField(_('Latitude'))
    longitude = models.FloatField(_('Longtitude'))
    altitude = models.FloatField(_('Altitude'), default=0.0, blank=True)

    def get_dict_location(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'altitude': self.altitude
        }

    def __str__(self) -> str:
        return f'{self.latitude}-{self.longitude}'

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')


class PassInformation(models.Model):
    headerFields = models.ManyToManyField(
        Field, related_name='header_fields', blank=True)
    primaryFields = models.ManyToManyField(
        Field, related_name='primary_fields', blank=True)
    secondaryFields = models.ManyToManyField(
        Field, related_name='secondary_fields', blank=True)
    backFields = models.ManyToManyField(
        Field, related_name='back_fields', blank=True)
    auxiliaryFields = models.ManyToManyField(
        Field, related_name='auxiliary_fields', blank=True)

    def get_dict(self) -> dict:
        d = {}
        if self.headerFields.exists():
            d['headerFields'] = [field.get_dict_field()
                                 for field in self.headerFields.all()]
        if self.primaryFields.exists():
            d['primaryFields'] = [field.get_dict_field()
                                  for field in self.primaryFields.all()]
        if self.secondaryFields.exists():
            d['secondaryFields'] = [field.get_dict_field()
                                    for field in self.secondaryFields.all()]
        if self.backFields.exists():
            d['backFields'] = [field.get_dict_field()
                               for field in self.backFields.all()]
        if self.auxiliaryFields.exists():
            d['auxiliaryFields'] = [field.get_dict_field()
                                    for field in self.auxiliaryFields.all()]
        return d

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = _('Pass Info')


class Pass(models.Model):
    # Required
    formatVersion = models.IntegerField(_('Format Version'), default=1)
    description = models.TextField(_('Description'))
    passTypeIdentifier = models.CharField(
        _('Pass Type Identifier'), max_length=255)
    serialNumber = models.CharField(_('Serial Number'), max_length=255)
    teamIdentifier = models.CharField(_('Team Identifier'), max_length=255)
    organizationName = models.CharField(_('Organization Name'), max_length=255)
    # Optional
    webServiceURL = models.URLField(
        _('Web Service URL'), blank=True, null=True)
    authenticationToken = models.CharField(
        _('Authentication Token'), max_length=255, blank=True, null=True)
    suppressStripShine = models.BooleanField(
        _('Suppress Strip Shine'), null=True, blank=True)
    relevantDate = models.DateTimeField(
        _('Relevant Date'), blank=True, null=True)
    logoText = models.CharField(
        _('Logo Text'), max_length=255, blank=True, null=True)
    foregroundColor = models.CharField(
        _('Foreground Color'), max_length=255, blank=True, null=True)
    backgroundColor = models.CharField(
        _('Background Color'), max_length=255, blank=True, null=True)
    labelColor = models.CharField(
        _('Label Color'), max_length=255, blank=True, null=True)
    expirationDate = models.DateTimeField(
        _('Expire Date'), blank=True, null=True)

    pass_information = models.ManyToManyField(
        PassInformation, related_name="passes")
    barcode = models.OneToOneField(
        Barcode, related_name="barcodes", on_delete=models.CASCADE)
    locations = models.ForeignKey(
        Location, related_name="locations", on_delete=models.CASCADE)

    json_name = models.CharField(
        _('Name pass'), choices=PassChoice.choices, default='')

    def get_full_dict(self):

        d = {
            'formatVersion': self.formatVersion,
            'description': self.description,
            'passTypeIdentifier': self.passTypeIdentifier,
            'serialNumber': self.serialNumber,
            'teamIdentifier': self.teamIdentifier,
            'organizationName': self.organizationName,
            'barcode': self.barcode.get_dict_barcode(),
            'locations': self.locations.get_dict_location()
        }

        if self.suppressStripShine:
            d['suppressStripShine'] = self.suppressStripShine
        if self.webServiceURL:
            d['webServiceURL'] = self.webServiceURL
        if self.authenticationToken:
            d['authenticationToken'] = self.authenticationToken
        if self.relevantDate:
            d['relevantDate'] = self.relevantDate.isoformat()
        if self.logoText:
            d['logoText'] = self.logoText
        if self.foregroundColor:
            d['foregroundColor'] = self.foregroundColor
        if self.backgroundColor:
            d['backgroundColor'] = self.backgroundColor
        if self.labelColor:
            d['labelColor'] = self.labelColor
        if self.expirationDate:
            d['expirationDate'] = self.expirationDate.isoformat()

        pass_information_data = {}
        for info in self.pass_information.all():
            pass_information_data.update(info.get_dict())

        d[self.json_name] = pass_information_data

        return d

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Pass')
        verbose_name_plural = _('Passes')
