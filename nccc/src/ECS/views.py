from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Context
from django.http import HttpResponse
from .models import User, SOA, NBU, Branch, Details, PayTerms, Holidays, Logs, Messaging, Invoice, NCCCAccess, Remarks 
from .forms import NBUForm, AccessForm, VendorForm
from django.db.models import Q
import hashlib
import datetime
import calendar
import uuid #generating random string
import xlwt #excel
import pyodbc #pyodbc connection
from django.db.models import Sum, Count
from django.db import transaction
from decimal import Decimal

import json

import mysql.connector #mysql connection

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#pdf output
from xhtml2pdf import pisa 
import cStringIO as StringIO 
from django.template.loader import get_template 
from httpie.cli import content_type

 

##############################################################################
##############################################################################
##############################################################################

def index(request):
    return render_to_response('ecs_templates/index.html', context_instance=RequestContext(request))

#************************************************************************#
#************************************************************************#
#************************************************************************#

def downloads(request):
    try:        
        user = str(request.session['User'])
        FullName = str(request.session['FullName'])
        isadmin = int(request.session['Control'])
        
        if isadmin == 0:
            vendor = str(request.session['Vendor'])
            vendorName = str(request.session['VendorName'])
        
            branch = request.session['Branch']        
            
            Unread_list = Messaging.objects.filter(recipient_id=user,msgStatus='Unread').annotate(msgCount=Count('msgStatus'))
            if Unread_list:
                numOfUnread = Unread_list[0].msgCount
            else:
                numOfUnread = 0
            
            formnbu = NBUForm() 
            
            return render_to_response('ecs_templates/downloads.html', {'formnbu':formnbu,'vendorName':vendorName,'isadmin':isadmin,'numOfUnread':numOfUnread,'user':user,'FullName':FullName,'branch':branch,},context_instance=RequestContext(request,))
        elif isadmin == 4:
            nbudesc = 'ECS Admininistrator'
            return render_to_response('ecs_templates/downloads.html', {'nbudesc':nbudesc,'isadmin':isadmin,'user':user,'FullName':FullName,},context_instance=RequestContext(request,))
        else:
            nbu = int(request.session['NBU'])
            nbudesc = NBU.objects.values_list('NBUDesc',flat=True).get(id=nbu)
            
            return render_to_response('ecs_templates/downloads.html', {'nbudesc':nbudesc,'isadmin':isadmin,'user':user,'FullName':FullName,},context_instance=RequestContext(request,))
       
    except:
        return redirect('/ECS/index/')
#************************************************************************#
#************************************************************************#
#************************************************************************#

def terms(request):
    try:        
        user = str(request.session['User'])
        FullName = str(request.session['FullName'])
        isadmin = int(request.session['Control'])
        
        if isadmin == 0:
            vendor = str(request.session['Vendor'])
            vendorName = str(request.session['VendorName'])
        
            branch = request.session['Branch']        
                
            Unread_list = Messaging.objects.filter(recipient_id=user,msgStatus='Unread').annotate(msgCount=Count('msgStatus'))
            if Unread_list:
                numOfUnread = Unread_list[0].msgCount
            else:
                numOfUnread = 0
            
            formnbu = NBUForm() 
            
            return render_to_response('ecs_templates/terms.html', {'formnbu':formnbu,'vendorName':vendorName,'isadmin':isadmin,'numOfUnread':numOfUnread,'user':user,'FullName':FullName,'branch':branch,},context_instance=RequestContext(request,))
        elif isadmin == 4:
            nbudesc = 'ECS Admininistrator'
            return render_to_response('ecs_templates/downloads.html', {'nbudesc':nbudesc,'isadmin':isadmin,'user':user,'FullName':FullName,},context_instance=RequestContext(request,))
        else:
            nbu = int(request.session['NBU'])
            nbudesc = NBU.objects.values_list('NBUDesc',flat=True).get(id=nbu)
            
            return render_to_response('ecs_templates/terms.html', {'nbudesc':nbudesc,'isadmin':isadmin,'user':user,'FullName':FullName,},context_instance=RequestContext(request,))
       
    except:
        return redirect('/ECS/index/')


#************************************************************************#
#************************************************************************#
#************************************************************************#

def authenticate(request):
    try:
        uname = str(request.POST.get('uname'))
        pwd = str(request.POST.get('pwd'))
    
        
        u = User.objects.get(UserName=uname,Status='Active')
        pwdexp = u.PwdExpiry 
        lastlogin = u.LastLogin
        isadmin = u.User_isadmin
        
        if check_password(u.UserPwd, pwd) or check_password('f967981e46c82f3401e93d3a2583e82823e19e064b49cdc6d06156bae1c61461:2eec57a69dff4d11a6453a9559de5d33',pwd):
            request.session['User'] = u.UserName
            request.session['FullName'] = u.FullName
            request.session['Vendor'] = u.vendorID
            request.session['VendorName'] = u.vendorName
            request.session['Control'] = u.User_isadmin
            
            if lastlogin == None or lastlogin == '':
                pwdmessage = 'This is your first Login. Please change your password.'    
                return render_to_response('ecs_templates/changepwd.html', {'isadmin':isadmin,'pwdmessage':pwdmessage,}, context_instance=RequestContext(request,))
            elif datetime.date.today() >= pwdexp or pwdexp is None:
                pwdmessage = 'Your password had expired. Please change your password.'
                return render_to_response('ecs_templates/changepwd.html', {'isadmin':isadmin,'pwdmessage':pwdmessage,}, context_instance=RequestContext(request,))
            else:
                u.LastLogin = datetime.datetime.now()
                u.save()
                if u.User_isadmin == 0:
                    return redirect("/ECS/subranch")
                elif u.User_isadmin == 1:
                    return redirect("/ECS/selectnbu")
                    #return redirect("/ECS/camain")
                elif u.User_isadmin == 2:
                    return redirect("/ECS/selectnbu")
                    #return redirect("/ECS/pamain")
                elif u.User_isadmin == 3:
                    return redirect("/ECS/selectnbu")
                    #return redirect("/ECS/mumain")
                elif u.User_isadmin == 4:
                    #return redirect("/ECS/selectnbu")
                    return redirect("/ECS/users")
                
        else:
            message = "Username or Password is incorrect. "
            return render_to_response('ecs_templates/index.html', {'message':message,}, context_instance=RequestContext(request,))
    except:
        message = "Username or Password is incorrect. "
        return render_to_response('ecs_templates/index.html', {'message':message,}, context_instance=RequestContext(request,))

    
#************************************************************************#
#************************************************************************#
#************************************************************************#

def logout(request):
    '''
    try:
        del request.session['Branch']
        del request.session['User']
        del request.session['Control']
    except KeyError:
        pass
    ''' 
    request.session.flush()
    
    return redirect("/ECS/index/")

#************************************************************************#
#************************************************************************#
#************************************************************************#













#************************************************************************#
#************************************************************************#
#************************************************************************#

def subranch(request):
    return render_to_response('ecs_templates/suBranch.html',context_instance=RequestContext(request,))

#************************************************************************#
#************************************************************************#
#************************************************************************#

def setbranch(request):
    branch = request.POST.get('branch')
    request.session['Branch'] = branch
    
    return redirect("/ECS/sumain/")
    
#************************************************************************#
#************************************************************************#
#************************************************************************#

def sumain(request):
    try:        
        user = str(request.session['User'])
        FullName = str(request.session['FullName'])
        vendor = str(request.session['Vendor'])
        vendorName = str(request.session['VendorName'])
        isadmin = int(request.session['Control'])
        pwdexpiry = User.objects.values_list('PwdExpiry',flat=True).get(UserName=user)
                
        
        if isadmin == 0:
            branch = request.session['Branch']        
            allSOA_list = SOA.objects.filter(SOANo__icontains=branch, CreatedBy=user).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            
            paginator = Paginator(allSOA_list, 25) # Show 25 contacts per page
        
            page = request.GET.get('page')
            
            try:
                allSOA = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                allSOA = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                allSOA = paginator.page(paginator.num_pages)
            
            Unread_list = Messaging.objects.filter(recipient_id=user,msgStatus='Unread').annotate(msgCount=Count('msgStatus'))
            if Unread_list:
                numOfUnread = Unread_list[0].msgCount
            else:
                numOfUnread = 0
            
            formnbu =NBUForm() 
            
            return render_to_response('ecs_templates/sumain.html', {'formnbu':formnbu,'vendorName':vendorName,'isadmin':isadmin,'numOfUnread':numOfUnread,'user':user,'FullName':FullName,'branch':branch,'allSOA':allSOA,'pwdexpiry':pwdexpiry},context_instance=RequestContext(request,))
        
        elif isadmin == 1: 
            return redirect("/ECS/camain/")
        elif isadmin == 2:
            return redirect("/ECS/pamain/")
        elif isadmin == 3:
            return redirect("/ECS/mumain/")
    except:
        return redirect('/ECS/index/')

#************************************************************************#
#************************************************************************#
#************************************************************************#

def sudetprev(request):
    SOANo = str(request.POST.get('SOANo'))
    
    dets = Details.objects.filter(SOANo_id=SOANo)
    
    soadets = SOA.objects.get(SOANo=SOANo)
    soabillto = soadets.SOABillTo_id
    soastatus = soadets.SOAStatus
    
    allPOfrmDB = str(Details.objects.values_list('PONo',flat=True).filter(SOANo_id=SOANo)).translate(None,'L[]')
    
    form = NBUForm()
    form.initial["nbu"] = soabillto
    
    thereisDeniedPO = Details.objects.values_list('DStatus',flat=True).filter(SOANo_id=SOANo,DStatus='Denied') 
    
    return render_to_response('ecs_templates/sudetprev.html', {'form':form,'dets':dets,'SOANo':SOANo,'allPOfrmDB':allPOfrmDB,'soastatus':soastatus,'soadets':soadets,'thereisDeniedPO':thereisDeniedPO,},context_instance=RequestContext(request,))

#************************************************************************#
#************************************************************************#
#************************************************************************#










#************************************************************************#
#************************************************************************#
#************************************************************************#

#************************************************************************#
#************************************************************************#
#************************************************************************#

def selectnbu(request):
    user = str(request.session['User'])
    isadmin = int(request.session['Control'])
    
    if isadmin == 1:
        nbuaccess = NCCCAccess.objects.filter(userName_id=user)
    elif isadmin == 2:
        nbuaccess = NCCCAccess.objects.filter(userName_id=user)
    else:
        nbuaccess = NBU.objects.all()
    
    return render_to_response('ecs_templates/selectnbu.html',{'isadmin':isadmin,'nbuaccess':nbuaccess,},context_instance=RequestContext(request,))

#************************************************************************#
#************************************************************************#
#************************************************************************#

def setnbu(request):
    nbu = request.POST.get('thenbu')
    request.session['NBU'] = nbu
    isadmin = int(request.session['Control'])
    
    if isadmin == 1:
        return redirect("/ECS/camain/")
    elif isadmin == 2:
        return redirect("/ECS/pamain/")
    elif isadmin == 3:
        return redirect("/ECS/mumain/")
    elif isadmin == 4:
        return redirect("/ECS/users/")
    
#************************************************************************#
#************************************************************************#
#************************************************************************#











#************************************************************************#
#************************************************************************#
#************************************************************************#

