from django import forms
from .models import User, Schedule, Branch
import datetime
#import numpy as np

class UserForm(forms.Form):
    id = forms.IntegerField(widget=forms.NumberInput
                (attrs={'id':'uid','tabindex':'1','class':'input-sm text-right numonly','placeholder':'Associate ID','required':'required'})
                    )  
    
    FName = forms.CharField(widget=forms.TextInput
                (attrs={'id':'FName','tabindex':'2','class':'input-sm','style':'width: 100%;','placeholder':'Given Name','required':'required'})
                    )  
    
    MName = forms.CharField(widget=forms.TextInput
                (attrs={'id':'MName','tabindex':'3','class':'input-sm','style':'width: 100%;','placeholder':'Middle','required':'required'})
                    )  
    
    LName = forms.CharField(widget=forms.TextInput
                (attrs={'id':'LName','tabindex':'4','class':'input-sm','style':'width: 100%;','placeholder':'Last Name','required':'required'})
                    )
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        approverchoices = [(None,'------------')]
        for x in User.objects.filter(isadmin=1).order_by('LName'):
            approverchoices.append((x.id, x.LName + ", " + x.FName + " " + x.MName)) 
            
        self.fields['Gender'] = forms.ChoiceField(choices=[('Male','Male'),('Female','Female')],
                                    widget=forms.Select
                                    (attrs={'id':'Gender','tabindex':'5','class':'input-sm', 'style':'vertical-align: middle; '})
                                    )
        
        self.fields['Approver'] = forms.ChoiceField(choices=approverchoices,
                                    widget=forms.Select
                                    (attrs={'id':'Approver','tabindex':'6','class':'input-sm', 'style':'vertical-align: middle;'})
                                    )
        
        
        branchchoices = [(None,'--- SELECT BRANCH ---')]
        for z in Branch.objects.all():
            branchchoices.append((z.Description, z.Description)) 
    
        self.fields['Branch'] = forms.ChoiceField(choices=branchchoices,
                                    widget=forms.Select
                                    (attrs={'id':'Branch','tabindex':'12','class':'input-sm','style':'width: 100%;','placeholder':'Branch','required':'required'})
                                    )
        
        self.fields['CivilStatus'] = forms.ChoiceField(choices=[('Single','Single'),('Married','Married'),('Widowed','Widowed'),('Separated','Separated')],
                                    widget=forms.Select
                                    (attrs={'id':'CivilStatus','tabindex':'23','class':'input-sm','style':'width: 20%; vertical-align: middle;'})
                                    )
        
        
        self.fields['BloodType'] = forms.ChoiceField(choices=[('O','O'),('O+','O+'),('O-','O-'),('A','A'),('A+','A+'),('A-','A-'),('B','B'),('B+','B+'),('B-','B-'),('AB','AB'),('AB+','AB+'),('AB-','AB-')],
                                    widget=forms.Select
                                    (attrs={'id':'BloodType','tabindex':'25','class':'input-sm','style':'width: 20%; vertical-align: middle;'})
                                    )
        
        
    Division = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Division','tabindex':'8','class':'input-sm','style':'width: 100%;','placeholder':'Division'})
                    )  
    
    Dept = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Dept','tabindex':'9','class':'input-sm','style':'width: 100%;','placeholder':'Department'})
                    )  
    
    SSSNo = forms.CharField(widget=forms.TextInput
                (attrs={'id':'SSSNo','tabindex':'14','class':'input-sm','style':'width: 100%;','placeholder':'SSS ID'})
                    )  
    
    PagIBIGNo = forms.CharField(widget=forms.TextInput
                (attrs={'id':'PagIBIGNo','tabindex':'15','class':'input-sm','style':'width: 100%;','placeholder':'Pag-IBIG ID'})
                    )  
    
    PhilHealthNo = forms.CharField(widget=forms.TextInput
                (attrs={'id':'PhilHealthNo','tabindex':'16','class':'input-sm','style':'width: 100%;','placeholder':'PhilHealth ID'})
                    )  
    
    
    
    
    Level = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Level','tabindex':'11','class':'input-sm uppercase','style':'width: 100%;','placeholder':'Level'})
                    )  
    
    RegDate = forms.DateField(
            widget=forms.DateInput
                (attrs={'id':'RegDate','tabindex':'13','class':'input-sm datepicker','style':'width: 100%;','readonly':'readonly'})
                    )
    
    
    TINNo = forms.CharField(widget=forms.TextInput
                (attrs={'id':'TINNo','tabindex':'17','class':'input-sm','style':'width: 100%;','placeholder':'TIN ID'})
                    )
    
    TaxCode = forms.CharField(widget=forms.TextInput
                (attrs={'id':'TaxCode','tabindex':'18','class':'input-sm uppercase','style':'width: 100%;','placeholder':'Tax Code'})
                    )
    
    TaxExemption = forms.CharField(widget=forms.TextInput
                (attrs={'id':'TaxExemption','tabindex':'19','class':'input-sm numdot amts text-right','style':'width: 100%;','placeholder':'Tax Exemption'})
                    )
    
    Designation = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Designation','tabindex':'10','class':'input-sm','style':'width: 100%;','placeholder':'Designation'})
                    )
    
    HomeAddress = forms.CharField(widget=forms.TextInput
                (attrs={'id':'HomeAddress','tabindex':'21','class':'input-sm','style':'width: 90%;','placeholder':'Home Address'})
                    )
    
    Email = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Email','tabindex':'22','class':'input-sm','style':'width: 50%;','placeholder':'Email Address'})
                    )
    #CIVIL STATUS#
    
    BDate = forms.DateField(
            widget=forms.DateInput
                (attrs={'id':'BDate','tabindex':'24','class':'input-sm datepicker','style':'width: 20%;','readonly':'readonly'})
                    )
    
    #BLOOD TYPE#
    
    Religion = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Religion','tabindex':'26','class':'input-sm','style':'width: 40%;','placeholder':'Religion'})
                    )
    
    Citizenship = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Citizenship','tabindex':'27','class':'input-sm','style':'width: 40%;','placeholder':'Citizenship'})
                    )
    
   
   
   
   
   
   
   
