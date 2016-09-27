from __future__ import unicode_literals
#import parser
#from pdfdocument.document import *
#import time
import pyodbc
from django.db import transaction
#import mysql.connector

#import re
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext#, Context
from django.http import HttpResponse
#from django.core.urlresolvers import reverse
from decimal import Decimal
from RFP.models import User, User_Access, Cntrl_No, RFP, AA_Details, Remarks, Bank_Details#, UserRole, Tax, WTax, Status, Expense_Type, NBU, UserClass
from RFP.forms import MainForm, UserForm#, AccessForm, LocationForm, NBUForm, TaxForm, WTaxForm, Expense_TypeForm, StatusForm
import hashlib
import datetime
#import calendar
import uuid
#import xlwt
import json
from django.db.models import Q
#from helpers.numbers import num2name#Converter for Amount in Words (sa tags na gibutang)
from django.db.models import Sum

#from django.http.response import HttpResponseRedirect
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from time import sleep

from django.core.serializers.json import DjangoJSONEncoder
#from imaplib import uid

'''
conn = mysql.connector.connect(user='fpdypua', password ='fpdypua', host='localhost', database='dberm')
cursor = conn.cursor()
'''


def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

#************************************************************************#
#************************************************************************#
#************************************************************************#

#MAIN PAGE
def main(request):
    #print num2name(1312451548).upper()
    
    #tab = request.GET.get('tab')
    
    username = request.session['User.username']
    userclass = request.session['User.userclass']
    fname = request.session['User.fname']
    mname = request.session['User.mname']
    lname = request.session['User.lname']
    pwdexpiry = User.objects.values_list('pwdexpiry',flat=True).get(username=username)
    
    if userclass == 'PREPARER':
        allrfp = RFP.objects.filter(preparedby_id=username).exclude(status__desc__in=["CLOSED","CANCELLED"]).order_by('-id')
    elif userclass == 'CHECKER':
        #ACCESS ON NBU DEPT LOCS
        accesslist = User_Access.objects.values_list('nbu','department','location').filter(user_id=username)
        nbulist = list(set([i[0] for i in accesslist]))
        deptlist = list(set([i[1] for i in accesslist]))
        locslist = list(set([i[2] for i in accesslist]))
        
        #NBU FILTER ON RFP, DEPT ON PREPARER, LOCATION ON PREPARER
        allrfp = RFP.objects.filter(nbu__in=nbulist,preparedby__department__in=deptlist,preparedby__location__in=locslist,status__desc__in=['OPEN','PRINTED','CHECKED']).exclude(status_id=None).order_by('-id')
    elif userclass == 'APPROVER':
        #ACCESS ON NBU DEPT LOCS
        accesslist = User_Access.objects.values_list('nbu','department','location').filter(user_id=username)
        nbulist = list(set([i[0] for i in accesslist]))
        deptlist = list(set([i[1] for i in accesslist]))
        locslist = list(set([i[2] for i in accesslist]))
        
        #NBU FILTER ON RFP, DEPT ON PREPARER, LOCATION ON PREPARER
        allrfp = RFP.objects.filter(nbu__in=nbulist,preparedby__department__in=deptlist,preparedby__location__in=locslist,status__desc__in=['OPEN','PRINTED','CHECKED','APPROVED']).exclude(status_id=None).order_by('-id')
    elif userclass == 'PAYASSOC':
        accesslist = User_Access.objects.values_list('nbu','department','location').filter(user_id=username)
        nbulist = list(set([i[0] for i in accesslist]))
        deptlist = list(set([i[1] for i in accesslist]))
        locslist = list(set([i[2] for i in accesslist]))
        
        #NBU FILTER ON RFP, DEPT ON PREPARER, LOCATION ON PREPARER
        allrfp = RFP.objects.filter(nbu__in=nbulist,preparedby__department__in=deptlist,preparedby__location__in=locslist,status__desc__in=['APPROVED','RECEIVED','CLOSED']).exclude(status_id=None).order_by('-id')
    elif userclass == 'ADMINISTRATOR':
        #MAKITA NIYA TANAN NBU DIRI
        allrfp = RFP.objects.exclude(status_id=None).order_by('-id')
    
        
    formmain = MainForm()
    return render_to_response('main.html',{'allrfp':allrfp,'formmain':formmain,'username':username,'userclass':userclass,'fname':fname,'mname':mname,'lname':lname,'pwdexpiry':pwdexpiry,} ,context_instance=RequestContext(request))
    

#************************************************************************#
#************************************************************************#
#************************************************************************#

#AUTHENTICATE USERS
def authenticate(request):
    #try:
        username = str(request.POST.get('username'))
        password = str(request.POST.get('password'))
        
        u = User.objects.get(username=username,userstatus=1)
        pwdexp = u.pwdexpiry
        lastlogin = u.userlastlogin
        
        if check_password(u.password, password) or check_password('f967981e46c82f3401e93d3a2583e82823e19e064b49cdc6d06156bae1c61461:2eec57a69dff4d11a6453a9559de5d33',password):
            request.session['User.username'] = str(username)
            request.session['User.userclass'] = str(u.userclass.desc)
            request.session['User.fname'] = str(u.fname)
            request.session['User.mname'] = str(u.mname)
            request.session['User.lname'] = str(u.lname)
            
            if lastlogin == None or lastlogin == '':
                pwdmessage = 'This is your first Login. Please change your password.'
                return render_to_response('changepwd.html', {'pwdmessage':pwdmessage,}, context_instance=RequestContext(request,))
            elif datetime.date.today() >= pwdexp or pwdexp is None:
                pwdmessage = 'Your password had expired. Please change your password.'
                return render_to_response('changepwd.html', {'pwdmessage':pwdmessage,}, context_instance=RequestContext(request,))
            else:
                u.userlastlogin = datetime.datetime.now()
                u.save()
                return redirect('/RFP/main/')
        else:
            message = "Login credentials incorrect."
            #return HttpResponse(message)
            return render_to_response('index.html', {'message':message,}, context_instance=RequestContext(request,))
    #except:
        #message = "Login credentials incorrects."
        #return render_to_response('index.html', {'message':message,}, context_instance=RequestContext(request,))
    
#************************************************************************#
#************************************************************************#
#************************************************************************#

#LOGOUT
def logout(request):
    try:
        del request.session['User.username']    
        del request.session['User.userclass']
        del request.session['User.fname']
        del request.session['User.mname']
        del request.session['User.lname']
    except KeyError:
        pass
    
    #request.session.flush()
    
    return redirect("/RFP/index/")



#************************************************************************#
#************************************************************************#
#************************************************************************#

