from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser,Group
from django.conf import settings
from django.utils import timezone

class CustomUser(AbstractUser):
    active_status = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20)
    financialStatus = models.TextField(default='')
    mortgageAmount = models.TextField(default='')
    mortgageType = models.TextField(default='')
    propertyLocation = models.TextField(default='')
    propertyType = models.TextField(default='')
    propertyValue = models.TextField(default='')    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Chatbot(models.Model):
    user_details = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    user_input = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_details.username +" "+self.user_input +" "+self.bot_response
    

class Ticket(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.client.username+" "+self.subject
    
    

STATUS_CHOICES = (
    ('Enquiry', 'Enquiry'),
    ('Application', 'In Application'),
    ('Completion stage', 'Completion stage'),
)    

class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    
class ChatMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender}: {self.message}"
    
class Property(models.Model):
    property=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.property


class Country(models.Model):
    country_name=models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.country_name

class PropertyType(models.Model):
    type=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.type

class SituationSearch(models.Model):
    search=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.search

    
class SituationExisting(models.Model):
    existing=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.existing
    


class CurrentCircumstances(models.Model):
    hear_my_services=models.CharField(max_length=100 ,blank=True, null=True)
    situation_regarding_search =models.ForeignKey(SituationSearch, on_delete=models.CASCADE)  
    situation_regarding_existing =models.ForeignKey(SituationExisting, on_delete=models.CASCADE)
    location_country=models.ForeignKey(Country, on_delete=models.CASCADE)
    location_town=models.CharField(max_length=50)  
    postal_address=models.TextField(blank=True, null=True)
    web_link=models.CharField(max_length=50,blank=True, null=True)
    property_type=models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    property=models.ForeignKey(Property, on_delete=models.CASCADE)
    checkbox = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.hear_my_services




OPTION = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)  

class SourceOfFunds(models.Model):
    source_of_funds=models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.source_of_funds


class MortgageRequirements(models.Model):
    purchase_price=models.IntegerField()
    currency=models.CharField(max_length=50)
    loan_required=models.IntegerField()
    years=models.IntegerField()
    savings_resources=models.CharField(max_length=50,choices=OPTION)
    source=models.ForeignKey(SourceOfFunds,on_delete=models.CASCADE)
    rent_new_property=models.CharField(max_length=50,choices=OPTION ,blank=True, null=True)
    improvements_in_property=models.CharField(max_length=50,choices=OPTION ,blank=True, null=True)
    checkbox = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.purchase_price

TITLE = (
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Miss', 'Miss'),
    ('Mx', 'Mx'),
    ('Dr', 'Dr'),
    ('Ms', 'Ms'),
    ('Ind.', 'Ind.'),
    ('Msr', 'Msr'),
    ('Mre', 'Mre'),
    ('M', 'M'),
    ('Pr', 'Pr'),
)  

class Apps(models.Model):
    apps=models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.apps

class Applicant(models.Model):
    title=models.CharField(max_length=50,choices=TITLE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    marital_status=models.CharField(max_length=50)
    nationality=models.CharField(max_length=50)
    current_residence=models.CharField(max_length=50,blank=True, null=True)
    three_years_address_history_including_dates=models.TextField()
    portfolio_details=models.TextField(blank=True, null=True)
    day_telephone=models.TextField(unique=True)
    home_telephone =models.IntegerField(blank=True, null=True)
    mobile_telephone=models.IntegerField(blank=True, null=True)
    whatsapp_telephone=models.IntegerField(blank=True, null=True)
    apps=models.ForeignKey(Apps, on_delete=models.CASCADE)
    email_address=models.CharField(max_length=50, unique=True)
    skype_address=models.CharField(max_length=50,blank=True, null=True)
    checkbox = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title +" "+self.first_name


class Status(models.Model):
    status=models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.status

class Employment(models.Model):
    status=models.ForeignKey(Status, on_delete=models.CASCADE)
    employer_name=models.CharField(max_length=50)
    employer_email=models.CharField(max_length=50, unique=True)
    occupation= models.CharField(max_length=50)
    shareholding_percent=models.IntegerField()
    employed_current_company=models.IntegerField(blank=True, null=True)  
    gross_income=  models.IntegerField(blank=True, null=True)
    income_after_tax=  models.IntegerField(blank=True, null=True)
    income_after_tax_and_pension_ANNUM=  models.IntegerField(blank=True, null=True)
    income_after_tax_and_pension_MONTH=  models.IntegerField(blank=True, null=True)
    bonus=  models.IntegerField(blank=True, null=True)
    checkbox = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.employer_name

class Loans(models.Model):
    school_fees=models.CharField(max_length=50,choices=OPTION)
    maintenance =models.CharField(max_length=50,choices=OPTION)    
    credit_card=models.CharField(max_length=50,choices=OPTION)    
    other_loans=models.CharField(max_length=50,choices=OPTION) 
    checkbox = models.BooleanField(default=False) 

    def __str__(self) -> str:
        return self.school_fees 


class AdditionalAssistance(models.Model):
    assistance=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.assistance

class Assets(models.Model):
    existing_property=models.TextField(blank=True, null=True)  
    other_savings=models.TextField(blank=True, null=True)
    bad_debts=models.CharField(max_length=50,choices=OPTION,blank=True, null=True) 
    assistance=models.ForeignKey(AdditionalAssistance, on_delete=models.CASCADE,blank=True, null=True)
    checkbox = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.existing_property


class AdditionalApplicnats(models.Model):
    applicant_form=models.CharField(max_length=50,choices=OPTION) 
    checkbox = models.BooleanField(default=False)  

    def __str__(self) -> str:
        return self.applicant_form     





    




