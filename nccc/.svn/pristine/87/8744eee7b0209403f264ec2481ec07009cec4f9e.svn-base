from django import template
import datetime
from src.ECS.models import Invoice, GPData, Remarks

from decimal import Decimal
import pyodbc

register = template.Library()

@register.filter
def hash3(dictionary, key):
    return dictionary.get(key, '')


@register.filter
def getdaydiff(pwdexpiry):
    today = datetime.date.today()
    daysdiff = (pwdexpiry - today).days
    
    return daysdiff


@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )
    
@register.filter
def holidaynumbering(ctr,num):
    return int(ctr + ((num-1)*25))
      
@register.filter
def invsOfPO(PONo,SOANo):
    allinvofPO = Invoice.objects.filter(PONo_id=PONo,SOANo_id=SOANo)#.exclude(IStatus='Denied')
    return allinvofPO

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def usernumbering(ctr,num):
    return int(ctr + ((num-1)*25))

@register.filter
def accessnumbering(ctr,num):
    return int(ctr + ((num-1)*25))

@register.simple_tag
def getIMAmount(InvNo,nbu,PONo,vendor):
    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    invquery = "SELECT ITFMCH, ITFSTP, ITFDSC FROM ITFLIB.ITFAPI WHERE TRIM(ITFINV) LIKE '%" + InvNo + "%' AND ITFCMP = '" + str(nbu) + "' AND ITFPNO = '" + str(PONo) + "' AND ITFTTYP = 'OUT' AND ITFNUM = '" + vendor + "'"
    cursor.execute(invquery)
    
    try:
        iDATA = cursor.fetchone()
        cursor.close()
        ITFMCH = Decimal(iDATA[0])
        ITFSTP = Decimal(iDATA[1])
        ITFDSC = Decimal(iDATA[2])
    
        IMAmount = ITFMCH + ITFSTP - ITFDSC
    except:
        IMAmount = None
    
    return IMAmount
    
    
@register.filter    
def totalinvamt(SOANo):  
    invamtsum = sum(Invoice.objects.values_list('Amount',flat=True).filter(SOANo_id=SOANo).exclude(Amount=None))
    return invamtsum

 
@register.filter    
def totalimamt(SOANo):  
    imamtsum = sum(Invoice.objects.values_list('IMAmount',flat=True).filter(SOANo_id=SOANo).exclude(IMAmount=None))
    return imamtsum


@register.filter    
def totalloweramt(SOANo):  
    loweramtsum = sum(Invoice.objects.values_list('LowerAmt',flat=True).filter(SOANo_id=SOANo).exclude(LowerAmt=None))
    return loweramtsum
    
@register.filter
def withremarks(SOANo):
    remarkslist = Remarks.objects.filter(SOANo_id=SOANo)
    return remarkslist
    

'''
@register.filter
def gpgetPAYAMOUNT(invno,vendorID):
    invno = '36236'
    vendorID = '306585'
    PAYAMOUNT = GPData.objects.values_list('PAYAMOUNT',flat=True).filter(DOCNO=invno,VENDORID=vendorID)
    if PAYAMOUNT:
        return PAYAMOUNT[0]
    else:
        return "-"


@register.filter
def gpgetPRINTCODE(invno,vendorID):
    invno = '36236'
    vendorID = '306585'
    PRINTCODE = GPData.objects.values_list('PRINTCODE',flat=True).filter(DOCNO=invno,VENDORID=vendorID)
    if PRINTCODE:
        return PRINTCODE[0]
    else:
        return ''
'''
'''
@register.filter
def getvendorName(vendorID):
    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    query = "SELECT ASNAME FROM APSUPP WHERE ASNUM ='" + vendorID + "'" 
    cursor.execute(query)
    name = cursor.fetchall()
    
    return name[0][0]
'''