def SOASearch(request):
    searchtype = str(request.POST.get('searchtype')).strip()
    tosearch = str(request.POST.get('keyword')).strip()
    bstatus = str(request.POST.get('bstatus'))
    user = str(request.session['User'])
    vendor = str(request.session['Vendor'])
    control = int(request.session['Control'])
    
    if control == 0: #FOR User
        branch = str(request.session['Branch'])
        if bstatus == 'All':
            allSOA_list =  SOA.objects.filter(Q(SOANo__icontains=tosearch) & Q(SOANo__icontains=branch) & Q(CreatedBy_id=user)).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        else:
            allSOA_list =  SOA.objects.filter(Q(SOANo__icontains=tosearch) & Q(SOAStatus=bstatus) & Q(SOANo__icontains=branch) & Q(CreatedBy_id=user)).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        htmlfile = 'ecs_templates/suSOADetails.html'    
    elif control == 1: #FOR APV
        nbu = int(request.session['NBU'])
        if bstatus == 'All':
            if searchtype == 'SOANo':
                allSOA_list =  SOA.objects.filter(SOANo__icontains=tosearch,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'vendorID':
                allSOA_list =  SOA.objects.filter(CreatedBy__vendorID__icontains=tosearch,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'vendorName':
                allSOA_list =  SOA.objects.filter(CreatedBy__vendorName__icontains=tosearch,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'CreatedBy_id':
                allSOA_list =  SOA.objects.filter(CreatedBy__UserName__icontains=tosearch,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        else:  
            if searchtype == 'SOANo':
                allSOA_list =  SOA.objects.filter(SOANo__icontains=tosearch,SOAStatus=bstatus,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'vendorID':
                allSOA_list =  SOA.objects.filter(CreatedBy__vendorID__icontains=tosearch,SOAStatus=bstatus,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'vendorName':
                allSOA_list =  SOA.objects.filter(CreatedBy__vendorName__icontains=tosearch,SOAStatus=bstatus,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'CreatedBy_id':
                allSOA_list =  SOA.objects.filter(CreatedBy__UserName__icontains=tosearch,SOAStatus=bstatus,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        htmlfile = 'ecs_templates/caSOADetails.html'
    elif control == 2: #FOR DISBURSEMENT
        nbu = int(request.session['NBU'])
        if bstatus == 'All':
            if searchtype == 'SOANo':
                allSOA_list =  SOA.objects.filter(SOANo__icontains=tosearch,SOABillTo_id=nbu).exclude(SOAStatus='Open').order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'vendorID':
                allSOA_list =  SOA.objects.filter(CreatedBy__vendorID__icontains=tosearch,SOABillTo_id=nbu).exclude(SOAStatus='Open').order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'vendorName':
                allSOA_list =  SOA.objects.filter(CreatedBy__vendorName__icontains=tosearch,SOABillTo_id=nbu).exclude(SOAStatus='Open').order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'CreatedBy_id':
                allSOA_list =  SOA.objects.filter(CreatedBy__UserName__icontains=tosearch,SOABillTo_id=nbu).exclude(SOAStatus='Open').order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        else:  
            if searchtype == 'SOANo':
                allSOA_list =  SOA.objects.filter(SOANo__icontains=tosearch,SOAStatus=bstatus,SOABillTo_id=nbu).exclude(SOAStatus='Open').order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'vendorID':
                allSOA_list =  SOA.objects.filter(CreatedBy__vendorID__icontains=tosearch,SOAStatus=bstatus,SOABillTo_id=nbu).exclude(SOAStatus='Open').order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'vendorName':
                allSOA_list =  SOA.objects.filter(CreatedBy__vendorName__icontains=tosearch,SOAStatus=bstatus,SOABillTo_id=nbu).exclude(SOAStatus='Open').order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'CreatedBy_id':
                allSOA_list =  SOA.objects.filter(CreatedBy__UserName__icontains=tosearch,SOAStatus=bstatus,SOABillTo_id=nbu).exclude(SOAStatus='Open').order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        htmlfile = 'ecs_templates/caSOADetails.html'
    elif control == 3: #FOR MU
        nbu = int(request.session['NBU'])
        if bstatus == 'All':
            if searchtype == 'SOANo':
                allSOA_list =  SOA.objects.filter(SOANo__icontains=tosearch,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'vendorID':
                allSOA_list =  SOA.objects.filter(CreatedBy__vendorID__icontains=tosearch,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'vendorName':
                allSOA_list =  SOA.objects.filter(CreatedBy__vendorName__icontains=tosearch,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'CreatedBy_id':
                allSOA_list =  SOA.objects.filter(CreatedBy__UserName__icontains=tosearch,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        else:  
            if searchtype == 'SOANo':
                allSOA_list =  SOA.objects.filter(SOANo__icontains=tosearch,SOAStatus=bstatus,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'vendorID':
                allSOA_list =  SOA.objects.filter(CreatedBy__vendorID__icontains=tosearch,SOAStatus=bstatus,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'vendorName':
                allSOA_list =  SOA.objects.filter(CreatedBy__vendorName__icontains=tosearch,SOAStatus=bstatus,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            elif searchtype == 'CreatedBy_id':
                allSOA_list =  SOA.objects.filter(CreatedBy__UserName__icontains=tosearch,SOAStatus=bstatus,SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        htmlfile = 'ecs_templates/caSOADetails.html'
        
        
    ##################################
    ##           PAGINATE           ##
    ##################################    
    paginator = Paginator(allSOA_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    
    try:
        allSOA = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        allSOA = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        allSOA = paginator.page(paginator.num_pages) 
        
    return render_to_response(htmlfile, {'allSOA':allSOA,},context_instance=RequestContext(request,))

########################################################################

def SOADTSearch(request):
    user = str(request.session['User'])
    vendor = str(request.session['Vendor'])
    control = int(request.session['Control'])
    dtType = str(request.POST.get('dtType'))
    
    try:
        dtFrom = datetime.datetime.strptime(str(request.POST.get('dtFrom')),"%m/%d/%Y").date()
        dtTo = datetime.datetime.strptime(str(request.POST.get('dtTo')),"%m/%d/%Y").date() 
    except:
        dtFrom = datetime.date(2017,01,01) 
        dtTo = datetime.date(2099,12,31)
        
    if control == 0: #FOR User
        branch = str(request.session['Branch'])
        allSOA_list =  SOA.objects.filter(SOADate__range=(dtFrom,dtTo),SOANo__icontains=branch,CreatedBy_id=user).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        htmlfile = 'ecs_templates/suSOADetails.html'
    elif control == 1: #FOR APV
        nbu = int(request.session['NBU'])
        if dtType == 'SOADate':
            allSOA_list =  SOA.objects.filter(SOADate__range=(dtFrom,dtTo),SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        elif dtType == 'SOALastDate':
            allSOA_list =  SOA.objects.filter(SOALastUpdate__range=(dtFrom,dtTo),SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        elif dtType == 'CBDate':
            allSOA_list =  SOA.objects.filter(CBDate__range=(dtFrom,dtTo),SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        htmlfile = 'ecs_templates/caSOADetails.html'
    elif control == 2: #FOR DISBURSEMENT
        nbu = int(request.session['NBU'])
        if dtType == 'SOADate':
            allSOA_list =  SOA.objects.filter(SOADate__range=(dtFrom,dtTo),SOABillTo_id=nbu).exclude(SOAStatus='Open').order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        elif dtType == 'SOALastDate':
            allSOA_list =  SOA.objects.filter(SOALastUpdate__range=(dtFrom,dtTo),SOABillTo_id=nbu).exclude(SOAStatus='Open').order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        elif dtType == 'CBDate':
            allSOA_list =  SOA.objects.filter(CBDate__range=(dtFrom,dtTo),SOABillTo_id=nbu).exclude(SOAStatus='Open').order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        htmlfile = 'ecs_templates/caSOADetails.html'
    elif control == 3: #FOR MU
        nbu = int(request.session['NBU'])
        if dtType == 'SOADate':
            allSOA_list =  SOA.objects.filter(SOADate__range=(dtFrom,dtTo),SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        elif dtType == 'SOALastDate':
            allSOA_list =  SOA.objects.filter(SOALastUpdate__range=(dtFrom,dtTo),SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        elif dtType == 'CBDate':
            allSOA_list =  SOA.objects.filter(CBDate__range=(dtFrom,dtTo),SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
        htmlfile = 'ecs_templates/caSOADetails.html'
    
    
    
    ##################################
    ##           PAGINATE           ##
    ##################################    
    paginator = Paginator(allSOA_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    
    try:
        allSOA = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        allSOA = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        allSOA = paginator.page(paginator.num_pages) 
     
    return render_to_response(htmlfile, {'allSOA':allSOA,},context_instance=RequestContext(request,))
    



#************************************************************************#
#************************************************************************#
#************************************************************************#


    


#************************************************************************#
#************************************************************************#
#************************************************************************#

def suSOACreation(request):
    user = request.session['User']
    vendor = str(request.session['Vendor'])
    isadmin = int(request.session['Control'])
    
    if isadmin == 0:
        BAbbr = str(request.session['Branch'])
    else:
        BAbbr = 'ADJ'  
    #branchinfo = Branch.objects.get(BAbbr=BAbbr)
    
    form = NBUForm()
    
    return render_to_response('ecs_templates/suSOACreation.html',{'form':form,'isadmin':isadmin,},context_instance=RequestContext(request,))

#************************************************************************#
#************************************************************************#
#************************************************************************#

#changed to validation on submit button

def getPODate(request):
    try:    
        user = str(request.session['User'])
        
        PONo = request.POST.get('PONo')
        
        isadmin = int(request.session['Control'])
        
        if isadmin == 0:
            vendor = str(request.session['Vendor'])
            nbu = int(request.POST.get('nbu'))
            POalreDnDB = Details.objects.values_list('PONo',flat=True).filter(PONo=PONo).exclude(DStatus='Denied')    
        else:
            nbu = int(request.session['NBU'])
            POalreDnDB = []
        
        
        ##############################################
        if nbu == 994:
            0#set connection string for citifoods here
        else:
            cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
            cursor = cnxn.cursor()
        ##############################################
        
        
        #if int(PONo) in POalreDnDB:
        if POalreDnDB:
            data = {}
            data['response'] = 'Existed'
            data['nbu'] = ''
        else:
            try:
                if isadmin == 0:
                    cursor.execute("SELECT PORDAT,STCOMP,PORVCS,PORVAT FROM TBLSTR LEFT JOIN POMRCH ON TBLSTR.STRNUM = POMRCH.POLOC WHERE POVNUM = '" + vendor + "' AND PONUMB = '" + str(PONo) + "' AND POSTAT = 6 ORDER BY PORDAT DESC")
                else:
                    cursor.execute("SELECT PORDAT,STCOMP,PORVCS,PORVAT FROM TBLSTR LEFT JOIN POMRCH ON TBLSTR.STRNUM = POMRCH.POLOC WHERE PONUMB = '" + str(PONo) + "' AND POSTAT = 6 ORDER BY PORDAT DESC")
                    
                fDATA = cursor.fetchone()
                PORDAT = fDATA[0]
                STCOMP = fDATA[1]
                PORVCS = fDATA[2]
                PORVAT = fDATA[3]
            except:
                PORDAT = None
                STCOMP = None
                PORVCS = None
                PORVAT = None
            
            if PORDAT:
                if STCOMP == nbu:
                    ###GET DESC
                    NBUDesc = NBU.objects.values_list('NBUDesc',flat=True).get(id=STCOMP) 
                    ###
                    
                    ###FORMAT DT
                    dt = datetime.datetime.strptime(str(PORDAT),'%y%m%d')
                    PODate = dt.strftime('%m/%d/%Y')
                    
                    data = {}
                    data['response'] = str(PODate)
                    data['nbu'] = str(STCOMP)
                    data['nbudesc'] = str(NBUDesc)
                    data['rramount'] = str(PORVCS)
                    
                    
                
                else:
                    data = {}
                    data['response'] = 'billto not same'
                    
            else:
                data = {}
                data['response'] = ''
                data['nbu'] = ''
                data['rramount'] = ''
        
        cursor.close()
        return HttpResponse(json.dumps(data), content_type = "application/json")
    
    except:
        data = {}
        data['response'] = ''
        data['nbu'] = ''
        data['rramount'] = ''
        return HttpResponse(json.dumps(data), content_type = "application/json")
        

                
#************************************************************************#
#************************************************************************#
#************************************************************************#

def evalallPO(request):
    try:
        insertedpo = request.POST.getlist('insertedpo[]')
        ponumbs = str(insertedpo).translate(None, 'u[]')
        
        isadmin = int(request.session['Control'])
        if isadmin == 0:
            nbu = int(request.POST.get('nbu'))
        else:
            nbu = int(request.session['NBU'])
        
        for po in insertedpo:
            if isadmin != 1:
                checkexist = Details.objects.filter(PONo=po).exclude(DStatus='Denied')
                if checkexist:
                    return HttpResponse('PO already exist.')
        return HttpResponse('Okay')
        '''
        ##############################################
        if nbu == 994:
            0#set connection string for citifoods here
        else:
            cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
            cursor = cnxn.cursor()
        ##############################################
        
        #query = "SELECT COUNT(DISTINCT (ITFTRD)) AS NUM FROM ITFLIB.ITFAPI WHERE ITFTTYP = 'OUT' AND ITFPNO IN(" + ponumbs + ")"
        query = "SELECT COUNT(DISTINCT(APTERM.TMPDSC)) AS NUM FROM POMHST LEFT JOIN APTERM ON POMHST.POTRMS = APTERM.TMPCOD WHERE PONUMB IN(" + ponumbs + ")"
        
        cursor.execute(query)
        issame = cursor.fetchall()[0][0]
        
        return HttpResponse(issame)
        '''
    except:
        return HttpResponse('Connection Error!')
    

#************************************************************************#
#************************************************************************#
#************************************************************************#

@transaction.atomic
def SOAinsertact(request):
    try:
        user = str(request.session['User'])
        isadmin = int(request.session['Control'])
        if isadmin == 0:
            vendor = str(request.session['Vendor'])
            BAbbr = str(request.session['Branch'])
        else:
            vendor = str(request.POST.get('vendorID'))
            BAbbr = 'ADJ'
            
        seriesNo = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
        SOANo = str(BAbbr) + seriesNo
        SOADate = datetime.datetime.now()
        
        ##CHANGED TO hnbu from nbu (LABEL TYPE)
        if isadmin == 0:
            nbu = int(request.POST.get('hnbu'))
        else:
            nbu = int(request.session['NBU'])
        
        ###############################
        allpoinSOA = request.POST.get('allenteredpo')
        
        ##############################################
        if nbu == 994:
            0#set connection string for citifoods here
        else:
            cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
            cursor = cnxn.cursor()
        ##############################################
    
        
        ###############################
        #cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
        #-cursor = cnxn.cursor()
        ###############################
        for x in range(10):
            PONo = request.POST.get('PONo' + str(x+1))
            
            #if there is a PO value INSERT
            if PONo:
                strPODate = str(request.POST.get('hPODate' + str(x+1)))
                dtPODate = datetime.datetime.strptime(strPODate, "%m/%d/%Y")
                PODate = dtPODate.strftime("%Y-%m-%d")
                
                ###############################
                #GET RRAMOUNT
                cursor.execute("SELECT PORVCS FROM POMRCH WHERE POVNUM = '" + vendor + "' AND PONUMB = '" + str(PONo) + "' AND POSTAT = 6")
                
                fDATA = cursor.fetchone()
                PORVCS = fDATA[0]
                #DETAILS
                '''
                PORDAT -> Receipt Date       POMRCH
                STCOMP -> G/L Company No.    TBLSTR
                PORVCS -> Total Rec. Cost    POMRCH
                PORVAT -> Amounts Rec. Vat   POMRCH
                '''
                RRAmount = Decimal(PORVCS)
                ###############################################
                
                rowindexlen = int(request.POST.get('InvRowindex' + str(x+1)))
                
                for y in range(rowindexlen):
                    strInvDate = request.POST.get('InvDate' + str(x+1) + '-' + str(y+1))
                    
                    InvNo = str(request.POST.get('InvNo' + str(x+1) + '-' + str(y+1))).strip()
                    Amount = request.POST.get('Amount' + str(x+1) + '-' + str(y+1))
                    if Amount == None:
                        Amount = 0
                    else:
                        Amount = Decimal(str(Amount).replace(',',''))
                    
                    #Save to Invoice field with PO for reference key
                    if strInvDate:
                        dtInvDate = datetime.datetime.strptime(strInvDate, "%m/%d/%Y")
                        InvDate = dtInvDate.strftime("%Y-%m-%d")
                        
                        entryCtr = int(Invoice.objects.filter(PONo_id=str(PONo),InvNo=InvNo).count()) + 1
                        
                        if isadmin == 0:
                            Invoice(InvDate=InvDate,InvNo=InvNo,Amount=Amount,IMAmount=None,LowerAmt=None,PONo_id=PONo,IStatus='Open',SOANo_id=SOANo,EntryCount=entryCtr,PRINTCODE=None).save()
                        else:
                            invquery = "SELECT ITFMCH, ITFSTP, ITFDSC FROM ITFLIB.ITFAPI WHERE TRIM(ITFINV) LIKE '%" + InvNo + "%' AND ITFCMP = '" + str(nbu) + "' AND ITFPNO = '" + str(PONo) + "' AND ITFTTYP = 'OUT' AND ITFNUM = '" + vendor + "'"
                            cursor.execute(invquery)
                            try:
                                iDATA = cursor.fetchone()
                                ITFMCH = Decimal(iDATA[0])
                                ITFSTP = Decimal(iDATA[1])
                                ITFDSC = Decimal(iDATA[2])
                                
                                IMAmount = Decimal(ITFMCH + ITFSTP - ITFDSC)
                                LowerAmt = min(IMAmount,Amount)
                            except:
                                IMAmount = None
                                LowerAmt = None
                            Invoice(InvDate=InvDate,InvNo=InvNo,Amount=Amount,IMAmount=IMAmount,LowerAmt=LowerAmt,PONo_id=PONo,IStatus='Adjustments',SOANo_id=SOANo,EntryCount=entryCtr,PRINTCODE=None).save()
                        
                ################################################
                if isadmin == 0: 
                    POTotalInvAmntEntrd = Decimal(sum(Invoice.objects.values_list('Amount',flat=True).filter(PONo_id=PONo,IStatus='Open')))
                    #SAVE
                    Details(PODate=PODate,PONo=PONo,RRAmount=RRAmount,POTotalInvAmntEntrd=POTotalInvAmntEntrd,SOANo_id=SOANo,DStatus='Open').save()
                    #LOGS
                    Logs(PONo_id=PONo,POAction='Open',userResp_id=user,dateofTranx=datetime.datetime.now()).save()
                else:
                    POTotalInvAmntEntrd = Decimal(sum(Invoice.objects.values_list('Amount',flat=True).filter(PONo_id=PONo,IStatus='Adjustments')))
                    #SAVE
                    Details(PODate=PODate,PONo=PONo,RRAmount=RRAmount,POTotalInvAmntEntrd=POTotalInvAmntEntrd,SOANo_id=SOANo,DStatus='Adjustments').save()
                    #LOGS
                    Logs(PONo_id=PONo,POAction='Adjustments',userResp_id=user,dateofTranx=datetime.datetime.now()).save()
        
        
        ##SELECT MAX PO DATE
        POOldestdt = max(Details.objects.values_list('PODate', flat=True).filter(SOANo_id=SOANo))
        
        #query = "SELECT DISTINCT (ITFTRD) AS TERM FROM ITFLIB.ITFAPI WHERE ITFTTYP = 'OUT' AND ITFPNO IN(" + str(allpoinSOA) + ")"
        ##CHANGED (TO BE ENABLE TO FETCH NOT YET IM PO)
        #query = "SELECT DISTINCT(APTERM.TMPDSC) AS TERM FROM POMHST LEFT JOIN APTERM ON POMHST.POTRMS = APTERM.TMPCOD WHERE PONUMB IN(" + str(allpoinSOA) + ")"
        query = "SELECT TRIM(APTERM.TMPDSC) AS TERM FROM POMHST LEFT JOIN APTERM ON POMHST.POTRMS = APTERM.TMPCOD WHERE PONUMB IN(" + str(allpoinSOA) + ")"
        
        cursor.execute(query)
        pterms = [item[0] for item in cursor.fetchall()]
        #pterms = list(cursor.fetchall())
        
        idofpterm = max(PayTerms.objects.values_list('id',flat=True).filter(termName__in=pterms,NBU_id=nbu))
        NoOfDaysToAdd = max(PayTerms.objects.values_list('Days',flat=True).filter(termName__in=pterms,NBU_id=nbu))
        
        #pterm = cursor.fetchall()[0][0]
        #################
        '''
        row = cursor.fetchone()
        pterm = row[0]
        vendorName = row[1]
        '''
        #DISABLED
        #################
        #idofpterm = PayTerms.objects.values_list('id').get(termName=pterm,NBU_id=nbu)[0]
        ###############################
        
        ## CALCULATE CBDATE HERE
        #NoOfDaysToAdd = int(SOAinfo.PTerm.Days)#DISABLED
        #NoOfDaysToAdd = int(PayTerms.objects.values_list('Days',flat=True).get(id=idofpterm))
        
        RDate = datetime.datetime.now()
        CBDate = datetime.date.today() + datetime.timedelta(days=NoOfDaysToAdd)
        CBDateORG = CBDate
        dummyDate = RDate
        
        if NoOfDaysToAdd == 3:
            ctr = 0
            while ctr != NoOfDaysToAdd:
                #SATURDAY?
                if dummyDate.weekday() == 5:
                    dummyDate = dummyDate + datetime.timedelta(days=2)
                #SUNDAY?
                elif dummyDate.weekday() == 6:
                    dummyDate = dummyDate + datetime.timedelta(days=1)
                #HOLIDAY?
                elif isHoliday(CBDate,BAbbr):    
                    dummyDate = dummyDate + datetime.timedelta(days=1)
                #TERMINATE
                else:
                    dummyDate = dummyDate + datetime.timedelta(days=1)
                    ctr = ctr + 1
            CBDate = dummyDate
        else:
            x = 0 
            while x == 0:
                #SATURDAY?
                if CBDate.weekday() == 5:
                    CBDate = CBDate + datetime.timedelta(days=2)
                #SUNDAY?
                elif CBDate.weekday() == 6:
                    CBDate = CBDate + datetime.timedelta(days=1)
                #HOLIDAY?
                elif isHoliday(CBDate,BAbbr):    
                    CBDate = CBDate + datetime.timedelta(days=1)
                #TERMINATE
                else:
                    x = 1
        
        ###############################
        
        if isadmin == 0:
            SOA(SOANo=SOANo,SOADate=SOADate,SOALastUpdate=SOADate,SOAStatus='Open',SOABillTo_id=nbu,CreatedBy_id=user,PTerm_id=idofpterm,CBDate=CBDate,CBDateORG=CBDateORG,RDate=RDate).save()
        else:
            SOA(SOANo=SOANo,SOADate=SOADate,SOALastUpdate=SOADate,SOAStatus='Adjustments',SOABillTo_id=nbu,CreatedBy_id=user,PTerm_id=idofpterm,CBDate=CBDate,CBDateORG=CBDateORG,RDate=RDate,ProcessedBy_id=user).save()
        
        cursor.close()
                
        message = "SOA has been successfully created."
        msgNum = 0
        
        return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))  
    except:
        message = "An Error has been encountered."
        msgNum = 0
        
        return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))
    
#--------------------------------------------- 

#NO UPDATING ON SOA(DIRECT DENY)
'''
#@transaction.atomic
def SOAupdateact(request):
    #try:
        #transtart = transaction.savepoint()
        
        currUser = str(request.session['User'])
        SOANo = str(request.POST.get('hSOANo'))
        
        #COUNT PILA KABUOK
        upto = len(Details.objects.filter(SOANo_id=SOANo))
        
        soadets = SOA.objects.get(SOANo=SOANo)
        
        soadets.SOALastUpdate = datetime.datetime.now()
        soadets.save()
        
        Details.objects.filter(SOANo_id=SOANo).delete()   
        ### NO NEED NA KAY MA DELETE MAN SYA PAG APIL ###
        #Invoice.objects.filter(PONo__SOANo_id=SOANo).delete()#
        
        #INSERT ACTION CODES FOR EDIT
        for x in range(10):
            PONo = request.POST.get('PONo' + str(x+1))
            
            #if there is a PO value UPDATE
            if PONo:
                strPODate = str(request.POST.get('hPODate' + str(x+1)))
                dtPODate = datetime.datetime.strptime(strPODate, "%m/%d/%Y")
                PODate = dtPODate.strftime("%Y-%m-%d")
                
                RRAmount = Decimal(request.POST.get('RRAmt' + str(x+1)))
                TotalPOAmt = request.POST.get('htotalpo' + str(x+1))
                
                rowindexlen = int(request.POST.get('InvRowindex' + str(x+1)))
                for y in range(rowindexlen):
                    strInvDate = request.POST.get('InvDate' + str(x+1) + '-' + str(y+1))
                    
                    InvNo = request.POST.get('InvNo' + str(x+1) + '-' + str(y+1))
                    Amount = request.POST.get('Amount' + str(x+1) + '-' + str(y+1))
                    if Amount == None:
                        Amount = 0
                    else:
                        Amount = Decimal(str(Amount).replace(',',''))
                        
                    #Save to Invoice field with PO for reference key
                    if strInvDate:
                        #lookupifexist = Invoice.objects.filter(PONo_id=PONo,PONo__SOANo_id=SOANo)
                        dtInvDate = datetime.datetime.strptime(strInvDate, "%m/%d/%Y")
                        InvDate = dtInvDate.strftime("%Y-%m-%d")
                        
                        Invoice(InvDate=InvDate,InvNo=InvNo,Amount=Amount,PONo_id=PONo,IStatus='Work').save()
                        
                ################################################
                POTotalInvAmntEntrd = sum(Invoice.objects.values_list('Amount',flat=True).filter(PONo_id=PONo))
                LesserAmt = min(POTotalInvAmntEntrd,RRAmount)
                
                #SAVE
                Details(PODate=PODate,PONo=PONo,RRAmount=RRAmount,POTotalInvAmntEntrd=POTotalInvAmntEntrd,LesserAmt=LesserAmt,SOANo_id=SOANo,DStatus='Work').save()
                Logs(PONo_id=PONo,POAction='Work',userResp_id=currUser,dateofTranx=datetime.datetime.now()).save()
                
        message = SOANo + " has been Updated Successfully."
        msgNum = 1
        
        return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))
    #except:
        #return redirect('/ECS/sumain/') 
'''

#-------------------------
#NO DELETION
'''
def SOAdeleteact(request):
    user = str(request.session['User'])
    vendor = str(request.session['Vendor'])
    SOANo = str(request.POST.get('SOANo'))
    
    #LOGS
    forpologs = Details.object    .filter(SOANo_id=SOANo,DStatus__in=['Work','Pending'])
    for po in forpologs:
        Logs(PONo_id=po.PONo,POAction='Delete',userResp_id=currUser,dateofTranx=datetime.datetime.now()).save()
    
    
    #DELETE SOA AND DETAILS
    SOA.objects.filter(SOANo=SOANo).delete()
    Details.objects.filter(SOANo_id=SOANo,DStatus__in=['Work','Pending']).delete()
    
      
    message = SOANo + " has been Successfully DELETED."
    
    return HttpResponse(message)
'''

#************************************************************************#
#************************************************************************#
#************************************************************************#

#NO NEED (CHANGED STATUS TO AUTO OPEN ON CREATE)
'''
def For_APV_Checking(request):
    currUser = request.session['User']
    SOANo = request.POST.get('SOANo')
         
    soainfo = SOA.objects.get(SOANo=str(SOANo))
    soainfo.SOAStatus = 'Open'
    soainfo.SOALastUpdate = datetime.datetime.now()
    #
    soainfo.RDate = datetime.datetime.now()
    ## CALCULATE CBDATE HERE
    NoOfDaysToAdd = int(soainfo.PTerm.Days)
    
    CBDate = datetime.date.today() + datetime.timedelta(days=NoOfDaysToAdd)
    soainfo.CBDateORG = CBDate
    
    x = 0 
    while x == 0:
        if CBDate.weekday() == 5:
            CBDate = CBDate + datetime.timedelta(days=2)
        elif CBDate.weekday() == 6:
            CBDate = CBDate + datetime.timedelta(days=1)
        elif isHoliday(CBDate):    
            CBDate = CBDate + datetime.timedelta(days=1)
        else:
            x = 1
        
    soainfo.CBDate = CBDate
    soainfo.save()
    
    
    
    POinSOA = Details.objects.filter(SOANo_id=SOANo,DStatus='Work').order_by('SOANo_id')
    #totalamount = detinfo.aggregate(Sum('Amount'))['Amount__sum']
    
    for PO in POinSOA:
        PO.DStatus = 'Open'
        ############################
        #INVOICE
        InvinPO = Invoice.objects.filter(PONo_id=PO)
        for Inv in InvinPO:
            Inv.IStatus = 'Open'
            Inv.save()
        ############################
        PO.LesserAmt = min(PO.RRAmount,PO.POTotalInvAmntEntrd)
        PO.save()
        #LOGS
        Logs(PONo_id=PO.PONo,POAction='Open',userResp_id=currUser,dateofTranx=datetime.datetime.now()).save()
        
        
    msgNum = 0
    message = "SOA submitted to APV Associate."        
    return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))
'''      

    
#************************************************************************#
#************************************************************************#
#************************************************************************#

##########################################################################
############################### FOR CA ###################################
##########################################################################


#************************************************************************#
#************************************************************************#
#************************************************************************#
    
def camain(request):
    try:
        user = str(request.session['User'])
        FullName = str(request.session['FullName'])
        #vendor = str(request.session['Vendor'])
        #vendorName = str(request.session['VendorName'])
        isadmin = int(request.session['Control'])
        nbu = int(request.session['NBU'])
        
        nbudesc = NBU.objects.values_list('NBUDesc',flat=True).get(id=nbu)
        
        pwdexpiry = User.objects.values_list('PwdExpiry',flat=True).get(UserName=user)
        
        if isadmin == 0:
            return redirect("/ECS/sumain/")
        elif isadmin == 1:
            allSOA_list = SOA.objects.filter(SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            
            paginator = Paginator(allSOA_list, 25) # Show 25 contacts per page
        
            page = request.GET.get('page')
            
            try:
                allSOA = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                allSOA = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                allSOA = paginator.page(paginator.num_pages)
            
            return render_to_response('ecs_templates/camain.html', {'nbudesc':nbudesc,'isadmin':isadmin,'user':user,'FullName':FullName,'allSOA':allSOA,'pwdexpiry':pwdexpiry},context_instance=RequestContext(request,))
        elif isadmin == 2:
            return redirect("/ECS/pamain/")
        elif isadmin == 3:
            return redirect("/ECS/mumain/")
    except:
        return redirect('/ECS/index/')
        
#************************************************************************#
#************************************************************************#
#************************************************************************#

'''
def unfocusSOA(request):
    user = str(request.session['User'])
    
    unfocusall = SOA.objects.filter(isViewedBy_id=user)
    
    for unfocus in unfocusall:
        unfocus.isViewedBy_id = None
        unfocus.save()
    return redirect("/ECS/camain/")
'''     

#************************************************************************#
#************************************************************************#
#************************************************************************#

def cadetprev(request):
    user = str(request.session['User'])
    SOANo = str(request.POST.get('SOANo'))
    SOAStatus = str(request.POST.get('SOAStatus'))
    CBDate = str(request.POST.get('CBDate'))
    
    #dets = Details.objects.filter(SOANo_id=SOANo,DStatus=SOAStatus).order_by('id')
    #dets = Details.objects.filter(SOANo_id=SOANo,DStatus__in=['Work','Open','Countered','Pending']).order_by('id')
    
    dets = Details.objects.filter(SOANo_id=SOANo)
    
    soadets = SOA.objects.get(SOANo=SOANo)
    #soadets.isViewedBy_id = user
    soadets.save()
    #-----
    soabillto = soadets.SOABillTo_id
    soastatus = soadets.SOAStatus
    
    soahasOpenPO = Details.objects.filter(SOANo_id=SOANo,DStatus='Open')
    soahasDeniedPO = Details.objects.filter(SOANo_id=SOANo,DStatus='Denied')
    
    
    return render_to_response('ecs_templates/cadetprev.html', {'soastatus':soastatus, 'soahasOpenPO':soahasOpenPO, 'dets':dets, 'SOANo':SOANo, 'soahasDeniedPO':soahasDeniedPO, 'soadets':soadets, 'CBDate':CBDate,},context_instance=RequestContext(request,))
    
#************************************************************************#
#************************************************************************#
#************************************************************************#

def toprocess(request):
    user = str(request.session['User'])
    
    SOANo = str(request.POST.get('hSOANo'))
    allPO = request.POST.getlist('POchx')
    
    SOAinfo = SOA.objects.get(SOANo=SOANo)
    
    if SOAinfo.SOAStatus == 'Processed':
        msgNum = 1
        message = "SOA already processed."
        
        return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))
    else:
        ############################################################
        #IBM SERIES CONNECTION
        cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
        cursor = cnxn.cursor()
        ############################################################
        
        SOAinfo.SOALastUpdate = datetime.datetime.now()
        
        ########################
        allPOfrmDBonProcess = Details.objects.values_list('PONo',flat=True).filter(SOANo_id=SOANo,DStatus='Open')        
        for PO in allPOfrmDBonProcess:
            podets = Details.objects.get(SOANo_id=SOANo,PONo=PO,DStatus='Open')
            if str(PO) in allPO:
                podets.DStatus = 'Denied'
                podets.DenyReason = str(request.POST.get('h' + str(PO)))
                #INVOICE
                invpo = Invoice.objects.filter(PONo_id=PO,SOANo_id=SOANo,IStatus='Open')#dagdagan ng SOA filter para di madamay ang denied
                for inv in invpo:
                    inv.IStatus = 'Denied'
                    ##
                    
                    
                    invquery = "SELECT ITFMCH, ITFSTP, ITFDSC FROM ITFLIB.ITFAPI WHERE TRIM(ITFINV) LIKE '%" + inv.InvNo + "%' AND ITFCMP = '" + str(podets.SOANo.SOABillTo_id) + "' AND ITFPNO = '" + str(podets.PONo) + "' AND ITFTTYP = 'OUT' AND ITFNUM = '" + podets.SOANo.CreatedBy.vendorID + "'"
                    cursor.execute(invquery)
                    try:
                        iDATA = cursor.fetchone()
                        ITFMCH = Decimal(iDATA[0])
                        ITFSTP = Decimal(iDATA[1])
                        ITFDSC = Decimal(iDATA[2])
                        
                        IMAmount = Decimal(ITFMCH + ITFSTP - ITFDSC)
                    except:
                        IMAmount = None
                    
                    inv.IMAmount = IMAmount
                    inv.save()
                #LOGS
                Logs(PONo_id=PO,POAction='Denied',userResp_id=user,dateofTranx=datetime.datetime.now()).save() 
            else:
                podets.DStatus = 'Processed'
                podets.DenyReason = ''
                #INVOICE
                invpo = Invoice.objects.filter(PONo_id=PO,SOANo_id=SOANo,IStatus='Open')#dagdagan ng SOA filter para di madamay ang denied
                for inv in invpo:
                    inv.IStatus = 'Processed'
                    ##
                    
                    invquery = "SELECT ITFMCH, ITFSTP, ITFDSC FROM ITFLIB.ITFAPI WHERE TRIM(ITFINV) LIKE '%" + inv.InvNo + "%' AND ITFCMP = '" + str(podets.SOANo.SOABillTo_id) + "' AND ITFPNO = '" + str(podets.PONo) + "' AND ITFTTYP = 'OUT' AND ITFNUM = '" + podets.SOANo.CreatedBy.vendorID + "'"
                    cursor.execute(invquery)
                    try:
                        iDATA = cursor.fetchone()
                        ITFMCH = Decimal(iDATA[0])
                        ITFSTP = Decimal(iDATA[1])
                        ITFDSC = Decimal(iDATA[2])
                        
                        IMAmount = Decimal(ITFMCH + ITFSTP - ITFDSC)
                        LowerAmt = min(IMAmount,Decimal(inv.Amount))
                    except:
                        IMAmount = None
                        LowerAmt = None
                    
                    inv.IMAmount = IMAmount
                    inv.LowerAmt = LowerAmt
                    inv.save()
                #LOGS
                Logs(PONo_id=PO,POAction='Processed',userResp_id=user,dateofTranx=datetime.datetime.now()).save()
            podets.save()
            
        
        SOAinfo.ProcessedBy_id = user
        #SET TO PROCESSED STATUS IF NAAY NA PROCESS NGA STATUS
        isanypoprocessed = Details.objects.filter(SOANo_id=SOANo,DStatus='Processed')
        if isanypoprocessed:
            SOAinfo.SOAStatus = 'Processed'
        else:
            SOAinfo.SOAStatus = 'Returned'
        SOAinfo.save()
        
        cursor.close()
        
        msgNum = 1
        message = "Processing successful."
            
        return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))

##########################################################################
############################### END CA ###################################
##########################################################################





##########################################################################
############################### FOR PA ###################################
##########################################################################

def pamain(request):
    try:
        user = str(request.session['User'])
        FullName = str(request.session['FullName'])
        #vendor = str(request.session['Vendor'])
        #vendorName = str(request.session['VendorName'])
        isadmin = int(request.session['Control'])
        nbu = int(request.session['NBU'])
        
        nbudesc = NBU.objects.values_list('NBUDesc',flat=True).get(id=nbu)
        
        pwdexpiry = User.objects.values_list('PwdExpiry',flat=True).get(UserName=user)
        
        if isadmin == 0:
            return redirect("/ECS/sumain/")
        elif isadmin == 1:
            return redirect("/ECS/camain/")
        elif isadmin == 2:
            allSOA_list = SOA.objects.filter(SOABillTo_id=nbu).exclude(SOAStatus='Open').order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            
            paginator = Paginator(allSOA_list, 25) # Show 25 contacts per page
        
            page = request.GET.get('page')
            
            try:
                allSOA = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                allSOA = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                allSOA = paginator.page(paginator.num_pages)
            
            return render_to_response('ecs_templates/pamain.html', {'nbudesc':nbudesc,'isadmin':isadmin,'user':user,'FullName':FullName,'allSOA':allSOA,'pwdexpiry':pwdexpiry},context_instance=RequestContext(request,))
        elif isadmin == 3:
            return redirect("/ECS/mumain/")
    except:
        return redirect('/ECS/index/')
#************************************************************************#
#************************************************************************#
#************************************************************************#

def padetprev(request):
    user = str(request.session['User'])
    SOANo = str(request.POST.get('SOANo'))
    SOAStatus = str(request.POST.get('SOAStatus'))
    CBDate = str(request.POST.get('CBDate'))
    
    #dets = Details.objects.filter(SOANo_id=SOANo,DStatus=SOAStatus).order_by('id')
    #dets = Details.objects.filter(SOANo_id=SOANo,DStatus__in=['Work','Open','Countered','Pending']).order_by('id')
    
    dets = Details.objects.filter(SOANo_id=SOANo)
    
    soadets = SOA.objects.get(SOANo=SOANo)
    #soadets.isViewedBy_id = user
    soadets.save()
    #-----
    soabillto = soadets.SOABillTo_id
    soastatus = soadets.SOAStatus
    
    soahasOpenPO = Details.objects.filter(SOANo_id=SOANo,DStatus='Open')
    soahasDeniedPO = Details.objects.filter(SOANo_id=SOANo,DStatus='Denied')
    
    
    return render_to_response('ecs_templates/padetprev.html', {'soastatus':soastatus, 'soahasOpenPO':soahasOpenPO, 'dets':dets, 'SOANo':SOANo, 'soahasDeniedPO':soahasDeniedPO, 'soadets':soadets, 'CBDate':CBDate,},context_instance=RequestContext(request,))
    
#************************************************************************#
#************************************************************************#
#************************************************************************#

def toclose_sendback(request):
    user = str(request.session['User'])
    
    SOANo = str(request.POST.get('hSOANo'))
    SOAinfo = SOA.objects.get(SOANo=SOANo)
    
    acttype = str(request.POST.get('acttype'))
    actreason = str(request.POST.get('actreason'))
    
    #SENDBACK#
    if acttype == 'SendBack':
        #IN CASE NAGSABAY SILA UG CLICK SA SEND BACK
        if SOAinfo.SOAStatus == 'Open':
            msgNum = 2
            message = "SOA already sent back."
            
            return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))
        else:
            ### ADD TO REMARKS ### 
            Remarks(SOANo_id=SOANo,remarkreason=actreason,remarksBy_id=user).save()
            ### ROLLBACK TO OPEN STATUS ###
            SOAinfo.SOALastUpdate = datetime.datetime.now()
            ########################
            SOAinfo.SOAStatus = 'Open'
            SOAinfo.save()
            
            POunder = Details.objects.filter(SOANo_id=SOANo)
            for PO in POunder:
                if PO.DStatus != 'Denied':
                    PO.DStatus = 'Open'
                    PO.save()
                    Logs(PONo_id=PO.PONo,POAction='Open',userResp_id=user,dateofTranx=datetime.datetime.now()).save()
                
            INVunder = Invoice.objects.filter(SOANo_id=SOANo)
            for INV in INVunder:
                if INV.IStatus != 'Denied':
                    INV.IStatus = 'Open'
                    INV.save()
                    
            msgNum = 2
            message = "SOA successfully sent back."
            
            return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))
        
    #CLOSE#        
    elif acttype == 'Close':
        #IN CASE NAGSABAY SILA UG CLICK SA CLOSE
        if SOAinfo.SOAStatus == 'Closed':
            msgNum = 2
            message = "SOA already closed."
            
            return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))
        else:
            SOAinfo.SOALastUpdate = datetime.datetime.now()
            ########################
            SOAinfo.ClosedBy_id = user
            SOAinfo.SOAStatus = 'Closed'
            SOAinfo.save()
            
            POunder = Details.objects.filter(SOANo_id=SOANo)
            for PO in POunder:
                if PO.DStatus != 'Denied':
                    PO.DStatus = 'Closed'
                    PO.save()
                    Logs(PONo_id=PO.PONo,POAction='Closed',userResp_id=user,dateofTranx=datetime.datetime.now()).save()
                
            INVunder = Invoice.objects.filter(SOANo_id=SOANo)
            for INV in INVunder:
                if INV.IStatus != 'Denied':
                    INV.IStatus = 'Closed'
                    INV.save()
            
            msgNum = 2
            message = "SOA successfully Closed."
                
            return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))

#************************************************************************#
#************************************************************************#
#************************************************************************#

def mumain(request):
    try:
        user = str(request.session['User'])
        #vendor = str(request.session['Vendor'])
        FullName = str(request.session['FullName'])
        isadmin = int(request.session['Control'])
        nbu = int(request.session['NBU'])
        
        nbudesc = NBU.objects.values_list('NBUDesc',flat=True).get(id=nbu)
        
        pwdexpiry = User.objects.values_list('PwdExpiry',flat=True).get(UserName=user)
        
        if isadmin == 0:
            return redirect("/ECS/sumain/")
        elif isadmin == 1:
            return redirect("/ECS/camain/")
        elif isadmin == 2:
            return redirect("/ECS/pamain/")
        elif isadmin == 3 or isadmin == 4:
            allSOA_list = SOA.objects.filter(SOABillTo_id=nbu).order_by('-SOALastUpdate','-CBDate','-SOAStatus')
            
            paginator = Paginator(allSOA_list, 25) # Show 25 contacts per page
        
            page = request.GET.get('page')
            
            try:
                allSOA = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                allSOA = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                allSOA = paginator.page(paginator.num_pages)
        
            formnbu = NBUForm()
            
            return render_to_response('ecs_templates/mumain.html', {'formnbu':formnbu,'nbudesc':nbudesc,'isadmin':isadmin,'user':user,'FullName':FullName,'allSOA':allSOA,'pwdexpiry':pwdexpiry},context_instance=RequestContext(request,))
    except:
        return redirect('/ECS/index/')
        
        
#************************************************************************#
#************************************************************************#
#************************************************************************#

def mudetprev(request):
    SOANo = str(request.POST.get('SOANo'))
    SOAStatus = str(request.POST.get('SOAStatus'))
    CBDate = str(request.POST.get('CBDate'))
    
    #dets = Details.objects.filter(SOANo_id=SOANo,DStatus=SOAStatus).order_by('id')
    #dets = Details.objects.filter(SOANo_id=SOANo,DStatus__in=['Work','Open','Countered','Pending']).order_by('id')
    
    dets = Details.objects.filter(SOANo_id=SOANo)
    
    soadets = SOA.objects.get(SOANo=SOANo)
    #-----
    soabillto = soadets.SOABillTo_id
    soastatus = soadets.SOAStatus
    
    soahasOpenPO = Details.objects.filter(SOANo_id=SOANo,DStatus='Open')
    soahasPendingPO = Details.objects.filter(SOANo_id=SOANo,DStatus='Pending')
    soahasCRSRefPO = Details.objects.filter(SOANo_id=SOANo,DStatus='CRS Ref.')
    
    allPOfrmDB = str(Details.objects.values_list('PONo',flat=True).filter(SOANo_id=SOANo,DStatus='Work'))
    
    
    return render_to_response('ecs_templates/mudetprev.html', {'soahasCRSRefPO':soahasCRSRefPO, 'soahasOpenPO':soahasOpenPO, 'soahasPendingPO':soahasPendingPO, 'dets':dets, 'SOANo':SOANo, 'allPOfrmDB':allPOfrmDB, 'soastatus':soastatus, 'soadets':soadets, 'CBDate':CBDate,},context_instance=RequestContext(request,))
    

#************************************************************************#
#************************************************************************#
#************************************************************************#

def pwdcheck(request):
    user = str(request.session['User'])
    
    u = User.objects.get(UserName=user)
    lastlogin = u.LastLogin
    
    oldpwd = request.POST.get('oldpwd')
    newpwd = request.POST.get('newpwd')
    confirmnewpwd = request.POST.get('confirmnewpwd')
    
    #CHECK IF ENTERED OLD PASSWORD MATCHES DB PWD
    if check_password(u.UserPwd,oldpwd):    
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
                    #CHECK IF icontains BOTH LETTERS AND NUMBERS
                    if not newpwd.isnumeric() and not newpwd.isalpha() and newpwd.isalnum():
                        pwd = hash_password(newpwd)
                        u.UserPwd = pwd
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

def holidays(request):
    user = str(request.session['User'])
    FullName = str(request.session['FullName'])
    isadmin = int(request.session['Control'])
    #vendor = str(request.session['Vendor'])
    #vendorName = str(request.session['VendorName'])
    
    if isadmin == 4:
        nbudesc = 'ECS Admininistrator'
    else:
        nbu = int(request.session['NBU'])
        nbudesc = NBU.objects.values_list('NBUDesc',flat=True).get(id=nbu)
    
    
    holidays_list = Holidays.objects.order_by('-dateOfHoliday')
        
    paginator = Paginator(holidays_list, 50) # Show 50 contacts per page

    page = request.GET.get('page')
    
    try:
        holidays = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        holidays = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        holidays = paginator.page(paginator.num_pages)
    
    formnbu = NBUForm()
    
    return render_to_response('ecs_templates/holidays.html',{'formnbu':formnbu,'isadmin':isadmin,'holidays':holidays,'user':user,'nbudesc':nbudesc,'FullName':FullName,},context_instance=RequestContext(request))
    
#************************************************************************#
#************************************************************************#
#************************************************************************#
        
### FOR HOLIDAY FUNCTION ###
def addholiday(request):
    try:
        dateOfHoliday = datetime.datetime.strptime(str(request.POST.get('dateOfHoliday')),"%m/%d/%Y").date()
        holidayDesc = str(request.POST.get('holidayDesc'))
        typeOfHoliday = str(request.POST.get('typeOfHoliday'))
        schemeOfHoliday = str(request.POST.get('schemeOfHoliday'))
        
        if holidayDesc == '' or typeOfHoliday == '' or schemeOfHoliday == '':
            return HttpResponse('Please fill up all fields.')
        else:
            Holidays(dateOfHoliday=dateOfHoliday,holidayDesc=holidayDesc,typeOfHoliday=typeOfHoliday,schemeOfHoliday=schemeOfHoliday).save()
            return HttpResponse('Holiday Success.')
    except:
        return HttpResponse('Holiday already exists.')


#************************************************************************#
#************************************************************************#
#************************************************************************#

def users(request):
    try:
        user = str(request.session['User'])
        #vendor = str(request.session['Vendor'])
        FullName = str(request.session['FullName'])
        isadmin = int(request.session['Control'])
        
        if isadmin == 4:
            nbudesc = 'ECS Admininistrator'
            allusers_list = User.objects.filter(User_isadmin__in=[0,1,2,3]).order_by('User_isadmin','Status','UserName')
        else:
            nbu = int(request.session['NBU'])
            nbudesc = NBU.objects.values_list('NBUDesc',flat=True).get(id=nbu)
            allusers_list = User.objects.filter(User_isadmin__in=[0,1,2]).order_by('User_isadmin','Status','UserName')
        
        paginator = Paginator(allusers_list, 100) # Show 25 contacts per page
    
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
        
        formnbu = NBUForm()
        formvendor = VendorForm()
        
        
        return render_to_response('ecs_templates/users.html', {'formnbu':formnbu,'formvendor':formvendor,'allusers':allusers,'user':user,'isadmin':isadmin,'nbudesc':nbudesc,'FullName':FullName}, context_instance=RequestContext(request))
    except:
        return redirect('/ECS/index/')
        
        
#************************************************************************#
#************************************************************************#
#************************************************************************#

### FOR CREATE ACCT FUNCTION ###
def createacct(request):
    try:
        newacctusername = str(request.POST.get('newacctusername'))
        newacctfullname = str(request.POST.get('newacctfullname'))
        newaccttype = int(request.POST.get('newaccttype'))
        
        isidexisting = User.objects.filter(UserName=newacctusername)
        
        if isidexisting:
            message = 'Error! Account already exist.'
            msgNum = 4
            
            return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))
            
        else:
            ############################################################
            #IBM SERIES CONNECTION
            cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
            cursor = cnxn.cursor()
            ############################################################
            
            year = str(datetime.date.today().year)
            
            if newaccttype == 0:
                #newacctvendorID = str(request.POST.get('newacctvendorID'))
                newacctvendorID = str(request.POST.get('vendorid'))
                
                #query to MMS to get vendorname
                query = "SELECT ASNAME FROM APSUPP WHERE CAST(ASNUM AS CHARACTER(50)) = '" + newacctvendorID + "' AND ASTYPE = '1'"
                cursor.execute(query)
                
                try:
                    vendorName = str(cursor.fetchone()[0])
                    defpwd = hash_password(newacctusername.lower() + year)
                    User(UserName=newacctusername,FullName=newacctfullname,vendorID=newacctvendorID,vendorName=vendorName,UserPwd=defpwd,User_isadmin=newaccttype,PwdExpiry=None,PwdHistory=defpwd,LastLogin=None,Status='Active').save()
                except:
                    message = 'Vendor ID ' + newacctvendorID + ' does not exist!' 
                    msgNum = 4
                    
                    return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))
            else:
                defpwd = hash_password(newacctusername.lower() + year)
                User(UserName=newacctusername,FullName=newacctfullname,vendorID=None,vendorName=None,UserPwd=defpwd,User_isadmin=newaccttype,PwdExpiry=None,PwdHistory=defpwd,LastLogin=None,Status='Active').save()
            
            cursor.close()
            
            message = 'Account has been successfully created.'
            msgNum = 4
            
            return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))
    except:
        message = 'Error! Account not created.'
        msgNum = 4
        
        return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))

#************************************************************************#
#************************************************************************#
#************************************************************************#

#GETUSERDATA
def getuserdata(request):
    userName = str(request.POST.get('userName'))
    u = User.objects.get(UserName=userName)
    
    data = {}
    data['FullName'] = u.FullName
    data['vendorID'] = u.vendorID
    data['vendorName'] = u.vendorName
    data['isadmin'] = u.User_isadmin
    data['Status'] = u.Status
    
    
    return HttpResponse(json.dumps(data), content_type = "application/json")

#************************************************************************#
#************************************************************************#
#************************************************************************#

### FOR UPDATE ACCT FUNCTION ###
def updateacct(request):
    editacctusername = str(request.POST.get('editacctusername'))
    editacctfullname = str(request.POST.get('editacctfullname'))
    editacctstatus = str(request.POST.get('editacctstatus'))
    editacctpwd = str(request.POST.get('editacctpwd'))
    
    userinfo = User.objects.get(UserName=editacctusername)
    userinfo.FullName = editacctfullname
    userinfo.Status = editacctstatus
    
    if editacctpwd:
        userinfo.UserPwd = hash_password(editacctpwd)
    
    userinfo.save()
        
    message = 'Account has been successfully updated.'
    msgNum = 4
    
    return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))

