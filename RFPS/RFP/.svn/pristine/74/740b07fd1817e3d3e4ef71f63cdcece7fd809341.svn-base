from __future__ import unicode_literals

from django.db import models
#import pyodbc
# Create your models here.

from django.core.files.storage import FileSystemStorage
#from encodings.punycode import digits
class OverwriteStorage(FileSystemStorage):
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name):
        return name

####################################################

#NBU
class NBU(models.Model):
    desc = models.CharField(max_length=60,default=None)
    alias = models.CharField(max_length=10,default=None)
    
    class Meta:
        db_table = 'rfp_nbu'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s' % (self.desc, self.alias)

#########################################################################################
#########################################################################################
#########################################################################################

#User Class
class UserClass(models.Model):
    desc = models.CharField(max_length=35,default=None)
    
    class Meta:
        db_table = 'rfp_user_class'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s' % (self.desc,)

#########################################################################################
#########################################################################################
#########################################################################################

#Positions
class UserRole(models.Model):
    position = models.CharField(max_length=30, default=None)
    amount_limit = models.DecimalField(max_digits=11,decimal_places=2)
    
    class Meta:
        db_table = 'rfp_user_role'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s' % (self.position,)

#########################################################################################
#########################################################################################
#########################################################################################

#User
class User(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=100)
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    pwdexpiry = models.DateField()
    pwdhistory = models.CharField(max_length=100)
    userlastlogin = models.DateTimeField()
    userstatus = models.BinaryField()
    userclass = models.ForeignKey(UserClass)
    #ADDITIONALS#
    userrole = models.ForeignKey(UserRole)
    nbu = models.ForeignKey(NBU)
    department = models.IntegerField()
    location = models.IntegerField()
    useramount_limit = models.DecimalField(max_digits=11,decimal_places=2)
    userclerknum = models.IntegerField()
    
    class Meta:
        db_table = 'rfp_user'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s %s %s %s' % (self.username, self.password, self.fname, self.mname, self.lname, self.pwdhistory,)

#########################################################################################
#########################################################################################
#########################################################################################

#User Access
class User_Access(models.Model):
    user = models.ForeignKey(User)
    nbu = models.ForeignKey(NBU)
    department = models.IntegerField()
    location = models.IntegerField()
    
    class Meta:
        db_table = 'rfp_user_access'

#########################################################################################
#########################################################################################
#########################################################################################

#TAX
class Tax(models.Model):
    desc = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'rfp_tax'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s' % (self.desc,)

#########################################################################################
#########################################################################################
#########################################################################################

#WTax
class WTax(models.Model):
    desc = models.CharField(max_length=50,default=None)
    rate = models.DecimalField(max_digits=11,decimal_places=2)
    
    class Meta:
        db_table = 'rfp_wtax'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s' % (self.desc,)    
    
#########################################################################################
#########################################################################################
#########################################################################################

#AA_Details
class AA_Details(models.Model):
    rfpno = models.CharField(max_length=17)
    nbu = models.ForeignKey(NBU)
    department = models.IntegerField()
    location = models.IntegerField()
    accounttype = models.IntegerField()
    desc = models.CharField(max_length=30)
    grossamount = models.DecimalField(max_digits=11,decimal_places=2)
    tax = models.ForeignKey(Tax)
    vatamount = models.DecimalField(max_digits=11,decimal_places=2)
    wtax = models.ForeignKey(WTax)
    wtaxamount = models.DecimalField(max_digits=11,decimal_places=2)
    netamount = models.DecimalField(max_digits=11,decimal_places=2)
    #keysconcat = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'rfp_aa_details'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s' % (self.rfpno, self.desc,)    

#########################################################################################
#########################################################################################
#########################################################################################

#Status
class Status(models.Model):
    desc = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'rfp_status'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s' % (self.desc,)    
    
#########################################################################################
#########################################################################################
#########################################################################################    
    
#Expense Type
class Expense_Type(models.Model):
    desc = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'rfp_expense_type'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s' % (self.desc,)    
    