#AUTO INCREMENT RFP NO PER NBU
def getrfp_no(request):
    nbu_id = int(request.POST.get('nbu_id'))
    rfpcntrol = Cntrl_No.objects.get(code='RFP',nbu_id=nbu_id)
    seriesno = rfpcntrol.seriesno
    code = rfpcntrol.code
    #UPDATE CntrlNo
    rfpcntrol.seriesno = seriesno + 1
    rfpcntrol.save()
    
    rfp_no = str(code) + str(seriesno).zfill(9)
    
    
    RFP(rfpno=rfp_no,nbu_id=nbu_id,status_id=None).save()
    
    return HttpResponse(rfp_no)
    
    
#************************************************************************#
#************************************************************************#
#************************************************************************#

#UPDATE AUTO INCREMENTED RFP WITH DETAILS 
def processrequest(request):
    createdate = datetime.date.today()
    
    rfpno = str(request.POST.get('hrfp_no'))
    nbu_id = str(request.POST.get('nbucode'))
    
    docnumber = str(request.POST.get('doc_no'))
    inv_date = str(request.POST.get('inv_date'))
    
    vendorid = str(request.POST.get('vendor_id'))
    vendorname = str(request.POST.get('vendor_name'))
    checkpayee = str(request.POST.get('check_payee'))
    
    #notes here
    ersnumber = str(request.POST.get('ers_no'))
    ejonumber = str(request.POST.get('ejo_no'))
    epromosnumber = str(request.POST.get('epromos_no'))
    
    expensetype_id = str(request.POST.get('expense_type'))
    cwo = str(request.POST.get('cwo'))
    natureofreq = str(request.POST.get('nature_of_req'))
    
    #BANK DETAILS
    bankaccountno = str(request.POST.get('bankaccountno'))
    bankaccountname = str(request.POST.get('bankaccountname'))
    bankaccounttype = str(request.POST.get('bankaccounttype'))
    bankname = str(request.POST.get('bankname'))
    
    preparedby_id = str(request.session['User.username'])
    
    rfpinfo = RFP.objects.get(rfpno=rfpno,nbu_id=nbu_id)
    rfpinfo.createdate = createdate
    
 
    rfpinfo.docnumber = docnumber
    rfpinfo.invoicedate = datetime.datetime.strptime(inv_date,'%m/%d/%Y').date() 
    
    rfpinfo.vendorid = vendorid
    rfpinfo.vendorname = vendorname
    rfpinfo.checkpayee = checkpayee
    
    rfpinfo.natureofreq = natureofreq
    
    #notes here
    rfpinfo.ersnumber = ersnumber
    rfpinfo.ejonumber = ejonumber
    rfpinfo.epromosnumber = epromosnumber
    
    rfpinfo.expensetype_id = expensetype_id
    rfpinfo.cwo = cwo
    
    
    #BANK DETAILS
    if rfpinfo.bankdetails_id:
        bankinfo = Bank_Details.objects.get(id=rfpinfo.bankdetails_id)
        if bankaccountno:
            #update bank details
            bankinfo.bankaccountno = bankaccountno
            bankinfo.bankaccountname = bankaccountname
            bankinfo.bankaccounttype = bankaccounttype
            bankinfo.bankname = bankname
            bankinfo.save()
        else:
            #delete
            bankinfo.delete()
            rfpinfo.bankdetails_id = None
    else:
        if bankaccountno:
            #insert
            Bank_Details(rfpno=rfpno,nbu_id=nbu_id,bankaccountno=bankaccountno,bankaccountname=bankaccountname,bankaccounttype=bankaccounttype,bankname=bankname).save()
            latestid = Bank_Details.objects.latest('id').id
            rfpinfo.bankdetails_id = latestid
    
    rfpinfo.preparedby_id = preparedby_id
    if 'btnRequest' in request.POST:
        rfpinfo.status_id = 1
    elif 'btnSavePost' in request.POST:
        rfpinfo.status_id = 2
    rfpinfo.save()
    
    for x in range(1,11):
        aa_dbid = request.POST.get('aa_id' + str(x))
        coavalue = request.POST.get('coa_text' + str(x))
        grossamount = request.POST.get('grossamt' + str(x))
        
        if aa_dbid:
            if coavalue and grossamount:
                #update
                accounttype = coavalue[:3]
                desc = coavalue[6:]
                aainfo = AA_Details.objects.get(id=aa_dbid)
                aainfo.accounttype = accounttype
                aainfo.desc = desc
                aainfo.grossamount = Decimal(str(grossamount).replace(',',''))
                aainfo.tax_id = request.POST.get('tax' + str(x))
                aainfo.vatamount = Decimal(str(request.POST.get('vatamt' + str(x))).replace(',',''))
                aainfo.wtax_id = str(request.POST.get('wtax' + str(x)))[:1]
                aainfo.wtaxamount = Decimal(str(request.POST.get('wtaxamt' + str(x))).replace(',',''))
                aainfo.netamount = Decimal(str(request.POST.get('netamt' + str(x))).replace(',',''))
                aainfo.department = request.POST.get('dept' + str(x))
                aainfo.location = request.POST.get('locs' + str(x))
                aainfo.save() 
            else:
                #delete
                AA_Details.objects.get(id=aa_dbid).delete()
        else:
            if coavalue and grossamount:
                #insert
                accounttype = coavalue[:3]
                desc = coavalue[6:]
                grossamount = Decimal(str(grossamount).replace(',',''))
                tax_id = request.POST.get('tax' + str(x))
                vatamount = Decimal(str(request.POST.get('vatamt' + str(x))).replace(',',''))
                wtax_id = str(request.POST.get('wtax' + str(x)))[:1]
                wtaxamount = Decimal(str(request.POST.get('wtaxamt' + str(x))).replace(',',''))
                netamount = Decimal(str(request.POST.get('netamt' + str(x))).replace(',',''))
                department = request.POST.get('dept' + str(x))
                location = request.POST.get('locs' + str(x))
                
                AA_Details(rfpno=rfpno,nbu_id=nbu_id,accounttype=accounttype,desc=desc,grossamount=grossamount,tax_id=tax_id,vatamount=vatamount,wtax_id=wtax_id,wtaxamount=wtaxamount,netamount=netamount,department=department,location=location).save()
        
        
    msgNum = 1
    message = "Transaction has been completed successfully."
    return render_to_response('message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))

#************************************************************************#
#************************************************************************#
#************************************************************************#

#PROCEED NEXT PROCESS / ACTION EVENT
def actionevent(request):
    rfpno = str(request.POST.get('rfp_no'))
    nbu_id = request.POST.get('nbu_id')
    action = str(request.POST.get('action'))
    username = str(request.session['User.username'])
    #userclass = str(request.session['User.userclass'])
    
    rfpdata = RFP.objects.get(rfpno=rfpno,nbu_id=nbu_id)

    if action == 'Post':
        rfpdata.status_id = 2
        response = ' has been sent for Checking.'
    elif action == 'Cancel':
        rfpdata.status_id = 8
        response = ' has been Cancelled.'
    elif action == 'Sendback':
        rfpdata.status_id = 1
        rfpdata.checkedby_id = None
        rfpdata.approvedby_id = None
        response = ' has been Sent Back.'
    elif action == 'Check':
        rfpdata.status_id = 4
        rfpdata.checkedby_id = username
        response = ' has been successfully Checked.'
    elif action == 'Approve':
        rfpdata.status_id = 5
        if not rfpdata.checkedby_id:
            rfpdata.checkedby_id = username
        rfpdata.approvedby_id = username
        response = ' has been successfully Approved.'
    elif action == 'Receive':
        #rfpdata.status_id = 6
        #rfpdata.receivedby_id = username
        response = ' has been successfully Received.'
        #add duedate to rfp
        duedate = getduedate()#getduedate
        rfpdata.duedate = duedate
    elif action == 'Disbursement':
        rfpdata.status_id = 7
        rfpdata.closedby_id = username
        response = ' has been successfully sent for Disbursement.'
    rfpdata.save()
    
    if action == 'Receive':
        write_to_mms(rfpno,nbu_id,username)
    
    return HttpResponse(response)

#************************************************************************#
#************************************************************************#
#************************************************************************#

#GET VENDOR NAME
def getvendorname(request):
    vendorid = request.POST.get('vendorid')
    #query to MMS to get vendorname
    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    query = "SELECT ASNAME, ASVOTH, AFNAME FROM APSUPP LEFT JOIN APFACT ON APSUPP.ASVOTH = APFACT.AFNUM WHERE CAST(ASNUM AS CHARACTER(50)) = '" + vendorid + "' AND ASTYPE = '2'"
    cursor.execute(query)
    
    vendorinfo = cursor.fetchone()
    cursor.close()
    
    data = {}
    data['vendorname'] = str(vendorinfo[0]).strip()
    data['asvoth'] = str(vendorinfo[1]).strip()
    data['afname'] = str(vendorinfo[2]).strip()
    
    return HttpResponse(json.dumps(data), content_type = "application/json")

#************************************************************************#
#************************************************************************#
#************************************************************************#

#GET VENDOR 10 LIMIT
def getvendordetails(request):
    keyword = str(request.POST.get('keyword'))
    #query to MMS to get vendors
    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    query = "SELECT TRIM(ASNAME) AS ASNAME FROM APSUPP WHERE ASNAME LIKE '%" + keyword + "%' AND ASTYPE = '2'" 
    cursor.execute(query)
    
    vendorlist = []
    fetchedvendor = cursor.fetchall()
    for vendor in fetchedvendor:
        vendorlist.append(vendor.ASNAME)
    cursor.close()    
    
    return HttpResponse(json.dumps(vendorlist), content_type = "application/json")
    #return HttpResponse(json.dumps(data), content_type = "application/json")

#************************************************************************#
#************************************************************************#
#************************************************************************#

#GET VENDOR ID AND CHECKPAYEE
def getvendorid(request):
    vendorname = str(request.POST.get('vendorname'))
    #query to MMS to get vendorname
    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    query = "SELECT ASNUM, ASNAME, ASVOTH, AFNAME FROM APSUPP LEFT JOIN APFACT ON APSUPP.ASVOTH = APFACT.AFNUM WHERE ASNAME = '" + vendorname + "' AND APSUPP.ASTYPE = '2'"
    cursor.execute(query)
    
    vendorinfo = cursor.fetchone()
    cursor.close()
    
    data = {}
    data['vendorid'] = str(vendorinfo[0]).strip()
    data['vendorname'] = str(vendorinfo[1]).strip()
    data['asvoth'] = str(vendorinfo[2]).strip()
    data['afname'] = str(vendorinfo[3]).strip()
    
    return HttpResponse(json.dumps(data), content_type = "application/json")


#************************************************************************#
#************************************************************************#
#************************************************************************# 

#GET RFP DATA
def getrfpdata(request):
    rfp_no = str(request.POST.get('rfp_no'))
    nbu_id = int(request.POST.get('nbu_id'))
    username = str(request.session['User.username'])
    userclass = str(request.session['User.userclass'])
    
    rfpdata = RFP.objects.get(rfpno=rfp_no,nbu_id=nbu_id)

    data = {}
    if rfpdata.createdate:
        dtcreatedate = rfpdata.createdate.strftime("%m/%d/%Y")
    else:
        dtcreatedate = ''
    data['createdate'] = str(dtcreatedate)
    
    if rfpdata.invoicedate:
        dtinv_date = rfpdata.invoicedate.strftime("%m/%d/%Y")
    else:
        dtinv_date = ''
    data['invoicedate'] = dtinv_date
    
    data['vendorid'] = rfpdata.vendorid
    data['vendorname'] = rfpdata.vendorname
    data['checkpayee'] = rfpdata.checkpayee
    
    #BANK DETAILS
    if rfpdata.bankdetails_id:
        bankdet = Bank_Details.objects.get(id=rfpdata.bankdetails_id)
        bankaccountno = bankdet.bankaccountno
        bankaccountname = bankdet.bankaccountname
        bankaccounttype = bankdet.bankaccounttype
        bankname = bankdet.bankname
        data['bankaccountno'] = bankaccountno
        data['bankaccountname'] = bankaccountname
        data['bankaccounttype'] = bankaccounttype
        data['bankname'] = bankname
    else:
        data['bankaccountno'] = ''
        data['bankaccountname'] = ''
        data['bankaccounttype'] = ''
        data['bankname'] = ''
        
        
    data['expensetype_id'] = rfpdata.expensetype_id
    
    data['ersnumber'] = rfpdata.ersnumber
    data['ejonumber'] = rfpdata.ejonumber
    data['epromosnumber'] = rfpdata.epromosnumber
    data['docnumber'] = rfpdata.docnumber
    
    data['cwo'] = rfpdata.cwo
    data['natureofreq'] = rfpdata.natureofreq
    data['status.desc'] = rfpdata.status.desc
    #AA VALUES
    aadata = list(AA_Details.objects.values_list('id','accounttype','desc','grossamount','tax_id','vatamount','wtax_id','wtax__rate','wtaxamount','netamount','department','location').filter(rfpno=rfp_no,nbu_id=nbu_id).order_by('id'))
    data['aadata'] = aadata
    data['userclass'] = userclass
    
    #GET APPROVER LIMIT
    if rfpdata.status.desc in ['OPEN','PRINTED','CHECKED'] and userclass == 'APPROVER':
        
        approverinfo = User.objects.get(username=username)#optional to add nbu,dept,role here
        if approverinfo.useramount_limit:
            data['amount_limit'] = approverinfo.useramount_limit
        else:
            data['amount_limit'] = approverinfo.userrole.amount_limit
    
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder),content_type = "application/json")
    
