# from django import forms
# from .models import Contact

# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = ['name', 'phone_number']

# class CSVUploadForm(forms.Form):
#     csv_file = forms.FileField(label='Select a CSV file')

from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number']

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='Select an Excel file',
        help_text='Accepted formats: .xlsx, .xls'
    )
