from django import forms
#import datetime
import pyodbc
from .models import NBU, Expense_Type, Status, UserClass, UserRole#, User, Tax, WTax




#MainForm
class MainForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        
        #NBU
        allnbu = NBU.objects.order_by('id')
        nbuChoices = [(None,'--- SELECT NBU ---')]
        for x in allnbu:
            nbuChoices.append((x.id, x.desc))
    
        self.fields['nbu'] = forms.ChoiceField(choices=nbuChoices,
                                    widget=forms.Select
                                    (attrs={'id':'nbu','name':'nbu','class':'text-left','style':'font-size:12px; width:100%','required':'required'})
                                    )
            
        #Expense_Type
        allexpensetype = Expense_Type.objects.order_by('id')
        expense_typeChoices = []
        for x in allexpensetype:
            expense_typeChoices.append((x.id, x.desc)) 
    
        self.fields['expense_type'] = forms.ChoiceField(choices=expense_typeChoices,
                                    widget=forms.Select
                                    (attrs={'id':'expense_type','name':'expense_type','class':'text-left reqdet','style':'font-size: 12px;','required':'required'})
                                    )
        
        #Status
        allstatus = Status.objects.order_by('id')
        statusChoices = [(None,'ALL')]#ALL is 10
        for x in allstatus:
            statusChoices.append((x.id, x.desc)) 
    
        self.fields['status'] = forms.ChoiceField(choices=statusChoices,
                                    widget=forms.Select
                                    (attrs={'id':'status','name':'status','class':'input-sm text-left','style':'font-size: 12px; font-weight: bold;','required':'required'})
                                    )
        '''
        cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
        cursor = cnxn.cursor()
        
        #Department
        query = "SELECT GLMAC1, GLMNAM FROM MMLTSLIB.GLMAJR WHERE GLMAC1 NOT IN (1,2,3,4)" #EXCEPT 1,2,3,4
        cursor.execute(query)
        alldept = cursor.fetchall()        
        cursor.close()
        
        deptChoices = [(None,'--- SELECT DEPARTMENT ---')]
        for dept in alldept:
            deptChoices.append((dept.GLMAC1, dept.GLMNAM)) 
        
        self.fields['dept'] = forms.ChoiceField(choices=deptChoices,
                                    widget=forms.Select
                                    (attrs={'id':'dept','name':'dept','class':'text-left reqdet','style':'font-size:12px; width:100%;','required':'required'})
                                    )
        '''

#UserForm
class UserForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        #NBU
        allnbu = NBU.objects.order_by('id')
        nbuChoices = [(None,'--- SELECT NBU ---')]
        for x in allnbu:
            nbuChoices.append((x.id, x.desc))
    
        self.fields['usernbu'] = forms.ChoiceField(choices=nbuChoices,
                                    widget=forms.Select
                                    (attrs={'id':'usernbu','name':'usernbu','class':'text-left','style':'font-size:12px; width:100%','required':'required'})
                                    )
        
        #USERCLASS
        allclass = UserClass.objects.exclude(id=5).order_by('id')
        classChoices = [(None,'--- SELECT CLASS ---')]
        for c in allclass:
            classChoices.append((c.id, c.desc))
    
        self.fields['userclass'] = forms.ChoiceField(choices=classChoices,
                                    widget=forms.Select
                                    (attrs={'id':'userclass','name':'userclass','class':'text-left','style':'font-size:12px; width:100%;','required':'required'})
                                    )
        #USERROLE
        allrole = UserRole.objects.order_by('id')
        roleChoices = [(None,'--- SELECT ROLE ---')]
        for r in allrole:
            roleChoices.append((r.id, r.position))
    
        self.fields['userrole'] = forms.ChoiceField(choices=roleChoices,
                                    widget=forms.Select
                                    (attrs={'id':'userrole','name':'userrole','class':'text-left','style':'font-size:12px; width:100%;'})
                                    )
    
        ### REQUIRES ODBC ###
        ############################################################################################
        cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
        cursor = cnxn.cursor()
        
        #Department
        deptquery = "SELECT CAST(TRIM(GLMAC1) AS CHAR(3)) AS GLMAC1, TRIM(GLMNAM) AS GLMNAM FROM mmltslib.GLMAJR WHERE GLMAC1 NOT IN(1,2,3,4) ORDER BY GLMAC1 ASC"

        cursor.execute(deptquery)
        alldept = cursor.fetchall()        
        cursor.close()
        
        deptChoices = [(None,'--- SELECT DEPARTMENT ---')]
        for dept in alldept:
            deptChoices.append((dept.GLMAC1.strip().zfill(3),str(dept.GLMAC1).strip().zfill(3) + ' - ' + str(dept.GLMNAM).strip()))
        
        self.fields['userdept'] = forms.ChoiceField(choices=deptChoices,
                                    widget=forms.Select
                                    (attrs={'id':'userdept','name':'userdept','class':'text-left','style':'font-size:12px; width:100%;','required':'required'})
                                    )
        
        
        '''
        #Clerk Num
        clerkquery = "SELECT CAST(TRIM(CLKNUM) AS NUMERIC(3)) AS CLKNUM, TRIM(CLKNAM) AS CLKNAM FROM MMLTSLIB.TBLCLK WHERE CLKNUM NOT IN(1,219) ORDER BY CLKNAM ASC"
        cursor.execute(clerkquery)
        allclerk = cursor.fetchall()
        
        clerkChoices = [(None,'--- MMS CLERK ---')]
        
        for clerk in allclerk:
            clerkChoices.append((str(clerk.CLKNUM), str(clerk.CLKNAM)))
        
            
        self.fields['userclerknum'] = forms.ChoiceField(choices=clerkChoices,
                                    widget=forms.Select
                                    (attrs={'id':'userclerknum','name':'userclerknum','class':'text-left','style':'font-size:12px; width:100%;','required':'required'})
                                 )
        cursor.close()
        '''
        
        ############################################################################################
        
        
