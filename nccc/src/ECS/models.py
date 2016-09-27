from django.db import models
from lib2to3.pgen2.token import LESS
from django.template.defaultfilters import default

# Create your models here.
class NBU(models.Model):
    NBUDesc = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'ecs_nbu'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s' % (self.NBUDesc)
    
class User(models.Model):
    UserName = models.CharField(primary_key=True, max_length=50)
    FullName = models.CharField(max_length=100)
    vendorID = models.CharField(max_length=30)
    vendorName = models.CharField(max_length=100)
    UserPwd = models.CharField(max_length=100)
    User_isadmin = models.IntegerField()
    PwdExpiry = models.DateField()
    PwdHistory = models.CharField(max_length=100)
    LastLogin = models.DateTimeField()
    LastMessage = models.DateTimeField()
    Status = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'ecs_user'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s %s %s %s %s' % (self.UserName, self.FullName, self.vendorID, self.vendorName, self.UserPwd, self.PwdHistory, self.Status)
    
class PayTerms(models.Model):
    termName = models.CharField(max_length=50)
    NBU = models.ForeignKey(NBU)
    Days = models.IntegerField()
   
    
    class Meta:
        db_table = 'ecs_payterms'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s' % (self.termName)
    
class NCCCAccess (models.Model):
    userName = models.ForeignKey(User)
    nbu = models.ForeignKey(NBU)
    
    class Meta:
        db_table = 'ecs_ncccaccess'
        unique_together = (("userName", "nbu"),)
    
class SOA(models.Model):
    SOANo = models.CharField(max_length=50,primary_key=True)
    SOADate = models.DateTimeField()
    SOALastUpdate = models.DateTimeField()
    SOAStatus = models.CharField(max_length=50)
    SOABillTo = models.ForeignKey(NBU)
    CreatedBy =  models.ForeignKey(User, related_name='CreatedBy')
    PTerm = models.ForeignKey(PayTerms)
    CBDate = models.DateField()
    CBDateORG = models.DateField()
    RDate = models.DateTimeField()
    IDate = models.DateTimeField()
    CRSCBDate = models.DateField()
    ProcessedBy = models.ForeignKey(User, related_name='ProcessedBy',default=None)
    ClosedBy = models.ForeignKey(User, related_name='ClosedBy',default=None)
    
    class Meta:
        db_table = 'ecs_soa'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s' % (self.SOANo, self.SOAStatus)



    
class Branch(models.Model):
    BAbbr = models.CharField(max_length=50)
    BDesc = models.CharField(max_length=50) 
    
    class Meta:
        db_table = 'ecs_branch'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s' % (self.BDesc)
    
    

class Details(models.Model):
    PODate = models.DateField()
    PONo = models.IntegerField(unique=True)
    RRAmount = models.DecimalField(max_digits=11, decimal_places=4)
    POTotalInvAmntEntrd = models.DecimalField(max_digits=11, decimal_places=4)
    SOANo = models.ForeignKey(SOA)
    DStatus = models.CharField(max_length=50)
    DenyReason = models.CharField(max_length=100)
     
    class Meta:
        db_table = 'ecs_details'
        unique_together = (("PONo", "SOANo"),)  
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s' % (self.DStatus, self.DenyReason)
    
    
class Invoice(models.Model):
    InvDate = models.DateField()
    InvNo = models.CharField(max_length=50)
    Amount = models.DecimalField(max_digits=11, decimal_places=2)
    IMAmount = models.DecimalField(max_digits=11, decimal_places=2)
    LowerAmt = models.DecimalField(max_digits=11, decimal_places=2)
    PONo = models.ForeignKey(Details, to_field="PONo", db_column="PONo_id")
    IStatus = models.CharField(max_length=50)
    SOANo = models.ForeignKey(SOA)
    EntryCount = models.IntegerField()
    PRINTCODE = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'ecs_invoice'
        unique_together = (("InvNo", "PONo"),)
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s' % (self.InvNo, self.IStatus, self.PRINTCODE)
    
    
class Holidays(models.Model):
    dateOfHoliday = models.DateField()
    holidayDesc = models.CharField(max_length=100)
    typeOfHoliday = models.CharField(max_length=30)
    schemeOfHoliday = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'ecs_holidays'
    
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s' % (self.holidayDesc, self.typeOfHoliday, self.schemeOfHoliday)



class Logs(models.Model):
    PONo = models.ForeignKey(Details, to_field="PONo", db_column="PONo_id")
    POAction = models.CharField(max_length=50)
    userResp = models.ForeignKey(User)
    dateofTranx = models.DateTimeField()
    
    class Meta:
        db_table = 'ecs_logs'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s' % (self.POAction)
    
class Messaging(models.Model):
    sender = models.ForeignKey(User, related_name='sender')
    recipient = models.ForeignKey(User, related_name='recipient')
    message = models.CharField(max_length=200)
    dateOfSending = models.DateTimeField()
    msgStatus = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'ecs_messaging'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s' % (self.message, self.msgStatus)
    
class GPData(models.Model):
    DOCDATE = models.DateTimeField()
    DOCNO = models.CharField(max_length=21)
    PAYAMOUNT = models.DecimalField(max_digits=11, decimal_places=2)
    VENDORID = models.CharField(max_length=10)
    NBU = models.CharField(max_length=10)
    PRINTCODE = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'ecs_gpdata'
        unique_together = (("DOCDATE", "DOCNO", "VENDORID"),)
    
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s %s' % (self.DOCNO, self.VENDORID, self.NBU, self.PRINTCODE)
    
#SOA REMARKS    
class Remarks(models.Model):
    SOANo = models.ForeignKey(SOA)
    remarkreason = models.CharField(max_length=100,default=None)
    remarksBy = models.ForeignKey(User, related_name='remarksBy')
    
    class Meta:
        db_table = 'ecs_remarks'
    
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s' % (self.remarkreason,)    
    
    
    
    
    
    
## UNUSED ##    
'''
class Vendors(models.Model):
    vendorID = models.CharField(primary_key=True, max_length=50)
    vendorName = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'ecs_vendors'
    
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s' % (self.vendorID, self.vendorName)
'''

'''
class CBDateChange_History(models.Model):
    SOANo = models.ForeignKey(SOA)
    CBDate = models.DateField()
    DateOfChange = models.DateTimeField()
    
    class Meta:
        db_table = 'ecs_cbdatechange_history'
'''
    