class EditForm(forms.Form):
    FNameedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'FNameedit','tabindex':'1','class':'input-sm','style':'width: 100%;','placeholder':'First Name','required':'required'})
                    )  
    
    MNameedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'MNameedit','tabindex':'2','class':'input-sm','style':'width: 100%;','placeholder':'Middle Name','required':'required'})
                    )  
    
    LNameedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'LNameedit','tabindex':'3','class':'input-sm','style':'width: 100%;','placeholder':'Last Name','required':'required'})
                    )
    
    
    
    
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        
        approverchoices = [(None,'------------')]
        for x in User.objects.filter(isadmin=1).order_by('LName'):
            approverchoices.append((x.id, x.LName + ", " + x.FName + " " + x.MName)) 

        self.fields['Genderedit'] = forms.ChoiceField(choices=[('Male','Male'),('Female','Female')],
                                    widget=forms.Select
                                    (attrs={'id':'Genderedit','tabindex':'4','class':'input-sm', 'style':'vertical-align: middle; '})
                                    )
    
        self.fields['Approveredit'] = forms.ChoiceField(choices=approverchoices,
                                    widget=forms.Select
                                    (attrs={'id':'Approveredit','tabindex':'5','class':'input-sm', 'style':'vertical-align: middle;'})
                                    )
        
        
        branchchoices = [(None,'--- SELECT BRANCH ---')]
        for z in Branch.objects.all():
            branchchoices.append((z.Description, z.Description)) 
    
        self.fields['Branchedit'] = forms.ChoiceField(choices=branchchoices,
                                    widget=forms.Select
                                    (attrs={'id':'Branchedit','tabindex':'11','class':'input-sm','required':'required'})
                                    )
        
        self.fields['CivilStatusedit'] = forms.ChoiceField(choices=[('Single','Single'),('Married','Married'),('Widowed','Widowed'),('Separated','Separated')],
                                    widget=forms.Select
                                    (attrs={'id':'CivilStatusedit','tabindex':'22','class':'input-sm', 'style':'width: 20%; vertical-align: middle;'})
                                    )
        
        self.fields['BloodTypeedit'] = forms.ChoiceField(choices=[('O','O'),('O+','O+'),('O-','O-'),('A','A'),('A+','A+'),('A-','A-'),('B','B'),('B+','B+'),('B-','B-'),('AB','AB'),('AB+','AB+'),('AB-','AB-')],
                                    widget=forms.Select
                                    (attrs={'id':'BloodTypeedit','tabindex':'24','class':'input-sm','style':'width: 20%; vertical-align: middle;'})
                                    )
         
        
    Divisionedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Divisionedit','tabindex':'7','class':'input-sm','style':'width: 100%;','placeholder':'Division'})
                    )  
    
    Deptedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Deptedit','tabindex':'8','class':'input-sm','style':'width: 100%;','placeholder':'Department'})
                    )  
       
    SSSNoedit= forms.CharField(widget=forms.TextInput
                (attrs={'id':'SSSNoedit','tabindex':'13','class':'input-sm','style':'width: 100%;','placeholder':'SSS ID'})
                    )  
    
    PagIBIGNoedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'PagIBIGNoedit','tabindex':'14','class':'input-sm','style':'width: 100%;','placeholder':'Pag-IBIG ID'})
                    )  
    
    PhilHealthNoedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'PhilHealthNoedit','tabindex':'15','class':'input-sm','style':'width: 100%;','placeholder':'PhilHealth ID'})
                    )  
    
    usrstatuschoices = [('Active','Active'),('Resigned/Retired','Resigned/Retired')]
    usrstatusedit = forms.ChoiceField(choices=usrstatuschoices,
                                    widget=forms.Select
                                    (attrs={'id':'usrstatusedit','tabindex':'27','class':'input-sm','style':'width: 100%; font-size:12px;','required':'required'})
                                    )
    
    
    Leveledit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Leveledit','tabindex':'10','class':'input-sm uppercase','style':'width: 100%;','placeholder':'Level'})
                    )
    
    RegDateedit = forms.DateField(
            widget=forms.DateInput
                (attrs={'id':'RegDateedit','tabindex':'12','class':'input-sm datepicker','style':'width: 100%;','readonly':'readonly'})
                    )
    
    TINNoedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'TINNoedit','tabindex':'16','class':'input-sm','style':'width: 100%;'})
                    )
    
    TaxCodeedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'TaxCodeedit','tabindex':'17','class':'input-sm uppercase','style':'width: 100%;'})
                    )
    
    TaxExemptionedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'TaxExemptionedit','tabindex':'18','class':'input-sm numdot amts text-right','style':'width: 100%;'})
                    )
    
    Designationedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Designationedit','tabindex':'9','class':'input-sm','style':'width: 100%;','placeholder':'Designation'})
                    )
    
    HomeAddressedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'HomeAddressedit','tabindex':'20','class':'input-sm','style':'width: 90%;','placeholder':'Home Address'})
                    )
    
    Emailedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Emailedit','tabindex':'21','class':'input-sm','style':'width: 50%;','placeholder':'Email'})
                    )
    #CIVIL STATUS#
    
    BDateedit = forms.DateField(
            widget=forms.DateInput
                (attrs={'id':'BDateedit','tabindex':'23','class':'input-sm datepicker','style':'width: 20%;','readonly':'readonly'})
                    )
    
    #BLOOD TYPE#
    
    Religionedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Religionedit','tabindex':'25','class':'input-sm','style':'width: 40%;','placeholder':'Religion'})
                    )
    
    Citizenshipedit = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Citizenshipedit','tabindex':'26','class':'input-sm','style':'width: 40%;','placeholder':'Citizenship'})
                    )
    
    
   
