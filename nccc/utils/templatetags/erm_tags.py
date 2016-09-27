from django import template
from src.ERM.models import Holidays, Leave, User, Schedule
import datetime

register = template.Library()

@register.filter
def hash3(dictionary, key):
    return dictionary.get(key, '')

@register.filter
def divide(value,by):
    if not value:
        return 0
    else:
        return int(value)/int(by)

@register.filter
def modulo(value,by):
    if not value:
        return "00"
    else:
        if value%by >= 0 and value%by < 9:
            return "0" + str(value%by)
        else:            
            return value%by 
        



@register.filter
def isdayoff(currUser, thedate):
    dis = str(thedate.year) + "," + str(thedate.month) + "," + str(thedate.day)
    dayname = datetime.datetime.strptime(dis, '%Y,%m,%d').strftime('%a')
    
    sched = Schedule.objects.values_list('Sked',flat=True).filter(User_id=currUser,dateFrom__lte=thedate,dateTo__gte=thedate).order_by('-id')[0]
    DayOffSched = Schedule.objects.values_list('DayOff1','DayOff2').filter(User_id=currUser,dateFrom__lte=thedate,dateTo__gte=thedate).order_by('-id')[0]  
    DayOffs = []
    
    for DayOff in DayOffSched:
        DayOffs.append(str(DayOff))
    
    if sched == 'CWW - Doctor (2 days a week)':
        #gibaliktad para sa 2days da ang work diri
        if dayname in DayOffs:
            return False
        else:
            return True
    else:
        if dayname in DayOffs:
            return True
        else:
            return False
        
    
@register.filter
def isHoliday(ddate,branch):
    seeholiday = Holidays.objects.values_list('dateOfHoliday', flat=True).filter(schemeOfHoliday__in=('All',branch)) 
    if ddate in seeholiday:
        return True
    else:
        return False
    
@register.filter
def getHolidayDesc(hdate):
    hdesc = Holidays.objects.get(dateOfHoliday=hdate) 
    return hdesc.Description


      
@register.filter
def VLR(year,currUser):
    p = User.objects.get(id=currUser)
    allowedVLthisYear = p.TotalAllowedVL
    
    totalvl = sum(Leave.objects.values_list('VacationL',flat=True).filter(User_id=currUser,DateofLeave__year=year,VLConsumeYear=year))#add year to filter VL credit limit
    return allowedVLthisYear-totalvl
    
@register.filter
def SILR(year,currUser):
    p = User.objects.get(id=currUser)
    allowedSILthisYear = p.TotalAllowedSIL
    
    totalsil = sum(Leave.objects.values_list('ServiceIncentiveL',flat=True).filter(User_id=currUser,DateofLeave__year=year))#add year to filter SIL credit limit
    return allowedSILthisYear-totalsil
    
@register.filter
def SLR(year,currUser):
    p = User.objects.get(id=currUser)
    allowedSLthisYear = p.TotalAllowedSL
    
    totalsl = sum(Leave.objects.values_list('SickL',flat=True).filter(User_id=currUser,DateofLeave__year=year))#add year to filter SL credit limit 
    return allowedSLthisYear-totalsl

    
@register.filter
def usernumbering(ctr,num):
    return int(ctr + ((num-1)*25))

@register.filter
def holidaynumbering(ctr,num):
    return int(ctr + ((num-1)*25))

@register.filter
def toapprovenumbering(ctr,num):
    return int(ctr + ((num-1)*100))


