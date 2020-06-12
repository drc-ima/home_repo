from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


HOME_TYPE = {
    ('Condo', 'Condo'),
    ('Commercial Building', 'Commercial Building'),
    ('Land Property', 'Land Property')
}

PROPERTY_TYPE = {
    ('Rent', 'Rent'),
    ('Sale', 'Sale')
}


class Property(models.Model):
    property_id = models.CharField(max_length=50, blank=True, null=True)
    property_type = models.CharField(choices=PROPERTY_TYPE, max_length=50, blank=True, null=True)
    home_type = models.CharField(choices=HOME_TYPE, max_length=50, blank=True, null=True)
    year_built = models.CharField(max_length=50, blank=True, null=True)
    price_sqft = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    gallery = models.FileField(blank=True, null=True, upload_to="gallery/")
    beds = models.IntegerField(blank=True, null=True)
    baths = models.IntegerField(blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)
    sqft = models.IntegerField(blank=True, null=True)
    located = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    bought = models.BooleanField(blank=True, null=True, default=False)
    title = models.CharField(max_length=50, blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='added_by')
    added_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    client_requests = models.ManyToManyField('Client', related_name='client_requests', blank=True)

    def __str__(self):
        return self.title


class Client(models.Model):
    client_id = models.CharField(max_length=50, blank=True, null=True)
    propertie = models.ForeignKey(Property, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='client_property')
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    pay_id = models.CharField(max_length=50, blank=True, null=True)
    propertie = models.ForeignKey(Property, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='payment_property')
    payment_type = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    card_type = models.CharField(max_length=50, blank=True, null=True)
    visa_master = models.CharField(max_length=50, blank=True, null=True)
    carrier = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='payment_client')
    expiry_date = models.DateField(blank=True, null=True)
    cvv = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.pay_id


class Receipt(models.Model):
    receipt_id = models.CharField(max_length=50, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='client_receipt')
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='payment_receipt')
    propertie = models.ForeignKey(Property, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='property_receipt')
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.receipt_id