class HolidayForm(forms.Form):
    dateOfHoliday = forms.DateField(
            widget=forms.DateInput
                (attrs={'id':'dateOfHoliday','class':'form-control datepicker','required':'required','readonly':'readonly'})
                    )  
    
    Description = forms.CharField(
            widget=forms.Textarea
                (attrs={'id':'Description','class':'form-control','required':'required','cols':'80','rows':'2'})
                    )  
    
    htypechoices = [('Regular/Legal','Regular/Legal'),('Special Non-Working','Special Non-Working')]
    typeOfHoliday = forms.ChoiceField(choices=htypechoices,
            widget=forms.Select
                (attrs={'id':'typeOfHoliday','class':'form-control','required':'required'})
                    )
      
    hschemechoices = [('All','All'),('Davao','Davao Holidays'),('Tagum','Tagum Holidays'),('Palawan','Palawan Holidays'),('Manila','Manila Holidays')]
    schemeOfHoliday =  forms.ChoiceField(choices=hschemechoices,
            widget=forms.Select
                (attrs={'id':'schemeOfHoliday','class':'form-control'})
                    ) 
    
class SchedForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(SchedForm, self).__init__(*args, **kwargs)
        
        alluid = [(x.id, str(x.id) + " - " + x.LName + ", " + x.FName + " " + x.MName) for x in User.objects.exclude(isadmin__in=[2,3,4]).exclude(id__in=Schedule.objects.values_list('User_id',flat=True))]
        self.fields['uid'] = forms.ChoiceField(choices=alluid,
                                    widget=forms.Select
                                    (attrs={'id':'uid','class':'form-control input-sm','required':'required'})
                                    )  
    
    schedchoices = [('CWW','CWW'),('REG','REG'),('CWD','CWW - Doctor (5hrs per day)'),('CWD2','CWW - Doctor (2 days a week)')]
    WorkSched = forms.ChoiceField(choices=schedchoices,widget=forms.Select
                (attrs={'id':'WorkSched','class':'form-control input-sm','required':'required'})
                    )  
    
    DayChoices = [(None,'------------'),('Sun','Sun'),('Mon','Mon'),('Tue','Tue'),('Wed','Wed'),('Thu','Thu'),('Fri','Fri'),('Sat','Sat')]
    DayOff1 = forms.ChoiceField(choices=DayChoices,widget=forms.Select
                (attrs={'id':'dayoff1','class':'form-control input-sm','required':'required'})
                    )  
    
    DayOff2 = forms.ChoiceField(choices=DayChoices,widget=forms.Select
                (attrs={'id':'dayoff2','class':'form-control input-sm','required':'required'})
                    )  
    
    
