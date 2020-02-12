from django.db import models

############################################################
# Name: Project
# Desc: The Project model simply defines all the necessary 
# attributes that Harvest's .csv file contains. 
############################################################
class Project(models.Model):
    date_text = models.DateField()
    client_text = models.CharField(max_length=50)
    project_text = models.CharField(max_length=50)
    project_code_text = models.CharField(max_length=10)
    task_text = models.CharField(max_length=50)
    notes_text = models.CharField(max_length=200)
    hours_decimal = models.DecimalField(max_digits=12, decimal_places=2)
    billable_text = models.CharField(max_length=10)
    invoiced_text = models.CharField(max_length=10)
    approved_text = models.CharField(max_length=10, null = True)
    first_name_text = models.CharField(max_length=50)
    last_name_text = models.CharField(max_length=50)
    roles_text = models.CharField(max_length=20)
    employee_text = models.CharField(max_length=10)
    billable_rate_text = models.CharField(max_length=10)
    billable_amount_decimal = models.DecimalField(max_digits=12, decimal_places=2)
    cost_rate_text = models.CharField(max_length=20)
    cost_amount_decimal = models.DecimalField(max_digits=12, decimal_places=2)
    currency_text = models.CharField(max_length=50)
    external_reference_text = models.CharField(max_length=200)

    def __str__(self):
        return self.project_text