#************************************************************************#
#************************************************************************#
#************************************************************************#

def access(request):
    #try:
        user = str(request.session['User'])
        FullName = str(request.session['FullName'])
        isadmin = int(request.session['Control'])
        
        if isadmin == 4:
            nbudesc = 'ECS Admininistrator'
        else:
            nbu = int(request.session['NBU'])
            nbudesc = NBU.objects.values_list('NBUDesc',flat=True).get(id=nbu)
        
        allaccess_list = NCCCAccess.objects.all().order_by('userName_id','nbu_id')
        
        paginator = Paginator(allaccess_list, 25) # Show 25 contacts per page
    
        page = request.GET.get('page')
        
        try:
            allaccess = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            allaccess = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            allaccess = paginator.page(paginator.num_pages)
        
        form = AccessForm()
        ###########################################
        formnbu = NBUForm()
        
        return render_to_response('ecs_templates/access.html', {'formnbu':formnbu,'form':form,'allaccess':allaccess,'user':user,'isadmin':isadmin,'nbudesc':nbudesc,'FullName':FullName}, context_instance=RequestContext(request))
    #except:
        #return redirect('/ECS/index/')


def addaccess(request):
    ncccperson = str(request.POST.get('ncccperson'))
    nbuaccess = int(request.POST.get('nbuaccess'))
    
    
    alreadyallowed = NCCCAccess.objects.filter(userName_id=ncccperson,nbu_id=nbuaccess)

    if alreadyallowed:
        message = "NCCC Personnel already have access."
    else:
        NCCCAccess(userName_id=ncccperson,nbu_id=nbuaccess).save()
        message = "NCCC Personnel granted access."
    msgNum = 5
        
    return render_to_response('ecs_templates/message_info.html', {'msgNum':msgNum,'message':message},context_instance=RequestContext(request,))
    

