from django.db import models
# Create your models here.

from django.core.files.storage import FileSystemStorage
class OverwriteStorage(FileSystemStorage):
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name):
        return name

#User
class User(models.Model):
    password = models.CharField(max_length=200)
    PwdExpiry = models.DateField(default=None)
    PwdHistory = models.CharField(max_length=100,default=None)
    LastLogin = models.DateTimeField(default=None)
    FName = models.CharField(max_length=50)
    MName = models.CharField(max_length=50)
    LName = models.CharField(max_length=50)
    Gender = models.CharField(max_length=50,default=None)
    Approver = models.IntegerField(default=None)
    isadmin = models.IntegerField()
    Division = models.CharField(max_length=100,default=None)
    Dept = models.CharField(max_length=100,default=None)
    Designation = models.CharField(max_length=200,default=None)
    Level = models.CharField(max_length=50,default=None)
    Branch = models.CharField(max_length=50,default=None)
    RegDate = models.DateField(default=None)
    SSSNo = models.CharField(max_length=50,default=None)
    PagIBIGNo = models.CharField(max_length=50,default=None)
    PhilHealthNo = models.CharField(max_length=50,default=None)
    TINNo = models.CharField(max_length=50,default=None)
    TaxCode = models.CharField(max_length=50,default=None)
    TaxExemption = models.DecimalField(max_digits=11,decimal_places=2,default=None)
    isProfFee = models.IntegerField(default=None)
    HomeAddress = models.CharField(max_length=200,default=None)
    Email = models.CharField(max_length=100,default=None)
    CivilStatus = models.CharField(max_length=50,default=None)
    BDate = models.DateField(default=None)
    BloodType = models.CharField(max_length=10,default=None)
    Religion = models.CharField(max_length=50,default=None)
    Citizenship = models.CharField(max_length=50,default=None)
    status = models.CharField(max_length=50)
    
    TotalAllowedVL = models.IntegerField()
    TotalAllowedSIL = models.IntegerField()
    TotalAllowedSL = models.IntegerField()
    
    
    class Meta:
        db_table = 'erm_user'
        
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.password, self.PwdHistory, self.FName, self.MName, self.LName, self.Gender, self.Division, self.Dept, self.Designation, self.Level, self.Branch, self.SSSNo, self.PagIBIGNo, self.PhilHealthNo, self.TINNo, self.TaxCode, self.HomeAddress, self.Email, self.CivilStatus, self.BloodType, self.Religion, self.Citizenship, self.status,)

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
        

#Leave
class Leave(models.Model):
    User = models.ForeignKey(User)
    DateofLeave = models.DateField()
    VacationL = models.IntegerField()
    VLConsumeYear = models.IntegerField()
    SickL = models.IntegerField()
    ServiceIncentiveL = models.IntegerField()
    AAbsent = models.IntegerField()
    reserve1 = models.CharField(max_length=50)
    reserve2 = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'erm_leave'
    
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s' % (self.reserve1, self.reserve2)

#Schedule
class Schedule(models.Model):
    User = models.ForeignKey(User)
    WorkingHours = models.IntegerField()
    dateFrom = models.DateField()
    dateTo = models.DateField()
    DayOff1 = models.CharField(max_length=50)
    DayOff2 = models.CharField(max_length=50)
    Sked = models.CharField(max_length=50)
    res1 = models.CharField(max_length=50)
    res2 = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'erm_schedule'
    
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s %s %s' % (self.DayOff1, self.DayOff2, self.Sked, self.res1, self.res2)


class Batch(models.Model):
    User = models.ForeignKey(User)
    BMonth = models.CharField(max_length=50)
    BYear = models.CharField(max_length=50)
    CutOff = models.CharField(max_length=50)
    BMonthOrder = models.IntegerField()
    reserve1 = models.CharField(max_length=50)
    reserve2 = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'erm_batch'
    
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s' % (self.CutOff, self.reserve1, self.reserve2)

#Attendance
class Attendance(models.Model):
    User = models.ForeignKey(User)
    attendanceDate = models.DateField()
    hoursWorked = models.IntegerField()
    Leave = models.ForeignKey(Leave)
    remarkNotes = models.TextField()
    status = models.IntegerField()
    Batch = models.ForeignKey(Batch)
    res1 = models.CharField(max_length=50)
    res2 = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'erm_attendance'
    
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s' % (self.remarkNotes, self.res1, self.res2)


class Holidays(models.Model):
    dateOfHoliday = models.DateField()
    Description = models.CharField(max_length=100)
    typeOfHoliday = models.CharField(max_length=50)
    schemeOfHoliday = models.CharField(max_length=50) 
    reserve1 = models.CharField(max_length=50)
    reserve2 = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'erm_holidays'
    
    def __str__(self):              # __unicode__ on Python 2
        return '%s %s %s %s %s' % (self.Description, self.typeOfHoliday, self.schemeOfHoliday, self.reserve1, self.reserve2)



class Branch(models.Model):
    Description = models.CharField(max_length=50)
    res1 = models.CharField(max_length=50)
    res2 = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'erm_branch'
    
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s' % (self.Description, self.res1, self.res2)

class PMS(models.Model):
    User = models.ForeignKey(User)
    pmsYear = models.CharField(max_length=4)
    pmsScore = models.DecimalField(max_digits=11,decimal_places=2)
    pmsStatus = models.CharField(max_length=30) 
    resCol1 = models.CharField(max_length=100)
    resCol2 = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'erm_pms'
    
    def __unicode__(self):              # __unicode__ on Python 2
        return '%s %s %s %s' % (self.pmsYear, self.pmsStatus, self.resCol1, self.resCol2)