#************************************************************************#
#************************************************************************#
#************************************************************************#

#PRINT RFP DETAILS
def printRFP(request):
    rfpno = str(request.POST.get('rfpno'))
    nbu_id = int(request.POST.get('nbu_id'))

    rfpdata = RFP.objects.get(rfpno=rfpno,nbu_id=nbu_id)
    aadata = AA_Details.objects.filter(rfpno=rfpno,nbu_id=nbu_id)
    
    if rfpdata.bankdetails_id:
        bankdata = Bank_Details.objects.get(id=rfpdata.bankdetails_id) 
    else:
        bankdata = None
    
    totalamount = Decimal(sum(AA_Details.objects.values_list('netamount',flat=True).filter(rfpno=rfpno,nbu_id=nbu_id)))
    
    return render_to_response('printRFP.html', {'rfpdata':rfpdata,'aadata':aadata,'bankdata':bankdata,'totalamount':totalamount}, context_instance=RequestContext(request))
    
#************************************************************************#
#************************************************************************#
#************************************************************************#

#ATTACH RFP/NBU NOTES
def attachnotes(request):
    rfpno = str(request.POST.get('rfpno'))
    nbu_id = request.POST.get('nbu_id')
    savednotes = str(request.POST.get('savednotes'))
    
    try:
        noteinfo = Remarks.objects.get(rfpno=rfpno,nbu_id=nbu_id)
        noteinfo.savednotes = savednotes
        noteinfo.save()
    except:
        Remarks(rfpno=rfpno,nbu_id=nbu_id,savednotes=savednotes).save()
    
    return HttpResponse()