class changeSchedForm(forms.Form):
    
    currSched = forms.CharField(widget=forms.TextInput
                (attrs={'id':'currSched','class':'form-control input-sm','disabled':'disabled'})
                    )  
    
    schedchoices = [('CWW','CWW'),('REG','REG'),('CWD','CWW - Doctor (5hrs per day)'),('CWD2','CWW - Doctor (2 days a week)')]
    WorkSched = forms.ChoiceField(choices=schedchoices,widget=forms.Select
                (attrs={'id':'WorkSched','class':'form-control input-sm','required':'required'})
                    )  
    
    DayChoices = [('','------------'),('Sun','Sun'),('Mon','Mon'),('Tue','Tue'),('Wed','Wed'),('Thu','Thu'),('Fri','Fri'),('Sat','Sat')]
    DayOff1 = forms.ChoiceField(choices=DayChoices,widget=forms.Select
                (attrs={'id':'dayoff1','class':'form-control input-sm','required':'required'})
                    )  
    
    DayOff2 = forms.ChoiceField(choices=DayChoices,widget=forms.Select
                (attrs={'id':'dayoff2','class':'form-control input-sm','required':'required'})
                    )  
    
    dateFrom = forms.DateField(
            widget=forms.DateInput
                (attrs={'id':'dateFrom','class':'form-control input-sm datepicker','required':'required','readonly':'readonly'})
                    )  
    
    dateTo = forms.DateField(
            widget=forms.DateInput
                (attrs={'id':'dateTo','class':'form-control input-sm datepicker','required':'required','readonly':'readonly'})
                    )  
    
     
    