#########################################################################################
#########################################################################################
#########################################################################################

#Remarks
class Remarks(models.Model):
    rfpno = models.CharField(max_length=17)
    nbu = models.ForeignKey(NBU)
    savednotes = models.CharField(max_length=250)
    
    class Meta:
        db_table = 'rfp_remarks'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s' % (self.rfpno, self.savednotes)    


#########################################################################################
#########################################################################################
#########################################################################################

#Bank Details
class Bank_Details(models.Model):
    rfpno = models.CharField(max_length=17)
    nbu = models.ForeignKey(NBU)
    bankaccountno = models.CharField(max_length=30)
    bankaccountname = models.CharField(max_length=60)
    bankaccounttype = models.CharField(max_length=30)
    bankname = models.CharField(max_length=60)
    
    class Meta:
        db_table = 'rfp_bank_details'
    
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s %s %s' % (self.rfpno, self.bankaccountno, self.bankaccountname, self.bankaccounttype, self.bankname) 
    
#########################################################################################
#########################################################################################
#########################################################################################

#RFP
class RFP(models.Model):
    createdate = models.DateField()
    
    rfpno = models.CharField(max_length=17)
    nbu = models.ForeignKey(NBU)
    
    docnumber = models.CharField(max_length=12)
    invoicedate = models.DateField(default=None)
    
    vendorid = models.CharField(max_length=15)
    vendorname = models.CharField(max_length=100)
    checkpayee = models.CharField(max_length=75,default=None)
    
    remarks = models.ForeignKey(Remarks)
    ersnumber = models.CharField(max_length=30,default=None)
    ejonumber = models.CharField(max_length=30,default=None)
    epromosnumber = models.CharField(max_length=30,default=None)
    
    expensetype = models.ForeignKey(Expense_Type)
    cwo = models.BinaryField(default=None)
    bankdetails = models.ForeignKey(Bank_Details)
    natureofreq = models.CharField(max_length=200,default=None)
    
    preparedby = models.ForeignKey(User,related_name="preparedby")#models.CharField(max_length=30)
    checkedby = models.ForeignKey(User,related_name="checkedby")#models.CharField(max_length=30,default=None)
    checkeddate = models.DateTimeField(default=None)
    approvedby = models.ForeignKey(User,related_name="approvedby")#models.CharField(max_length=30,default=None)
    approveddate = models.DateTimeField(default=None)
    
    receivedby = models.ForeignKey(User,related_name="receivedby")#models.CharField(max_length=30,default=None)
    receiveddate = models.DateTimeField(default=None)
    
    closedby = models.ForeignKey(User,related_name="closedby")#models.CharField(max_length=30,default=None)
    closeddate = models.DateTimeField(default=None)
    
    duedate = models.DateField(default=None)
    status = models.ForeignKey(Status)
    
    
    class Meta:
        db_table = 'rfp_rfp'
        unique_together = (("rfpno", "nbu"),)
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s %s %s %s %s %s' % (self.rfpno, self.vendorid, self.vendorname, self.checkpayee, self.ersnumber, self.ejonumber, self.epromosnumber, self.docnumber, )    

#########################################################################################
#########################################################################################
#########################################################################################

#Control Number
class Cntrl_No(models.Model):
    code = models.CharField(max_length=5,default=None)
    nbu = models.ForeignKey(NBU)
    seriesno = models.IntegerField()
    rfpnumber = models.CharField(max_length=17,default=None)
    
    class Meta:
        db_table = 'rfp_cntrl_no'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s' % (self.code, self.rfpnumber,)    
    
#########################################################################################
#########################################################################################
#########################################################################################

    



















'''
import os

###################
def upload_filename(instance, filename):
    path = "avatars/"
    format = str(instance.imguser_id) + '.jpg'
    return os.path.join(path, format)
###################

#Image Avatars
class Images(models.Model):
    avatar = models.ImageField(storage=OverwriteStorage(), upload_to = upload_filename)
    imguser = models.ForeignKey(User)
    
    class Meta:
        db_table = 'erm_images'
        
'''


        

    