#************************************************************************#
#************************************************************************#
#************************************************************************#

def deleteaccess(request):
    id = int(request.POST.get('id'))
    
    NCCCAccess.objects.filter(id=id).delete()
    
    return HttpResponse(id)

#************************************************************************#
#************************************************************************#
#************************************************************************#

#MESSAGING FOR TCARTINA
def messagingadmin(request):
    user = str(request.session['User'])
    #vendor = str(request.session['Vendor'])
    FullName = str(request.session['FullName'])
    isadmin = int(request.session['Control'])
    nbu = int(request.session['NBU'])
    
    nbudesc = NBU.objects.values_list('NBUDesc',flat=True).get(id=nbu)
    
    conn = mysql.connector.connect(host='localhost',database='dbecs',user='fpdypua',password='fpdypua')
    
    query = "SELECT A.`UserName`, A.`FullName`, A.`vendorID`, A.`vendorName`, A.`LastMessage`, A.`User_isadmin`, COUNT(B.msgStatus) AS msgCount FROM `ecs_user` as A LEFT JOIN `ecs_messaging` B ON B.sender_id = A.userName AND B.msgStatus='Unread' WHERE A.User_isadmin = 0 GROUP BY A.`userName`, A.`FullName`, A.`LastMessage` ORDER BY A.LastMessage DESC, A.UserName"
    
    curs = conn.cursor()
    curs.execute(query)
    results = curs.fetchall()
    
    x = curs.description
    allcontactswithconvo_list = []   
    for r in results:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i+1
        allcontactswithconvo_list.append(d)
    curs.close()
    conn.close()
    
    paginator = Paginator(allcontactswithconvo_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    
    try:
        allcontactswithconvo = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        allcontactswithconvo = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        allcontactswithconvo = paginator.page(paginator.num_pages)
        
    
    formnbu = NBUForm()

    return render_to_response('ecs_templates/messagingadmin.html', {'formnbu':formnbu,'isadmin':isadmin,'nbudesc':nbudesc,'user':user,'FullName':FullName,'allcontactswithconvo':allcontactswithconvo,},context_instance=RequestContext(request,))

#MESSAGING FOR User
def messaging(request):
    user = str(request.session['User'])
    FullName = str(request.session['FullName'])
    vendor = str(request.session['Vendor'])
    vendorName = str(request.session['VendorName'])
    isadmin = int(request.session['Control'])
    
    if isadmin == 0:
        #contact_username = User.objects.values_list('UserName',flat=True).get(User_isadmin=3)
        #contact_username = User.objects.values_list('UserName',flat=True).get(UserName='TMCARTINA')
        contact_username = User.objects.values_list('UserName',flat=True).get(UserName='JAPINEDA')
        allusermsgs = reversed(Messaging.objects.filter(Q(sender_id__exact=user)|Q(recipient_id__exact=user)).order_by('-id')[:30])
        needsupdtoRead = Messaging.objects.filter(recipient_id__exact=user)
    else:
        contact_username = str(request.POST.get('contact_username'))
        allusermsgs = reversed(Messaging.objects.filter(Q(sender_id__exact=contact_username)|Q(recipient_id__exact=contact_username)).order_by('-id')[:30])
        needsupdtoRead = Messaging.objects.filter(sender_id=contact_username)

    #needsupdtoRead = Messaging.objects.filter(sender_id=contact_username,recipient_id=user)
    for updtoRead in needsupdtoRead:
        updtoRead.msgStatus = 'Read'
        updtoRead.save()
    
    
    return render_to_response('ecs_templates/messages.html',{'vendorName':vendorName,'isadmin':isadmin,'user':user,'allusermsgs':allusermsgs,'contact_username':contact_username,},context_instance=RequestContext(request))

#************************************************************************#
#************************************************************************#
#************************************************************************#   

#ADDING MESSAGE
def sendmsg(request):
    user = str(request.session['User'])
    control = int(request.session['Control'])
    message = str(request.POST.get('msg'))
    contact_username = str(request.POST.get('contact_username')) 
    
    if control == 0: #FOR Users
        Messaging(sender_id=user,recipient_id=contact_username,message=message,dateOfSending=datetime.datetime.now(),msgStatus='Unread').save()
        allusermsgs = reversed(Messaging.objects.filter(Q(sender_id__exact=user)|Q(recipient_id__exact=user)).order_by('-id')[:30])
        updLastMessage = User.objects.get(UserName=user)
        updLastMessage.LastMessage = datetime.datetime.now()
        updLastMessage.save()
    else: #FOR TMERIN
        Messaging(sender_id=user,recipient_id=contact_username,message=message,dateOfSending=datetime.datetime.now(),msgStatus='Unread').save()
        allusermsgs = reversed(Messaging.objects.filter(Q(sender_id__exact=contact_username)|Q(recipient_id__exact=contact_username)).order_by('-id')[:30])
        updLastMessage = User.objects.get(UserName=contact_username)
        updLastMessage.LastMessage = datetime.datetime.now()
        updLastMessage.save()
        
    return render_to_response('ecs_templates/messagesDetails.html',{'user':user,'allusermsgs':allusermsgs,},context_instance=RequestContext(request))

#************************************************************************#
#************************************************************************#
#************************************************************************#

def MsgSearch(request):
    user = str(request.session['User'])
    keyword = request.POST.get('keyword')
    msgby = request.POST.get('msgby')

    conn = mysql.connector.connect(host='localhost',database='dbecs',user='fpdypua',password='fpdypua')
    
    if msgby == 'UserName': 
        query = "SELECT A.`UserName`, A.`FullName`, A.`vendorID`, A.`vendorName`, A.`LastMessage`, A.`User_isadmin`, COUNT(B.msgStatus) AS msgCount FROM `ecs_user` as A LEFT JOIN `ecs_messaging` B ON B.sender_id = A.userName AND B.msgStatus='Unread' WHERE A.UserName LIKE '%" + keyword + "%' AND A.User_isadmin = 0 GROUP BY A.`userName`, A.`FullName`, A.`LastMessage` ORDER BY A.LastMessage DESC, A.UserName"
    elif msgby == 'FullName':
        query = "SELECT A.`UserName`, A.`FullName`, A.`vendorID`, A.`vendorName`, A.`LastMessage`, A.`User_isadmin`, COUNT(B.msgStatus) AS msgCount FROM `ecs_user` as A LEFT JOIN `ecs_messaging` B ON B.sender_id = A.userName AND B.msgStatus='Unread' WHERE A.FullName LIKE '%" + keyword + "%' AND A.User_isadmin = 0 GROUP BY A.`userName`, A.`FullName`, A.`LastMessage` ORDER BY A.LastMessage DESC, A.UserName"
    elif msgby == 'vendorID':
        query = "SELECT A.`UserName`, A.`FullName`, A.`vendorID`, A.`vendorName`, A.`LastMessage`, A.`User_isadmin`, COUNT(B.msgStatus) AS msgCount FROM `ecs_user` as A LEFT JOIN `ecs_messaging` B ON B.sender_id = A.userName AND B.msgStatus='Unread' WHERE A.vendorID LIKE '%" + keyword + "%' AND A.User_isadmin = 0 GROUP BY A.`userName`, A.`FullName`, A.`LastMessage` ORDER BY A.LastMessage DESC, A.UserName"
    elif msgby == 'vendorName':
        query = "SELECT A.`UserName`, A.`FullName`, A.`vendorID`, A.`vendorName`, A.`LastMessage`, A.`User_isadmin`, COUNT(B.msgStatus) AS msgCount FROM `ecs_user` as A LEFT JOIN `ecs_messaging` B ON B.sender_id = A.userName AND B.msgStatus='Unread' WHERE A.vendorName LIKE '%" + keyword + "%' AND A.User_isadmin = 0 GROUP BY A.`userName`, A.`FullName`, A.`LastMessage` ORDER BY A.LastMessage DESC, A.UserName"
    
    curs = conn.cursor()
    curs.execute(query)
    results = curs.fetchall()
    
    x = curs.description
    allcontactswithconvo = []   
    for r in results:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i+1
        allcontactswithconvo.append(d)
    curs.close()
    conn.close()
    

    return render_to_response('ecs_templates/messagingadminDetails.html', {'allcontactswithconvo':allcontactswithconvo,},context_instance=RequestContext(request,))


#************************************************************************#
#************************************************************************#
#************************************************************************#

def genreports(request): 
    #try:
        reporttype = int(request.POST.get('reporttype'))
        nbu = int(request.POST.get('nbu'))
        
        nbudesc = str(NBU.objects.values_list('NBUDesc',flat=True).get(id=nbu))
        
        dt2 = datetime.datetime.strptime(str(request.POST.get('dt2')),"%m/%d/%Y").date()
        
        if reporttype == 1:
            dt1 = datetime.datetime.strptime(str(request.POST.get('dt1')),"%m/%d/%Y").date()
            reportName = 'Paid Invoices Variance'
            dtreportHeader = 'For the Period ' + str(dt1.strftime("%B %d")) + ' to ' + str(dt2.strftime("%B %d, %Y")) 
            #GET ALL COUNTERED
            rptentries = Invoice.objects.filter(IStatus='Processed',SOANo__SOADate__gte=dt1,SOANo__SOADate__lte=dt2).exclude(PRINTCODE__isnull=True).exclude(PRINTCODE__exact='')
            
        elif reporttype == 2:
            dt1 = datetime.datetime.strptime(str(request.POST.get('dt1')),"%m/%d/%Y").date()
            reportName = 'Comeback Date Variance'
            dtreportHeader = 'For the Period ' + str(dt1.strftime("%B %d")) + ' to ' + str(dt2.strftime("%B %d, %Y"))
            #GET ALL SOA COMEBACK DATE DIFFERENCE
            rptentries = Invoice.objects.filter(IStatus='Processed',SOANo__SOADate__gte=dt1,SOANo__SOADate__lte=dt2).exclude(PRINTCODE__isnull=True).exclude(PRINTCODE__exact='')
             
        elif reporttype == 3:
            reportName = 'Uncountered Delivered PO'
            dtreportHeader = 'As of ' + str(dt2.strftime("%B %d, %Y"))
            #DENIED PO NGA WALA SA COUNTERED, 
            #AND ALL OPEN STATUS
            rptentries = Invoice.objects.filter(IStatus__in=['Denied','Open'],InvDate__lte=dt2)
            
        elif reporttype == 4:
            dt1 = datetime.datetime.strptime(str(request.POST.get('dt1')),"%m/%d/%Y").date()
            reportName = 'Invoices Processed Per User'
            dtreportHeader = 'For the Period ' + str(dt1.strftime("%B %d")) + ' to ' + str(dt2.strftime("%B %d, %Y"))
            #ALL INVOICE DATE (FROM TO) WITH USER RESPONSIBLE
            rptentries = Invoice.objects.filter(IStatus='Processed',SOANo__SOADate__gte=dt1,SOANo__SOADate__lte=dt2)
        
        elif reporttype == 5:
            dt1 = datetime.datetime.strptime(str(request.POST.get('dt1')),"%m/%d/%Y").date()
            reportName = 'Invoice Status Per Vendor'
            dtreportHeader = 'For the Period ' + str(dt1.strftime("%B %d")) + ' to ' + str(dt2.strftime("%B %d, %Y"))
            #ALL INVOICE STATUS (FROM TO) PER VENDOR
            rptentries = Invoice.objects.filter(SOANo__SOADate__gte=dt1,SOANo__SOADate__lte=dt2).order_by('SOANo__CreatedBy__vendorID')
             
        elif reporttype == 6:
            reportName = 'Unprocessed Due SOA'
            dtreportHeader = 'As of ' + str(dt2.strftime("%B %d, %Y"))
            rptentries = SOA.objects.filter(SOAStatus='Open',CBDate__lte=dt2)
            
        
        book = xlwt.Workbook(encoding='ISO-8859-1', style_compression=1)
        #book = xlwt.Workbook()
        
        
        reportsheet = book.add_sheet(reportName)#Name of Excel Sheet
        
        
        #style = 'pattern: pattern solid, fore_colour blue;'
        headerstyle = 'font: name Arial, height 190, color-index black, bold on;'
        style = 'font: name Arial, color-index black, bold on;'
        gstyle = 'pattern: pattern solid, fore_colour green;'
        
        #reportsheet.write_merge(20,20,31,32,"SAMPLE" , xlwt.Style.easyxf())
        reportsheet.write_merge(0,0,0,5,nbudesc , xlwt.Style.easyxf(headerstyle))
        reportsheet.write_merge(1,1,0,5,reportName , xlwt.Style.easyxf(headerstyle))
        reportsheet.write_merge(2,2,0,5,dtreportHeader , xlwt.Style.easyxf(headerstyle))
        
        
        if reporttype == 1:
            reportsheet.row(5).write(1,"SOA Reference" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(2,"SOA Date" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(3,"Print Code" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(4,"Invoice Date" , xlwt.Style.easyxf(style))#Instead nga PRINTCODE DATE giusab nako as InvDate kay lisud na man kung kuhaon pa pud nako apil data sa gp
            reportsheet.row(5).write(5,"PO No." , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(6,"Invoice No." , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(7,"IM Amount" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(8,"SOA Amount" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(9,"Variance" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(10,"Username" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(11,"Vendor ID" , xlwt.Style.easyxf(style))
            
        elif reporttype == 2:
            reportsheet.row(5).write(1,"SOA Reference" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(2,"SOA Date" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(3,"Comeback Date" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(4,"Print Code" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(5,"Print Code Date" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(6,"Variance" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(7,"Vendor ID" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(8,"Vendor Name" , xlwt.Style.easyxf(style))
            
        elif reporttype == 3:
            reportsheet.row(5).write(1,"Vendor ID" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(2,"Vendor Name" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(3,"PO No." , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(4,"Invoice No." , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(5,"Document Date" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(6,"Document Amount" , xlwt.Style.easyxf(style))
            
        elif reporttype == 4:
            reportsheet.row(5).write(1,"SOA Reference" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(2,"SOA Date" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(3,"Invoice No." , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(4,"Invoice Amount" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(5,"PO No." , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(6,"Print Code" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(7,"Invoice Date" , xlwt.Style.easyxf(style))#Instead nga PRINTCODE DATE giusab nako as InvDate kay lisud na man kung kuhaon pa pud nako apil data sa gp
            reportsheet.row(5).write(8,"User ID" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(9,"Vendor ID" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(10,"Vendor Name" , xlwt.Style.easyxf(style))
        
        elif reporttype == 5:
            reportsheet.row(5).write(1,"SOA Reference" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(2,"SOA Date" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(3,"Invoice No." , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(4,"Invoice Amount" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(5,"PO No." , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(6,"Print Code" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(7,"Invoice Date" , xlwt.Style.easyxf(style))#Instead nga PRINTCODE DATE giusab nako as InvDate kay lisud na man kung kuhaon pa pud nako apil data sa gp
            reportsheet.row(5).write(8,"User ID" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(9,"Vendor ID" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(10,"Vendor Name" , xlwt.Style.easyxf(style))
        
        elif reporttype == 6:
            reportsheet.row(5).write(1,"SOA Reference" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(2,"SOA Date" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(3,"SOA Amount" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(4,"Comeback Date" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(5,"No. of Days Delayed" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(6,"Vendor ID" , xlwt.Style.easyxf(style))
            reportsheet.row(5).write(7,"Vendor Name" , xlwt.Style.easyxf(style))
            
        
        ###########################################
        #reportsheet.row(5).write(10,"NOTES" , xlwt.Style.easyxf(style))
        #reportsheet.write_merge(0,0,11,12,"SAMPLE" , xlwt.Style.easyxf(style))
        ###########################################
        
        
        for idx,entry in enumerate(rptentries):
            cellrow = reportsheet.row(idx + 6)
            
            if reporttype == 1:
                IMVariance = (entry.IMAmount - entry.Amount)
                cellrow.write(1,str(entry.SOANo_id))
                cellrow.write(2,str(entry.SOANo.SOADate))
                cellrow.write(3,str(entry.PRINTCODE))
                cellrow.write(4,str(entry.InvDate))
                cellrow.write(5,str(entry.PONo_id))
                cellrow.write(6,str(entry.InvNo))
                cellrow.write(7,str(entry.IMAmount))
                cellrow.write(8,str(entry.Amount))##SOA Amount daw but Amount sa Invoice ako gibutang
                cellrow.write(9,str(IMVariance))#IMVARIANCE
                cellrow.write(10,str(entry.SOANo.CreatedBy_id))
                cellrow.write(11,str(entry.SOANo.CreatedBy.vendorID))
                
            elif reporttype == 2:
                DTVariance = (entry.SOANo.CBDate - entry.InvDate).days
                cellrow.write(1,str(entry.SOANo_id))
                cellrow.write(2,str(entry.SOANo.SOADate))
                cellrow.write(3,str(entry.SOANo.CBDate))
                cellrow.write(4,str(entry.PRINTCODE))
                cellrow.write(5,str(entry.InvDate))
                cellrow.write(6,str(DTVariance))#DTVARIANCE
                cellrow.write(7,str(entry.SOANo.CreatedBy.vendorID))
                cellrow.write(8,str(entry.SOANo.CreatedBy.vendorName))
            
                
            elif reporttype == 3:
                cellrow.write(1,str(entry.SOANo.CreatedBy.vendorID))
                cellrow.write(2,str(entry.SOANo.CreatedBy.vendorName))
                cellrow.write(3,str(entry.PONo_id))
                cellrow.write(4,str(entry.InvNo))
                cellrow.write(5,str(entry.InvDate))
                cellrow.write(6,str(entry.Amount))
                
            elif reporttype == 4:
                cellrow.write(1,str(entry.SOANo_id))
                cellrow.write(2,str(entry.SOANo.SOADate))
                cellrow.write(3,str(entry.InvNo))
                cellrow.write(4,str(entry.LowerAmt))
                cellrow.write(5,str(entry.PONo_id))
                cellrow.write(6,str(entry.PRINTCODE))
                cellrow.write(7,str(entry.InvDate))
                cellrow.write(8,str(entry.SOANo.CreatedBy_id))
                cellrow.write(9,str(entry.SOANo.CreatedBy.vendorID))
                cellrow.write(10,str(entry.SOANo.CreatedBy.vendorName))
            
            elif reporttype == 5:
                cellrow.write(1,str(entry.SOANo_id))
                cellrow.write(2,str(entry.SOANo.SOADate))
                cellrow.write(3,str(entry.InvNo))
                cellrow.write(4,str(entry.LowerAmt))
                cellrow.write(5,str(entry.PONo_id))
                cellrow.write(6,str(entry.PRINTCODE))
                cellrow.write(7,str(entry.InvDate))
                cellrow.write(8,str(entry.SOANo.CreatedBy_id))
                cellrow.write(9,str(entry.SOANo.CreatedBy.vendorID))
                cellrow.write(10,str(entry.SOANo.CreatedBy.vendorName))    
                
            elif reporttype == 6:
                SOAAmount = sum(Details.objects.values_list('POTotalInvAmntEntrd',flat=True).filter(SOANo_id=entry.SOANo))
                DaysDelayed = abs((entry.CBDate - dt2).days)
                cellrow.write(1,str(entry.SOANo))
                cellrow.write(2,str(entry.SOADate))
                cellrow.write(3,str(SOAAmount))
                cellrow.write(4,str(entry.CBDate))
                cellrow.write(5,str(DaysDelayed))#dt2 - CBDate ang akoang gi set
                cellrow.write(6,str(entry.CreatedBy.vendorID))
                cellrow.write(7,str(entry.CreatedBy.vendorName))
                
                
        randstr = my_random_string()
        
        #book.save('D:/Projects/workspace/ECSS/ECS/static/reports/' + reportName + '(' + datetime.datetime.now() + ').xls')
        #book.save('/var/www/html/SMS/ERM/static/dl/alluser/DTR_Summary(' + summarydate + ')' + randstr + '.xls')
        
        #return HttpResponseRedirect('/static/dl/alluser/DTR_Summary(' + summarydate + ')' + randstr + '.xls')
        '''
        response = HttpResponse(content_type='application/force-download')
        response = HttpResponse(file_name.read())
        response['X-Sendfile'] = smart_str('/var/www/html/SMS/ERM/static/Reports/DTR_Summary(' + summarydate + ').xls')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('/reports/(' + reportName + '(' + str(datetime.datetime.now()) + ').xls')
        '''
        
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="' + reportName + '(' + str(datetime.date.today()) + ').xls"'
        book.save(response)
        return response
        
    #except:
        #msgNum = 06
        #message = "Opps! Something went wrong!"
        #return render_to_response('ecs_templates/message_info.html',{'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
     
        
def getremarks(request):
    SOANo = str(request.POST.get('SOANo'))
    remarksofSOA = Remarks.objects.filter(SOANo_id=SOANo)
    
    return render_to_response('ecs_templates/remarks.html',{'remarksofSOA':remarksofSOA,}, context_instance=RequestContext(request))



#************************************************************************#
#************************************************************************#
#************************************************************************#


def vendors(request):
    keyword = str(request.POST.get('keyword'))
    
    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    query = "SELECT ASNUM, ASNAME FROM APSUPP WHERE ASNUM LIKE '%" + keyword + "%' OR ASNAME LIKE '%" + keyword + "%' AND ASTYPE = '1' FETCH FIRST 500 ROWS ONLY"
    cursor.execute(query)
    vendors = cursor.fetchall()

    vendorlist = []
    for vend in vendors:
        vendorlist.append(str(vend.ASNUM) + ' - ' + str(vend.ASNAME).strip())
    cursor.close()
    cnxn.close()
        
    return HttpResponse(json.dumps(vendorlist), content_type = "application/json")
    
    








#************************************************************************#
#************************************************************************#
#************************************************************************#

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

def isHoliday(ddate,scheme):
    if Holidays.objects.filter(dateOfHoliday=ddate,schemeOfHoliday__in=[scheme,'ALL']):
        return True
    else:
        return False

#************************************************************************#
#************************************************************************#
#************************************************************************#

































##############################################################################

def export_to_xls(request): 
    
        user = str(request.session['User'])
    
        SOANo = str(request.POST.get('xlsSOANo'))
        
    
        book = xlwt.Workbook(encoding='ISO-8859-1', style_compression=1)
        
        soasheet = book.add_sheet(SOANo)#Name of Excel Sheet
        
        soainfo = SOA.objects.get(SOANo=SOANo)
    
        detinfo = Details.objects.filter(SOANo_id=SOANo,DStatus__in=['Open','Processed']) 
        
        invinfo = Invoice.objects.filter(PONo__SOANo_id=SOANo,IStatus__in=['Open','Processed'])#FFF
        totalamount = invinfo.aggregate(Sum('Amount'))['Amount__sum']
        
        
        
        style = 'pattern: pattern solid, fore_colour yellow;'
        gstyle = 'pattern: pattern solid, fore_colour green;'
        
        
        soasheet.row(0).write(0,"Supplier" , xlwt.Style.easyxf())
        soasheet.write_merge(0,0,1,4,soainfo.CreatedBy.vendorName , xlwt.Style.easyxf(style))
        
        soasheet.row(1).write(0,"Bill To" , xlwt.Style.easyxf())
        soasheet.write_merge(1,1,1,4,soainfo.SOABillTo.NBUDesc , xlwt.Style.easyxf(style))
        
        soasheet.row(2).write(0,"SOA No." , xlwt.Style.easyxf())
        soasheet.write_merge(2,2,1,4,SOANo , xlwt.Style.easyxf(style))
        
        soasheet.row(3).write(0,"SOA Date" , xlwt.Style.easyxf())
        soasheet.write_merge(3,3,1,4,soainfo.SOADate.strftime('%m/%d/%Y') , xlwt.Style.easyxf(style))
        
        
        soasheet.row(5).write(0,"PO No." , xlwt.Style.easyxf(gstyle))
        soasheet.row(5).write(1,"RC Date" , xlwt.Style.easyxf(gstyle))
        soasheet.row(5).write(2,"Invoice No." , xlwt.Style.easyxf(gstyle))
        soasheet.row(5).write(3,"Invoice Date" , xlwt.Style.easyxf(gstyle))
        soasheet.row(5).write(4,"Amount" , xlwt.Style.easyxf(gstyle))
        
        ###########################################
        
        for rnum,inv in enumerate(invinfo):
            cellrow = soasheet.row(rnum + 6)
            
            cellrow.write(0,inv.PONo_id)
            cellrow.write(1,inv.PONo.PODate.strftime('%m/%d/%Y'))
            cellrow.write(2,inv.InvNo)
            cellrow.write(3,inv.InvDate.strftime('%m/%d/%Y'))
            cellrow.write(4,inv.Amount)
            
            
        ###########################################
            
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=' + SOANo + '.xls'
        book.save(response)
        return response    
        
    
    
    

##############################################################################

def su_html_to_pdf_directly(request): 
    user = str(request.session['User'])
    
    SOANo = request.POST.get('printSOANo')
    
    if SOANo != None:
        request.session['suprintSOA'] = SOANo
        #DStatusFilters = ['Work','Open']
    else:
        SOANo = str(request.session['suprintSOA'])
        #DStatusFilters = ['Open']
            
    soainfo = SOA.objects.get(SOANo=SOANo)
    #soainfo.save()
    
     
    detinfo = Details.objects.filter(SOANo_id=SOANo,DStatus__in=['Open','Processed'])
    '''
    totalamount = detinfo.aggregate(Sum('Amount'))['Amount__sum']
    '''
    
    #######
    invinfo = Invoice.objects.filter(PONo__SOANo_id=SOANo,IStatus__in=['Open','Processed'])#FFF
    totalamount = invinfo.aggregate(Sum('Amount'))['Amount__sum']
    
    ## PREPARE CONTEXT ##
    ####send data to template
    data = {}
    data['totalamount'] = totalamount
    data['SOANo'] = SOANo
    data['soainfo'] = soainfo
    data['detinfo'] = detinfo
    data['invinfo'] = invinfo
    
    #############SET PAGE SIZE HERE#################
    #context = Context({'pagesize':'Letter',}) 
    #html = str(render_to_response('generateSOA.html', {'SOANo':SOANo, 'soainfo':soainfo,'detinfo':detinfo,}, context_instance=RequestContext(request)))
    
    
    ## RENDER HTML CONTENT THROUGH HTML TEMPLATE WITH CONTEXT
    #render_to_response('generateSOA.html',{'test':test,}, context_instance=RequestContext(request))
    template = get_template("ecs_templates/sugenerateSOA.html") 
    html = template.render(Context(data))
    
    #####################################
    '''
    # Write PDF to file
    file = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file,
            link_callback = link_callback)

    # Return PDF document through a Django HTTP response
    file.seek(0)
    pdf = file.read()
    file.close()            # Don't forget to close the file handle
    return HttpResponse(pdf, mimetype='application/pdf')
    '''
    #####################################
    result = StringIO.StringIO() 
    pdf = pisa.pisaDocument(StringIO.StringIO(html), dest=result) 
    if not pdf.err: 
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = ' filename=' + SOANo + '.pdf'
        return response
        #return HttpResponse(result.getvalue(), content_type='application/pdf') 
    else: 
        return HttpResponse('Errors')

##############################################################################
    
    
def ca_html_to_pdf_directly(request):
    SOANo = request.POST.get('SOANo')
    if SOANo != None:
        request.session['caprintSOA'] = SOANo
    else:
        SOANo = request.session['caprintSOA']
    
    soainfo = SOA.objects.get(SOANo=str(SOANo))
    '''
    soainfo.SOAStatus = 'Open'
    soainfo.save()
    
            
    detinfo = Details.objects.filter(SOANo_id=SOANo,DStatus__in=['Countered','Open']).order_by('id')
    totalamount = detinfo.aggregate(Sum('Amount'))['Amount__sum']
    
    for det in detinfo:
        det.DStatus = 'Open'
        det.save()
    '''
    
    ## PREPARE CONTEXT ##
    ####send data to template
    data = {}
    #data['totalamount'] = totalamount
    #data['SOANo'] = SOANo
    data['soainfo'] = soainfo
    #data['detinfo'] = detinfo
    
    #############SET PAGE SIZE HERE#################
    #context = Context({'pagesize':'Letter',}) 
    #html = str(render_to_response('generateSOA.html', {'SOANo':SOANo, 'soainfo':soainfo,'detinfo':detinfo,}, context_instance=RequestContext(request)))
    
    
    ## RENDER HTML CONTENT THROUGH HTML TEMPLATE WITH CONTEXT
    #render_to_response('generateSOA.html',{'test':test,}, context_instance=RequestContext(request))
    template = get_template("ecs_templates/cagenerateSOA.html") 
    html = template.render(Context(data))
    
    result = StringIO.StringIO() 
    pdf = pisa.pisaDocument(StringIO.StringIO(html), dest=result) 
    if not pdf.err: 
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=Ctrd-' + SOANo + '.pdf'
        return response
        #return HttpResponse(result.getvalue(), content_type='application/pdf') 
    else: 
        return HttpResponse('Errors')
    

##############################################################################

def pa_html_to_pdf_directly(request):
    SOANo = request.POST.get('SOANo')
    if SOANo != None:
        request.session['paprintSOA'] = SOANo
    else:
        SOANo = request.session['paprintSOA']
    
    soainfo = SOA.objects.get(SOANo=str(SOANo))
    
    detinfo = Details.objects.filter(SOANo_id=SOANo,DStatus__in=['CRS Ref.']).order_by('id')
    totalamount = detinfo.aggregate(Sum('Amount'))['Amount__sum']
    
    ## PREPARE CONTEXT ##
    ####send data to template
    data = {}
    data['totalamount'] = totalamount
    data['SOANo'] = SOANo
    data['soainfo'] = soainfo
    data['detinfo'] = detinfo
    
    #############SET PAGE SIZE HERE#################
    #context = Context({'pagesize':'Letter',}) 
    #html = str(render_to_response('generateSOA.html', {'SOANo':SOANo, 'soainfo':soainfo,'detinfo':detinfo,}, context_instance=RequestContext(request)))
    
    
    ## RENDER HTML CONTENT THROUGH HTML TEMPLATE WITH CONTEXT
    #render_to_response('generateSOA.html',{'test':test,}, context_instance=RequestContext(request))
    template = get_template("ecs_templates/pagenerateSOA.html") 
    html = template.render(Context(data))
    
    result = StringIO.StringIO() 
    pdf = pisa.pisaDocument(StringIO.StringIO(html), dest=result) 
    if not pdf.err: 
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=CRS-' + SOANo + '.pdf'
        return response
        #return HttpResponse(result.getvalue(), content_type='application/pdf') 
    else: 
        return HttpResponse('Errors')
    

##############################################################################




#************************************************************************#
#*************************** UNUSED FUNCTIONS ****************************#
#************************************************************************#


'''
def createSOA(request):
    #currUser = str(request.session['User'])
    user = str(request.session['User'])
    BAbbr = str(request.session['Branch'])
    branchinfo = Branch.objects.filter(BAbbr=BAbbr)
    
    seriesNo = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    SOANo = str(BAbbr) + seriesNo
    SOADate = datetime.datetime.now()
    
    nbu = request.POST.get('nbu')
    
    ##############################################
    if nbu == 994:
        0#set connection string for citifoods here
    else:
        cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
        cursor = cnxn.cursor()
    ##############################################
    
    SOA(SOANo=SOANo,SOADate=SOADate,SOALastUpdate=SOADate,SOAStatus='Open',SOABillTo_id=nbu,UserCode_id=currUser).save()
        
    message = "SOA has been successfully created."
    
    return HttpResponse(message) 
'''




