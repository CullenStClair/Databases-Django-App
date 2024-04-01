import datetime

from hotel_system.models import Customer

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class BookingForm(forms.Form):
    customer_id = forms.IntegerField(help_text='Enter your customer ID.')
    check_in_date = forms.DateField(help_text='(dd/mm/yyyy)')
    check_out_date = forms.DateField(help_text='(dd/mm/yyyy)')

    def clean_customer_id(self):
        try:
            customer = Customer.objects.get(id=self.cleaned_data['customer_id'])
        except Customer.DoesNotExist:
            raise ValidationError(_('Invalid customer ID - customer id does not exist.'))
        return customer


    def clean_check_in_date(self):
        check_in = self.cleaned_data['check_in_date']

        # Check if a date is not in the past.
        if check_in < datetime.date.today():
            raise ValidationError(_('Invalid date - check-in in past.'))

        # Remember to always return the cleaned check_in.
        return check_in

    def clean_check_out_date(self):
        check_in = self.cleaned_data['check_in_date']
        check_out = self.cleaned_data['check_out_date']

        # Check if a date is not in the past.
        if check_out < datetime.date.today():
            raise ValidationError(_('Invalid date - check-out in past'))

        if check_out < check_in:
            raise ValidationError(_('Invalid date - check-out date before check-in'))

        # Remember to always return the cleaned data.
        return check_out