class DateForm(forms.Form):
    currentyear = datetime.date.today().year
    yearchoices = [(year, year) for year in range(currentyear, currentyear-15, -1)]
    year = forms.ChoiceField(choices=yearchoices,
                widget=forms.Select
                (attrs={'id':'viewyear','class':'form-control input-sm'})
                    )  
    
    monthchoices = []
    for i in range(1,13):
        monthchoices.append((i, datetime.date(currentyear, i, 1).strftime('%B')))
 
    month = forms.ChoiceField(choices=monthchoices,
                widget=forms.Select
                (attrs={'id':'viewmonth','class':'form-control input-sm'})
                    )  
    cutoffchoices = [('1st','1st'),('2nd',('2nd'))]
    cutoff = forms.ChoiceField(choices=cutoffchoices,
                widget=forms.Select
                (attrs={'id':'cutofftype','class':'form-control input-sm'})
                    )
    
class ChangePwdForm(forms.Form):
    oldpwd = forms.CharField(widget=forms.PasswordInput
                (attrs={'id':'oldpwd','class':'form-control input-sm','required':'required'})
                    )  
                                             
    newpwd = forms.CharField(widget=forms.PasswordInput
                (attrs={'id':'newpwd','class':'form-control input-sm','required':'required'})
                    )  
                     
    confirmnewpwd = forms.CharField(widget=forms.PasswordInput
                (attrs={'id':'confirmnewpwd','class':'form-control input-sm','required':'required'})
                    )  
    
class ReportsForm(forms.Form):
    def __init__(self, arrangeby, *args, **kwargs):
        super(ReportsForm, self).__init__(*args, **kwargs)
        
        allusers = [(-1,'-- All --'),(-2,'-- Active ERMs --'), (-3,'-- Resigned/Retired ERMs --')]
        if arrangeby == 'id':
            for x in User.objects.exclude(isadmin__in=[2,3,4]).order_by('id'):
                allusers.append((x.id, str(x.id) + ' - ' + x.LName + ", " + x.FName + " " + x.MName)) 
        elif arrangeby == 'LName':
            for x in User.objects.exclude(isadmin__in=[2,3,4]).order_by('LName'):
                allusers.append((x.id, x.LName + ", " + x.FName + " " + x.MName))
        elif arrangeby == 'FName':
            for x in User.objects.exclude(isadmin__in=[2,3,4]).order_by('FName'):
                allusers.append((x.id, x.FName + " " + x.MName + " " + x.LName))
    
        #allusers = [ for x in User.objects.exclude(isadmin=2).order_by('LName')]
        self.fields['users'] = forms.ChoiceField(choices=allusers,
                                    widget=forms.Select
                                    (attrs={'id':'users','class':'form-control input-sm','required':'required'})
                                    )
    
    
    currentyear = datetime.date.today().year
    yearchoices = [(year, year) for year in range(currentyear, currentyear-15, -1)]
    year = forms.ChoiceField(choices=yearchoices,
                widget=forms.Select
                (attrs={'id':'ryear','class':'form-control input-sm'})
                    )  
    
    monthchoices = []
    for i in range(1,13):
        monthchoices.append((i, datetime.date(currentyear, i, 1).strftime('%B')))
 
    month = forms.ChoiceField(choices=monthchoices,
                widget=forms.Select
                (attrs={'id':'rmonth','class':'form-control input-sm'})
                    )  
    cutoffchoices = [('1st','1st'),('2nd',('2nd'))]
    cutoff = forms.ChoiceField(choices=cutoffchoices,
                widget=forms.Select
                (attrs={'id':'rcutoff','class':'form-control input-sm'})
                    )


