from django import forms
#import datetime
import pyodbc
from .models import NBU, User


class NBUForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super(NBUForm, self).__init__(*args, **kwargs)
        
        allnbu = NBU.objects.all().order_by('id')
        #nbuChoices = [(None,'----------------------------')]
        nbuChoices = []
        for x in allnbu:
            nbuChoices.append((x.id, x.NBUDesc)) 
    
        self.fields['nbu'] = forms.ChoiceField(choices=nbuChoices,
                                    widget=forms.Select
                                    (attrs={'id':'nbu','class':' text-left','style':'font-size: 12px; margin-bottom: 20px;','required':'required'})
                                    )

class AccessForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super(AccessForm, self).__init__(*args, **kwargs)
        
        allncccactiveusers = User.objects.filter(User_isadmin__in=[1,2],Status='Active').order_by('UserName')
        
        ncccchoices = []
        for x in allncccactiveusers:
            ncccchoices.append((x.UserName, x.UserName + " - " + x.FullName)) 
    
        self.fields['ncccperson'] = forms.ChoiceField(choices=ncccchoices,
                                    widget=forms.Select
                                    (attrs={'id':'ncccperson','class':'normaltext','style':'margin-bottom: 20px;','required':'required'})
                                    )
        #########################################
        allnbu = NBU.objects.all().order_by('id')
        
        nbuchoices = []
        for n in allnbu:
            nbuchoices.append((n.id, n.NBUDesc)) 
        
        self.fields['nbuaccess'] = forms.ChoiceField(choices=nbuchoices,
                                    widget=forms.Select
                                    (attrs={'id':'nbuaccess','class':'normaltext','required':'required'})
                                    )

class VendorForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)
        
        cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
        cursor = cnxn.cursor()
        
        query = "SELECT ASNUM, ASNAME FROM APSUPP WHERE ASTYPE = '1' ORDER BY ASNAME"
        cursor.execute(query)
        allvendors = cursor.fetchall()
        
        cursor.close()
        cnxn.close()
        
        vendorChoices = [(None,'')]
        #vendorChoices = []
        for z in allvendors:
            vendorChoices.append((str(z.ASNUM).strip(), unicode(z.ASNAME, "latin-1").strip()))
            
        self.fields['vendorid'] = forms.ChoiceField(choices=vendorChoices,
                                    widget=forms.Select
                                    (attrs={'id':'vendorid','class':'chosen-select text-left','style':'font-size: 12px; margin-bottom: 20px;','required':'required'})
                                    )
        

        
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#------------------------------------------------------------------#
class BranchForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        
        
        allbranch = Branch.objects.all()
        branchChoices = [(None,'All')]
        for x in allbranch:
            branchChoices.append((x.id, x.BDesc)) 
    
        self.fields['branch'] = forms.ChoiceField(choices=branchChoices,
                                    widget=forms.Select
                                    (attrs={'id':'branch','class':'form-control input-sm text-left',})
                                    )
        
        
        
#------------------------------------------------------------------#
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
#------------------------------------------------------------------#    
class POForm(forms.Form):
    
    def __init__(self, currUser,*args, **kwargs):
        super(POForm, self).__init__(*args, **kwargs)
        query = "SELECT * FROM POMRCH WHERE POSTAT='6' AND POVNUM='" + currUser + "' ORDER BY PONUMB"
        cursor.execute(query)
        allPO = cursor.fetchall()
        
        POChoices = [(None,'------------')]
        for x in allPO:
            POChoices.append((x.PONUMB, x.PONUMB)) 
    
        self.fields['POS'] = forms.ChoiceField(choices=POChoices,
                                    widget=forms.Select
                                    (attrs={'id':'PO','class':'form-control input-sm text-center','required':'required'})
                                    )
    PONo = forms.CharField(
            widget=forms.TextInput
                (attrs={'id':'PONo','class':'form-control input-sm text-center POfield','placeholder':'PO Number','required':'required'})
                    )  

    invdate = forms.DateField(
            widget=forms.DateInput
                (attrs={'id':'invdate','class':'form-control input-sm datepicker text-center','placeholder':'Invoice Date','required':'required'})
                    )  
    
    invno = forms.IntegerField(widget=forms.NumberInput
                (attrs={'id':'invno','class':'form-control input-sm text-center','placeholder':'Invoice No.','required':'required'})
                    )  
    
    invamt = forms.DecimalField(widget=forms.TextInput
                (attrs={'id':'invamt','class':'form-control input-sm text-right','placeholder':'Invoice No.','required':'required'})
                    )
    