''' 
class AccessForm(forms.Form):  
    def __init__(self,*args, **kwargs):
        super(AccessForm, self).__init__(*args, **kwargs)
        
        #NBU
        allnbu = NBU.objects.order_by('id')
        nbuChoices = [(None,'--- SELECT NBU ---')]
        for x in allnbu:
            nbuChoices.append((x.id, x.desc))
    
        self.fields['accessnbu'] = forms.ChoiceField(choices=nbuChoices,
                                    widget=forms.Select
                                    (attrs={'id':'accessnbu','name':'accessnbu','class':'text-left','style':'font-size:12px; width:100%','required':'required'})
                                    )
        
        cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
        cursor = cnxn.cursor()
        
        #Department
        query = "SELECT CAST(TRIM(GLMAC1) AS CHAR(3)) AS GLMAC1, TRIM(GLMNAM) AS GLMNAM FROM mmltslib.GLMAJR WHERE GLMAC1 NOT IN(1,2,3,4) ORDER BY GLMAC1 ASC"

        cursor.execute(query)
        alldept = cursor.fetchall()        
        cursor.close()
        
        deptChoices = [(None,'--- SELECT DEPARTMENT ---')]
        for dept in alldept:
            deptChoices.append((dept.GLMAC1.strip().zfill(3),str(dept.GLMAC1).strip().zfill(3) + ' - ' + str(dept.GLMNAM).strip()))
        
        self.fields['accessdept'] = forms.ChoiceField(choices=deptChoices,
                                    widget=forms.Select
                                    (attrs={'id':'accessdept','name':'accessdept','class':'text-left','style':'font-size:12px; width:100%;','required':'required'})
                                    )
'''
####################################################################################







        
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#------------------------------------------------------------------#

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
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#------------------------------------------------------------------#
#------------------------------------------------------------------#

#STORAGE FOR NOT USED FORMS