class ProfileForm(forms.Form):
    uid = forms.IntegerField(widget=forms.NumberInput
                (attrs={'id':'uid','class':'form-control input-sm','placeholder':'Associate ID','disabled':'disabled'})
                    )  
    
    FName = forms.CharField(widget=forms.TextInput
                (attrs={'id':'FName','class':'form-control input-sm','placeholder':'Given Name','disabled':'disabled'})
                    )  
    
    MName = forms.CharField(widget=forms.TextInput
                (attrs={'id':'MName','class':'form-control input-sm','placeholder':'Middle Name','disabled':'disabled'})
                    )  
    
    LName = forms.CharField(widget=forms.TextInput
                (attrs={'id':'LName','class':'form-control input-sm','placeholder':'Family Name','disabled':'disabled'})
                    )
    
    Approver = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Approver','class':'form-control input-sm','placeholder':'Approver','disabled':'disabled'})
                    )  
   
        
    Division = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Division','class':'form-control input-sm','placeholder':'Division','disabled':'disabled'})
                    )  
    
    Dept = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Dept','class':'form-control input-sm','placeholder':'Department','disabled':'disabled'})
                    )  
    
    Branch = forms.CharField(widget=forms.TextInput
                (attrs={'id':'Branch','class':'form-control input-sm','placeholder':'Branch','disabled':'disabled'})
                    )  
    
    SSSNo = forms.CharField(widget=forms.TextInput
                (attrs={'id':'SSSNo','class':'form-control input-sm','placeholder':'SSS No.','disabled':'disabled'})
                    )  
    
    PagIBIGNo = forms.CharField(widget=forms.TextInput
                (attrs={'id':'PagIBIGNo','class':'form-control input-sm','placeholder':'Pag-IBIG No.','disabled':'disabled'})
                    )  
    
    PhilHealthNo = forms.CharField(widget=forms.TextInput
                (attrs={'id':'PhilHealthNo','class':'form-control input-sm','placeholder':'PhilHealth No.','disabled':'disabled'})
                    )  
    
class UploadForm(forms.Form):
    avatar = forms.ImageField(
                label='Select an image',
                help_text=''
                    )
    
'''
class PMSForm(forms.Form):
    def __init__(self, currUser, *args, **kwargs):
        super(PMSForm, self).__init__(*args, **kwargs)
    
        allusers = [(x.id, str(x.id) + " - " + x.LName + ", " + x.FName + " " + x.MName) for x in User.objects.filter(Approver__contains=currUser).order_by('LName')]            
        self.fields['pmsuser'] = forms.ChoiceField(choices=allusers,
                                    widget=forms.Select
                                    (attrs={'id':'pmsuser','class':'form-control input-sm','required':'required'})
                                    )

    currentyear = datetime.date.today().year
    yearchoices = [(year, year) for year in range(currentyear, currentyear-15, -1)]
    pmsyear = forms.ChoiceField(choices=yearchoices,
                widget=forms.Select
                (attrs={'id':'pmsyear','class':'form-control input-sm'})
                    )  
    
    scorechoices = [('3.0','3.0'),('2.75','2.75'),('2.5','2.5'),('2.25','2.25'),('2.0','2.0'),('1.75','1.75'),('1.5','1.5'),('1.25','1.25'),('1.0','1.0')]
    pmsscore = forms.ChoiceField(choices=scorechoices,
                widget=forms.Select
                (attrs={'id':'pmsscore','class':'form-control input-sm'})
                    )  
'''
    
    
class xlsyearForm(forms.Form): 
    currentyear = datetime.date.today().year
    yearchoices = [(year, year) for year in range(currentyear, currentyear-10, -1)]
    xlsyear = forms.ChoiceField(choices=yearchoices,
                widget=forms.Select
                (attrs={'id':'xlsyear','class':'form-control input-sm'})
                    )  
  
class SearchyearForm(forms.Form): 
    currentyear = datetime.date.today().year
    yearchoices = [(year, year) for year in range(currentyear, currentyear-5, -1)]
    year = forms.ChoiceField(choices=yearchoices,
                widget=forms.Select
                (attrs={'id':'dtrentryyear','class':'form-control input-sm text-left','style':'width: auto !important; display: inline-block; vertical-align: middle;'})
                    ) 
    
    
    