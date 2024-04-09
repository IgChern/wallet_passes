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
    label = models.CharField(_('Label'), max_length=255, blank=True)
    change_message = models.CharField(
        _('Change Message'), max_length=255, blank=True)
    text_alignment = models.CharField(
        _('Text Alignment'), max_length=50, choices=Alignment.choices, default=Alignment.LEFT)

    def get_dict_field(self) -> dict:
        return {
            'key': self.key,
            'value': self.value,
            'label': self.label,
            'change_message': self.change_message if self.change_message else None
        }

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _('Field')
        verbose_name_plural = _('Fields')


class Barcode(models.Model):
    message = models.CharField(_('Barcode message'), max_length=255)
    format = models.CharField(_('Barcode format'),
                              max_length=50, choices=BarcodeFormat.choices, default=BarcodeFormat.PDF417)
    alt_text = models.CharField(_('Text'), max_length=255, blank=True)
    message_encoding = models.CharField(
        _('Encoding'), max_length=50, default='iso-8859-1')

    def get_dict_barcode(self):
        return {
            'message': self.message,
            'format': self.format,
            'message_encoding': self.message_encoding,
            'alt_text': self.alt_text if self.alt_text else None
        }

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = _('Barcode')
        verbose_name_plural = _('Barcodes')


class Location(models.Model):
    latitude = models.FloatField(_('Latitude'))
    longitude = models.FloatField(_('Longtitude'))
    altitude = models.FloatField(_('Altitude'), default=0.0, blank=True)

    def __str__(self) -> str:
        return f'{self.latitude}-{self.longitude}'

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')


class PassInformation(models.Model):
    header_fields = models.ManyToManyField(
        Field, related_name='header_fields', blank=True)
    primary_fields = models.ManyToManyField(
        Field, related_name='primary_fields', blank=True)
    secondary_fields = models.ManyToManyField(
        Field, related_name='secondary_fields', blank=True)
    back_fields = models.ManyToManyField(
        Field, related_name='back_fields', blank=True)
    auxiliary_fields = models.ManyToManyField(
        Field, related_name='auxiliary_fields', blank=True)
    json_name = models.CharField(_('Name pass'), choices=PassChoice.choices)

    def add_header(self, key, value, label):
        field = Field.objects.create(key=key, value=value, label=label)
        self.header_fields.add(field)

    def add_primary_field(self, key, value, label):
        field = Field.objects.create(key=key, value=value, label=label)
        self.primary_fields.add(field)

    def add_secondary_field(self, key, value, label):
        field = Field.objects.create(key=key, value=value, label=label)
        self.secondary_fields.add(field)

    def add_back_field(self, key, value, label):
        field = Field.objects.create(key=key, value=value, label=label)
        self.back_fields.add(field)

    def add_auxiliary_field(self, key, value, label):
        field = Field.objects.create(key=key, value=value, label=label)
        self.auxiliary_fields.add(field)

    def get_dict(self) -> dict:
        d = {}
        if self.header_fields.exists():
            d['headerFields'] = [field.get_dict_field()
                                 for field in self.header_fields.all()]
        if self.primary_fields.exists():
            d['primaryFields'] = [field.get_dict_field()
                                  for field in self.primary_fields.all()]
        if self.secondary_fields.exists():
            d['secondaryFields'] = [field.get_dict_field()
                                    for field in self.secondary_fields.all()]
        if self.back_fields.exists():
            d['backFields'] = [field.get_dict_field()
                               for field in self.back_fields.all()]
        if self.auxiliary_fields.exists():
            d['auxiliaryFields'] = [field.get_dict_field()
                                    for field in self.auxiliary_fields.all()]
        return d

    def __str__(self):
        return self.json_name

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
        _('Suppress Strip Shine'), default=False)
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

    passInformation = models.ForeignKey(
        PassInformation, related_name="passes", on_delete=models.CASCADE)
    barcode = models.OneToOneField(
        Barcode, related_name="barcodes", on_delete=models.CASCADE)
    location = models.ForeignKey(
        Location, related_name="locations", on_delete=models.CASCADE)

    def get_full_dict(self):

        d = {
            'formatVersion': self.formatVersion,
            'description': self.description,
            'passTypeIdentifier': self.passTypeIdentifier,
            'serialNumber': self.serialNumber,
            'teamIdentifier': self.teamIdentifier,
            'organizationName': self.organizationName,
            'suppressStripShine': self.suppressStripShine,
            self.passInformation.json_name: self.passInformation.get_dict(),
            'barcode': self.barcode.get_dict_barcode()
        }

        if self.webServiceURL:
            d['webServiceURL'] = self.webServiceURL
        if self.authenticationToken:
            d['authenticationToken'] = self.authenticationToken
        if self.relevantDate:
            d['relevantDate'] = self.relevantDate
        if self.logoText:
            d['logoText'] = self.logoText
        if self.foregroundColor:
            d['foregroundColor'] = self.foregroundColor
        if self.backgroundColor:
            d['backgroundColor'] = self.backgroundColor
        if self.labelColor:
            d['labelColor'] = self.labelColor

        return d

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Pass')
        verbose_name_plural = _('Passes')