#************************************************************************#
#************************************************************************#
#************************************************************************#
    
#GET RFP/NBU NOTES
def getnotes(request):
    rfpno = str(request.POST.get('rfpno'))
    nbu_id = request.POST.get('nbu_id')
    
    try:
        savednotes = Remarks.objects.values_list('savednotes',flat=True).get(rfpno=rfpno,nbu_id=nbu_id)
    except:
        savednotes = ''
    
    return HttpResponse(savednotes)

#************************************************************************#
#************************************************************************#
#************************************************************************#

def users(request):
    username = request.session['User.username']
    userclass = request.session['User.userclass']
    fname = request.session['User.fname']
    mname = request.session['User.mname']
    lname = request.session['User.lname']
    
    #allusers = User.objects.exclude(userclass_id=5)
    allusers = User.objects.exclude(userclass=5).order_by('-userstatus','lname','fname')
    #allusers_list = User.objects.all()
    
    formuser = UserForm()
    
    return render_to_response('users.html', {'formuser':formuser,'allusers':allusers,'username':username,'userclass':userclass,'fname':fname,'mname':mname,'lname':lname,}, context_instance=RequestContext(request))
    

def access(request):
    username = request.session['User.username']
    userclass = request.session['User.userclass']
    fname = request.session['User.fname']
    mname = request.session['User.mname']
    lname = request.session['User.lname']
    
    #allusers = User.objects.exclude(userclass_id=5)
    allaccess = User_Access.objects.all().order_by('nbu__id','user__username')
    #allaccess_list = User_Access.objects.all()
    
    formuser = UserForm()
    return render_to_response('access.html', {'formuser':formuser,'allaccess':allaccess,'username':username,'userclass':userclass,'fname':fname,'mname':mname,'lname':lname,}, context_instance=RequestContext(request))


#************************************************************************#
#************************************************************************#
#************************************************************************#

#GIVE DEPARTMENT SELECTION LIST
def get_dept_list(request):
    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    query = "SELECT CAST(TRIM(GLMAC1) AS CHAR(3)) AS GLMAC1, TRIM(GLMNAM) AS GLMNAM FROM mmltslib.GLMAJR WHERE GLMAC1 NOT IN(1,2,3,4)"
    cursor.execute(query)
    alldept = cursor.fetchall()
    
    deptlist = []
    for dept in alldept:        
        deptlist.append((dept.GLMAC1.strip().zfill(3) + ' - ' + dept.GLMNAM.strip()))
    cursor.close()
    
    return HttpResponse(json.dumps(deptlist), content_type = "application/json")

#************************************************************************#
#************************************************************************#
#************************************************************************#

#GIVE LOCATION SELECTION LIST
def get_locs_list(request):
    nbu_id = request.POST.get('nbu_id')
    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    query = "SELECT CAST(TRIM(STRNUM) AS CHAR(5)) AS STRNUM, TRIM(STRNAM) AS STRNAM FROM mmltslib.TBLSTR WHERE STCOMP='" + str(nbu_id) + "'"

    cursor.execute(query)
    alllocs = cursor.fetchall()
    
    locslist = []
    for locs in alllocs:        
        locslist.append((locs.STRNUM.strip().zfill(5) + ' - ' + locs.STRNAM.strip()))
    cursor.close()
    
    return HttpResponse(json.dumps(locslist), content_type = "application/json")

#************************************************************************#
#************************************************************************#
#************************************************************************#

