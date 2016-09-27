import re
#from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Context
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from decimal import Decimal
from .models import User, Leave, Schedule, Attendance, Holidays, Batch, PMS, Images
from .forms import DateForm, UserForm, SchedForm, ChangePwdForm, HolidayForm, changeSchedForm, ProfileForm, ReportsForm, xlsyearForm, EditForm, UploadForm, SearchyearForm
import hashlib
import datetime
#import parser
#from pdfdocument.document import *
import calendar
#import time
import uuid
import arial10
#import pyodbc
#from django.db import transaction
import xlwt
import json
from django.db.models import Q


import mysql.connector
from django.http.response import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#conn = mysql.connector.connect(user='root', password ='', host='localhost', database='dberm')

def index(request):
    return render_to_response('erm_templates/DTR/index.html', context_instance=RequestContext(request))

#************************************************************************#
#************************************************************************#
#************************************************************************#

def main(request):
    try:
        ##############################################################
        ########################### START ############################
        ##############################################################
        currUser = request.session['User.id']#session sa user here
        ######################GET USER INFO###########################
        u = User.objects.get(id=currUser)
        isadmin = u.isadmin
        fname = u.FName
        mname = u.MName
        lname = u.LName
        branch = u.Branch
        
        try:
            approver = int(u.Approver)
            #status = 0
        except:
            approver = None 
            #status = 1
            
        ###########################################    
        
        ### *** GET DAY OFF *** ###
        try:
            DayOffSched = Schedule.objects.values_list('DayOff1','DayOff2').filter(User_id=currUser,dateFrom__lte=datetime.date.today(),dateTo__gte=datetime.date.today()).order_by('-id')[0]  
            DayOffs = []
            
            for DayOff in DayOffSched:
                DayOffs.append(str(DayOff))
        except:
            message = "Your default schedule was not assigned.\n Please contact admin scheduler."
            return render_to_response('erm_templates/DTR/index.html', {'message':message,}, context_instance=RequestContext(request,))
        ###########################################
        ### *** GET WORKING HOURS *** ###
        WorkTime = Schedule.objects.values_list('WorkingHours').filter(User_id=currUser,dateFrom__lte=datetime.date.today(),dateTo__gte=datetime.date.today()).order_by('-id')[0][0]
        
        ###########################################
        ### *** DATE SETTINGS *** ###
        currentdaynum = datetime.date.today().day
        currentmonth = datetime.date.today().strftime('%b')
        currentmonthnum = datetime.date.today().month
        currentyearnum = datetime.date.today().year
        currentmonth_max_days = calendar.monthrange(currentyearnum,currentmonthnum)[1]
        ############# FORM #############
        form = DateForm()
        form.fields["year"].initial = currentyearnum
        form.fields["month"].initial = currentmonthnum
        ########################################
        
        ## *** GET ATTENDANCE LIST *** ##
        if currentdaynum <= 15:
            dtrlist = Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(currentyearnum, currentmonthnum, 1), attendanceDate__lte=datetime.date(currentyearnum, currentmonthnum, 15))
            try:
                dtrstatus = Attendance.objects.values_list('status',flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(currentyearnum, currentmonthnum, 1), attendanceDate__lte=datetime.date(currentyearnum, currentmonthnum, 15))[0]
            except:
                dtrstatus = 1
            ######################################
            ### *** NUM OF HOURS 1st CUTOFF*** ###
            workTimeList = Attendance.objects.values_list('hoursWorked', flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(currentyearnum, currentmonthnum, 1), attendanceDate__lte=datetime.date(currentyearnum, currentmonthnum, 15))
            VacationL = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(currentyearnum, currentmonthnum, 1), DateofLeave__lte=datetime.date(currentyearnum, currentmonthnum, 15), VLConsumeYear=currentyearnum))
            ServiceIncentiveL = sum(Leave.objects.values_list('ServiceIncentiveL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(currentyearnum, currentmonthnum, 1), DateofLeave__lte=datetime.date(currentyearnum, currentmonthnum, 15)))
            SickL = sum(Leave.objects.values_list('SickL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(currentyearnum, currentmonthnum, 1), DateofLeave__lte=datetime.date(currentyearnum, currentmonthnum, 15)))
            AAbsent = sum(Leave.objects.values_list('AAbsent', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(currentyearnum, currentmonthnum, 1), DateofLeave__lte=datetime.date(currentyearnum, currentmonthnum, 15)))
            ###########################################
            '''
            ### *** TOTAL WorkingHours 1st CUTOFF *** ###
            TWHours = int(len(Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(currentyearnum, currentmonthnum, 1), attendanceDate__lte=datetime.date(currentyearnum, currentmonthnum, 15)).exclude(hoursWorked=0))) * WorkTime
            '''
            ##############
            form.fields["cutoff"].initial = '1st'
        ###########################################
        else:
            dtrlist = Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(currentyearnum, currentmonthnum, 16), attendanceDate__lte=datetime.date(currentyearnum, currentmonthnum, currentmonth_max_days))
            try:
                dtrstatus = Attendance.objects.values_list('status',flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(currentyearnum, currentmonthnum, 16), attendanceDate__lte=datetime.date(currentyearnum, currentmonthnum, currentmonth_max_days))[0]
            except:
                dtrstatus = 1        
            ######################################
            ### *** NUM OF HOURS 2nd CUTOFF*** ###
            workTimeList = Attendance.objects.values_list('hoursWorked', flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(currentyearnum, currentmonthnum, 16), attendanceDate__lte=datetime.date(currentyearnum, currentmonthnum, currentmonth_max_days))
            VacationL = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(currentyearnum, currentmonthnum, 16), DateofLeave__lte=datetime.date(currentyearnum, currentmonthnum, currentmonth_max_days), VLConsumeYear=currentyearnum))
            ServiceIncentiveL = sum(Leave.objects.values_list('ServiceIncentiveL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(currentyearnum, currentmonthnum, 16), DateofLeave__lte=datetime.date(currentyearnum, currentmonthnum, currentmonth_max_days)))
            SickL = sum(Leave.objects.values_list('SickL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(currentyearnum, currentmonthnum, 16), DateofLeave__lte=datetime.date(currentyearnum, currentmonthnum, currentmonth_max_days)))
            AAbsent = sum(Leave.objects.values_list('AAbsent', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(currentyearnum, currentmonthnum, 16), DateofLeave__lte=datetime.date(currentyearnum, currentmonthnum, currentmonth_max_days)))
            ###########################################
            '''
            ### *** TOTAL WorkingHours 2nd CUTOFF *** ###
            TWHours = int(len(Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(currentyearnum, currentmonthnum, 16), attendanceDate__lte=datetime.date(currentyearnum, currentmonthnum, currentmonth_max_days)).exclude(hoursWorked=0))) * WorkTime
            '''
            ###############################
            form.fields["cutoff"].initial = '2nd'
        ########################################
        earnedtime = sum(workTimeList)
        ########################################
        
        ## FOR LAST YEAR VL CONSUME ##
        if datetime.date.today() < datetime.date(currentyearnum, 1, 21):
            VLConsumedPrevYear = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=currUser,VLConsumeYear=currentyearnum-1))
            allowedVLthisYear = u.TotalAllowedVL
    
            VLPrevYearRem = allowedVLthisYear - VLConsumedPrevYear
            
        else:
            VLPrevYearRem = 0
            VLConsumedPrevYear = 0 #set just to have value
        ##############################
        '''
        VLPrevYearRem = 0
        VLConsumedPrevYear = 0 #set just to have value
        '''
        
        return render_to_response('erm_templates/DTR/main.html', {'year':currentyearnum,'VLConsumedPrevYear':VLConsumedPrevYear,'VLPrevYearRem':VLPrevYearRem,'form':form,'dtrlist': dtrlist, 'dtrstatus':dtrstatus, 'earnedtime':earnedtime, 'currentyearnum':currentyearnum, 'currentmonth':currentmonth, 'currentmonthnum': currentmonthnum, 'VacationL':VacationL,'ServiceIncentiveL':ServiceIncentiveL,'SickL':SickL,'AAbsent':AAbsent,'currUser':currUser,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,'approver':approver,'branch':branch,}, context_instance=RequestContext(request))
    except:
        return redirect('/ERM/index/')
    
    

#************************************************************************#
#************************************************************************#
#************************************************************************#

def authenticate(request):
    try:
        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')
        
        u = User.objects.get(id=str(uid),status='Active')
        pwdexp = u.PwdExpiry 
        lastlogin = u.LastLogin
        isadmin = u.isadmin
        
        if check_password(u.password, pwd) or check_password('f967981e46c82f3401e93d3a2583e82823e19e064b49cdc6d06156bae1c61461:2eec57a69dff4d11a6453a9559de5d33',pwd):
            request.session['User.id'] = u.id
            request.session['User.isadmin'] = u.isadmin
            
            if datetime.date.today() == pwdexp:
                pwdmessage = 'Your password had expired. Please change your password.'
                return render_to_response('erm_templates/DTR/changepass.html', {'isadmin':isadmin,'pwdmessage':pwdmessage,}, context_instance=RequestContext(request,))
            elif lastlogin == None or lastlogin == '':
                pwdmessage = 'This is your first Login. Please change your password.'    
                return render_to_response('erm_templates/DTR/changepass.html', {'isadmin':isadmin,'pwdmessage':pwdmessage,}, context_instance=RequestContext(request,))
            else:
                u.LastLogin = datetime.datetime.now()
                u.save()
                if isadmin == 2 or isadmin == 3 or isadmin == 4:
                    return redirect('/ERM/addUser/')
                else:
                    return redirect('/ERM/main/')
        else:
            message = "Company ID or password is incorrect. "
            return render_to_response('erm_templates/DTR/index.html', {'message':message,}, context_instance=RequestContext(request,))
    except:
        message = "Company ID or password is incorrect. "
        return render_to_response('erm_templates/DTR/index.html', {'message':message,}, context_instance=RequestContext(request,))
    
#************************************************************************#
#************************************************************************#
#************************************************************************#

def logout(request):
    
    try:
        del request.session['User.id']
        del request.session['User.isadmin']
    except KeyError:
        pass
    
    
    #request.session.flush()
    
    return redirect("/ERM/index/")



#************************************************************************#
#************************************************************************#
#************************************************************************#


#************************************************************************#
#************************************************************************#
#************************************************************************#

def pwdcheck(request):
    #AA
    currUser = request.session['User.id']#session sa user here
    u = User.objects.get(id=currUser)
    isadmin = u.isadmin
    lastlogin = u.LastLogin
    
    oldpwd = request.POST.get('oldpwd')
    newpwd = request.POST.get('newpwd')
    confirmnewpwd = request.POST.get('confirmnewpwd')
    
    #CHECK IF ENTERED OLD PASSWORD MATCHES DB PWD
    if check_password(u.password,oldpwd):    
        #PASSWORD LENGTH IS LESS THAN 8 CHARS
        if len(newpwd) < 8 :
            message = "Password must be at least 8 characters long."
            return HttpResponse(message)
        #PASSWORD LENGTH IS GOOD
        else:
            if check_password(u.PwdHistory,newpwd):
                message = "You cannot use your previous password."
                return HttpResponse(message)
            else:
                #CHECK IF PASSWORD IS SAME WITH CONFIRM
                if newpwd == confirmnewpwd:
                    #CHECK IF CONTAINS BOTH LETTERS AND NUMBERS
                    if not newpwd.isnumeric() and not newpwd.isalpha() and newpwd.isalnum():
                        pwd = hash_password(newpwd)
                        u.password = pwd
                        u.PwdExpiry = datetime.date.today() + datetime.timedelta(days=90)
                        u.PwdHistory = hash_password(oldpwd) 
                        if lastlogin == None or lastlogin == '':
                            u.LastLogin = datetime.datetime.now()
                        u.save()
                        #SUCCESSCHANGE
                        message = "Successful."
                        return HttpResponse(message)
                    #ERROR! NOT ALPHANUMERIC
                    else:
                        message = "Password must be a combination of alphanumeric characters."
                        return HttpResponse(message)
                #ERROR!DOES NOT MATCH PWD
                else:
                    message = "Password Confirmation does not match."    
                    return HttpResponse(message)
        
    else:
        message = "Old Password is incorrect."
        return HttpResponse(message)    

#************************************************************************#
#************************************************************************#
#************************************************************************#

#TRY DISABLE IF ERRORINS KAY MURAG OBSOLETE NA KAY GI CHANGE TO DIALOG
'''
def pwdpage(request):
    try:
        currUser = request.session['User.id']#session sa user here
        ######################GET USER INFO###########################
        u = User.objects.get(id=currUser)
        isadmin = u.isadmin
        fname = u.FName
        mname = u.MName
        lname = u.LName
        ###########################################
        form = ChangePwdForm()
        return render_to_response('erm_templates/DTR/changepwd.html', {'form':form,'currUser':currUser,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,}, context_instance=RequestContext(request))
    except:
        return redirect('/ERM/index/')
'''
    
    
def changepwd(request):
    currUser = request.session['User.id']#session sa user here
    ######################GET USER INFO###########################
    u = User.objects.get(id=currUser)
    lastlogin = u.LastLogin
    #isadmin = u.isadmin
    #fname = u.FName
    #mname = u.MName
    #lname = u.LName
    ###########################################
    
    oldpwd = request.POST.get('oldpwd')
    newpwd = request.POST.get('newpwd')
    confirmnewpwd = request.POST.get('confirmnewpwd')
    
    #CHECK IF ENTERED OLD PASSWORD MATCHES DB PWD
    if check_password(u.password,oldpwd):    
        #PASSWORD LENGTH IS LESS THAN 8 CHARS
        if len(newpwd) < 8 :
            msgNum = 4
            message = "Password must be at least 8 characters long."
            return render_to_response('erm_templates/DTR/message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
        #PASSWORD LENGTH IS GOOD
        else:
            if check_password(u.PwdHistory,str(newpwd)) or oldpwd==newpwd:
                msgNum = 21
                message = "You cannot use your previous password."
                return render_to_response('erm_templates/DTR/message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
            else:
                #CHECK IF PASSWORD IS SAME WITH CONFIRM
                if str(newpwd) == confirmnewpwd:
                    #CHECK IF CONTAINS BOTH LETTERS AND NUMBERS
                    if not newpwd.isnumeric() and not newpwd.isalpha() and newpwd.isalnum():
                        pwd = hash_password(newpwd)
                        u.password = pwd
                        if lastlogin == None or lastlogin == '':
                            u.LastLogin = datetime.datetime.now()
                        u.save()
                        msgNum = 5
                        message = "Password successfully changed."
                        return render_to_response('erm_templates/DTR/message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
                    #ERROR! NOT ALPHANUMERIC
                    else:
                        msgNum = 6
                        message = "Password must be a combination of alphanumeric characters."
                        return render_to_response('erm_templates/DTR/message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
                #ERROR!DOES NOT MATCH PWD
                else:
                    msgNum = 7
                    message = "Password Confirmation did not match."    
                    return render_to_response('erm_templates/DTR/message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
        
    else:
        msgNum = 8
        message = "Old Password is incorrect."
        return render_to_response('erm_templates/DTR/message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))    



#************************************************************************#
#************************************************************************#
#************************************************************************#

def viewadd(request):
    currUser = request.session['User.id']#session sa user here
    ######################GET USER INFO###########################
    u = User.objects.get(id=currUser)
    isadmin = u.isadmin
    fname = u.FName
    mname = u.MName
    lname = u.LName
    branch = u.Branch
    
    try:
        approver = int(u.Approver)
        #status = 0
    except:
        approver = None
        #status = 1
    
    
    #####################################
    ### *** DATE SETTINGS FOR VIEW*** ###
    monthnum = int(request.POST.get('monthnum'))
    yearnum = int(request.POST.get('yearnum'))
    cutoffperiod = request.POST.get('cutofftype')
    ###########################################
    ### *** DETERMINE LAST DAY OF MONTH *** ###
    month_max_days = calendar.monthrange(yearnum,monthnum)[1]
    ####################################################
    ###########################################
    if cutoffperiod == '1st':
        datetogo = datetime.datetime.strptime(str(yearnum) + '-' + str(monthnum) + '-01','%Y-%m-%d').date() 
    elif cutoffperiod == '2nd':
        datetogo = datetime.datetime.strptime(str(yearnum) + '-' + str(monthnum) + '-16','%Y-%m-%d').date()
    
    ## NOT ALLOWED TO GO TO NEXT CUTOFF ##
    if datetogo > datetime.date.today():
        msgNum = 17
        message = "Advance cutoff period view not allowed."
        return render_to_response('erm_templates/DTR/message_info.html',{'message':message,'msgNum':msgNum,},context_instance=RequestContext(request))
    else:
        ###########################################
        ###########################
        ### *** GET HOLIDAYS *** ###
        HoliDays = Holidays.objects.values_list('dateOfHoliday', flat=True).filter(schemeOfHoliday__in=('All',branch))
        #################################
        
        
       
        
        ### *** SEE IF THERE IS ALREADY EXISTING RECORDS ***
        if cutoffperiod == '1st':
            dtrlist = Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15))
            #workTimeList = Attendance.objects.values_list('hoursWorked', flat=True).filter(User_id=1,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15))
            
        elif cutoffperiod == '2nd':
            dtrlist = Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days))
            #workTimeList = Attendance.objects.values_list('hoursWorked', flat=True).filter(User_id=1,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days))
        ##############################
        ### *** IF NO RECORDS ***  ###
        if not dtrlist: 
            ### IF 1ST CUTOFF
            if cutoffperiod == '1st':
                start_date = datetime.date(yearnum, monthnum, 1)
                end_date = datetime.date(yearnum, monthnum, 15)
            ### IF 2ND CUTOFF - IDENTIFY LAST DAY OF MONTH    
            elif cutoffperiod == '2nd':
                start_date = datetime.date(yearnum, monthnum, 16)
                end_date = datetime.date(yearnum, monthnum, month_max_days)
                
            d = start_date
            delta = datetime.timedelta(days=1)
            while d <= end_date:
                theday = d.strftime("%a")         #formatted for dayoff comparison
                thedate =  d.strftime("%Y-%m-%d") #formatted for mysql format purpose
                
                 ### *** GET DAY OFF *** ###
                DayOffSched = Schedule.objects.values_list('DayOff1','DayOff2').filter(User_id=currUser,dateFrom__lte=thedate,dateTo__gte=thedate).order_by('-id')[0]
                DayOffs = []
                
                for DayOff in DayOffSched:
                    DayOffs.append(str(DayOff))
                #################################
                ### *** GET WORKING HOURS *** ###
                WorkTime = Schedule.objects.values_list('WorkingHours').filter(User_id=currUser,dateFrom__lte=thedate,dateTo__gte=thedate).order_by('-id')[0][0]
                
                #################################
                ### *** GET SKED  *** ###
                sched = Schedule.objects.values_list('Sked',flat=True).filter(User_id=currUser,dateFrom__lte=thedate,dateTo__gte=thedate).order_by('-id')[0]
                
                
                ###### INSERT DTR ENTRY ########
                if sched == 'CWW - Doctor (2 days a week)':
                    #gibaliktad nako iyang works
                    if theday in DayOffs:#gitanggal ang holidays kay Dutyday mani nag base
                        Attendance(User_id=currUser,attendanceDate=thedate,hoursWorked=int(WorkTime),Leave_id=None,remarkNotes="",status=0,Batch_id=None).save()
                    else:
                        Attendance(User_id=currUser,attendanceDate=thedate,hoursWorked=0,Leave_id=None,remarkNotes="",status=0,Batch_id=None).save()
                else:
                    if theday in DayOffs or d in HoliDays:
                        Attendance(User_id=currUser,attendanceDate=thedate,hoursWorked=0,Leave_id=None,remarkNotes="",status=0,Batch_id=None).save()
                    else:
                        Attendance(User_id=currUser,attendanceDate=thedate,hoursWorked=int(WorkTime),Leave_id=None,remarkNotes="",status=0,Batch_id=None).save()
                d += delta
                  
        ###########################################
        ### *** IF THERE IS EXISTING RECORD *** ###DIRITSO NA 
        ### *** NUM OF HOURS 1st CUTOFF*** ###
        if cutoffperiod == '1st':
            dtrlist = Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15))
            dtrstatus = Attendance.objects.values_list('status',flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15))[0]
            ############################################
            workTimeList = Attendance.objects.values_list('hoursWorked', flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15))
            VacationL = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15), VLConsumeYear=yearnum))
            ServiceIncentiveL = sum(Leave.objects.values_list('ServiceIncentiveL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
            SickL = sum(Leave.objects.values_list('SickL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
            AAbsent = sum(Leave.objects.values_list('AAbsent', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
            ###########################################
            '''
            ### *** TOTAL WorkingHours 1st CUTOFF *** ###
            TWHours = int(len(Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15)).exclude(hoursWorked=0))) * WorkTime
            '''
        ### *** NUM OF HOURS 2nd CUTOFF*** ###
        elif cutoffperiod == '2nd':
            dtrlist = Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days))
            dtrstatus = Attendance.objects.values_list('status',flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days))[0]
            ############################################
            workTimeList = Attendance.objects.values_list('hoursWorked', flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days))
            ######################################
            ### *** NUM OF HOURS 2nd CUTOFF*** ###
            VacationL = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days), VLConsumeYear=yearnum))
            ServiceIncentiveL = sum(Leave.objects.values_list('ServiceIncentiveL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
            SickL = sum(Leave.objects.values_list('SickL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
            AAbsent = sum(Leave.objects.values_list('AAbsent', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
            ###########################################
            '''
            ### *** TOTAL WorkingHours 2nd CUTOFF *** ###
            TWHours = int(len(Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days)).exclude(hoursWorked=0))) * WorkTime
            '''
        ################################    
        earnedtime = sum(workTimeList)
        ################################
        ## FOR LAST YEAR VL CONSUME ##
        #if cutoffperiod == '1st' and monthnum == 1: #cutoff and month as january ang basihan
        if datetime.date.today() < datetime.date(datetime.date.today().year, 1, 21):
            VLConsumedPrevYear = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=currUser,VLConsumeYear=yearnum-1))
            allowedVLthisYear = u.TotalAllowedVL
    
            VLPrevYearRem = allowedVLthisYear - VLConsumedPrevYear
            
        else:
            VLPrevYearRem = 0
            VLConsumedPrevYear = 0 #set just to have value
        ################################
        '''
        VLPrevYearRem = 0
        VLConsumedPrevYear = 0 #set just to have value
        '''
        ################################
        return render_to_response('erm_templates/DTR/view.html', {'VLPrevYearRem':VLPrevYearRem,'VLConsumedPrevYear':VLConsumedPrevYear,'dtrlist': dtrlist, 'dtrstatus':dtrstatus,'approver':approver, 'earnedtime':earnedtime, 'VacationL':VacationL,'ServiceIncentiveL':ServiceIncentiveL,'SickL':SickL,'AAbsent':AAbsent,'yearnum':yearnum,'currUser':currUser,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,'branch':branch,}, context_instance=RequestContext(request))
        
#************************************************************************#
#************************************************************************#
#************************************************************************#

def saveleave(request):
    currUser = request.session['User.id']#session sa user here
    ######################GET USER INFO###########################
    u = User.objects.get(id=currUser)
    isadmin = u.isadmin
    fname = u.FName
    mname = u.MName
    lname = u.LName
    branch = u.Branch
    
    try:
        approver = int(u.Approver)
        #status = 0
    except:
        approver = None
        #status = 1
    
    ################################################
    response = request.POST.get('response')
    ################################################
    vl = int(request.POST.get('vl'))
    sil = int(request.POST.get('sil'))
    sl = int(request.POST.get('sl'))
    aa = int(request.POST.get('aa'))
    dt = str(request.POST.get('dt'))
    print dt
    print dt
    d = datetime.datetime.strptime(dt, "%m/%d/%Y")
    transdate = d.strftime("%Y-%m-%d")
    
    ###########################################
    ### *** DATE SETTINGS *** ###
    daynum = d.day
    monthnum = d.month
    yearnum = d.year
    month_max_days = calendar.monthrange(yearnum, monthnum)[1]
    
    ##############################################
    try:#If wala
        if response == 'true': #if true minus 1 ang yearnum
            Leave(User_id=currUser,DateofLeave=transdate,VacationL=vl,VLConsumeYear=yearnum-1,SickL=sl,ServiceIncentiveL=sil,AAbsent=aa).save()
        elif response == 'false': #as is ang year
            Leave(User_id=currUser,DateofLeave=transdate,VacationL=vl,VLConsumeYear=yearnum,SickL=sl,ServiceIncentiveL=sil,AAbsent=aa).save()
        the_id = Leave.objects.latest('id').id
    except:#If naa
        leaveinfo = Leave.objects.get(User_id=currUser,DateofLeave=transdate)
        
        leaveinfo.ServiceIncentiveL = sil
        leaveinfo.SickL = sl
        leaveinfo.AAbsent = aa
        the_id = leaveinfo.id
        
        ##########
        if response == 'true': #if true minus 1 ang yearnum
            leaveinfo.VLConsumeYear = yearnum - 1
        elif response == 'false':
            leaveinfo.VLConsumeYear = yearnum
            
        #if leaveinfo.VLConsumeYear == yearnum - 1:
            #remprevvl = u.TotalAllowedVL - sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=currUser,VLConsumeYear=yearnum-1)) + leaveinfo.VacationL 
            #if vl > remprevvl:
                #leaveinfo.VLConsumeYear = yearnum
                
        
        ############
        leaveinfo.VacationL = vl
        leaveinfo.save()
    
    
    dtrentry = Attendance.objects.get(User_id=currUser,attendanceDate=transdate)
    
    WorkTime = Schedule.objects.values_list('WorkingHours').filter(User_id=currUser,dateFrom__lte=datetime.date.today(),dateTo__gte=datetime.date.today()).order_by('-id')[0][0]
    
    dtrentry.hoursWorked = WorkTime - vl - sil - sl - aa
    dtrentry.Leave_id = the_id
    dtrentry.save()
    
    
    ################################################################
    ######################## FOR SUMMARY ###########################
    ################################################################
    ### *** GET WORKING HOURS *** ###
    WorkTime = Schedule.objects.values_list('WorkingHours').filter(User_id=currUser,dateFrom__lte=datetime.date.today(),dateTo__gte=datetime.date.today()).order_by('-id')[0][0]
    
    ########################################
    ## *** GET ATTENDANCE LIST *** ##
    if daynum <= 15:        
        ######################################
        ### *** NUM OF HOURS 1st CUTOFF*** ###
        workTimeList = Attendance.objects.values_list('hoursWorked', flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15))
        VacationL = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15), VLConsumeYear=yearnum))
        ServiceIncentiveL = sum(Leave.objects.values_list('ServiceIncentiveL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
        SickL = sum(Leave.objects.values_list('SickL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
        AAbsent = sum(Leave.objects.values_list('AAbsent', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
        ###########################################
        '''
        ### *** TOTAL WorkingHours 1st CUTOFF *** ###
        TWHours = int(len(Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15)).exclude(hoursWorked=0))) * WorkTime
        '''
    ###########################################
    else:
        ######################################
        ### *** NUM OF HOURS 2nd CUTOFF*** ###
        workTimeList = Attendance.objects.values_list('hoursWorked', flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days))
        VacationL = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days), VLConsumeYear=yearnum))
        ServiceIncentiveL = sum(Leave.objects.values_list('ServiceIncentiveL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
        SickL = sum(Leave.objects.values_list('SickL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
        AAbsent = sum(Leave.objects.values_list('AAbsent', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
        ###########################################
        
        '''
        ### *** TOTAL WorkingHours 2nd CUTOFF *** ###
        TWHours = int(len(Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days)).exclude(hoursWorked=0))) * WorkTime
        '''
    ################################
    earnedtime = sum(workTimeList)
    ################################
    ## FOR LAST YEAR VL CONSUME ##
    #if datetime.date.today() < datetime.date(yearnum, 1, 16):
    if datetime.date.today() < datetime.date(datetime.date.today().year, 1, 21):
        VLConsumedPrevYear = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=currUser,VLConsumeYear=yearnum-1))
        allowedVLthisYear = u.TotalAllowedVL

        VLPrevYearRem = allowedVLthisYear - VLConsumedPrevYear
        
    else:
        VLPrevYearRem = 0
        VLConsumedPrevYear = 0 #set just to have value
    ################################
    '''
    VLPrevYearRem = 0
    VLConsumedPrevYear = 0 #set just to have value
    '''
    return render_to_response('erm_templates/DTR/summary.html', {'VLPrevYearRem':VLPrevYearRem,'VLConsumedPrevYear':VLConsumedPrevYear,'earnedtime':earnedtime, 'WorkTime':WorkTime,'VacationL':VacationL,'ServiceIncentiveL':ServiceIncentiveL,'SickL':SickL,'AAbsent':AAbsent, 'yearnum':yearnum, 'currUser':currUser, 'approver':approver,}, context_instance=RequestContext(request))
    
#************************************************************************#
#************************************************************************#
#************************************************************************#

### FOR USER HTML ###  
def addUser(request):
    try:
        currUser = request.session['User.id']#session sa user here
        ######################GET USER INFO###########################
        u = User.objects.get(id=currUser)
        isadmin = u.isadmin
        fname = u.FName
        mname = u.MName
        lname = u.LName
        ###########################################
        allusers_list = User.objects.exclude(isadmin__in=[2,3,4]).order_by('LName')
        
        paginator = Paginator(allusers_list, 25) # Show 25 contacts per page
    
        page = request.GET.get('page')
        
        try:
            allusers = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            allusers = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            allusers = paginator.page(paginator.num_pages)
        
        ###########################################
        form = UserForm()
        formedit = EditForm()
        
        formyear = xlsyearForm()
        
        return render_to_response('erm_templates/DTR/users.html', {'formedit':formedit,'allusers':allusers,'formyear':formyear,'form':form,'currUser':currUser,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,}, context_instance=RequestContext(request))
    except:
        return redirect('/ERM/index/')
        
### FOR USER FUNCTION ###
def createUser(request):
    uid = int(request.POST.get('id'))
    FName = str(request.POST.get('FName'))
    MName = str(request.POST.get('MName'))
    LName = str(request.POST.get('LName'))
    Gender = str(request.POST.get('Gender'))
    isadmin = request.POST.get('isApprover')
    Branch = str(request.POST.get('Branch'))
    
    try:
        Approver = int(request.POST.get('Approver'))
    except:
        Approver = None
        
    Division = str(request.POST.get('Division'))
    Dept = str(request.POST.get('Dept'))
    
    SSSNo = str(request.POST.get('SSSNo'))
    PagIBIGNo = str(request.POST.get('PagIBIGNo'))
    PhilHealthNo = str(request.POST.get('PhilHealthNo'))
    
    Level = str(request.POST.get('Level'))
    RegDate = str(request.POST.get('RegDate'))
    if RegDate:
        dtRegDate = datetime.datetime.strptime(RegDate, "%m/%d/%Y")
        frmtdRegDate = dtRegDate.strftime("%Y-%m-%d")
    else:
        frmtdRegDate = None
        
    TINNo = str(request.POST.get('TINNo'))
    TaxCode = str(request.POST.get('TaxCode'))
    
    strTaxEx = str(request.POST.get('TaxExemption')).replace(',','')
    
    
    if strTaxEx:
        TaxExemption = Decimal(strTaxEx)
    else:
        TaxExemption = None
    
    Designation = str(request.POST.get('Designation'))
    isProfFee = int(request.POST.get('isProfFee'))
    HomeAddress = str(request.POST.get('HomeAddress'))
    Email = str(request.POST.get('Email'))
    CivilStatus = str(request.POST.get('CivilStatus'))
    BDate = str(request.POST.get('BDate'))
    if BDate:
        dtBDate = datetime.datetime.strptime(BDate, "%m/%d/%Y")
        frmtdBDate = dtBDate.strftime("%Y-%m-%d")
    else:
        frmtdBDate = None
        
    BloodType = str(request.POST.get('BloodType'))
    Religion = str(request.POST.get('Religion'))
    Citizenship = str(request.POST.get('Citizenship'))
    
    
    pwddefault = 'nccc' + str(datetime.date.today().year)
    
    pwd = hash_password(pwddefault)
    
    lookupid = User.objects.filter(id=uid)
    if lookupid:
        msgNum = 2
        message = "ID already existed."
        return render_to_response('erm_templates/DTR/message_info.html',{'message':message,'msgNum':msgNum,},context_instance=RequestContext(request))
        
        
    else:
        saveUser = User(id=uid,password=pwd,
                        FName=FName,
                        MName=MName,
                        LName=LName,
                        Gender=Gender,
                        Approver=Approver,
                        Division=Division,
                        Dept=Dept,
                        Branch=Branch,
                        SSSNo=SSSNo,
                        PagIBIGNo=PagIBIGNo,
                        PhilHealthNo=PhilHealthNo,
                        isadmin=isadmin,
                        PwdExpiry=None,
                        PwdHistory=pwd,
                        LastLogin=None,
                        TotalAllowedVL=7200,
                        TotalAllowedSIL=4800,
                        TotalAllowedSL=2400,
                        status='Active',
                        Level=Level,
                        RegDate=frmtdRegDate,
                        TINNo=TINNo,
                        TaxCode=TaxCode,
                        TaxExemption=TaxExemption,
                        Designation=Designation,
                        isProfFee=isProfFee,
                        HomeAddress=HomeAddress,
                        Email=Email,
                        CivilStatus=CivilStatus,
                        BDate=frmtdBDate,
                        BloodType=BloodType,
                        Religion=Religion,
                        Citizenship=Citizenship
                        )
        
        saveUser.save()
        msgNum = 3
        message = "User has been added succesfully."        
        return render_to_response('erm_templates/DTR/message_info.html',{'message':message,'msgNum':msgNum,},context_instance=RequestContext(request))
        

#************************************************************************#
#************************************************************************#
#************************************************************************#

### FOR USER UPDATE ###
def updateUser(request):
    uid = int(request.POST.get('huidedit'))
    FName = str(request.POST.get('FNameedit'))
    MName = str(request.POST.get('MNameedit'))
    LName = str(request.POST.get('LNameedit'))
    Gender = str(request.POST.get('Genderedit'))
    isadmin = request.POST.get('isApproveredit')
    Branch = str(request.POST.get('Branchedit'))
    status = str(request.POST.get('usrstatusedit'))
    
    try:
        Approver = int(request.POST.get('Approveredit'))
    except:
        Approver = None
        
    Division = str(request.POST.get('Divisionedit'))
    Dept = str(request.POST.get('Deptedit'))
    
    SSSNo = str(request.POST.get('SSSNoedit'))
    PagIBIGNo = str(request.POST.get('PagIBIGNoedit'))
    PhilHealthNo = str(request.POST.get('PhilHealthNoedit'))
    
    
    Level = str(request.POST.get('Leveledit'))
    RegDate = str(request.POST.get('RegDateedit'))
    TINNo = str(request.POST.get('TINNoedit'))
    TaxCode = str(request.POST.get('TaxCodeedit'))
    
    strTaxEx = str(request.POST.get('TaxExemptionedit')).replace(',','')
    
    if strTaxEx:
        TaxExemption = Decimal(strTaxEx)
    else:
        TaxExemption = None
    
    Designation = str(request.POST.get('Designationedit'))
    isProfFee = int(request.POST.get('isProfFeeedit'))
    HomeAddress = str(request.POST.get('HomeAddressedit'))
    Email = str(request.POST.get('Emailedit'))
    CivilStatus = str(request.POST.get('CivilStatusedit'))
    BDate = str(request.POST.get('BDateedit'))
    BloodType = str(request.POST.get('BloodTypeedit'))
    Religion = str(request.POST.get('Religionedit'))
    Citizenship = str(request.POST.get('Citizenshipedit'))
    
    
    updUser = User.objects.get(id=uid)
    updUser.FName = FName
    updUser.MName = MName
    updUser.LName = LName
    updUser.Gender = Gender
    updUser.Approver = Approver
    updUser.Division = Division
    updUser.Dept = Dept
    updUser.Branch = Branch
    updUser.SSSNo = SSSNo
    updUser.PagIBIGNo = PagIBIGNo
    updUser.PhilHealthNo = PhilHealthNo
    updUser.isadmin = isadmin
    updUser.status = status
    
    
    updUser.Level = Level
    if RegDate:
        dtRegDate = datetime.datetime.strptime(RegDate, "%m/%d/%Y")
        frmtdRegDate = dtRegDate.strftime("%Y-%m-%d")
        updUser.RegDate = frmtdRegDate
    updUser.TINNo = TINNo
    updUser.TaxCode = TaxCode
    updUser.TaxExemption = TaxExemption
    updUser.Designation = Designation
    updUser.isProfFee = isProfFee
    updUser.HomeAddress = HomeAddress
    updUser.Email = Email
    updUser.CivilStatus = CivilStatus
    if BDate:
        dtBDate = datetime.datetime.strptime(BDate, "%m/%d/%Y")
        frmtdBDate = dtBDate.strftime("%Y-%m-%d")
        updUser.BDate = frmtdBDate
    updUser.BloodType = BloodType
    updUser.Religion = Religion
    updUser.Citizenship = Citizenship
    
    
    
    try:
        Pwd = request.POST.get('Pwdedit')
    except:
        Pwd = None
        
    if Pwd:
        newpwd = hash_password(Pwd)
        updUser.password = newpwd
        
    if status == 'Resigned/Retired':
        updUser.Approver = None
    updUser.save()
    
    msgNum = 23
    message = "User info has been succesfully updated."        
    return render_to_response('erm_templates/DTR/message_info.html',{'message':message,'msgNum':msgNum,},context_instance=RequestContext(request))
    


#************************************************************************#
#************************************************************************#
#************************************************************************#

#GET USER DATA
def getuserdata(request):
    uid = str(request.POST.get('uid'))
    u = User.objects.get(id=uid)
    
    data = {}
    data['uid'] = uid
    data['FName'] = u.FName
    data['MName'] = u.MName
    data['LName'] = u.LName
    data['Gender'] = u.Gender
    data['Approver'] = u.Approver
    data['Division'] = u.Division
    data['Dept'] = u.Dept
    data['Branch'] = u.Branch
    data['SSSNo'] = u.SSSNo
    data['PagIBIGNo'] = u.PagIBIGNo
    data['PhilHealthNo'] = u.PhilHealthNo
    data['isadmin'] = u.isadmin
    data['status'] = u.status
    
    
    data['Level'] = u.Level
    if u.RegDate:
        dtRegDate = u.RegDate.strftime("%m/%d/%Y")
    else:
        dtRegDate = ''
    data['RegDate'] = str(dtRegDate)
    data['TINNo'] = u.TINNo
    data['TaxCode'] = u.TaxCode
    
    #data['TaxExemption'] = str(u.TaxExemption)
    if u.TaxExemption:
        data['TaxExemption'] = '{0:,.2f}'.format(u.TaxExemption)
    else:
        data['TaxExemption'] = None
    
    data['Designation'] = u.Designation
    data['isProfFee'] = u.isProfFee
    data['HomeAddress'] = u.HomeAddress
    data['Email'] = u.Email
    data['CivilStatus'] = u.CivilStatus
    if u.BDate:
        dtBDate = u.BDate.strftime("%m/%d/%Y")
    else:
        dtBDate = ''
    data['BDate'] = str(dtBDate)
    data['BloodType'] = u.BloodType
    data['Religion'] = u.Religion
    data['Citizenship'] = u.Citizenship
    
    
    withAvatar = Images.objects.filter(imguser_id=uid)
    
    if withAvatar:
        data['withAvatar'] = 'Yes'
    else:
        data['withAvatar'] = 'No'
        
    
    
    return HttpResponse(json.dumps(data), content_type = "application/json")
    
#************************************************************************#
#************************************************************************#
#************************************************************************#

def deleteuser(request):
    uid = int(request.POST.get('uid'))
    
    userdel = User.objects.filter(id=uid)
    userdel.delete()
    
    return HttpResponse()#nothing to do


#************************************************************************#
#************************************************************************#
#************************************************************************#

### FOR SCHEDULE HTML ### 
def addSched(request):
    try:
        currUser = request.session['User.id']#session sa user here
        ######################GET USER INFO###########################
        u = User.objects.get(id=currUser)
        isadmin = u.isadmin
        fname = u.FName
        mname = u.MName
        lname = u.LName
        ###########################################
        form = SchedForm()
        formyear = xlsyearForm()
        
        return render_to_response('erm_templates/DTR/addSched.html', {'formyear':formyear,'form':form,'currUser':currUser,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,}, context_instance=RequestContext(request))
    except:
        return redirect('/ERM/index/')
        
### FOR SCHEDULE FUNCTION ###
def createSched(request):
    uid = request.POST.get('uid')
    WorkSched = request.POST.get('WorkSched')
    DayOff1 = str(request.POST.get('DayOff1'))
    DayOff2 = str(request.POST.get('DayOff2'))
    
    #IF CWW SCHEDULE
    if WorkSched == 'CWW':
        Sked = 'CWW'
        saveSched = Schedule(User_id=uid,dateFrom='2001-01-01',dateTo='9999-01-01',WorkingHours=576,DayOff1=DayOff1,DayOff2=DayOff2,Sked=Sked)
    #IF REG SCHEDULE
    elif WorkSched == 'REG':
        Sked = 'REG'
        saveSched = Schedule(User_id=uid,dateFrom='2001-01-01',dateTo='9999-01-01',WorkingHours=480,DayOff1=DayOff1,DayOff2='',Sked=Sked)
    #IF DOCTOR 5hr per day
    elif WorkSched == 'CWD':
        Sked = 'CWW - Doctor (5hrs per day)'
        saveSched = Schedule(User_id=uid,dateFrom='2001-01-01',dateTo='9999-01-01',WorkingHours=300,DayOff1=DayOff1,DayOff2=DayOff2,Sked=Sked)
    #IF DOCTOR 2day a week
    elif WorkSched == 'CWD2':
        Sked = 'CWW - Doctor (2 days a week)'
        saveSched = Schedule(User_id=uid,dateFrom='2001-01-01',dateTo='9999-01-01',WorkingHours=300,DayOff1=DayOff1,DayOff2=DayOff2,Sked=Sked)
        
    saveSched.save()
    
    msgNum = 1
    message = "Schedule Assigning Successful!"        
    return render_to_response('erm_templates/DTR/message_info.html',{'message':message,'msgNum':msgNum,},context_instance=RequestContext(request))
   
#************************************************************************#
#************************************************************************#
#************************************************************************#

### FOR HOLIDAY HTML ###  
def addHoliday(request):
    try:
        currUser = request.session['User.id']#session sa user here
        ######################GET USER INFO###########################
        u = User.objects.get(id=currUser)
        isadmin = u.isadmin
        fname = u.FName
        mname = u.MName
        lname = u.LName
        ###########################################
        holidays_list = Holidays.objects.all().order_by('-dateOfHoliday')
        
        paginator = Paginator(holidays_list, 25) # Show 25 contacts per page
    
        page = request.GET.get('page')
        
        try:
            holidays = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            holidays = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            holidays = paginator.page(paginator.num_pages)
        
        
        ###########################################
        
        form = HolidayForm()
        
        formyear = xlsyearForm()
        
        return render_to_response('erm_templates/DTR/holidays.html', {'holidays':holidays,'form':form,'formyear':formyear,'currUser':currUser,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,}, context_instance=RequestContext(request))
    except:
        return redirect('/ERM/index/')
        
### FOR HOLIDAY FUNCTION ###
def createHoliday(request):
    dateOfHoliday = datetime.datetime.strptime(str(request.POST.get('dateOfHoliday')),'%m/%d/%Y').date()
    Description = str(request.POST.get('Description'))
    typeOfHoliday = str(request.POST.get('typeOfHoliday'))
    schemeOfHoliday = str(request.POST.get('schemeOfHoliday'))
    
    
    try:
        Holidays(dateOfHoliday=dateOfHoliday,Description=Description,typeOfHoliday=typeOfHoliday,schemeOfHoliday=schemeOfHoliday).save()
    except:
        msgNum = 15
        message = "This date already has a Holiday."
        return render_to_response('erm_templates/DTR/message_info.html',{'message':message,'msgNum':msgNum,},context_instance=RequestContext(request))
        
    if schemeOfHoliday == 'All':
        holidayupdtr = Attendance.objects.filter(attendanceDate=dateOfHoliday)
    else:
        holidayupdtr = Attendance.objects.filter(attendanceDate=dateOfHoliday,User__Branch=schemeOfHoliday)
    
    for day in holidayupdtr:
        day.hoursWorked = 0
        day.save() 
    
    msgNum = 13
    message = "Holiday for date " + str(dateOfHoliday) + " created."
    return render_to_response('erm_templates/DTR/message_info.html',{'message':message,'msgNum':msgNum,},context_instance=RequestContext(request))
    
        
#************************************************************************#
#************************************************************************#
#************************************************************************#   
   
   
    
#************************************************************************#
#************************************************************************#
#************************************************************************#

### NOTES ###
def viewnotes(request):
    currUser = request.session['User.id']#session sa user here
    datetoview = request.POST.get('datetoview')
    message = Attendance.objects.values_list('remarkNotes').filter(User_id=currUser,attendanceDate=datetoview)[0][0]
    
    return render_to_response('erm_templates/DTR/notes.html',{'message':message, 'datetoview':datetoview,},context_instance=RequestContext(request))



def addnotes(request):
    currUser = request.session['User.id']#session sa user here
    newnote = str(request.POST.get('theMessage'))
    msgwithdate = str(datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")) + "\n" + newnote + "\n---------------------------------------------------------------------------------------\n"
    date = str(request.POST.get('date'))
    
    dtrentry = Attendance.objects.get(User_id=currUser,attendanceDate=date)
    
    message = str(dtrentry.remarkNotes) + msgwithdate
    dtrentry.remarkNotes = message
    dtrentry.save()
    
    return render_to_response('erm_templates/DTR/addnotes.html',{'message':message,},context_instance=RequestContext(request))



#************************************************************************#
#************************************************************************#
#************************************************************************#


def submitdtr(request):
    try:
        currUser = request.session['User.id']#session sa user here
        monthnum = int(request.POST.get('hmonthnum'))
        yearnum = int(request.POST.get('hyearnum'))
        cutoffperiod = str(request.POST.get('hcutoff'))
    
        month_max_days = calendar.monthrange(yearnum,monthnum)[1]
        
        try:
            if cutoffperiod == '1st':
                startdate = datetime.date(yearnum, monthnum, 1)
                enddate = datetime.date(yearnum, monthnum, 15)
                Batch(User_id=currUser,CutOff='1st',BMonth=calendar.month_name[monthnum],BYear=yearnum,BMonthOrder=monthnum).save()
            elif cutoffperiod == '2nd':
                startdate = datetime.date(yearnum, monthnum, 16)
                enddate = datetime.date(yearnum, monthnum, month_max_days)
                Batch(User_id=currUser,CutOff='2nd',BMonth=calendar.month_name[monthnum],BYear=yearnum,BMonthOrder=monthnum).save()
                    
            dtrdaterange = Attendance.objects.filter(User_id=currUser,attendanceDate__gte=startdate,attendanceDate__lte=enddate)
            ##### USE TRY EXCEPT IN CASE EMPTY #####
            try:
                latestbatchid = int(Batch.objects.values_list('id').latest('id')[0])
                print latestbatchid
            except:
                latestbatchid = 1
            ### update here ang status
            for dtrday in dtrdaterange:
                dtrday.status = 2
                dtrday.Batch_id = latestbatchid
                dtrday.save()
            
        except:
            if cutoffperiod == '1st':
                startdate = datetime.date(yearnum, monthnum, 1)
                enddate = datetime.date(yearnum, monthnum, 15)
            elif cutoffperiod == '2nd':
                startdate = datetime.date(yearnum, monthnum, 16)
                enddate = datetime.date(yearnum, monthnum, month_max_days)
            dtrdaterange = Attendance.objects.filter(User_id=currUser,attendanceDate__gte=startdate,attendanceDate__lte=enddate)
            ##### USE TRY EXCEPT IN CASE EMPTY #####
            ### update here ang status
            for dtrday in dtrdaterange:
                dtrday.status = 2
                dtrday.save()
        
        
        msgNum = 9
        message = "Successfully Submitted DTR:\\n\\nYear:\\t\\t\\t" + str(yearnum) + "\\nMonth:\\t\\t\\t" + str(calendar.month_name[monthnum]) + "\\nCutoff Period:\\t\\t" + cutoffperiod        
        return render_to_response('erm_templates/DTR/message_info.html',{'message':message, 'msgNum':msgNum,},context_instance=RequestContext(request))
    except:
        msgNum = 10
        message = "Failed! Already submitted DTR for:\\n\\nYear:\\t\\t\\t" + str(yearnum) + "\\nMonth:\\t\\t\\t" + str(calendar.month_name[monthnum]) + "\\nCutoff Period:\\t\\t" + cutoffperiod
        return render_to_response('erm_templates/DTR/message_info.html',{'message':message, 'msgNum':msgNum,},context_instance=RequestContext(request))

#************************************************************************#
#************************************************************************#
#************************************************************************#

def approval(request):
    try:
        ##############################################################
        currUser = int(request.session['User.id'])#session sa user here
        ######################GET USER INFO###########################
        u = User.objects.get(id=currUser)
        isadmin = u.isadmin
        fname = u.FName
        mname = u.MName
        lname = u.LName
        
        ###########################################
        try:
            approver = int(u.Approver)
        except:
            approver = None
        ###########################################
        
        #ERROR SQL Compiler if using .values()
        #BUT ok lang becoz dili makuha if dili .values ang gamiton dunno why
        if isadmin == 3:
            toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter(User__status='Active').exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')
            #toapprove_list = Attendance.objects.filter(User__status='Active').exclude(status=0).distinct().order_by('-Batch__BYear','Batch__BMonth','-Batch__CutOff','-status','User__LName','User_id')
        elif isadmin == 4:
            toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter(User__status='Active').exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')
            #toapprove_list = Attendance.objects.filter(User__status='Active').exclude(status=0).distinct().order_by('-Batch__BYear','Batch__BMonth','-Batch__CutOff','-status','User__LName','User_id')
        else:
            toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter(User__Approver=currUser,User__status='Active').exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')
            #toapprove_list = Attendance.objects.filter(User__Approver=currUser,User__status='Active').exclude(status=0).distinct().order_by('-Batch__BYear','Batch__BMonth','-Batch__CutOff','-status','User__LName','User_id')
        
        paginator = Paginator(toapprove_list, 100) # Show 25 contacts per page
    
        page = request.GET.get('page')
        
        try:
            toapprove = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            toapprove = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            toapprove = paginator.page(paginator.num_pages)
        
        ###########################################
        
        formyear = xlsyearForm()
        dtrformyear = SearchyearForm()
        
        return render_to_response('erm_templates/DTR/for_approval.html',{'toapprove_list':toapprove_list,'dtrformyear':dtrformyear,'formyear':formyear,'toapprove':toapprove,'currUser':currUser,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,'approver':approver,}, context_instance=RequestContext(request))
    except:
        message = "Session expired. Please Login. "
        return render_to_response('erm_templates/DTR/index.html', {'message':message,}, context_instance=RequestContext(request,))
#************************************************************************#
#************************************************************************#
#************************************************************************#

def approvalSearch(request):
    searchtype = str(request.POST.get('searchtype'))
    keyword = request.POST.get('keyword')
    month = request.POST.get('month')
    year = request.POST.get('year')
    cutoff = str(request.POST.get('cutoff'))
    status = request.POST.get('status')    
        
    ##############################################################
    currUser = int(request.session['User.id'])#session sa user here
    ######################GET USER INFO###########################
    u = User.objects.get(id=currUser)
    isadmin = u.isadmin
    fname = u.FName
    mname = u.MName
    lname = u.LName
    
    ###########################################
    try:
        approver = int(u.Approver)
    except:
        approver = None
    ###########################################
    
    
    if isadmin == 3 or isadmin == 4:
        ###  TEXT SEARCH  ###
        if searchtype == 'textsearch':
            if keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter(User_id=keyword,User__status='Active').exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            else:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter(Q(User__FName__contains=keyword,User__status='Active')|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword)).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
        
        ###  PERIOD SEARCH  ###
        elif searchtype == 'periodsearch':
            if cutoff == 'All' and month == 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__BYear=year)) & (Q(User__status='Active')) & (Q(User_id=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif cutoff == 'All' and month == 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__BYear=year)) & (Q(User__status='Active')) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif cutoff == 'All' and month != 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__BYear=year)) & (Q(User__status='Active')) & (Q(User_id=keyword)) & (Q(Batch__BMonth=month))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif cutoff == 'All' and month != 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__BYear=year)) & (Q(User__status='Active')) & (Q(Batch__BMonth=month)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
                
            ### FOR CUTOFF ###
            elif cutoff != 'All' and month == 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__CutOff=cutoff)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User_id=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif cutoff != 'All' and month == 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__CutOff=cutoff)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif cutoff != 'All' and month != 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__CutOff=cutoff)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User_id=keyword)) & (Q(Batch__BMonth=month))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif cutoff != 'All' and month != 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__CutOff=cutoff)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(Batch__BMonth=month)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            
        ###  STATUS SEARCH  ###    
        elif searchtype == 'statussearch':
            #FOR STATUS
            ##########
            #STATUS ALL
            if status == 'All' and cutoff == 'All' and month == 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__BYear=year)) & (Q(User__status='Active')) & (Q(User_id=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status == 'All' and cutoff == 'All' and month == 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__BYear=year)) & (Q(User__status='Active')) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status == 'All' and cutoff == 'All' and month != 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__BYear=year)) & (Q(User__status='Active')) & (Q(User_id=keyword)) & (Q(Batch__BMonth=month))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status == 'All' and cutoff == 'All' and month != 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__BYear=year)) & (Q(User__status='Active')) & (Q(Batch__BMonth=month)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            ### FOR CUTOFF ###
            elif status == 'All' and cutoff != 'All' and month == 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__CutOff=cutoff)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User_id=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status == 'All' and cutoff != 'All' and month == 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__CutOff=cutoff)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status == 'All' and cutoff != 'All' and month != 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__CutOff=cutoff)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User_id=keyword)) & (Q(Batch__BMonth=month))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status == 'All' and cutoff != 'All' and month != 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(Batch__CutOff=cutoff)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(Batch__BMonth=month)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            #STATUS !ALL
            elif status != 'All' and cutoff == 'All' and month == 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(status=int(status))) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User_id=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status != 'All' and cutoff == 'All' and month == 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(status=int(status))) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status != 'All' and cutoff == 'All' and month != 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(status=int(status))) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User_id=keyword)) & (Q(Batch__BMonth=month))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status != 'All' and cutoff == 'All' and month != 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(status=int(status))) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(Batch__BMonth=month)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            ### FOR CUTOFF ###
            elif status != 'All' and cutoff != 'All' and month == 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(status=int(status))) & (Q(User__status='Active')) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(User_id=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status != 'All' and cutoff != 'All' and month == 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(status=int(status))) & (Q(User__status='Active')) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status != 'All' and cutoff != 'All' and month != 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(status=int(status))) & (Q(User__status='Active')) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(User_id=keyword)) & (Q(Batch__BMonth=month))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status != 'All' and cutoff != 'All' and month != 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(status=int(status))) & (Q(User__status='Active')) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(Batch__BMonth=month)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            #######
              
                
    ### FOR USER APPROVER ###
    else:
        ###  TEXT SEARCH  ###
        if searchtype == 'textsearch':
            if keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter(Q(User__Approver=currUser,User__status='Active') & Q(User_id=keyword)).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            else:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
        
        ###  PERIOD SEARCH  ###
        elif searchtype == 'periodsearch':
            if cutoff == 'All' and month == 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User_id=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif cutoff == 'All' and month == 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif cutoff == 'All' and month != 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User_id=keyword)) & (Q(Batch__BMonth=month))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif cutoff == 'All' and month != 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(Batch__BMonth=month)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
                
            ### FOR CUTOFF ###
            elif cutoff != 'All' and month == 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(User_id=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif cutoff != 'All' and month == 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif cutoff != 'All' and month != 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(User_id=keyword)) & (Q(Batch__BMonth=month))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif cutoff != 'All' and month != 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(Batch__BMonth=month)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
        ###  STATUS SEARCH  ###    
        elif searchtype == 'statussearch':
            #FOR STATUS
            ##########
            #STATUS ALL
            if status == 'All' and cutoff == 'All' and month == 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User_id=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status == 'All' and cutoff == 'All' and month == 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status == 'All' and cutoff == 'All' and month != 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(User_id=keyword)) & (Q(Batch__BMonth=month))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status == 'All' and cutoff == 'All' and month != 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__BYear=year)) & (Q(Batch__BMonth=month)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            ### FOR CUTOFF ###
            elif status == 'All' and cutoff != 'All' and month == 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(User_id=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status == 'All' and cutoff != 'All' and month == 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status == 'All' and cutoff != 'All' and month != 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(User_id=keyword)) & (Q(Batch__BMonth=month))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status == 'All' and cutoff != 'All' and month != 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(Batch__BMonth=month)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            #STATUS !ALL
            elif status != 'All' and cutoff == 'All' and month == 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(status=int(status))) & (Q(Batch__BYear=year)) & (Q(User_id=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status != 'All' and cutoff == 'All' and month == 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(status=int(status))) & (Q(Batch__BYear=year)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status != 'All' and cutoff == 'All' and month != 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(status=int(status))) & (Q(Batch__BYear=year)) & (Q(User_id=keyword)) & (Q(Batch__BMonth=month))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status != 'All' and cutoff == 'All' and month != 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(status=int(status))) & (Q(Batch__BYear=year)) & (Q(Batch__BMonth=month)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            ### FOR CUTOFF ###
            elif status != 'All' and cutoff != 'All' and month == 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(status=int(status))) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(User_id=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status != 'All' and cutoff != 'All' and month == 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(status=int(status))) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status != 'All' and cutoff != 'All' and month != 'All' and keyword.isdigit() == True:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(status=int(status))) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(User_id=keyword)) & (Q(Batch__BMonth=month))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            elif status != 'All' and cutoff != 'All' and month != 'All' and keyword.isdigit() == False:
                toapprove_list = Attendance.objects.values('User_id','User__LName','User__FName','User__MName','status','Batch_id','Batch__BMonth','Batch__BYear','Batch__CutOff','Batch__BMonthOrder').filter((Q(User__Approver=currUser)) & (Q(User__status='Active')) & (Q(status=int(status))) & (Q(Batch__CutOff=cutoff)) & (Q(Batch__BYear=year)) & (Q(Batch__BMonth=month)) & (Q(User__FName__contains=keyword)|Q(User__MName__contains=keyword)|Q(User__LName__contains=keyword))).exclude(status=0).distinct().order_by('-Batch__BYear','-Batch__BMonthOrder','-Batch__CutOff','-status','User__LName','User_id')[:100]
            #######
    
    ##### LIMIT TO 100 RESULTS - PAGINATION ON RESULT DISABLED ###
    '''
    paginator = Paginator(toapprove_list, 100) # Show 25 contacts per page
        
    page = request.GET.get('page')
    
    try:
        toapprove = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        toapprove = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        toapprove = paginator.page(paginator.num_pages)
    '''
    return render_to_response('erm_templates/DTR/approvalSearchResult.html',{'toapprove_list':toapprove_list,'currUser':currUser,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,'approver':approver,}, context_instance=RequestContext(request))

    

