from django.shortcuts import render, redirect
from django.http import HttpResponse
from harvest.models import Project
import csv

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def upload_csv(request, template_name='harvest/upload_csv.html'):
    data = {}

    if "GET" == request.method:
        return render(request, "harvest/upload_csv.html", data)
    
    # Django saves file input to request.FILES
    csv_file = request.FILES["csv_file"]

    # Decode raw input to utf-8
    file_data = csv_file.read().decode("utf-8")

    # Utf-8 data to iterable list, needed for csv reader
    list_data = file_data.splitlines()

    # Define the csv dictionary reader
    reader = csv.DictReader(list_data)

    # Clear the 'harvest_project' DB 
    Project.objects.all().delete()

    # Bulk create notation
    # TODO: Need to test time difference, seems faster
    objs = [
            Project(
                date_text= date_formatter(row['Date']),
                client_text=row['Client'],
                project_text=row['Project'],
                project_code_text=row['Project Code'],
                task_text=row['Task'],
                notes_text=row['Notes'],
                hours_decimal=row['Hours'],
                billable_text=row['Billable?'],
                invoiced_text=row['Invoiced?'],
                approved_text=row['Approved?'],
                first_name_text=row['First Name'],
                last_name_text=row['Last Name'],
                roles_text=row['Roles'],
                employee_text=row['Employee?'],
                billable_rate_text=row['Billable Rate'],
                billable_amount_decimal=row['Billable Amount'],
                cost_rate_text=row['Cost Rate'],
                cost_amount_decimal=row['Cost Amount'],
                currency_text=row['Currency'],
                external_reference_text=row['External Reference URL']
                )
            for row in reader
            ]
    p = Project.objects.bulk_create(objs)

    """
    # For loop notation
    for row in reader:
        # "Model Name" = row["CSV Name"]
        p = Project(
                date_text= date_formatter(row['Date']),
                client_text=row['Client'],
                project_text=row['Project'],
                project_code_text=row['Project Code'],
                task_text=row['Task'],
                notes_text=row['Notes'],
                hours_decimal=row['Hours'],
                billable_text=row['Billable?'],
                invoiced_text=row['Invoiced?'],
                approved_text=row['Approved?'],
                first_name_text=row['First Name'],
                last_name_text=row['Last Name'],
                roles_text=row['Roles'],
                employee_text=row['Employee?'],
                billable_rate_text=row['Billable Rate'],
                billable_amount_decimal=row['Billable Amount'],
                cost_rate_text=row['Cost Rate'],
                cost_amount_decimal=row['Cost Amount'],
                currency_text=row['Currency'],
                external_reference_text=row['External Reference URL']
                )
        p.save()
    """

    return HttpResponseRedirect(reverse("search"))

# From: MM/DD/YYYY  harvest format
# To:   YYYY-MM-DD  sqlite format
def date_formatter(harvest_date):
    date_list = harvest_date.split('/')
    sqlite_date = date_list[2] + "-" + date_list[0] + "-" + date_list[1]
    return sqlite_date


def search(request, template_name='harvest/search.html'):
    # Grab distinct project names
    projects = Project.objects.values('project_text').distinct()
    return render(request, template_name, {'projects': projects})


def results(request, template_name='harvest/results.html'):
    data = {}
    codes = ['INT', 'EXT', 'MNT']

    # Check data posted from /search
    if request.method == 'POST':
        post_data = request.POST.copy()
        data['start_date'] = post_data.get('start-date')
        data['end_date'] = post_data.get('end-date')
        # Project name or three character code?
        data['project_type'] = post_data.get('project-type')
        if data['project_type'] in codes:
            data['is_code'] = True
        else:
            data['is_code'] = False
        data['hours_checkbox'] = post_data.get('hours-checkbox')
        data['billable_checkbox'] = post_data.get('billable-checkbox')
        data['cost_checkbox'] = post_data.get('cost-checkbox')
        
        data['results'] = calculate(data)
        #results = calculate(data)
        print(data['results']['hours'])

    return render(request, template_name, {'data': data})
    

def calculate(data):

    # By project code (INT, EXT or MNT)
    if data['is_code']:
        sql = Project.objects.raw('''   SELECT * 
                                        FROM harvest_project 
                                        WHERE project_code_text = %s 
                                        AND date_text BETWEEN %s AND %s;
                                  ''', [data['project_type'],  data['start_date'], data['end_date']])
    # By project name
    else:
        sql = Project.objects.raw('''   SELECT * 
                                        FROM harvest_project 
                                        WHERE project_text = %s 
                                        AND date_text BETWEEN %s AND %s;
                                  ''', [data['project_type'],  data['start_date'], data['end_date']])

    # Calculate and gather results
    results = {}
    results['name'] = data['project_type']
    results['count'] = len(sql)
    results['hours'] = 0
    results['billable'] = 0
    results['cost'] = 0
    for elem in sql: 
        if data['hours_checkbox']:
            results['hours'] += elem.hours_decimal

        if data['billable_checkbox']:
            results['billable'] += elem.billable_amount_decimal

        if data['cost_checkbox']:
            results['cost'] += elem.cost_amount_decimal

    return results