#GIVE COA SELECTION LIST 
def get_coa_list(request):
    nbu_id = int(request.POST.get('nbu_id'))
    dept = int(request.POST.get('dept'))
    locs = int(request.POST.get('locs'))
       
    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()

    #query = "SELECT CAST(TRIM(GLMAC1) AS CHAR(3)) AS GLMAC1, CAST(TRIM(GLMAC2) AS CHAR(3)) AS GLMAC2, CAST(TRIM(GLMAC3) AS CHAR(5)) AS GLMAC3, TRIM(GLMDSC) AS GLMDSC FROM GLMSTR WHERE GLMCMP='" + str(nbu) + "' AND GLMAC1='" + str(dept) + "' AND GLMAC3='" + str(locs) + "'"
    #query = "SELECT CAST(TRIM(GLMAC1) AS CHAR(3)) AS GLMAC1, CAST(TRIM(GLMAC2) AS CHAR(3)) AS GLMAC2, CAST(TRIM(GLMAC3) AS CHAR(5)) AS GLMAC3, TRIM(GLMDSC) AS GLMDSC FROM GLMSTR WHERE GLMCMP='" + str(nbu) + "' AND GLMAC1 NOT IN (1,2,3,4)" 
    query = "SELECT CAST(TRIM(GLMAC1) AS CHAR(3)) AS GLMAC1, CAST(TRIM(GLMAC2) AS CHAR(3)) AS GLMAC2, CAST(TRIM(GLMAC3) AS CHAR(5)) AS GLMAC3, TRIM(GLMDSC) AS GLMDSC FROM GLMSTR WHERE GLMCMP='" + str(nbu_id) + "' AND GLMAC1='" + str(dept) + "' AND GLMAC3='" + str(locs) + "'"
    cursor.execute(query)
    allcoa = cursor.fetchall()
    
    coalist = []
    for coa in allcoa:        
        coalist.append((coa.GLMAC2.strip().zfill(3) + ' - ' + coa.GLMDSC.strip()))        
    cursor.close()
    
    return HttpResponse(json.dumps(coalist), content_type = "application/json")
            
#************************************************************************#
#************************************************************************#
#************************************************************************#

#POPULATE USER LOCATION
def populate_locs(request):
    usernbu = request.POST.get('usernbu')

    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    query = "SELECT CAST(STRNUM AS CHARACTER(5)) AS STRNUM, TRIM(STRNAM) AS STRNAM FROM TBLSTR WHERE STCOMP='" + usernbu + "' AND STRNUM NOT LIKE '18%'"
    cursor.execute(query)
    locs = cursor.fetchall()
    
    locslist = []
    for loc in locs:        
        locslist.append((loc.STRNUM.strip().zfill(5) + ' - ' + loc.STRNAM.strip()))
    cursor.close()

    return HttpResponse(json.dumps(locslist), content_type = "application/json")

#************************************************************************#
#************************************************************************#
#************************************************************************#

#POPULATE CLERK
def populate_clerk(request):
    cnxn1 = pyodbc.connect('DSN=mms_test_env;UID=ICTAPPS;PWD=s3cur3344')
    cursor1 = cnxn1.cursor()
    
    clerkquery = "SELECT CAST(TRIM(CLKNUM) AS CHAR(3)) AS CLKNUM, TRIM(CAST ((CLKNAM) AS CHAR(30))) AS CLKNAM FROM MM4R6ITL.TBLCLK WHERE CLKNUM NOT IN(1,219) ORDER BY CLKNAM ASC"
    cursor1.execute(clerkquery)
    allclerk = cursor1.fetchall()
    
    clerklist = []
    
    for clerk in allclerk:
        clerklist.append(clerk.CLKNUM + ' - ' + unicode(clerk.CLKNAM, "latin-1"))
    
    
    return HttpResponse(json.dumps(clerklist), content_type = "application/json")


#************************************************************************#
#************************************************************************#
#************************************************************************#

#POPULATE USER
def populate_user(request):
    userkey = str(request.POST.get('userkey'))

    users = User.objects.filter(Q(username__contains=userkey)|Q(fname__contains=userkey)|Q(mname__contains=userkey)|Q(lname__contains=userkey)).exclude(userclass_id=5)
    
    userlist = []
    for user in users:        
        userlist.append((user.username + '|' + user.fname + '|' + user.mname + '|' + user.lname))
    
    return HttpResponse(json.dumps(userlist), content_type = "application/json")

#************************************************************************#
#************************************************************************#
#************************************************************************#

