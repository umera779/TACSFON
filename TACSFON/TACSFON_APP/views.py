import csv
import io
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact, AttendanceRecord


from django.http import HttpResponseForbidden

def superuser_required(view_func):
    """
    A decorator to restrict access to superusers only.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

from django.shortcuts import render
from .models import AttendanceRecord

from django.shortcuts import render
from .models import AttendanceRecord

from django.shortcuts import render
from .models import AttendanceRecord

def index(request):
    # Get the last two attendance records
    latest_attendances = AttendanceRecord.objects.all().order_by('-timestamp')[:2]

    # Prepare the data to be passed to the template
    attendance_data = []
    for attendance in latest_attendances:
        present = attendance.present.split(", ")
        absent = attendance.absent.split(", ")
        new = attendance.new.split(", ")
        # timestamp = attendance.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        attendance.formatted_timestamp = attendance.timestamp.strftime('%d %A %Y')

        attendance_data.append({
            'present': present,
            'absent': absent,
            'new': new,
            'timestamp': attendance.formatted_timestamp
        })

    # Pass the data to the template
    return render(request, 'index.html', {'attendance_data': attendance_data})


@superuser_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact added successfully!')
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, 'add_contact.html', {'form': form})

@superuser_required
def add_new_contacts(request):
    if request.method == 'POST':
        new_contacts = request.POST.getlist('new_contacts')
        for contact_data in new_contacts:
            name, phone = contact_data.split('|')
            Contact.objects.create(name=name, phone_number=phone)
        messages.success(request, f'{len(new_contacts)} new contacts added successfully!')
        return redirect('index')
    return redirect('upload_excel')



import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm, ExcelUploadForm

@superuser_required
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            
            # Check file extension
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                messages.error(request, 'Please upload an Excel file (.xlsx, .xls)')
                return redirect('upload_excel')
            
            # Store results
            attendance_results = {
                'present': [],
                'absent': [],
                'new': []
            }
            
            # Get all existing contacts for efficient comparison
            existing_contacts = list(Contact.objects.all())
            existing_phones = {contact.phone_number: contact for contact in existing_contacts}
            
            try:
                # Process Excel file using pandas
                df = pd.read_excel(excel_file)
                
                # Verify the DataFrame has at least two columns
                if len(df.columns) < 2:
                    messages.error(request, 'Excel file must have at least two columns')
                    return redirect('upload_excel')
                
                # Rename the first two columns for consistency
                df.columns.values[0] = 'name'
                df.columns.values[1] = 'phone'
                
                # Process each row in the dataframe
                excel_phones = set()
                for _, row in df.iterrows():
                    name = str(row['name']).strip()
                    phone = str(row['phone']).strip()
                    
                    # Skip rows with empty name or phone
                    if not name or not phone or pd.isna(row['name']) or pd.isna(row['phone']):
                        continue
                        
                    excel_phones.add(phone)
                    
                    if phone in existing_phones:
                        # Contact exists, mark as present
                        contact = existing_phones[phone]
                        attendance_results['present'].append({
                            'name': contact.name,
                            'phone_number': contact.phone_number
                        })
                    else:
                        # Contact doesn't exist, mark as new
                        attendance_results['new'].append({
                            'name': name,
                            'phone_number': phone
                        })
                
                # Find absent contacts (in database but not in Excel)
                for contact in existing_contacts:
                    if contact.phone_number not in excel_phones:
                        attendance_results['absent'].append({
                            'name': contact.name,
                            'phone_number': contact.phone_number
                        })
                
            except Exception as e:
                messages.error(request, f'Error processing Excel file: {str(e)}')
                return redirect('upload_excel')
            
            return render(request, 'excel_results.html', {'results': attendance_results})
    else:
        form = ExcelUploadForm()
    return render(request, 'upload_excel.html', {'form': form})