'''

#TaxForm
class TaxForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super(TaxForm, self).__init__(*args, **kwargs)
        
        alltax = Tax.objects.order_by('id')
        #vatChoices = [(None,'----------------------------')]
        taxChoices = []
        for x in alltax:
            taxChoices.append((x.id, x.desc)) 
    
        self.fields['tax'] = forms.ChoiceField(choices=taxChoices,
                                    widget=forms.Select
                                    (attrs={'id':'tax','name':'tax','class':' text-left','style':'font-size: 12px;','required':'required'})
                                    )

#WTaxForm
class WTaxForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super(WTaxForm, self).__init__(*args, **kwargs)
        
        allwtax = WTax.objects.order_by('id')
        #wtaxChoices = [(None,'----------------------------')]
        wtaxChoices = []
        for x in allwtax:
            wtaxChoices.append((x.id, x.desc)) 
    
        self.fields['wtax'] = forms.ChoiceField(choices=wtaxChoices,
                                    widget=forms.Select
                                    (attrs={'id':'wtax','name':'wtax','class':' text-left','style':'font-size: 12px;','required':'required'})
                                    )



#Expense_TypeForm
class Expense_TypeForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super(Expense_TypeForm, self).__init__(*args, **kwargs)
        
        allexpensetype = Expense_Type.objects.order_by('id')
        #wtaxChoices = [(None,'----------------------------')]
        expense_typeChoices = []
        for x in allexpensetype:
            expense_typeChoices.append((x.id, x.desc)) 
    
        self.fields['expense_type'] = forms.ChoiceField(choices=expense_typeChoices,
                                    widget=forms.Select
                                    (attrs={'id':'expense_type','name':'expense_type','class':'text-left','style':'font-size: 12px;','required':'required'})
                                    )



#StatusForm
class StatusForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        
        allstatus = Status.objects.order_by('id')
        statusChoices = [(None,'ALL')]#ALL is 10
        #statusChoices = []
        for x in allstatus:
            statusChoices.append((x.id, x.desc)) 
    
        self.fields['status'] = forms.ChoiceField(choices=statusChoices,
                                    widget=forms.Select
                                    (attrs={'id':'status','name':'status','class':'input-sm text-left','style':'font-size: 12px; font-weight: bold;','required':'required'})
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
  
        
#LocationForm     
class LocationForm(forms.Form):
    def __init__(self,nbu,*args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
    
        #Location
        cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
        cursor = cnxn.cursor()
        query = "SELECT CAST(STRNUM AS CHARACTER(5)) AS STRNUM, TRIM(STRNAM) AS STRNAM FROM TBLSTR WHERE STCOMP='" + str(nbu) + "'"
        cursor.execute(query)
        alllocation = cursor.fetchall()
        
        locationChoices = [(None,'--- SELECT LOCATION ---')]
        for location in alllocation:
            locationChoices.append((location[0], location[0] + " - " + location[1])) 
    
        cursor.close()
        
        self.fields['location'] = forms.ChoiceField(choices=locationChoices,
                                    widget=forms.Select
                                    (attrs={'id':'location','name':'location','class':'text-left reqdet','style':'font-size:12px; width:100%;','required':'required'})
                                    )
    
        ''
        #Chart of Accounts
        query = "SELECT CAST(GLMAC1 AS CHAR(3)) AS GLMAC1, CAST(GLMAC1 AS CHAR(3)) AS GLMAC2, CAST(GLMAC3 AS CHAR(5)) AS GLMAC3, TRIM(GLMDSC) AS GLMDSC FROM GLMSTR WHERE GLMCMP='10'"
        cursor.execute(query)
        allcoa = cursor.fetchall()
        print allcoa
        coaChoices = [(None,'--- SELECT COA ---')]
        for coa in allcoa:
            coaChoices.append((coa.GLMAC1 + '-' + coa.GLMAC2 + '2' + coa.GLMAC3, coa.GLMAC1 + '-' + coa.GLMAC2 + '2' + coa.GLMAC3 + ' ' + coa.GLMDSC)) 
        
        self.fields['coa'] = forms.ChoiceField(choices=coaChoices,
                                    widget=forms.Select
                                    (attrs={'id':'coa{{forloop.counter}}','name':'coa{{forloop.counter}}','class':' text-left','style':'font-size:12px; width:100%;','required':'required'})
                                    )
        ''
            

#COAForm     
class COAForm(forms.Form):
    def __init__(self,nbu,dept,locs,*args, **kwargs):
        super(COAForm, self).__init__(*args, **kwargs)
    
        #COA
        cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
        cursor = cnxn.cursor()
        
        query = "SELECT CAST(TRIM(GLMAC1) AS CHAR(3)) AS GLMAC1, CAST(TRIM(GLMAC1) AS CHAR(3)) AS GLMAC2, CAST(TRIM(GLMAC3) AS CHAR(5)) AS GLMAC3, TRIM(GLMDSC) AS GLMDSC FROM GLMSTR WHERE GLMCMP='" + str(nbu) + "' AND GLMAC1='" + str(dept) + "' AND GLMAC3='" + str(locs) + "'" 
        cursor.execute(query)
        allcoa = cursor.fetchall()
        
        coaChoices = [(None,'--- SELECT ---')]
        for coa in allcoa:
            coaChoices.append((coa[0].strip() + '-' + coa[1].strip() + '-' + coa[2].strip(), coa[1].strip() + '-' + coa[3].strip()))
    
        cursor.close()
        
        self.fields['coa'] = forms.ChoiceField(choices=coaChoices,
                                    widget=forms.Select
                                    (attrs={'name':'location','class':'text-left reqdet','style':'font-size:12px; width:100%;','required':'required'})
                                    )

  
#NBUForm
class NBUForm(forms.Form):
    def __init__(self,*args, **kwargs):
        super(NBUForm, self).__init__(*args, **kwargs)
        
        allnbu = NBU.objects.order_by('id')
        nbuChoices = [(None,'--- SELECT NBU ---')]
        #nbuChoices = []
        for x in allnbu:
            nbuChoices.append((x.id, x.desc)) 
    
        self.fields['nbu'] = forms.ChoiceField(choices=nbuChoices,
                                    widget=forms.Select
                                    (attrs={'id':'nbu','name':'nbu','class':' text-left','style':'font-size: 12px;','required':'required'})
                                    )    
        
'''
    
    
''' 
def smart_str(self):
    print self
    return smart_str(self)


'''