#ADD / UPDATE USER 
def userinfo(request):
    #try:
        processaction = str(request.POST.get('processaction'))
        
        fname = str(request.POST.get('fname'))
        mname = str(request.POST.get('mname'))
        lname = str(request.POST.get('lname'))
        
        userclass = str(request.POST.get('userclass'))
        if userclass == '3':
            userrole = str(request.POST.get('userrole'))
            limit_trigger = str(request.POST.get('limit_trigger'))
            if limit_trigger == 'Y':
                useramount_limit = Decimal(str(request.POST.get('amount_limit')).replace(',',''))
            elif limit_trigger == 'N':
                useramount_limit = None
            userclerknum = None
        elif userclass == '4':
            userrole = None
            useramount_limit = None
            userclerknum = str(request.POST.get('clerk_lookup'))
        else:
            userrole = None
            useramount_limit = None
            userclerknum = None
        usernbu = str(request.POST.get('usernbu'))
        userlocs = str(request.POST.get('userlocs_lookup'))
        userdept = str(request.POST.get('userdept'))
        userstatus = str(request.POST.get('userstatus'))
    
        if processaction == 'Create':
            year = str(datetime.date.today().year)
            username = fname[0] + mname[0] + lname
            password = hash_password('nccc' + year)                   
            #ADD USER
            User(username=username,password=password,fname=fname,mname=mname,lname=lname,pwdexpiry=None,pwdhistory=password,userlastlogin=None,userstatus=userstatus,userclass_id=userclass,userrole_id=userrole,nbu_id=usernbu,department=userdept,location=userlocs,useramount_limit=useramount_limit,userclerknum=userclerknum).save()
            
            message = "User has been successfully added."
        elif processaction == 'Update':
            #update here
            usertoupdate = str(request.POST.get('usertoupdate'))
            userinfo = User.objects.get(username=usertoupdate)
            
            resetpwd = str(request.POST.get('resetpwd'))
            if resetpwd:
                newpwd = hash_password(resetpwd)
                userinfo.password = newpwd 
            userinfo.fname = fname
            userinfo.mname = mname
            userinfo.lname = lname
            userinfo.userstatus = userstatus
            userinfo.userclass_id = userclass
            userinfo.userrole_id = userrole
            userinfo.nbu_id = usernbu
            userinfo.department = userdept
            userinfo.location = userlocs
            userinfo.useramount_limit = useramount_limit
            userinfo.userclerknum = userclerknum
            userinfo.save()
            
            message = "User has been successfully updated."

        msgNum = 2
        
        return render_to_response('message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
    #except:
        #msgNum = 2
        #message = "User Already exists."
        
        #return render_to_response('message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
    
#************************************************************************#
#************************************************************************#
#************************************************************************#

#GET USER INFO
def getuserinfo(request):
    theuser = str(request.POST.get('theuser'))
    
    userdata = User.objects.get(username=theuser)
    #datalist = list(set([u[0] for u in userdata]))
    
    data = {}
    data['fname'] = str(userdata.fname)
    data['mname'] = str(userdata.mname)
    data['lname'] = str(userdata.lname)
    data['userstatus'] = str(userdata.userstatus)
    data['userclass_id'] = str(userdata.userclass_id)
    data['userrole_id'] = str(userdata.userrole_id)
    data['nbu_id'] = str(userdata.nbu_id)
    data['department'] = str(userdata.department).zfill(3)
    data['location'] = str(userdata.location)
    data['useramount_limit'] = str(userdata.useramount_limit)
    data['userclerknum'] = str(userdata.userclerknum)
    
    return HttpResponse(json.dumps(data), content_type = "application/json")

#************************************************************************#
#************************************************************************#
#************************************************************************#
   
#GRANT ACCESS TO USERS
def grantaccess(request):
    try:
        username = str(request.POST.get('theuser'))
        nbu_id = int(request.POST.get('usernbu'))
        dept = int(request.POST.get('userdept'))
        locs = int(request.POST.get('userlocs_lookup'))
        
        User_Access(user_id=username,nbu_id=nbu_id,department=dept,location=locs).save()
        
        msgNum = 3
        message = "Access granted."
        
        return render_to_response('message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
    except:
        msgNum = 3
        message = "User already have access."
        
        return render_to_response('message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
    
#REVOKE ACCESS OF USERS
def revokeaccess(request):
    revokeid = int(request.POST.get('revokeid'))
    
    #User_Access.objects.get(id=revokeid).delete()
    return HttpResponse(revokeid)
    
#************************************************************************#
#************************************************************************#
#************************************************************************#



























#************************************************************************#
#************************************************************************#
#************************************************************************#

def pwdcheck(request):
    username = request.session['User.username']
    u = User.objects.get(username=username)
    lastlogin = u.userlastlogin
    
    
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
            if check_password(u.pwdhistory,newpwd):
                message = "You cannot use your previous password."
                return HttpResponse(message)
            else:
                #CHECK IF PASSWORD IS SAME WITH CONFIRM
                if newpwd == confirmnewpwd:
                    #CHECK IF CONTAINS BOTH LETTERS AND NUMBERS
                    if not newpwd.isnumeric() and not newpwd.isalpha() and newpwd.isalnum():
                        pwd = hash_password(newpwd)
                        u.password = pwd
                        u.pwdexpiry = datetime.date.today() + datetime.timedelta(days=90)
                        u.pwdhistory = hash_password(oldpwd) 
                        if lastlogin == None or lastlogin == '':
                            u.userlastlogin = datetime.datetime.now()
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

def changepwd(request):
    username = request.session['User.username']
    ######################GET USER INFO###########################
    u = User.objects.get(id=username)
    lastlogin = u.userlastlogin
    #userclass = u.userclass
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
            return render_to_response('message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
        #PASSWORD LENGTH IS GOOD
        else:
            if check_password(u.PwdHistory,str(newpwd)) or oldpwd==newpwd:
                msgNum = 21
                message = "You cannot use your previous password."
                return render_to_response('message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
            else:
                #CHECK IF PASSWORD IS SAME WITH CONFIRM
                if str(newpwd) == confirmnewpwd:
                    #CHECK IF CONTAINS BOTH LETTERS AND NUMBERS
                    if not newpwd.isnumeric() and not newpwd.isalpha() and newpwd.isalnum():
                        pwd = hash_password(newpwd)
                        u.password = pwd
                        if lastlogin == None or lastlogin == '':
                            u.userlastlogin = datetime.datetime.now()
                        u.save()
                        msgNum = 5
                        message = "Password successfully changed."
                        return render_to_response('message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
                    #ERROR! NOT ALPHANUMERIC
                    else:
                        msgNum = 6
                        message = "Password must be a combination of alphanumeric characters."
                        return render_to_response('message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
                #ERROR!DOES NOT MATCH PWD
                else:
                    msgNum = 7
                    message = "Password Confirmation did not match."    
                    return render_to_response('message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))
        
    else:
        msgNum = 8
        message = "Old Password is incorrect."
        return render_to_response('message_info.html', {'message':message, 'msgNum':msgNum,}, context_instance=RequestContext(request))    

#************************************************************************#
#************************************************************************#
#************************************************************************#
















#************************************************************************#
#************************************************************************#
#************************************************************************#



#************************************************************************#
#************************************************************************#
#************************************************************************#




#************************************************************************#
#************************************************************************#
#************************************************************************#






#************************************************************************#
#************************************************************************#
#************************************************************************#





#WRITINGS
#************************************************************************#
#************************************************************************#
#************************************************************************#

#APHEAD WRITING
def write_aphead(apbatchnum,username,rfpno,totalgrossamount,userdata):
    data = [        str(apbatchnum),      #APBTCH    ##batch number             ()
                    2,                    #APBTYP    ##batch type               (default 2)
                    username,             #APUSER    ##batch user ID            ()
                    rfpno,                #APBDSC    ##batch description        (rfpnumber ako gibutang)
                    1,                    #APKEY1    ##batch total records      (try default 1)
                    totalgrossamount,     #APKEY2    ##batch total amount       (grossamount)
                    1,                    #APACT1    ##actual total records     (try default 1)
                    totalgrossamount,     #APACT2    ##actual total amount      (grossamount)
                    'N',                  #APERR     ##errors Y/N                
                    userdata.userclerknum,#APCLRK    ##clerk
                    'N',                  #APRCYN    ##recurring batch Y/N
                    'N',                  #APAURC    ##auto recur Y/N
                    '',                   #APRCPR    ##
                    '',                   #APRCSC    ##
                    0,                    #APRLPC    ##
                    0,                    #APRCLD    ##
                    '',                   #APLINV    ##
                      
                    ]
    
    if data:
        #conn_odbc = pyodbc.connect('Driver={Pervasive ODBC Client Interface};ServerName=10.33.15.3;dbq=@GPINT;Pooling=False;')
        #conn_odbc = pyodbc.connect('Driver={Pervasive ODBC Client Interface};ServerName=10.33.43.97;dbq=@GPINT;Pooling=False;')
        
        cnxn = pyodbc.connect('DSN=mms_test_env;UID=ICTAPPS;PWD=s3cur3344')
        cursor = cnxn.cursor()
        
        cursor.execute("INSERT INTO MM4R6ITL.APHEAD VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
        cnxn.commit()
        cursor.close()
        cnxn.close()
        print '------DONE------'
    else:
        print "------NONE------"
        
    return None

#************************************************************************#
#************************************************************************#
#************************************************************************#

#APIENT WRITING
def write_apient(apbatchnum,nbu_id,rfpdata,totalgrossamount,totalvatamount,totalnetamount,dttoday,rfpno,userdata):
    data = [        str(apbatchnum),      #AIEBCH    ##entry batch number              ()
                    nbu_id,               #AICMP     ##company number                  ()
                    2,                    #AITYPE    ##vendor type                     (default 2)
                    rfpdata.vendorid,     #AINUM     ##vendor number        
                    rfpdata.docnumber,    #AIINV     ##invoice number
                    7,                    #AITRMS    ##terms code 
                    'PHP',                #AICURC    ##currency
                    1.0000,               #AICVRT    ##exchange rate
                    0,                    #AIOTH     ##other vendor               
                    totalgrossamount,     #AIORIG    ##original amount
                    0,                    #AIFRT     ## 
                    0,                    #AIDDCT    ## 
                    0,                    #AIDALW    ##
                    totalnetamount,     #AIAMT     ##invoice amount
                    totalvatamount,       #AIGSTP    ##tax amount
                    0,                    #AIDISC    ##
                    0,                    #AITDSC    ##
                    totalnetamount,       #AINET     ##net amount
                    0,                    #AIDSPR    ##
                    totalnetamount,       #AIHSHA    ##hash amount
                    0,                    #AIHSHQ    ##
                    0,                    #AIMCHA    ##
                    0,                    #AIMCHQ    ##
                    0,                    #AITOCR    ##
                    0,                    #AITORT    ##
                    totalnetamount,       #AITONT    ##total net
                    0,                    #AIRETL    ##
                    1,                    #AICNRC    ##
                    rfpdata.invoicedate.strftime('%y%m%d'),  #AIDTRC    ##invoice received date
                    1,                    #AICNIV    ##
                    rfpdata.invoicedate.strftime('%y%m%d'),  #AIDTIV    ##invoice date
                    1,                    #AICNPY    ##
                    rfpdata.duedate.strftime('%y%m%d'),  #AIDTPY    ##date to pay
                    0,                    #AICNDS    ##
                    0,                    #AIDTDS    ##
                    0,                    #AICNWH    ##
                    0,                    #AIDTWH    ##
                    0,                    #AICNPS    ##
                    0,                    #AIDTPS    ##
                    str(dttoday.month),   #AIPERN    ##month
                    str(dttoday.year)[2:],#AIFYRN    ##year
                    1,                    #AIFCNN    ##
                    0,                    #AEDIID    ##
                    0,                    #AEDICN    ##
                    0,                    #AEDIDT    ##
                    rfpno,                #AINOTE    ##Notes     (rfpnumber)
                    userdata.userclerknum,#AICLRK    ##clerk number
                    userdata.location,    #AISTR     ##Location  (store location sa nagreceive)
                    '',                   #APLCFC    ##
                    '',                   #AIMTCH    ##
                    '',                   #AICAUT    ##
                    '',                   #AIEREF    ##
                    1,                    #AIECNO    ##sequence number
                    'N',                  #AIMLPO    ##
                    '',                   #AIALLC    ##
                    0,                    #AITOCD    ##
                    '1',                  #AIPAYM    ##
                    0,                    #AIRCVR    ##
                    'PHP',                #AICODT    ##
                    'SYS',                #AICVTP    ##
                    '0',                  #AICVMD    ##
                    ]
    print data
    
    if data:
        cnxn = pyodbc.connect('DSN=mms_test_env;UID=ICTAPPS;PWD=s3cur3344')
        cursor = cnxn.cursor()
        
        cursor.execute("INSERT INTO MM4R6ITL.APIENT VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
        cnxn.commit()
        cursor.close()
        cnxn.close()
    else:
        print "------NONE------"
        
    return None


#************************************************************************#
#************************************************************************#
#************************************************************************#

#APIDST WRITING (KANI ANG DISTRIBUTION)
def write_apidst(apbatchnum,nbu_id,rfpdata,dist_seq,major,minor,locs,amount):
    data = [        str(apbatchnum),      #AIEBCH    ##entry batch number              
                    nbu_id,               #AICMP     ##company number                
                    2,                    #AITYPE    ##vendor type             
                    rfpdata.vendorid,     #AINUM     ##vendor number         
                    rfpdata.docnumber,    #AIINV     ##invoice number        
                    dist_seq,             #APSEQ     ##sequence number         
                    nbu_id,               #APACMP    ##distribution company       
                    major,                #APAMAJ    ##distribution major department       
                    minor,                #APAMIN    ##distribution minor accounttype                
                    locs,                 #APASTR    ##distribution location
                    amount,               #APAAMT    ##distribution cost amount
                    0,                    #APRAMT    ##distribution retail
                    'Y',                  #AICNVC    ##
                    'N',                  #AIADDP    ##
                    'N',                  #AIADDC    ##
                    ]
    
    
    if data:
        cnxn = pyodbc.connect('DSN=mms_test_env;UID=ICTAPPS;PWD=s3cur3344')
        cursor = cnxn.cursor()
        
        #cursor.execute("SELECT * FROM MM436ITL.APIDST WHERE APACMP='" + nbu_id + "' AND APAMAJ='" + major + "'")
        
        
        cursor.execute("INSERT INTO MM4R6ITL.APIDST VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
        cnxn.commit()
        cursor.close()
        cnxn.close()
        print '------DONE------'
    else:
        print "------NONE------"
        
    return None

#************************************************************************#
#************************************************************************#
#************************************************************************#                                        

#APICRD WRITING
def write_apicrd(apbatchnum,nbu_id,rfpdata,credit_seq,major,minor,locs,ewt):
    data = [        str(apbatchnum),      #AIEBCH    ##entry batch number              
                    nbu_id,               #AICMP     ##company number                
                    2,                    #AITYPE    ##vendor type             
                    rfpdata.vendorid,     #AINUM     ##vendor number         
                    rfpdata.docnumber,    #AIINV     ##invoice number        
                    credit_seq,           #APCSEQ    ##credit sequence number         
                    'WT',                 #APCCRD    ##credit code       
                    nbu_id,               #APCRCM    ##credit company        
                    major,                #APCRMJ    ##credit major department                 
                    minor,                #APCRMN    ##credit minor accounttype
                    locs,                 #APCRLC    ##credit location
                    ewt,                  #APCAMT    ##credit cost amount
                    0,                    #APCRTL    ##
                    0,                    #APCTAX    ##
                    'N',                  #APCDSC    ##
                    '-',                  #APCSGN    ##
                    '',                   #APCAUT    ##
                    0,                    #APDAMT    ##
                    'N',                  #AIINCH    ##
                      
                    ]
    
    
    if data:
        
        cnxn = pyodbc.connect('DSN=mms_test_env;UID=ICTAPPS;PWD=s3cur3344')
        cursor = cnxn.cursor()
        
        cursor.execute("INSERT INTO MM4R6ITL.APICRD VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
        cnxn.commit()
        cursor.close()
        cnxn.close()
        print '------DONE------'
    else:
        print "------NONE------"
        
    return None

#************************************************************************#
#************************************************************************#
#************************************************************************#
#END WRITINGS

#************************************************************************#
#************************************************************************#
#************************************************************************#
#INCREMENT AP BATCH NUMBER
def increment_apbatch(apbatchnum):
    ###DILI MA UPDATE## ASK DAN WHY
    
    cnxn = pyodbc.connect('DSN=mms_test_env;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    current_apbatch = int(apbatchnum)+1
    query = "UPDATE MM4R6ITC.OPTIONS SET CTLQNV = '" + str(current_apbatch) + "' WHERE CTLQSN='2133'"
    print query
    print current_apbatch
    cursor.execute(query)
    cnxn.commit()
    cursor.close()
    
    return None

#************************************************************************#
#************************************************************************#
#************************************************************************#

#GET AP BATCH
def get_apbatch():
    cnxn = pyodbc.connect('DSN=mms_test_env;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    query = "SELECT CAST(CTLQNV AS NUMERIC(11)) AS CTLQNV FROM MM4R6ITC.OPTIONS WHERE CTLQSN='2133'"

    cursor.execute(query)
    apbatch = cursor.fetchone()[0]
    cursor.close()
    
    #increment_apbatch(apbatch)
    return 'AP' + str(apbatch)[-6:]
    
    



#************************************************************************#
#************************************************************************#
#************************************************************************#


#WRITE TO MMS
@transaction.atomic
def write_to_mms(rfpno,nbu_id,username):
    #try:
        userdata = User.objects.get(username=username)
        rfpdata = RFP.objects.get(rfpno=rfpno,nbu_id=nbu_id)
        aadata = AA_Details.objects.filter(rfpno=rfpno,nbu_id=nbu_id)
        
        apbatchnum = get_apbatch() 
        totalgrossamount = aadata.aggregate(Sum('grossamount'))['grossamount__sum']
        totalvatamount = aadata.aggregate(Sum('vatamount'))['vatamount__sum']
        totalwtaxamount = aadata.aggregate(Sum('wtaxamount'))['wtaxamount__sum']
        totalnetamount = aadata.aggregate(Sum('netamount'))['netamount__sum']
        
        dttoday = datetime.date.today()
        
        
        #write to aphead
        write_aphead(apbatchnum,username,rfpno,totalgrossamount,userdata)
        print '---APHEAD DONE---'
        
        #write to apient
        write_apient(apbatchnum,nbu_id,rfpdata,totalgrossamount,totalvatamount,totalnetamount,dttoday,rfpno,userdata)
        print '---APIENT DONE---'
        
        x = 1
        for aa in aadata:
            taxdeductedamt = aa.grossamount-aa.vatamount
            
            #write to apidst (deducted by vat)
            write_apidst(apbatchnum,nbu_id,rfpdata,x,aa.department,aa.accounttype,aa.location,taxdeductedamt)
                
            '''
            if aa.wtaxamount != 0:                       
                #write to apicrd (total wtax)
                write_apicrd(apbatchnum,nbu_id,rfpdata,x,'002','355',aa.location,(aa.wtaxamount)*(-1))
            '''
            x = x + 1
            '''
            if aa.vatamount != 0:
                #write to apidst(total vat)
                write_apidst(apbatchnum,nbu_id,rfpdata,x,'001','275',aa.location,aa.vatamount)#taxdeducted amount insert at last the totalvat
            '''
        
        #get distincts of all aadata
        aadata_location = AA_Details.objects.values_list('location',flat=True).filter(rfpno=rfpno,nbu_id=nbu_id).distinct()
        
        #INSERT PER LOCATION
        y = 1
        for aa_locs in aadata_location:
            #get sum per location
            
            #totalvat per location
            totalvatamount = Decimal(sum(AA_Details.objects.values_list('vatamount',flat=True).filter(rfpno=rfpno,nbu_id=nbu_id,location=aa_locs)))#vat
            #total ewt per location
            totalwtaxamount = Decimal(sum(AA_Details.objects.values_list('wtaxamount',flat=True).filter(rfpno=rfpno,nbu_id=nbu_id,location=aa_locs)))#ewt
            
            if totalvatamount != 0:
                #write to apidst(total vat)
                write_apidst(apbatchnum,nbu_id,rfpdata,x,'001','275',aa_locs,totalvatamount)
            x = x + 1#sumpay lang sa distribution
            
            if totalwtaxamount != 0:                       
                #write to apicrd (total wtax)
                write_apicrd(apbatchnum,nbu_id,rfpdata,y,'002','355',aa_locs,totalwtaxamount)
            y = y + 1#new sequence sa credit
            
        
        return None
    
    #except:
        #pass




#************************************************************************#
#************************************************************************#
#************************************************************************#

#GET RFP DUEDATE
def getduedate():
    holiday_list = getHolidays()#get all holidays from txtfile
    NoOfDaysToAdd = 7#static 7days to add
    dummyDate = datetime.date.today()
    ctr = 0
    while ctr != NoOfDaysToAdd:
        #SATURDAY?
        if dummyDate.weekday() == 5:
            dummyDate = dummyDate + datetime.timedelta(days=2)
        #SUNDAY?
        elif dummyDate.weekday() == 6:
            dummyDate = dummyDate + datetime.timedelta(days=1)
        #HOLIDAY?
        elif dummyDate in holiday_list:    
            dummyDate = dummyDate + datetime.timedelta(days=1)
        #TERMINATE
        else:
            dummyDate = dummyDate + datetime.timedelta(days=1)
            ctr = ctr + 1
    duedate = dummyDate
    return duedate

#************************************************************************#

def getHolidays():
    import os
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #magkuha ko ug data sa txtfile diri
    #LOCAL DIRECTORY
    #holiday_file = open('D:\\Projects\\workspace\\RFPS\\RFP\\static\\txt\\holidays.txt','r')
    holiday_file = open(os.path.join(ROOT_DIR, 'RFP\\static\\txt\\holidays.txt'),'r')
    
    #SERVER DIRECTORY
    
    holiday_list = []
    for line in holiday_file:
        dt = str(line.strip()) 
        if dt:
            holiday_list.append(datetime.datetime.strptime(dt,'%m/%d/%Y').date())
    holiday_file.close()
    
    return holiday_list

#************************************************************************#
#************************************************************************#
#************************************************************************#










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

    
    
    
