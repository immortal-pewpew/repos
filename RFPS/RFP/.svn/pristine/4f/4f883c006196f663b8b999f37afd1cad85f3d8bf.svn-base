from django import template
import datetime
import pyodbc
from RFP.helpers.numbers import num2name#Converter for Amount in Words

register = template.Library()

@register.filter
def hash3(dictionary, key):
    return dictionary.get(key, '')

@register.filter
def getdeptdesc(deptid):
    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    query = "SELECT TRIM(GLMNAM) AS GLMNAM FROM mmltslib.GLMAJR WHERE GLMAC1 ='" + str(deptid) + "'"    
    cursor.execute(query)
    deptname = str(cursor.fetchone()[0])
    deptcombi = str(deptid).zfill(3) + ' - ' + deptname.strip()
    cursor.close()
    return deptcombi


@register.filter
def getlocsdesc(locsid):
    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    query = "SELECT TRIM(STRNAM) AS STRNAM FROM MMLTSLIB.TBLSTR WHERE STRNUM ='" + str(locsid) + "'"    
    cursor.execute(query)
    locsname = str(cursor.fetchone()[0])
    locscombi = str(locsid).zfill(5) + ' - ' + locsname.strip()
    cursor.close()
    return locscombi

@register.simple_tag
def getaccttypedesc(nbu_id,dept,locs,accttypeid):
    cnxn = pyodbc.connect('DSN=mms_sku;UID=ICTAPPS;PWD=s3cur3344')
    cursor = cnxn.cursor()
    
    query = "SELECT TRIM(GLMDSC) AS GLMDSC FROM GLMSTR WHERE GLMCMP='" + str(nbu_id) + "' AND GLMAC1='" + str(dept) + "' AND GLMAC3='" + str(locs) + "' AND GLMAC2='" + str(accttypeid) + "'"    
    cursor.execute(query)
    accttypename = str(cursor.fetchone()[0])
    accttypecombi = str(accttypeid).zfill(3) + ' - ' + accttypename.strip()
    cursor.close()
    return accttypecombi

@register.filter
def towords(amount):
    pesos,cents = str(amount).split('.')
    
    pesoword = num2name(int(pesos)).upper()     
    centword = str(cents) + ' / 100 ONLY'
    return '**** ' + pesoword + ' AND ' + centword + ' ****'
    

@register.filter
def getdaydiff(pwdexpiry):
    today = datetime.date.today()
    daysdiff = (pwdexpiry - today).days
    
    return daysdiff

@register.filter
def fill3(tofill):
    return str(tofill).zfill(3)
    
@register.filter
def fill5(tofill):
    return str(tofill).zfill(5)


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
        


    

