from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^index/$', views.index, name='url_index'),
    url(r'^authenticate/$', views.authenticate, name='url_authenticate'),
    url(r'^main/?$', views.main, name='url_main'),
    url(r'^logout/$', views.logout, name='url_logout'),
    ################################################################################
    # GET DATA FROM DB
    url(r'^getrfp_no/$', views.getrfp_no, name='url_getrfp_no'),
    url(r'^getrfpdata/$', views.getrfpdata, name='url_getrfpdata'),
    url(r'^getvendorname/$', views.getvendorname, name='url_getvendorname'),
    
    #url(r'^getallvendor/$', views.getallvendor, name='url_getallvendor'),
    url(r'^getvendordetails/$', views.getvendordetails, name='url_getvendordetails'),
    url(r'^getvendorid/$', views.getvendorid, name='url_getvendorid'),
    
    url(r'^attachnotes/$', views.attachnotes, name='url_attachnotes'),
    url(r'^getnotes/$', views.getnotes, name='url_getnotes'),
    ################################################################################
    # FOR DROPDOWNS
    #url(r'^select_locations/$', views.select_locations, name='url_select_locations'),
    url(r'^get_dept_list/$', views.get_dept_list, name='url_get_dept_list'),
    url(r'^get_locs_list/$', views.get_locs_list, name='url_get_locs_list'),
    url(r'^get_coa_list/$', views.get_coa_list, name='url_get_coa_list'),
    ################################################################################
    # ADD / UPDATE RFP
    url(r'^processrequest/$', views.processrequest, name='url_processrequest'),
    ################################################################################
    # PROCEED WITH THE PROCESS / ACTION EVENT
    url(r'^actionevent/$', views.actionevent, name='url_actionevent'),
    ################################################################################
    # PRINT RFP
    url(r'^printRFP/$', views.printRFP, name='url_printRFP'),
    ################################################################################
    # PASSWORD AUTHENTICATION
    url(r'^pwdcheck/$', views.pwdcheck, name='url_pwdcheck'),
    ################################################################################
    url(r'^users/$', views.users, name='url_users'),
    url(r'^access/$', views.access, name='url_access'),
    ################################################################################
    #url(r'^vendor_lookup/$', views.vendor_lookup, name='url_vendor_lookup'),
    #url(r'^get_deptlocs_name/$', views.get_deptlocs_name, name='url_get_deptlocs_name'),
    
    
    #FOR ADMINISTRATOR
    url(r'^populate_user/$', views.populate_user, name='url_populate_user'),
    url(r'^populate_clerk/$', views.populate_clerk, name='url_populate_clerk'),
    url(r'^populate_locs/$', views.populate_locs, name='url_populate_locs'),
    url(r'^userinfo/$', views.userinfo, name='url_userinfo'),
    url(r'^getuserinfo/$', views.getuserinfo, name='url_getuserinfo'),
    url(r'^grantaccess/$', views.grantaccess, name='url_grantaccess'),
    url(r'^revokeaccess/$', views.revokeaccess, name='url_revokeaccess'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    
 
    