#************************************************************************#
#************************************************************************#
#************************************************************************#

def modal_approve(request):
    ##############################################################
    currUser = request.session['User.id']#session sa user here
    cu = User.objects.get(id=currUser)
    cu_isadmin = cu.isadmin
    ####################GET SUBMITTED INFO########################
    uid= int(request.POST.get('uid'))
    status = int(request.POST.get('status'))
    
    month = str(request.POST.get('month'))
    yearnum = int(request.POST.get('yearnum'))
    cutofftype = str(request.POST.get('cutofftype'))
    monthnum = list(calendar.month_name).index(month)
    
    month_max_days = calendar.monthrange(yearnum,monthnum)[1]
    
    ######################GET USER INFO###########################
    u = User.objects.get(id=uid)
    isadmin = u.isadmin
    fname = u.FName
    mname = u.MName
    lname = u.LName
    #branch = u.Branch
    
    try:
        approver = int(u.Approver)
    except:
        approver = None
    
    
    ###########################################
    ### *** GET BRANCH *** ###
    branch= User.objects.values_list('Branch',flat=True).filter(id=uid)[0]
    
    ###########################################
    ### *** GET DAY OFF *** ###
    DayOffSched = Schedule.objects.values_list('DayOff1','DayOff2').filter(User_id=uid,dateFrom__lte=datetime.date.today(),dateTo__gte=datetime.date.today()).order_by('-id')[0]  
    
    DayOffs = []
        
    for DayOff in DayOffSched:
        DayOffs.append(str(DayOff))
    ###########################################
    
    
    if cutofftype == '1st':
        dtstart = datetime.date(yearnum, monthnum, 1)
        dtend = datetime.date(yearnum, monthnum, 15)
    elif cutofftype == '2nd':
        dtstart = datetime.date(yearnum, monthnum, 16)
        dtend = datetime.date(yearnum, monthnum, month_max_days)
    
    toapprdata =  Attendance.objects.filter(User_id=uid,attendanceDate__gte=dtstart,attendanceDate__lte=dtend)
    
    
    return render_to_response('erm_templates/DTR/modal_approve.html',{'toapprdata':toapprdata,'status':status,'DayOffs':DayOffs,'currUser':currUser,'cu_isadmin':cu_isadmin,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,'approver':approver, 'dtstart':dtstart,'dtend':dtend,'uid':uid,'branch':branch,}, context_instance=RequestContext(request))


#************************************************************************#
#************************************************************************#
#************************************************************************#

def apprnoteprev(request):
#     ##############################################################
#     currUser = request.session['User.id']#session sa user here
#     ######################GET USER INFO###########################
#     u = User.objects.get(id=currUser)
#     isadmin = u.isadmin
#     fname = u.FName
#     mname = u.MName
#     lname = u.LName
#     approver = int(u.Approver)

    uid = int(request.POST.get('uid'))
    thedate = str(request.POST.get('thedate'))
    
    message = Attendance.objects.get(User_id=uid,attendanceDate=thedate)
    
    
    
    return render_to_response('erm_templates/DTR/apprnoteprev.html',{'message':message,}, context_instance=RequestContext(request))

#************************************************************************#
#************************************************************************#
#************************************************************************#

def appraction(request):

    uid = int(request.POST.get('uid'))
    dtstart = str(request.POST.get('start'))
    dtend = str(request.POST.get('end'))
    
    dtrtoapprove = Attendance.objects.filter(User_id=uid,attendanceDate__gte=dtstart,attendanceDate__lte=dtend)
    
    if 'Approve' in request.POST:
        for dtr in dtrtoapprove:
            dtr.status = 1
            dtr.save()
        msgNum = 11
        message = "DTR Approved!"
    elif 'Deny' in request.POST:
        for dtr in dtrtoapprove:
            dtr.status = 3
            dtr.save()
        msgNum = 12
        message = "DTR Sent Back!"
    
    
    return render_to_response('erm_templates/DTR/message_info.html',{'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))

#************************************************************************#
#************************************************************************#
#************************************************************************#


def changeSched(request):
    ##############################################################
    currUser = request.session['User.id']#session sa user here
    ######################GET USER INFO###########################
    u = User.objects.get(id=currUser)
    isadmin = u.isadmin
    fname = u.FName
    mname = u.MName
    lname = u.LName
    
    try:
        approver = int(u.Approver)
    except:
        approver = None
    ###########################################
    
    form = changeSchedForm()
    
    try:
        sched = Schedule.objects.values_list('Sked',flat=True).filter(User_id=currUser,dateFrom__lte=datetime.date.today(),dateTo__gte=datetime.date.today()).order_by('-id')[0]
        
        DayOffSched = Schedule.objects.values_list('DayOff1','DayOff2').filter(User_id=currUser,dateFrom__lte=datetime.date.today(),dateTo__gte=datetime.date.today()).order_by('-id')[0]  
        DayOffs = []
        
        for DayOff in DayOffSched:
            DayOffs.append(str(DayOff))
    
    except:
        message = "Your default schedule was not assigned.\n Please contact admin scheduler."
        return render_to_response('erm_templates/DTR/index.html', {'message':message,}, context_instance=RequestContext(request,))
    
    
    if sched == 'CWW':
        dayofffin = DayOffs[0] + ", " + DayOffs[1]
    elif sched == 'REG':
        dayofffin = DayOffs[0]
    elif sched == 'CWW - Doctor (5hrs per day)':
        dayofffin = DayOffs[0] + ", " + DayOffs[1]
    elif sched == 'CWW - Doctor (2 days a week)':
        dayofffin = DayOffs[0] + ", " + DayOffs[1]
        
    strdtToday = str(datetime.date.today())
    initialdate = datetime.datetime.strptime(strdtToday, "%Y-%m-%d")
    dtToday = initialdate.strftime("%m/%d/%Y")
    
    form.fields["currSched"].initial = sched + " - " + dayofffin
    form.fields["dateFrom"].initial = dtToday
    form.fields["dateTo"].initial = dtToday
        
        
        
    return render_to_response('erm_templates/DTR/changeSched.html',{'form':form, 'currUser':currUser,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,'approver':approver,}, context_instance=RequestContext(request))


def schedaction(request):
    ##############################################################
    currUser = int(request.session['User.id'])#session sa user here
    ######################GET USER INFO###########################
    
    u = User.objects.get(id=currUser)
    isadmin = u.isadmin
    fname = u.FName
    mname = u.MName
    lname = u.LName
    branch = u.Branch
    
    WorkSched = str(request.POST.get('WorkSched'))
    DayOff1 = str(request.POST.get('DayOff1'))
    DayOff2 = str(request.POST.get('DayOff2'))
    
    strdateFrom = str(request.POST.get('dateFrom'))
    dtdateFrom = datetime.datetime.strptime(strdateFrom, "%m/%d/%Y")
    dateFrom = dtdateFrom.strftime("%Y-%m-%d")
    
    strdateTo = str(request.POST.get('dateTo'))
    dtdateTo = datetime.datetime.strptime(strdateTo, "%m/%d/%Y")
    dateTo = dtdateTo.strftime("%Y-%m-%d")
    
    ###########################################
    if WorkSched == 'CWW':
        Sked = 'CWW'
        WorkingHours = 576
    elif WorkSched == 'REG':
        Sked = 'REG'
        DayOff2 = ''
        WorkingHours = 480
    elif WorkSched == 'CWD':
        Sked = 'CWW - Doctor (5hrs per day)'
        WorkingHours = 300
    elif WorkSched == 'CWD2':
        Sked = 'CWW - Doctor (2 days a week)'
        WorkingHours = 300
    
    ###########################################
    dtrentrylocklookup = Attendance.objects.filter(attendanceDate__gte=dtdateFrom, attendanceDate__lte=dtdateTo, User_id=currUser, status__in=[1,2])
    ###########################################
    if dtrentrylocklookup:
        msgNum = 24
        message = "Error! Locked DTR entry found in entered date range."
    else:
        Schedule(User_id=currUser,dateFrom=dateFrom,dateTo=dateTo,WorkingHours=WorkingHours,DayOff1=DayOff1,DayOff2=DayOff2,Sked=Sked).save()
    
        ### *** GET HOLIDAYS *** ###
        HoliDays = Holidays.objects.values_list('dateOfHoliday', flat=True).filter(schemeOfHoliday__in=('All',branch))
        #################################
    
        ### *** GET DAY OFF *** ###
        try:
            DayOffSched = Schedule.objects.values_list('DayOff1','DayOff2').filter(User_id=currUser,dateFrom__exact=dtdateFrom,dateTo__exact=dtdateTo).order_by('-id')[0]  
            DayOffs = []
            
            for DayOff in DayOffSched:
                DayOffs.append(str(DayOff))
        except:
            message = "Your default schedule was not assigned.\n Please contact admin scheduler."
            return render_to_response('erm_templates/DTR/index.html', {'message':message,}, context_instance=RequestContext(request,))
        ###########################################
        ### *** GET WORKING HOURS *** ###
        WorkTime = Schedule.objects.values_list('WorkingHours').filter(User_id=currUser,dateFrom__exact=dtdateFrom,dateTo__exact=dtdateTo).order_by('-id')[0][0]
        ###########################################
    
        attendrange = Attendance.objects.filter(attendanceDate__gte=dtdateFrom, attendanceDate__lte=dtdateTo, User_id=currUser)
    
        for day in attendrange:
            theday = day.attendanceDate.strftime("%a")         #formatted for dayoff comparison
            thedate =  day.attendanceDate.strftime("%Y-%m-%d") #formatted for mysql format purpose
            
            day.Leave_id = None
            if Sked == 'CWW - Doctor (2 days a week)':
                if theday in DayOffs: #gibaliktad ug gitanggal ang holidays kay special doc
                    #day.hoursWorked = int(WorkTime)#Fixed na ata nga iyang workinghours sa change same sa taas
                    day.hoursWorked = WorkingHours
                else:
                    day.hoursWorked = 0
            else:
                if theday in DayOffs or day.attendanceDate in HoliDays:
                    day.hoursWorked = 0
                else:
                    #day.hoursWorked = int(WorkTime)#Fixed na ata nga iyang workinghours sa change same sa taas
                    day.hoursWorked = WorkingHours
            day.save()
            Leave.objects.filter(User_id=currUser,DateofLeave=thedate).delete()
            
        msgNum = 14
        message = "Schedule successfully updated."    
     
    return render_to_response('erm_templates/DTR/message_info.html',{'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))



#************************************************************************#
#************************************************************************#
#************************************************************************#

def dtr1appr(request):
    ##############################################################
    currUser = int(request.session['User.id'])#session sa user here
    ######################GET USER INFO###########################
    
    monthnum = int(request.POST.get('hmonthnum'))
    yearnum = int(request.POST.get('hyearnum'))
    cutoffperiod = str(request.POST.get('hcutoff'))
    
    month_max_days = calendar.monthrange(yearnum,monthnum)[1]
        
    if cutoffperiod == '1st':
        dtstart = datetime.date(yearnum, monthnum, 1)
        dtend = datetime.date(yearnum, monthnum, 15)
        
    elif cutoffperiod == '2nd':
        dtstart = datetime.date(yearnum, monthnum, 16)
        dtend = datetime.date(yearnum, monthnum, month_max_days)
                
    
    dtrtopost = Attendance.objects.filter(User_id=currUser,attendanceDate__gte=dtstart,attendanceDate__lte=dtend)
    
    for dtr in dtrtopost:
        dtr.status = 1
        dtr.save()
    
    msgNum = 18
    message = "DTR Posted!"
    
    return render_to_response('erm_templates/DTR/message_info.html',{'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))


#************************************************************************#
#************************************************************************#
#************************************************************************#

def profile(request):
    try:
        ##############################################################
        currUser = request.session['User.id']#session sa user here
        ######################GET USER INFO###########################
        u = User.objects.get(id=currUser)
        isadmin = u.isadmin
        fname = u.FName
        mname = u.MName
        lname = u.LName
        division = u.Division
        dept = u.Dept
        branch = u.Branch
        sss = u.SSSNo
        pagibig = u.PagIBIGNo
        philhealth = u.PhilHealthNo
        
        ###########################
        ## FOR PHOTO ##
        try:
            photo = str(Images.objects.values_list('avatar',flat=True).filter(imguser=currUser)[0])
        except:
            photo = 'avatars/default_avatar.jpg'
        
        ###########################
        
        try:
            approver = int(u.Approver)
            approverdetails = User.objects.get(id=approver)
        except:
            approver = 'N/A'
        
        approvername = str(approverdetails.id) + ' - ' + str(approverdetails.LName) + ', ' + str(approverdetails.FName) + ' ' + str(approverdetails.MName)
        ###########################################
        
        form = ProfileForm()

        form.fields["uid"].initial = currUser
        form.fields["FName"].initial = fname
        form.fields["MName"].initial = mname
        form.fields["LName"].initial = lname
        form.fields["Approver"].initial = str(approverdetails.id) + ' - ' + str(approverdetails.LName) + ', ' + str(approverdetails.FName) + ' ' + str(approverdetails.MName) 
        
        form.fields["Division"].initial = division
        form.fields["Dept"].initial = dept
        form.fields["Branch"].initial = branch
        form.fields["SSSNo"].initial = sss
        form.fields["PagIBIGNo"].initial = pagibig
        form.fields["PhilHealthNo"].initial = philhealth
        
        
        
        formyear = xlsyearForm()
        
        formimg = UploadForm()
         
        return render_to_response('erm_templates/DTR/MyProfile.html',{'userinfo':u, 'photo':photo,'formimg':formimg,'formyear':formyear,'form':form, 'currUser':currUser,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,'approver':approver,'approvername': approvername,}, context_instance=RequestContext(request))
    except:
        return redirect('/ERM/index/')

#************************************************************************#
#************************************************************************#
#************************************************************************#

def periodreports(request):
    try:
        ##############################################################
        currUser = request.session['User.id']#session sa user here
        ######################GET USER INFO###########################
        u = User.objects.get(id=currUser)
        isadmin = u.isadmin
        fname = u.FName
        mname = u.MName
        lname = u.LName

        ###########################################
        ### *** DEFAULT DATE SETTINGS *** ###
        currentdaynum = int(datetime.date.today().day)
        
        if currentdaynum <= 15:
            currentmonthnum = int(datetime.date.today().month)
            currentyearnum = int(datetime.date.today().year)
            defmonthnum = currentmonthnum - 1 
            if currentmonthnum == 1:
                defyearnum = currentyearnum - 1
                defmonthnum = 12
            else:
                defyearnum = currentyearnum
            cutoff = '2nd'
        else:
            defmonthnum = int(datetime.date.today().month)
            defyearnum = int(datetime.date.today().year)
            cutoff = '1st'
        
        ############# FORM #############
        form = ReportsForm('id')
        form.fields["year"].initial = defyearnum
        form.fields["month"].initial = defmonthnum
        form.fields["cutoff"].initial = cutoff
        ########################################
        formyear = xlsyearForm()
        
        return render_to_response('erm_templates/DTR/reports.html',{'form':form,'formyear':formyear, 'currUser':currUser,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,}, context_instance=RequestContext(request))
    except:
        return redirect('/ERM/index/')

####################_-------------------------------##########

def changecmbgenby(request):
    arrangeby = request.POST.get('arrangeby')

    form = ReportsForm(arrangeby)
    return render_to_response('erm_templates/DTR/cmbgenby.html',{'form':form,}, context_instance=RequestContext(request))
    
######################################################################
######################################################################
######################################################################

def genreports(request):
         
    #try:
        withrem = request.POST.get('withrem')
        
        year = int(request.POST.get('year'))
        monthnum = int(request.POST.get('month'))
        cutoff = str(request.POST.get('cutoff'))
        
        printerctrl = int(request.POST.get('users'))
        
        #########################
        if cutoff == '1st':
            day = 25
            month = str(monthnum).zfill(2)
        elif cutoff == '2nd':
            day = 10
            month = str(monthnum + 1).zfill(2)
        
        if month == '13':
            summarydate = str(year) + '-01-' + str(day)
        else:
            summarydate = str(year) + '-' + month + '-' + str(day)
        
        #########################  
        payyear = year
        paymonth = monthnum
        if day == 10:    
            paymonth_max_days = calendar.monthrange(payyear,paymonth)[1]
            
            dtstart = str(payyear) + '-' + str(paymonth).zfill(2) + '-16' 
            dtend = str(payyear) + '-' + str(paymonth).zfill(2) + '-' + str(paymonth_max_days)
        
        elif day == 25:
            dtstart = str(payyear) + '-' + str(paymonth).zfill(2) + '-01'
            dtend = str(payyear) + '-' + str(paymonth).zfill(2) + '-15'
        
        
        book = xlwt.Workbook(encoding='ISO-8859-1', style_compression=1)
        #book = xlwt.Workbook()
        dtrsheet = book.add_sheet("DTR Summary")#Name of Excel Sheet
        
        if printerctrl == -1:
            allusers = User.objects.exclude(isadmin__in=[2,3,4]).order_by('LName')
        elif printerctrl == -2:
            allusers = User.objects.filter(status='Active').exclude(isadmin__in=[2,3,4]).order_by('LName')
        elif printerctrl == -3:
            allusers = User.objects.filter(status='Resigned/Retired').exclude(isadmin__in=[2,3,4]).order_by('LName')
        
        
        style = 'pattern: pattern solid, fore_colour yellow;'
        gstyle = 'pattern: pattern solid, fore_colour green;'
        
        dtrsheet.row(0).write(0,"PAYROLL DATE" , xlwt.Style.easyxf(style))
        dtrsheet.row(0).write(1,"ASSOCIATE ID" , xlwt.Style.easyxf(style))
        dtrsheet.row(0).write(2,"LAST NAME" , xlwt.Style.easyxf(style))
        dtrsheet.row(0).write(3,"FIRST NAME" , xlwt.Style.easyxf(style))
        dtrsheet.row(0).write(4,"MIDDLE NAME" , xlwt.Style.easyxf(style))
        dtrsheet.row(0).write(5,"HOURS WORKED" , xlwt.Style.easyxf(style))
        dtrsheet.row(0).write(6,"VL" , xlwt.Style.easyxf(style))
        dtrsheet.row(0).write(7,"SIL" , xlwt.Style.easyxf(style))
        dtrsheet.row(0).write(8,"SL" , xlwt.Style.easyxf(style))
        dtrsheet.row(0).write(9,"ABSENT" , xlwt.Style.easyxf(style))
        #dtrsheet.row(0).write(10,"NOTES" , xlwt.Style.easyxf(style))
        
        #dtrsheet.write_merge(0,0,11,12,"SAMPLE" , xlwt.Style.easyxf(style))
        
        ###########################################
        if withrem == 'YES':
            dtrsheet.row(0).write(11,"REMAINING VL" , xlwt.Style.easyxf(gstyle))
            dtrsheet.row(0).write(12,"REMAINING SIL" , xlwt.Style.easyxf(gstyle))
            dtrsheet.row(0).write(13,"REMAINING SL" , xlwt.Style.easyxf(gstyle))
        
        ###########################################
        
        for idx,user in enumerate(allusers):
            cellrow = dtrsheet.row(idx + 2)
            
            query = "select a.hours,sum(b.VacationL),sum(b.ServiceIncentiveL),sum(b.SickL),sum(b.AAbsent),a.notes from (SELECT User_id,SUM(hoursWorked) as hours, status, attendanceDate, remarkNotes as notes FROM `erm_attendance` WHERE status = 1 AND attendanceDate BETWEEN '" + dtstart + "' AND '" + dtend + "' group by User_id)a left join erm_leave b on b.user_id = a.user_id AND b.DateofLeave BETWEEN '" + dtstart + "' AND '" + dtend + "' WHERE a.user_id =" + str(user.id)
            
            conn = mysql.connector.connect(user='fpdypua', password ='fpdypua', host='localhost', database='dberm')
            cursor = conn.cursor()
            
            cursor.execute(query)
            dtrsummary = cursor.fetchall()
            
            cellrow.write(0,summarydate)
            cellrow.write(1,str(user.id))
            cellrow.write(2,str(user.LName))
            cellrow.write(3,str(user.FName))
            cellrow.write(4,str(user.MName))
            
            if dtrsummary[0][0] == None or dtrsummary[0][0] == '':
                cellrow.write(5,'---')
            else:
                cellrow.write(5, tohrs(dtrsummary[0][0]) + ':' + tomins(dtrsummary[0][0]))
            
            if dtrsummary[0][1] == None or dtrsummary[0][1] == '':
                cellrow.write(6,'---')
            else:
                cellrow.write(6, tohrs(dtrsummary[0][1]) + ':' + tomins(dtrsummary[0][1]))
            
            if dtrsummary[0][2] == None or dtrsummary[0][2] == '':
                cellrow.write(7,'---')
            else:
                cellrow.write(7, tohrs(dtrsummary[0][2]) + ':' + tomins(dtrsummary[0][2]))
            
            if dtrsummary[0][3] == None or dtrsummary[0][3] == '':
                cellrow.write(8,'---')
            else:
                cellrow.write(8, tohrs(dtrsummary[0][3]) + ':' + tomins(dtrsummary[0][3]))
            
            if dtrsummary[0][4] == None or dtrsummary[0][4] == '':
                cellrow.write(9,'---')
            else:
                cellrow.write(9, tohrs(dtrsummary[0][4]) + ':' + tomins(dtrsummary[0][4]))
            
            #cellrow.write(10, dtrsummary[0][5])
            '''
            if dtrsummary[0][5] == None or dtrsummary[0][5] == '':
                cellrow.write(10,'---')
            else:
                cellrow.write(10, tohrs(dtrsummary[0][5]) + ':' + tomins(dtrsummary[0][5]))
            '''
            
            
          
            ###########################################
            ## IF WITH LEAVE CREDITS
            if withrem == 'YES':
                currUser = user.id
                
                vlmin = 7200 - sum(Leave.objects.values_list('VacationL',flat=True).filter(User_id=currUser,DateofLeave__year=year))#add year to filter VL credit limit
                silmin = 4800 - sum(Leave.objects.values_list('ServiceIncentiveL',flat=True).filter(User_id=currUser,DateofLeave__year=year))#add year to filter SIL credit limit
                slmin = 2400 - sum(Leave.objects.values_list('SickL',flat=True).filter(User_id=currUser,DateofLeave__year=year))#add year to filter SL credit limit
                
                vlrem = tohrs(vlmin) + ':' + tomins(vlmin)
                silrem = tohrs(silmin) + ':' + tomins(silmin)
                slrem = tohrs(slmin) + ':' + tomins(slmin)
                
                cellrow.write(11, vlrem)
                cellrow.write(12, silrem)
                cellrow.write(13, slrem)
            ############################################
            cursor.close()
            
        randstr = my_random_string()
        
        #book.save('D:/Projects/workspace/SMS/ERM/static/dl/alluser/DTR_Summary(' + summarydate + ')' + randstr + '.xls')
        book.save('/var/www/html/SMS/ERM/static/dl/alluser/DTR_Summary(' + summarydate + ')' + randstr + '.xls')
        book.save('/var/www/html/nccc/static/dl/alluser/DTR_Summary(' + summarydate + ')' + randstr + '.xls')
        
        return HttpResponseRedirect('/static/dl/alluser/DTR_Summary(' + summarydate + ')' + randstr + '.xls')
        #file_name = open('/var/www/html/SMS/ERM/static/Reports/DTR_Summary(' + summarydate + ').xls','rw')
        #response = HttpResponse(content_type='application/force-download')
        #response = HttpResponse(file_name.read())
        #response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('DTR_Summary(' + summarydate + ').xls')
        #response['X-Sendfile'] = smart_str('/var/www/html/SMS/ERM/static/Reports/DTR_Summary(' + summarydate + ').xls')
        #return response
    
    #except:
        #msgNum = 16
        #message = "Opps! Something went wrong!"
        #return render_to_response('erm_templates/DTR/message_info.html',{'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
        
    

#####________________________________###############

#---------------------------------------------------------------------

### FUNCTIONS ###
def tohrs(totalminutes):
    return str(int(totalminutes/60));
 
def tomins(totalminutes):
    return str(totalminutes%60).zfill(2);
 
#----------------------------------------------------------------------
'''
class FitSheetWrapper(object):
    """Try to fit columns to max size of any entry.
    To use, wrap this around a worksheet returned from the 
    workbook's add_sheet method, like follows:

        sheet = FitSheetWrapper(book.add_sheet(sheet_name))

    The worksheet interface remains the same: this is a drop-in wrapper
    for auto-sizing columns.
    """
    def __init__(self, sheet):
        self.sheet = sheet
        self.widths = dict()

    def write(self, r, c, label='', *args, **kwargs):
        self.sheet.write(r, c, label, *args, **kwargs)
        width = arial10.fitwidth(label)
        if width > self.widths.get(c, 0):
            self.widths[c] = width
            self.sheet.col(c).width = width

    def __getattr__(self, attr):
        return getattr(self.sheet, attr)
   
''' 
   
#************************************************************************#
#************************************************************************#
#************************************************************************#


def viewrep(request):
    try:
        uid = request.POST.get('associate')
        
        ######################GET USER INFO###########################
        u = User.objects.get(id=uid)
        isadmin = u.isadmin
        fname = u.FName
        mname = u.MName
        lname = u.LName
        branch = u.Branch
        
        #####################################
        ### *** DATE SETTINGS FOR VIEW*** ###
        monthnum = int(request.POST.get('monthnum'))
        yearnum = int(request.POST.get('yearnum'))
        cutoffperiod = request.POST.get('cutofftype')
        ###########################################
        ### *** DETERMINE LAST DAY OF MONTH *** ###
        month_max_days = calendar.monthrange(yearnum,monthnum)[1]
        ####################################################
        ###########################################
        if cutoffperiod == '1st':
            datetogo = datetime.datetime.strptime(str(yearnum) + '-' + str(monthnum) + '-01','%Y-%m-%d').date() 
        elif cutoffperiod == '2nd':
            datetogo = datetime.datetime.strptime(str(yearnum) + '-' + str(monthnum) + '-16','%Y-%m-%d').date()
        
        ## NOT ALLOWED TO GO TO NEXT CUTOFF ##
        if datetogo > datetime.date.today():
            msgNum = 19
            message = "Cutoff has no existing data yet."
            return render_to_response('erm_templates/DTR/message_info.html',{'message':message,'msgNum':msgNum,},context_instance=RequestContext(request))
        else:
            ###########################################
            ###########################
            ### *** GET HOLIDAYS *** ###
            HoliDays = Holidays.objects.values_list('dateOfHoliday', flat=True).filter(schemeOfHoliday__in=('All',branch))
            #################################
            
            
            ### *** GET DAY OFF *** ###
            DayOffSched = Schedule.objects.values_list('DayOff1','DayOff2').filter(User_id=uid,dateFrom__lte=datetime.date.today(),dateTo__gte=datetime.date.today()).order_by('-id')[0]
            DayOffs = []
            
            for DayOff in DayOffSched:
                DayOffs.append(str(DayOff))
            #################################
            ### *** GET WORKING HOURS *** ###
            WorkTime = Schedule.objects.values_list('WorkingHours').filter(User_id=uid,dateFrom__lte=datetime.date.today(),dateTo__gte=datetime.date.today()).order_by('-id')[0][0]
            
           
            ###########################################
            ### *** IF THERE IS EXISTING RECORD *** ###DIRITSO NA 
            ### *** NUM OF HOURS 1st CUTOFF*** ###
            if cutoffperiod == '1st':
                dtrlist = Attendance.objects.filter(User_id=uid,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15))
                '''
                if dtrlist:
                    dtrstatus = Attendance.objects.values_list('status',flat=True).filter(User_id=uid,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15))[0]
                '''
                ############################################
                workTimeList = Attendance.objects.values_list('hoursWorked', flat=True).filter(User_id=uid,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15))
                VacationL = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=uid,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
                ServiceIncentiveL = sum(Leave.objects.values_list('ServiceIncentiveL', flat=True).filter(User_id=uid,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
                SickL = sum(Leave.objects.values_list('SickL', flat=True).filter(User_id=uid,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
                AAbsent = sum(Leave.objects.values_list('AAbsent', flat=True).filter(User_id=uid,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
                ###########################################
                
            ### *** NUM OF HOURS 2nd CUTOFF*** ###
            elif cutoffperiod == '2nd':
                dtrlist = Attendance.objects.filter(User_id=uid,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days))
                '''
                if dtrlist:
                    dtrstatus = Attendance.objects.values_list('status',flat=True).filter(User_id=uid,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days))[0]
                '''
                ############################################
                workTimeList = Attendance.objects.values_list('hoursWorked', flat=True).filter(User_id=uid,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days))
                ######################################
                ### *** NUM OF HOURS 2nd CUTOFF*** ###
                VacationL = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=uid,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
                ServiceIncentiveL = sum(Leave.objects.values_list('ServiceIncentiveL', flat=True).filter(User_id=uid,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
                SickL = sum(Leave.objects.values_list('SickL', flat=True).filter(User_id=uid,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
                AAbsent = sum(Leave.objects.values_list('AAbsent', flat=True).filter(User_id=uid,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
                ###########################################
                
            earnedtime = sum(workTimeList)
            monthname = calendar.month_name[monthnum]
                
            return render_to_response('erm_templates/DTR/viewrep.html', {'dtrlist': dtrlist, 'DayOffs': DayOffs, 'WorkTime':WorkTime, 'earnedtime':earnedtime, 'VacationL':VacationL,'ServiceIncentiveL':ServiceIncentiveL,'SickL':SickL,'AAbsent':AAbsent,'yearnum':yearnum,'monthnum':monthnum,'uid':uid,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,'branch':branch,'cutoffperiod':cutoffperiod,'monthname':monthname,}, context_instance=RequestContext(request))
    except:
        msgNum = 22
        message = "Chosen Associate has no Schedule!"
        return render_to_response('erm_templates/DTR/message_info.html',{'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
    
#************************************************************************#
#************************************************************************#
#************************************************************************#
        
def genindi(request):
        ######################
        currUser = request.POST.get('hassociate')
        ######################GET USER INFO###########################
        u = User.objects.get(id=currUser)
        isadmin = u.isadmin
        fname = u.FName
        mname = u.MName
        lname = u.LName
        branch = u.Branch
        
        name = str(lname) + ', ' + str(fname) + ' ' + str(mname)
        #####################################
        ### *** DATE SETTINGS FOR VIEW*** ###
        monthnum = int(request.POST.get('hmonthnum'))
        yearnum = int(request.POST.get('hyearnum'))
        cutoffperiod = request.POST.get('hcutoff')
        ###########################################
        #########################
        if cutoffperiod == '1st':
            day = 25
            month = str(monthnum).zfill(2)
        elif cutoffperiod == '2nd':
            day = 10
            month = str(monthnum + 1).zfill(2)
        
        if month == '13':
            summarydate = str(yearnum) + '-01-' + str(day)
        else:
            summarydate = str(yearnum) + '-' + month + '-' + str(day)
        
        ######################### 
        
        
        
        
        
        ### *** DETERMINE LAST DAY OF MONTH *** ###
        month_max_days = calendar.monthrange(yearnum,monthnum)[1]
        ####################################################
        ###########################################
        if cutoffperiod == '1st':
            datetogo = datetime.datetime.strptime(str(yearnum) + '-' + str(monthnum) + '-01','%Y-%m-%d').date() 
        elif cutoffperiod == '2nd':
            datetogo = datetime.datetime.strptime(str(yearnum) + '-' + str(monthnum) + '-16','%Y-%m-%d').date()
        
        
        
        ### *** GET HOLIDAYS *** ###
        HoliDays = Holidays.objects.values_list('dateOfHoliday', flat=True).filter(schemeOfHoliday__in=('All',branch))
        #################################
        
        
        ### *** GET DAY OFF *** ###
        DayOffSched = Schedule.objects.values_list('DayOff1','DayOff2').filter(User_id=currUser,dateFrom__lte=datetime.date.today(),dateTo__gte=datetime.date.today()).order_by('-id')[0]
        DayOffs = []
        
        for DayOff in DayOffSched:
            DayOffs.append(str(DayOff))
        #################################
        
        if cutoffperiod == '1st':
            dtrlist = Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15))
            dtrstatus = Attendance.objects.values_list('status',flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15))[0]
            ############################################
            workTimeList = Attendance.objects.values_list('hoursWorked', flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 1), attendanceDate__lte=datetime.date(yearnum, monthnum, 15))
            VacationL = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
            ServiceIncentiveL = sum(Leave.objects.values_list('ServiceIncentiveL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
            SickL = sum(Leave.objects.values_list('SickL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
            AAbsent = sum(Leave.objects.values_list('AAbsent', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 1), DateofLeave__lte=datetime.date(yearnum, monthnum, 15)))
            ###########################################
            
        ### *** NUM OF HOURS 2nd CUTOFF*** ###
        elif cutoffperiod == '2nd':
            dtrlist = Attendance.objects.filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days))
            dtrstatus = Attendance.objects.values_list('status',flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days))[0]
            ############################################
            workTimeList = Attendance.objects.values_list('hoursWorked', flat=True).filter(User_id=currUser,attendanceDate__gte=datetime.date(yearnum, monthnum, 16), attendanceDate__lte=datetime.date(yearnum, monthnum, month_max_days))
            ######################################
            ### *** NUM OF HOURS 2nd CUTOFF*** ###
            VacationL = sum(Leave.objects.values_list('VacationL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
            ServiceIncentiveL = sum(Leave.objects.values_list('ServiceIncentiveL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
            SickL = sum(Leave.objects.values_list('SickL', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
            AAbsent = sum(Leave.objects.values_list('AAbsent', flat=True).filter(User_id=currUser,DateofLeave__gte=datetime.date(yearnum, monthnum, 16), DateofLeave__lte=datetime.date(yearnum, monthnum, month_max_days)))
            ###########################################
            
        earnedtime = sum(workTimeList)
        monthname = calendar.month_name[monthnum]
        
        
        ##################
        ## BOOK WRITING ##
        ##################
        book = xlwt.Workbook(encoding='ISO-8859-1', style_compression=1)
        
        dtrsheet = book.add_sheet("Individual DTR Summary")#Name of Excel Sheet
        
        hstyle = 'font: colour red, bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;'
        tstyle = 'pattern: pattern solid, fore_colour red; align: horiz left;'
        nstyle = 'align: horiz left;'
        gstyle = 'font: colour green; align: horiz left;'
        btextstyle = 'font: colour blue; align: horiz left;'
        rtextstyle = 'font: colour red; align: horiz left;'
        
        
        dtrsheet.write_merge(0,0,0,5,"DTR SUMMARY", xlwt.Style.easyxf(hstyle))
        
        dtrsheet.write_merge(2,2,0,1,"Associate ID")
        dtrsheet.write_merge(2,2,2,5, currUser, xlwt.Style.easyxf(nstyle))
        
        dtrsheet.write_merge(3,3,0,1,"Associate Name")
        dtrsheet.write_merge(3,3,2,5, name, xlwt.Style.easyxf(nstyle))
        
        dtrsheet.write_merge(4,4,0,1,"Year")
        dtrsheet.write_merge(4,4,2,5, yearnum, xlwt.Style.easyxf(nstyle))
        
        dtrsheet.write_merge(5,5,0,1,"Month")
        dtrsheet.write_merge(5,5,2,5, monthname, xlwt.Style.easyxf(nstyle))
        
        dtrsheet.write_merge(6,6,0,1,"Cutoff Period")
        dtrsheet.write_merge(6,6,2,5, cutoffperiod, xlwt.Style.easyxf(nstyle))
        
        
        dtrsheet.row(8).write(0,"DATE" , xlwt.Style.easyxf(tstyle))
        dtrsheet.row(8).write(1,"HOURS WORKED" , xlwt.Style.easyxf(tstyle))
        dtrsheet.row(8).write(2,"VL" , xlwt.Style.easyxf(tstyle))
        dtrsheet.row(8).write(3,"SIL" , xlwt.Style.easyxf(tstyle))
        dtrsheet.row(8).write(4,"SL" , xlwt.Style.easyxf(tstyle))
        dtrsheet.row(8).write(5,"ABSENT" , xlwt.Style.easyxf(tstyle))
        dtrsheet.row(8).write(6,"NOTES" , xlwt.Style.easyxf(tstyle))
        
        
        ##################################
        for idx,dtr in enumerate(dtrlist):
            cellrow = dtrsheet.row(idx + 9)
            
            dt = dtr.attendanceDate.strftime('%b %d')
            
            seeholiday = Holidays.objects.values_list('dateOfHoliday', flat=True).filter(schemeOfHoliday__in=('All',branch)) 
            
            dis = str(dtr.attendanceDate.year) + "," + str(dtr.attendanceDate.month) + "," + str(dtr.attendanceDate.day)
            dayname = datetime.datetime.strptime(dis, '%Y,%m,%d').strftime('%a')
            
            
            if dayname in DayOffs and dtr.attendanceDate in seeholiday:
                hdesc = Holidays.objects.get(dateOfHoliday=dtr.attendanceDate).Description
                cellrow.write(0, dt)
                dtrsheet.write_merge(idx+9,idx+9,1,5, 'DAYOFF|' + hdesc)
            elif not dayname in DayOffs and dtr.attendanceDate in seeholiday:
                hdesc = Holidays.objects.get(dateOfHoliday=dtr.attendanceDate).Description
                cellrow.write(0, dt)
                dtrsheet.write_merge(idx+9,idx+9,1,5, hdesc)
            elif dayname in DayOffs and not dtr.attendanceDate in seeholiday:
                cellrow.write(0, dt)
                dtrsheet.write_merge(idx+9,idx+9,1,5, 'DAYOFF')
            else:
                if dtr.hoursWorked != 0:
                    hw = tohrs(dtr.hoursWorked) + ':' + tomins(dtr.hoursWorked)
                else:
                    hw = ''
                
                try:
                    if dtr.Leave.VacationL != 0:
                        vl = tohrs(dtr.Leave.VacationL) + ':' + tomins(dtr.Leave.VacationL)
                    else:
                        vl = ''
                except:
                    vl = ''
                
                try:
                    if dtr.Leave.ServiceIncentiveL != 0:
                        sil = tohrs(dtr.Leave.ServiceIncentiveL) + ':' + tomins(dtr.Leave.ServiceIncentiveL)
                    else:
                        sil = ''
                except:
                    sil = ''
                
                try:
                    if dtr.Leave.SickL != 0:
                        sl = tohrs(dtr.Leave.SickL) + ':' + tomins(dtr.Leave.SickL)
                    else:
                        sl = ''
                except:
                    sl = ''
                
                try:
                    if dtr.Leave.AAbsent != 0:
                        aa = tohrs(dtr.Leave.AAbsent) + ':' + tomins(dtr.Leave.AAbsent)
                    else:
                        aa = ''
                except:
                    aa = ''
                
                cellrow.write(0, dt)
                cellrow.write(1, hw)
                cellrow.write(2, vl)
                cellrow.write(3, sil)
                cellrow.write(4, sl)
                cellrow.write(5, aa)
            
            #write notes
            note = re.sub('\---------------------------------------------------------------------------------------$', '', str(dtr.remarkNotes))
            cellrow.write(6, note)
                
        '''
        dtrsheet.write_merge(26,26,0,1,"Leave Credits", xlwt.Style.easyxf(gstyle))
        
        dtrsheet.row(27).write(2,"Used", xlwt.Style.easyxf(btextstyle))
        dtrsheet.row(27).write(3,"Remaining", xlwt.Style.easyxf(btextstyle))
        ################
        dtrsheet.row(28).write(1,"VL")
        dtrsheet.row(29).write(1,"SIL")
        dtrsheet.row(30).write(1,"SL")
        ################
        vlused = tohrs(VacationL) + ':' + tomins(VacationL)
        silused = tohrs(ServiceIncentiveL) + ':' + tomins(ServiceIncentiveL)
        slused = tohrs(SickL) + ':' + tomins(SickL)
        
        dtrsheet.row(28).write(2, vlused)
        dtrsheet.row(29).write(2, silused)
        dtrsheet.row(30).write(2, slused)
        ################
        vlmin = 7200 - sum(Leave.objects.values_list('VacationL',flat=True).filter(User_id=currUser,DateofLeave__year=yearnum))#add year to filter VL credit limit
        silmin = 4800 - sum(Leave.objects.values_list('ServiceIncentiveL',flat=True).filter(User_id=currUser,DateofLeave__year=yearnum))#add year to filter SIL credit limit
        slmin = 2400 - sum(Leave.objects.values_list('SickL',flat=True).filter(User_id=currUser,DateofLeave__year=yearnum))#add year to filter SL credit limit
        
        vlrem = tohrs(vlmin) + ':' + tomins(vlmin)
        silrem = tohrs(silmin) + ':' + tomins(silmin)
        slrem = tohrs(slmin) + ':' + tomins(slmin)
        
        dtrsheet.row(28).write(3, vlrem)
        dtrsheet.row(29).write(3, silrem)
        dtrsheet.row(30).write(3, slrem)
        '''
        ################
        dtrsheet.write_merge(26,26,0,1,"Summary", xlwt.Style.easyxf(gstyle))
        
        dtrsheet.row(27).write(4,"No. of Hours", xlwt.Style.easyxf(btextstyle))
        ################
        dtrsheet.write_merge(28,28,0,3,"WORKED HOURS")
        dtrsheet.write_merge(29,29,0,3,"VACATION LEAVE")
        dtrsheet.write_merge(30,30,0,3,"SERVICE INCENTIVE LEAVE")
        dtrsheet.write_merge(31,31,0,3,"SICK LEAVE")
        dtrsheet.write_merge(32,32,0,3,"ABSENT HOURS")
        ################
        
        hwtime = tohrs(earnedtime) + ':' + tomins(earnedtime)
        vlused = tohrs(VacationL) + ':' + tomins(VacationL)
        silused = tohrs(ServiceIncentiveL) + ':' + tomins(ServiceIncentiveL)
        slused = tohrs(SickL) + ':' + tomins(SickL)
        aa = tohrs(AAbsent) + ':' + tomins(AAbsent)
        
        dtrsheet.row(28).write(4, hwtime)
        dtrsheet.row(29).write(4, vlused)
        dtrsheet.row(30).write(4, silused)
        dtrsheet.row(31).write(4, slused)
        dtrsheet.row(32).write(4, aa, xlwt.Style.easyxf(rtextstyle))
        ################
        
        randstr = my_random_string()
        #book.save('D:/Projects/workspace/SMS/ERM/static/dl/individual/' + currUser + 'DTR_Summary(' + summarydate + ')' + randstr + '.xls')
        book.save('/var/www/html/nccc/static/dl/individual/' + currUser + 'DTR_Summary(' + summarydate + ')' + randstr + '.xls')
        
        return HttpResponseRedirect('/static/dl/individual/' + currUser + 'DTR_Summary(' + summarydate + ')' + randstr + '.xls')
        

#************************************************************************#
#************************************************************************#
#************************************************************************#

def assocpms(request):
    try:
        ##############################################################
        currUser = request.session['User.id']#session sa user here
        ######################GET USER INFO###########################
        u = User.objects.get(id=currUser)
        isadmin = u.isadmin
        fname = u.FName
        mname = u.MName
        lname = u.LName

        allpms_list = PMS.objects.filter(User_id__Approver__exact=currUser,User__status='Active').order_by('-pmsYear')
        #form = PMSForm(currUser)
        formyear = xlsyearForm()
        
        
        paginator = Paginator(allpms_list, 20) # Show 25 contacts per page
    
        page = request.GET.get('page')
        
        try:
            allpms = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            allpms = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            allpms = paginator.page(paginator.num_pages)
    
        
        return render_to_response('erm_templates/DTR/assocpms.html',{'allpms_list':allpms_list,'allpms':allpms,'formyear':formyear,'currUser':currUser,'isadmin':isadmin,'fname':fname,'mname':mname,'lname':lname,}, context_instance=RequestContext(request))        
    except:
        return redirect('/ERM/index/')


def pmsadd(request):
    '''
    pmsuser = request.POST.get('pmsuser')
    pmsyear = request.POST.get('pmsyear')
    pmsscore = request.POST.get('pmsscore')
    
    checkdb = PMS.objects.filter(User_id=pmsuser,pmsYear=pmsyear)
    
    if checkdb:
        return HttpResponse('This user has been rated already this year.')
    else:
        PMS(User_id=pmsuser,pmsYear=pmsyear,pmsScore=pmsscore,resCol1=None,resCol2=None).save()
        return HttpResponse('PMS added.')
    '''
    try:
        currUser = request.session['User.id']#session sa user here
        pmsyear = datetime.date.today().year
        
        allunders = User.objects.filter(Approver__exact=currUser,status='Active')
        
        for user in allunders:
            checkdb = PMS.objects.filter(User_id=user.id,pmsYear=pmsyear)
            if not checkdb: 
                PMS(User_id=user.id,pmsYear=pmsyear,pmsScore=0,pmsStatus='Unposted',resCol1=None,resCol2=None).save()
        return HttpResponse('PMS added.')
    except:
        return HttpResponse('Error! Something went wrong.')
   
#************************************************************************#
#************************************************************************#
#************************************************************************#

def postchecked(request):
    try:
        allid = request.POST.getlist('chkentries[id][]')
        allscores = request.POST.getlist('chkentries[scores][]')
        
        
        for ctr,id in enumerate(allid):
            postid = PMS.objects.get(id=int(id))        
            postid.pmsStatus = 'Posted'
            postid.pmsScore = allscores[ctr]
            postid.save()
          
        return HttpResponse('Posting Successful.')
    except:
        return HttpResponse('Error.')
#************************************************************************#
#************************************************************************#
#************************************************************************#


def outputtoxls(request): 
    try:
        currUser = request.session['User.id']#session sa user here
        u = User.objects.get(id=currUser)
        isadmin = u.isadmin
        
        year = int(request.POST.get('xlsyear'))
        
        book = xlwt.Workbook(encoding='ISO-8859-1', style_compression=1)
        
        dtrsheet = book.add_sheet("PMS Sheet")#Name of Excel Sheet
        
        if isadmin == 2 or isadmin == 3 or isadmin == 4:
            alldata = PMS.objects.filter(pmsYear=year,pmsStatus='Posted')
        else:
            alldata = PMS.objects.filter(pmsYear=year,pmsStatus='Posted',User_id__Approver__exact=currUser)
        
        style = 'pattern: pattern solid, fore_colour yellow;'
        gstyle = 'pattern: pattern solid, fore_colour green;'
        
        dtrsheet.row(0).write(0,"YEAR" , xlwt.Style.easyxf(style))
        dtrsheet.row(0).write(1,year , xlwt.Style.easyxf(style))
        
        dtrsheet.row(2).write(0,"ID" , xlwt.Style.easyxf(gstyle))
        dtrsheet.row(2).write(1,"Last Name" , xlwt.Style.easyxf(gstyle))
        dtrsheet.row(2).write(2,"First Name" , xlwt.Style.easyxf(gstyle))
        dtrsheet.row(2).write(3,"Middle Name" , xlwt.Style.easyxf(gstyle))
        dtrsheet.row(2).write(4,"PMS Score" , xlwt.Style.easyxf(gstyle))
        
        ###########################################
        
        for rnum,data in enumerate(alldata):
            cellrow = dtrsheet.row(rnum + 3)
            
            cellrow.write(0,data.User_id)
            cellrow.write(1,str(data.User.LName))
            cellrow.write(2,str(data.User.FName))
            cellrow.write(3,str(data.User.MName))
            cellrow.write(4,str(data.pmsScore))
            
            
        ###########################################
            
            
        randstr = my_random_string()
        
        #book.save('D:/Projects/workspace/SMS/ERM/static/dl/pms-xls/PMS' + str(year) + '-' + str(currUser) + '(' + randstr + ').xls')
        book.save('/var/www/html/nccc/static/dl/pms-xls/PMS' + str(year) + '-' + str(currUser) + '(' + randstr + ').xls')
        
        return HttpResponseRedirect('/static/dl/pms-xls/PMS' + str(year) + '-' + str(currUser) + '(' + randstr + ').xls')
    
        #data = {}
        #data['currUser'] = currUser
        #data['randstr'] = randstr
        #return HttpResponse(json.dumps(data), content_type = "application/json")
    
    except:
        msgNum = 20
        message = "Oops! Something went wrong!"
        return render_to_response('erm_templates/DTR/message_info.html',{'isadmin':isadmin,'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
    
    








def upload_avatar(request):
    
    currUser = request.session['User.id']#session sa user here
    
    u = User.objects.get(id=currUser)
    # Handle file upload
    if request.method == 'POST':
        formimg = UploadForm(request.POST, request.FILES)
        
        if formimg.is_valid():
            ## DELETE old picture
            img = Images.objects.filter(imguser_id=currUser)
            img.delete()
            
            ## INSERT IMAGE TO DB BLOB
            newimage = Images(avatar = request.FILES['avatar'],imguser_id=currUser)
            newimage.save()
            
            # Redirect to the document list after POST
            return redirect('/ERM/profile/')

    return redirect('/ERM/profile/')




















def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

#************************************************************************#
#************************************************************************#
#************************************************************************#

def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.

#************************************************************************#
#************************************************************************#
#************************************************************************#
