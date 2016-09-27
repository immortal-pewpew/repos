/**
 * @author fdypua
 */

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$(document).ready(function(){

// var d = new Date()
// var monthnum = d.getMonth();
// document.getElementById('viewmonth').value=monthnum;
    	
		
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$('input#hmonth').val($('select#viewmonth').val());
$('input#hyear').val($('select#viewyear').val());
$('input#hcutoff').val($('select#cutofftype').val());

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

var vl;
var sil;
var sl;
var aa;
var dt;
			
			

$(function() {
	
	$("#dialogdelconfirm").dialog({
	      modal: true,
	      autoOpen: false,
	      closeOnEscape: false,
	      position: { my: 'top', at: 'top+150',of: window },
	      buttons: {
	        Yes: function() {
				$("#dialogdelconfirm").dialog("close");
				
				var uid = $('input#huidedit').val();	
				
				$.ajax({
			        url : "/ERM/deleteuser/", // the endpoint
			        type : "post", // http method
			        data : { uid: uid }, // data sent with the post request
				
					success : function(data) {
			        	window.location.replace('/ERM/addUser/');
			        	},
			
			        // handle a non-successful response
			    	error : function(data) {
			        	alert('Delete Error! Something went wrong.');
			        	}
					});
				
	        	},
	        Cancel: function() {
	        	//event.preventDefault();
	            $("#dialogdelconfirm").dialog("close");
	        	}
			}
	
	});//dialog end
	
	
	$("#dialogconfirmLastYearVL").dialog({
	      modal: true,
	      autoOpen: false,
	      closeOnEscape: false,
	      position: { my: 'top', at: 'top+150',of: window },
	      open: function(event, ui) { $(".ui-dialog-titlebar-close", ui.dialog | ui).hide();
	      			}, 
	      buttons: {
	        Yes: function() {
				$("#dialogconfirmLastYearVL").dialog("close");
				callback(true,vl,sil,sl,aa,dt);
	        	},
	        No: function() {
	        	//event.preventDefault();
	            $("#dialogconfirmLastYearVL").dialog("close");
	            callback(false,vl,sil,sl,aa,dt);
	        	}
			}
	
	});//dialog end
	
	function callback(response,vl,sil,sl,aa,dt){
		//----------------------------------------------//
		//             AJAX for Leave Save              //
		//----------------------------------------------//
		
		$.ajax({
	        url : "/ERM/saveleave/", // the endpoint
	        type : "post", // http method
	        data : { vl: vl, sil: sil, sl:sl, aa: aa, dt: dt, response: response,}, // data sent with the post request
			
			// handle a successful response
	        success : function(data) {
	        	$('#summary').html(data);
	        	},
	
	        // handle a non-successful response
	        error : function(data) {
	        	
	        	}
			 });
		}
	////////////////////////////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////

	
	//DIALOG CHANGE PASSWORD
		$("#dialogchangepwd").dialog({
	      modal: true,
	      autoOpen: false,
	      position: { my: 'top', at: 'top+100',of: window },
	      
	      buttons: {
	        Ok: function() {
				//ajax check for filters
				var oldpwd = $('input#oldpwd').val();
				var newpwd = $('input#newpwd').val();
				var confirmnewpwd = $('input#confirmnewpwd').val();
				
				$.ajax({
			        url : "/ERM/pwdcheck/", // the endpoint
			        type : "post", // http method
			        data : { oldpwd:oldpwd, newpwd:newpwd, confirmnewpwd:confirmnewpwd }, // data sent with the post request
					
					// handle a successful response
			        success : function(data) {
			        	if (data == 'Successful.'){
				        	$("#dialogchangepwd").dialog("close");
				        	$("#dialogpwdchngsuccess").dialog("open");
				        	}
			        	else{
				        	document.getElementById('pwdnote').innerHTML = data;
				        	}
			        	},
			
			        // handle a non-successful response
			        error : function(data) {
			        	
			        	}
					 });
				
				
	        },
	        Cancel: function() {
	        	//event.preventDefault();
	            $("#dialogchangepwd").dialog("close");
	        }
	        
	      },
	      beforeClose: function(){
	        //event.preventDefault();
	        
	      }
	    });
	    
	////////////////////////////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////

	    //CHANGE PWD NOTIF
	    $("#dialogpwdchngsuccess").dialog({
	      modal: true,
	      autoOpen: false,
	      closeOnEscape: false,
	      position: { my: 'top', at: 'top+150',of: window },
	      open: function(event, ui) { $(".ui-dialog-titlebar-close", ui.dialog | ui).hide();
	      			}, 
	      buttons: {
	        Ok: function() {
				var isadmin = $('input#isadmin').val();
				$("#dialogpwdchngsuccess").dialog("close");
				if (isadmin == '2'){
					window.location.replace('/ERM/periodreports/');
				} 
				else {
					window.location.replace('/ERM/main/');
				}
	        },
	        
	      },
	      beforeClose: function(){
	        //event.preventDefault();
	        
	      }
	      
	    });
	    
	////////////////////////////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////	    
	    
	    //DIALOG ADD USER
	    $("#dialogadduser").dialog({
	      modal: true,
	      autoOpen: false,
	      position: { my: 'top', at: 'top+20',of: window },
	      width: 750,
	      buttons: {
	        Ok: function() {
				var uid = $('input#uid').val();
				var FName = $('input#FName').val();
				var MName = $('input#MName').val();
				var LName = $('input#LName').val();
				//var Approver = $('select#Approver').val();
				//var isApprover = $('select#isApprover').val();
				//var Division = $('input#Division').val();
				//var Dept = $('input#Dept').val();
				var Branch = $('select#Branch').val();
				//var SSSNo = $('input#SSSNo').val();
				//var PagIBIGNo = $('input#PagIBIGNo').val();
				//var PhilHealthNo = $('input#PhilHealthNo').val();
				
				
				if ((uid == '')||(FName == '')||(MName == '')||(LName == '')||(Branch == '')){
					document.getElementById('addnote').innerHTML = 'Please fill all required fields.<br />(Indicated with asterisks.)';
					$('input#FName').focus();
				}
				else{
					$('form#frmAddUser').submit();
					$("#dialogadduser").dialog("close");	
				}
				
				
				
	        },
	        Cancel: function() {
	            $("#dialogadduser").dialog("close");
	        }
	        
	      },
	      beforeClose: function(){
	        //event.preventDefault();
	        
	      }
	    
	      
	    });
	    
		
	////////////////////////////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////
		
		//DIALOG ADD USER
	    $("#dialogedituser").dialog({
	      modal: true,
	      autoOpen: false,
	      position: { my: 'top', at: 'top+20',of: window },
	      width: 1000,
	      buttons: {
	        Ok: function() {
				var FName = $('input#FNameedit').val();
				var MName = $('input#MNameedit').val();
				var LName = $('input#LNameedit').val();
				//var Approver = $('select#Approver').val();
				//var isApprover = $('select#isApprover').val();
				//var Division = $('input#Division').val();
				//var Dept = $('input#Dept').val();
				var Branch = $('select#Branchedit').val();
				//var SSSNo = $('input#SSSNo').val();
				//var PagIBIGNo = $('input#PagIBIGNo').val();
				//var PhilHealthNo = $('input#PhilHealthNo').val();
				
				
				if ((FName == '')||(MName == '')||(LName == '')||(Branch == '')){
					document.getElementById('editnote').innerHTML = 'Please fill all required fields.<br />(Indicated with asterisks.)';
				}
				else{
					$('form#frmUpdateuser').submit();
					$("#dialogedituser").dialog("close");	
				}
				
	        },
	        Cancel: function() {
	            $("#dialogedituser").dialog("close");
	        }
	        
	      },
	      beforeClose: function(){
	        //event.preventDefault();
	        
	      }
	    
	      
	    });
	
	////////////////////////////////////////////////////////////////////////
	////////////////////////////////////////////////////////////////////////
		//DIALOG ADD USER
	    $("#dialogaddholiday").dialog({
	      modal: true,
	      autoOpen: false,
	      position: { my: 'top', at: 'top+100',of: window },
	      width: 350,
	      buttons: {
	        Ok: function() {
				var dateOfHoliday = $('input#dateOfHoliday').val();
				var Description = $('textarea#Description').val();
				
				if ((dateOfHoliday == '')||(Description == '')){
					document.getElementById('holidaynote').innerHTML = 'Please fill all fields.';
				}
				else{
					$('form#frmAddHoliday').submit();
					$("#dialogaddholiday").dialog("close");	
				}
				
				
				
	        },
	        Cancel: function() {
	            $("#dialogaddholiday").dialog("close");
	        }
	        
	      },
	      beforeClose: function(){
	        //event.preventDefault();
	        
	      }
	    
	      
	    });	    
	});


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$('#userlink').on('click', function(event){
	event.preventDefault();
	$("#dialogadduser").dialog("open");
	//$("input[type='text']").val('');
	//$("input[type='number']").val('');
	$("input.input-sm").val('');
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//EDIT
$('.editlink').on('click', function(event){
	event.preventDefault();
	//ajax get data of user
	var uid = $(this).attr('id');
	$('input#huidedit').val(uid);
	
	$.ajax({
        url : "/ERM/getuserdata/", // the endpoint
        type : "post", // http method
        data : { uid:uid, }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$("#dialogedituser").dialog("open");
			$("input[type='text']").val('');
			document.getElementById('userid').innerHTML = uid;
			
			$('input#FNameedit').val(data.FName);
			$('input#MNameedit').val(data.MName);
			$('input#LNameedit').val(data.LName);
			$('select#Genderedit').val(data.Gender);
			$('select#Approveredit').val(data.Approver);
			$('input#Divisionedit').val(data.Division);
			$('input#Deptedit').val(data.Dept);
			$('select#Branchedit').val(data.Branch);
			$('input#SSSNoedit').val(data.SSSNo);
			$('input#PagIBIGNoedit').val(data.PagIBIGNo);
			$('input#PhilHealthNoedit').val(data.PhilHealthNo);
			$('select#isApproveredit').val(data.isadmin);
			$('select#usrstatusedit').val(data.status);
			
			$('input#Leveledit').val(data.Level);
			$('input#RegDateedit').val(data.RegDate);
			$('input#TINNoedit').val(data.TINNo);
			$('input#TaxCodeedit').val(data.TaxCode);
			$('input#TaxExemptionedit').val(data.TaxExemption);
			$('input#Designationedit').val(data.Designation);
			$('select#isProfFeeedit').val(data.isProfFee);
			$('input#HomeAddressedit').val(data.HomeAddress);
			$('input#Emailedit').val(data.Email);
			$('select#CivilStatusedit').val(data.CivilStatus);
			$('input#BDateedit').val(data.BDate);
			$('select#BloodTypeedit').val(data.BloodType);
			$('input#Religionedit').val(data.Religion);
			$('input#Citizenshipedit').val(data.Citizenship);
			
			if (data['withAvatar'] == 'Yes'){
				document.getElementById('user_image').innerHTML = '<img src="/media/avatars/' + uid + '.jpg" width="100%" height="100%"/>';
				}
			else{
				document.getElementById('user_image').innerHTML = '<img src="/media/avatars/default_avatar.jpg" width="100%" height="100%"/>';
			}	
			
			$('input#FNameedit').focus();
			
        	},

        // handle a non-successful response
    	error : function(data) {
        	
        	}
		 });
	 
});
















////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$('#holidaylink').on('click', function(event){
	event.preventDefault();
	$("#dialogaddholiday").dialog("open");
	$("input[type='text']").val('');
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$('#pwdlink').on('click', function(event){
	event.preventDefault();
	$("#dialogchangepwd").dialog("open");
	$("input[type='password']").val('');
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


//pmspager
$('input#pmspager').on('focusout', function(event){
	var page = $(this).val();
	window.location.replace("/ERM/assocpms/?page=" + page);
});

//pmspager
$('input#pmspager').on('keydown', function(event){
	if(event.keyCode == 13){
		var page = $(this).val();
		window.location.replace("/ERM/assocpms/?page=" + page);
	}
});

///////////////////////////////////////////////////////////////////////

//userpager
$('input#userpager').on('focusout', function(event){
	var page = $(this).val();
	window.location.replace("/ERM/addUser/?page=" + page);
});

//userpager
$('input#userpager').on('keydown', function(event){
	if(event.keyCode == 13){
		var page = $(this).val();
		window.location.replace("/ERM/addUser/?page=" + page);
	}
});

///////////////////////////////////////////////////////////////////////

//holidaypager
$('input#holidaypager').on('focusout', function(event){
	var page = $(this).val();
	window.location.replace("/ERM/addHoliday/?page=" + page);
});

//holidaypager
$('input#holidaypager').on('keydown', function(event){
	if(event.keyCode == 13){
		var page = $(this).val();
		window.location.replace("/ERM/addHoliday/?page=" + page);
	}
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//approvalpager
$('input#approvalpager').on('focusout', function(event){
	var page = $(this).val();
	window.location.replace("/ERM/approval/?page=" + page);
});

//holidaypager
$('input#approvalpager').on('keydown', function(event){
	if(event.keyCode == 13){
		var page = $(this).val();
		window.location.replace("/ERM/approval/?page=" + page);
	}
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$('input#postchckd').on('click', function(event){
	$("#dialogconfirmPOST").dialog("open");
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


$('#genunders').on('click', function(event){
	$.ajax({
        url : "/ERM/pmsadd/", // the endpoint
        type : "post", // http method
        data : { }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	if (data == 'PMS added.'){
	        	window.location.reload();
	        	}
        	else{
	        	alert(data);
	        	}
        	},

        // handle a non-successful response
    	error : function(data) {
        	
        	}
		 });
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$("body").on("click","input#deluser",function(event) {
	event.preventDefault();
	$("#dialogdelconfirm").dialog("open");
	/*
	var uid = $('input#huidedit').val();	
	
	$.ajax({
        url : "/ERM/deleteuser/", // the endpoint
        type : "post", // http method
        data : { uid: uid }, // data sent with the post request
	
		success : function(data) {
        	window.location.replace('/ERM/addUser/');
        	},

        // handle a non-successful response
    	error : function(data) {
        	alert('Delete Error! Something went wrong.');
        	}
		});
	*/
});


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//WALA NANI GIGAMIT
/*
//HIDE 
$('select.pmsScore').on('click', function(event){
	var id = $(this).attr('id');
	var scorevalue = $(this).attr('score');
	if (scorevalue == '0.00'){
		$('select option#opfirst' + id).hide();
		}
});


$("select").each(function(){
	var id = $(this).attr('id');
	var pmsScore = $(this).attr('score');
	
	$("select option.op" + id).each(function(){
	    if($(this).val()==pmsScore){ // EDITED THIS LINE
	        $(this).attr("selected","selected");    
	    }
	});
});
*/

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


$("#dialogconfirmPOST").dialog({
	  modal: true,
	  autoOpen: false,
	  position: { my: 'top', at: 'top+150',of: window },
	  buttons: {
	    Ok: function() {
	    	var chkentries = {};
		    chkentries.id = $('input[name=chkposting]:checked').map(function(){
		    	return this.value;
		    }).get();
		    
		    chkentries.scores = $('input[name=chkposting]:checked').map(function(){
		        var targetid = $(this).attr('id');
		        return $('input#score-' + targetid).val();
		    }).get();
		   
			
			$.ajax({
		        url : "/ERM/postchecked/", // the endpoint
		        type : "post", // http method
		        data : { chkentries:chkentries, }, // data sent with the post request
				
				// handle a successful response
		        success : function(data) {
		        	if(data == 'Posting Successful.'){
			        	$("input[type='text']").val('');
			        	$("input[type='checkbox']").attr('checked', false);
			        	window.location.reload();
			        	}
			        else{
			        	alert('Please fill in score fields for entry that you want to post.');
			        	window.location.reload();
			        	}
		        	},
		
		        // handle a non-successful response
		    	error : function(data) {
		        	
		        	}
				 });
	    	
	    	
			$("#dialogconfirmPOST").dialog("close");
	    },
	    Cancel: function() {
	        $("#dialogconfirmPOST").dialog("close");
	    }
	    
	  },
	  beforeClose: function(){
	    //event.preventDefault();
	    
	  }
	
	  
	});
	    
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$('.outputxlslink').on('click', function(event){
	event.preventDefault();
	$("#dialogoutputxls").dialog("open");
});


$("#dialogoutputxls").dialog({
	  modal: true,
	  autoOpen: false,
	  position: { my: 'top', at: 'top+100',of: window },
	  buttons: {
	    Ok: function() {
	    	$('form#frmoutputxls').submit();
	    	/*
	    	var year = $('select#xlsyear').val();
			
			$.ajax({
		        url : "/ERM/outputtoxls/", // the endpoint
		        type : "post", // http method
		        data : { year:year, }, // data sent with the post request
				
				// handle a successful response
		        success : function(data) {
		        	
		        	window.location.replace('\\10.33.33.115\d$\Projects\workspace\SMS\ERM\static\dl\pms-xls\PMS' + year + '-' + data + '(' + randstr + ')'); 
		        	//window.location.reload();
		        	},
		
		        // handle a non-successful response
		    	error : function(data) {
		        	
		        	}
				 });
	    	*/
	    	
			$("#dialogoutputxls").dialog("close");
	    },
	    Cancel: function() {
	        $("#dialogoutputxls").dialog("close");
	    }
	    
	  },
	  beforeClose: function(){
	    //event.preventDefault();
	    
	  }
	
	  
	});
	
	
//ON pmslink click
/*
$('#pmslink').on('click', function(event){
	event.preventDefault();
	$("#dialogpmsadd").dialog("open");
	$("input[type='text']").val('');
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

	//Dialog for pms
	$("#dialogpmsadd").dialog({
	      modal: true,
	      autoOpen: false,
	      buttons: {
	        Ok: function() {
				//ajax check for filters
				var pmsuser = $('select#pmsuser').val();
				var pmsyear = $('select#pmsyear').val();
				var pmsscore = $('select#pmsscore').val();
				
				$.ajax({
			        url : "/ERM/pmsadd/", // the endpoint
			        type : "post", // http method
			        data : { pmsuser:pmsuser, pmsyear:pmsyear, pmsscore:pmsscore }, // data sent with the post request
					
					// handle a successful response
			        success : function(data) {
			        	if (data == 'PMS added.'){
				        	$("#dialogpmsadd").dialog("close");
				        	window.location.reload();
				        	}
			        	else{
				        	document.getElementById('pmsnote').innerHTML = data;
				        	}
			        	},
			
			        // handle a non-successful response
			        error : function(data) {
			        	
			        	}
					 });
				
	        },
	        Cancel: function() {
	            $("#dialogpmsadd").dialog("close");
	        }
	        
	      },
	      beforeClose: function(){
	        //event.preventDefault();
	        
	      }
	    
	      
	    });
*/
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//$('input.btndtrdetails').on('click', function(event){
$("body").on("click","input.btndtrdetails",function(event) {
	var uid = $(this).attr('uid');
	var month = $(this).attr('month');
	var yearnum = $(this).attr('year');
	var cutofftype = $(this).attr('cutoff'); 
	var status = $(this).attr('status');
	
	$.ajax({
        url : "/ERM/modal_approve/", // the endpoint
        type : "post", // http method
        data : { uid:uid, month: month, yearnum: yearnum, cutofftype: cutofftype, status:status }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#apprmodal').html(data);
        	//$('#amodal').modal('show');
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });

});


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$('select#WorkSched').on('change', function(event){
	if ($('select#WorkSched').val() == 'CWW'){
		$('select#dayoff2').prop('disabled', false);
		document.getElementById('Day1').innerHTML = 'Day-off 1';
		document.getElementById('Day2').innerHTML = 'Day-off 2';
	}
	else if ($('select#WorkSched').val() == 'REG'){
		$('select#dayoff2').prop('disabled', true);
		document.getElementById('Day1').innerHTML = 'Day-off 1';
		document.getElementById('Day2').innerHTML = 'Day-off 2';
	}
	else if ($('select#WorkSched').val() == 'CWD'){
		$('select#dayoff2').prop('disabled', false);
		document.getElementById('Day1').innerHTML = 'Day-off 1';
		document.getElementById('Day2').innerHTML = 'Day-off 2';
	}
	else if ($('select#WorkSched').val() == 'CWD2'){
		$('select#dayoff2').prop('disabled', false);
		document.getElementById('Day1').innerHTML = 'Duty 1';
		document.getElementById('Day2').innerHTML = 'Duty 2';
		
	}

});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//notes Trigger
$("body").on("click","input.notesTrigger",function(event) {
	$('#nmodal').modal('show');
	var datetoview = $(this).attr('id');
	
	$.ajax({
        url : "/ERM/viewnotes/", // the endpoint
        type : "post", // http method
        data : { datetoview: datetoview, }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#notesmodal').html(data);
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
});

//btnClose
$("body").on("click","#btnClose",function(event) {
	$('#nmodal').modal('hide');
});

//btntopX
$("body").on("click","#btntopX",function(event) {
	$('#nmodal').modal('hide');
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//Search for approver
$('input.SearchBtn').on('click', function(event){
	var searchtype = $(this).attr('searchtype');
	var keyword;
	var month;
	var year;
	var cutoff;
	var status;
	
	if (searchtype == 'textsearch'){
		keyword = $('input#txtApprovalSearch').val();
		
	}
	else if (searchtype == 'periodsearch'){
		keyword = $('input#txtApprovalSearch').val();
		month = $('select#dtrentrymonth').val();
		year = $('select#dtrentryyear').val();
		cutoff = $('select#dtrentrycutoff').val();
		
	}
	else if (searchtype == 'statussearch'){
		keyword = $('input#txtApprovalSearch').val();
		month = $('select#dtrentrymonth').val();
		year = $('select#dtrentryyear').val();
		cutoff = $('select#dtrentrycutoff').val();
		status = $('select#dtrentrystatus').val();
		
	}
	
	
	$.ajax({
        url : "/ERM/approvalSearch/", // the endpoint
        type : "post", // http method
        data : { searchtype:searchtype, keyword:keyword, month:month, year:year, cutoff:cutoff, status:status }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#apprcontent').html(data);
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
	
});





////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////



//view other dates
$('input[id="btnGo"]').on('click', function(event){
	var monthnum = $('select#viewmonth option:selected').index() + 1;
	var yearnum = $('select#viewyear').val();
	var cutofftype = $('select#cutofftype').val(); 
	
	$('input#hmonth').val(monthnum);
	$('input#hyear').val(yearnum);
	$('input#hcutoff').val(cutofftype);
	
	$.ajax({
        url : "/ERM/viewadd/", // the endpoint
        type : "post", // http method
        data : { monthnum: monthnum, yearnum: yearnum, cutofftype: cutofftype }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#dtrdata').html(data);
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });

});





$('input.save').hide();
$('input.inputmask').prop('disabled', true);
$('input.inputmask').mouseup(function(e){
	e.preventDefault();
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

// replace the 'n'th character of 's' with 't'
		function replaceAt(s, n, t) {
		    return s.substring(0, n) + t + s.substring(n + 1);
		}

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//If min is greater than 59 or 60up set it to 59min
$('input.inputmask').on('focusout', function(event) {
	var str = $(this).val();
	var numOfMinutes = $(this).val().substring(4,6);
	if(numOfMinutes >= 60){
		str1 = replaceAt(str,4,"5");
		str2 = replaceAt(str1,5,"9");
		$(this).val(str2);
	
	}
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//Change hoursWorkedValue every focusout
$('input.inputmask').on('focusout', function(event){
	var day = $(this).attr('id').slice(-2);
	var theValue = $(this).val(); //value of leave input
	
	
	if(theValue.indexOf('_') === -1){
		var hr = theValue.charAt(0);
		var min = theValue.substring(4,6);
		var totalmins = parseInt(min) + (parseInt(hr)*60);
		//////////////
		var strhwValue = $('input[id="hw'+ day +'"]').val();
		var numOfHours = $('input[id="hw'+ day +'"]').val().charAt(0);
		var numOfMinutes = $('input[id="hw'+ day +'"]').val().substring(4,6);
		var totalminutesworked = parseInt(numOfMinutes) + (parseInt(numOfHours)*60);
		
		var addValue;
		if ($('input[id="hidden'+ $(this).attr('id') + '"]').val() == "" ){
			addValue = 0;
		}
		else {
			addValue = parseInt($('input[id="hidden'+ $(this).attr('id') + '"]').val());
		}
		
		newhwtotalmins = totalminutesworked - totalmins + addValue; 
		
		
		///////////////////////////////////////////
		///			FOR LEAVE CREDITS			///
		///////////////////////////////////////////
		//var rvl = $('input#hvlrem').val();
		//var rsil = $('input#hsilrem').val();
		//var rsl = $('input#hslrem').val();
		
		
		/*
		alert(rvl);
		alert(rsil);
		alert(rsl);
		*/
		
		var theid = String($(this).attr('id'));
		
		//if ($(this).val().indexOf('vl') > -1) {
		//if (String($(this).attr('id')).contains('vl')){
		if (theid.indexOf('vl') > -1){	
		 	var fieldrem = parseInt($('input#hvlrem').val()) + addValue; //addValue to enable as long as di mulapas
		 	//rvl = 7200 - parseInt($('input[id="htotalvl"]').val()) - totalmins;
		}
		//else if ($(this).val().indexOf('sil') > -1) {
		//else if (String($(this).attr('id')).contains('sil')){
		else if (theid.indexOf('sil') > -1){
			var fieldrem = parseInt($('input#hsilrem').val()) + addValue; //addValue to enable as long as di mulapas
			//rsil = 4800 - parseInt($('input[id="htotalsil"]').val()) - totalmins;
			//alert('SIL');
		}
		//else if ($(this).val().indexOf('sl') > -1) {
		//else if (String($(this).attr('id')).contains('sl')){
		else if (theid.indexOf('sl') > -1){
			var fieldrem = parseInt($('input#hslrem').val()) + addValue; //addValue to enable as long as di mulapas
			//rsl = 2400 - parseInt($('input[id="htotalsl"]').val()) - totalmins;
			//alert('SL');
		}
		
		////////////////////////////////////////////
		////////////////////////////////////////////
		////////////////////////////////////////////
		
		//if ((newhwtotalmins >= 0) && ((totalmins <= fieldrem) || ($(this).attr('id').contains('absent')))) {
		if ((newhwtotalmins >= 0) && ((totalmins <= fieldrem) || (theid.indexOf('absent') > -1))) {
			finhr = newhwtotalmins/60;
			mins = newhwtotalmins%60;
			finmin = ("0" + mins).slice(-2);
			
			rephrchar = replaceAt(strhwValue,0,String(parseInt(finhr)));
			repminchar = rephrchar.replaceAt(4, String(finmin));
			
			$('input[id="hw'+ day +'"]').val(repminchar);
			$('input[id="hiddenhw'+ day +'"]').val(newhwtotalmins);
			$('input[id="hidden'+ $(this).attr('id') + '"]').val(totalmins);
			
			}
		else{
			//convert to nhr nmin
			pasttotalmins = parseInt($('input[id="hidden'+ $(this).attr('id') + '"]').val());
			pasthr = pasttotalmins/60;
			tomin = pasttotalmins%60;
			pastmin = ("0" + tomin).slice(-2);
			
			rhrchar = replaceAt(theValue,0,String(parseInt(pasthr)));
			rminchar = rhrchar.replaceAt(4, String(pastmin));
			
			$(this).val(rminchar);
			}
		}
	else{
		pasttotalmins = parseInt($('input[id="hidden'+ $(this).attr('id') + '"]').val());
		pasthr = pasttotalmins/60;
		tomin = pasttotalmins%60;
		pastmin = ("0" + tomin).slice(-2);
		
		rhrchar = replaceAt(theValue,0,String(parseInt(pasthr)));
		rminchar = rhrchar.replaceAt(4, String(pastmin));
		
		$(this).val(rminchar);
	}
	

	
});



////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$('input.modify').on('click', function(event){
	var day = $(this).attr('day');

	$('input[id="vl'+ day +'"]').prop('disabled', false);
	$('input[id="sil'+ day +'"]').prop('disabled', false);
	$('input[id="sl'+ day +'"]').prop('disabled', false);
	$('input[id="absent'+ day +'"]').prop('disabled', false);

	$('input[id="save'+ day +'"]').show();
	$(this).hide();
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$('input.save').on('click', function(event){
//$("body").on("click","input.save",function(event) {
	//event.preventDefault();
	var day = $(this).attr('day');
	var numOfHours = $('input[id="hw'+ day +'"]').val().charAt(0);
	var numOfMinutes = $('input[id="hw'+ day +'"]').val().substring(4,6);
	
	var totalminutesworked = parseInt(numOfMinutes) + (parseInt(numOfHours)*60);
	
	$('input[id="vl'+ day +'"]').prop('disabled', true);
	$('input[id="sil'+ day +'"]').prop('disabled', true);
	$('input[id="sl'+ day +'"]').prop('disabled', true);
	$('input[id="absent'+ day +'"]').prop('disabled', true);

	$(this).hide();
	$('input[id="modify'+ day +'"]').show();
	//----------------------------------------------//
	//              OK na here and up               //
	//----------------------------------------------//
	//Save and Update database Leave/Attendance data//
	//----------------------------------------------//
	vl = $('input[id="hiddenvl'+ day +'"]').val();
	sil = $('input[id="hiddensil'+ day +'"]').val();
	sl = $('input[id="hiddensl'+ day +'"]').val();
	aa = $('input[id="hiddenabsent'+ day +'"]').val();
	dt = $('input[id="hiddendt'+ day +'"]').val();
	
	/*
	var vl = $('input[id="hiddenvl'+ day +'"]').val();
	var sil = $('input[id="hiddensil'+ day +'"]').val();
	var sl = $('input[id="hiddensl'+ day +'"]').val();
	var aa = $('input[id="hiddenabsent'+ day +'"]').val();
	var dt = $('input[id="hiddendt'+ day +'"]').val();
	*/
	
	//////////////////////////////////////////////////
	var vlconsumeyear = $('input[id="hiddenVLConsumeYear'+ day +'"]').val();
	
	//----------------------------------------------//
	//               Get Hidden Values              //
	//----------------------------------------------//
	var totalhwmin = $('input[id="htotalhw"]').val();
	var totalaamin = $('input[id="htotalaa"]').val();
	var totalvlmin = $('input[id="htotalvl"]').val();
	var totalsilmin = $('input[id="htotalsil"]').val();
	var totalslmin = $('input[id="htotalsl"]').val();
	

	//----------------------------------------------//
	//           Default to 0 if no input           //
	//----------------------------------------------//
	
	if (vl==''){
		vl=0;
	}
	if (sil==''){
		sil=0;
	}
	if (sl==''){
		sl=0;
	}
	if (aa==''){
		aa=0;
	}
	

	
	
	
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	
	//////////////////////////////////
	// CONTROLLER FOR PREVIOUS YEAR VL
	//var ctrlforprevyrvl = parseInt($('input#ctrlforprevyrvl').val());
	//var thisyear = new Date().getFullYear();
	//var response = false;
	
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	
	//if (ctrlforprevyrvl > 0){
	var remprevyrvl = parseInt($('input#hprevyrvlrem').val());
	if ((vl <= remprevyrvl) && (vl != 0) ) {
		$("#dialogconfirmLastYearVL").dialog("open");
		//response = confirm("Consume Previous Year VL?");
		//for Vl Last Year dialog initialization
		
	}
	else{
		//----------------------------------------------//
		//             AJAX for Leave Save              //
		//----------------------------------------------//
		response = false;
		$.ajax({
	        url : "/ERM/saveleave/", // the endpoint
	        type : "post", // http method
	        data : { vl: vl, sil: sil, sl:sl, aa: aa, dt: dt, response: response,}, // data sent with the post request
			
			// handle a successful response
	        success : function(data) {
	        	$('#summary').html(data);
	        	},
	
	        // handle a non-successful response
	        error : function(data) {
	        	
	        	}
			 });
	}
	//}
	
	//////////////////////////////////////////////////////////////////////
	
	
	
	
	
	
	
	
	//////////////////////////////////////////////////////////////////////
	/*
	//----------------------------------------------//
	//             AJAX for Leave Save              //
	//----------------------------------------------//
	
	$.ajax({
        url : "/ERM/saveleave/", // the endpoint
        type : "post", // http method
        data : { vl: vl, sil: sil, sl:sl, aa: aa, dt: dt, response: response,}, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#summary').html(data);
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
	*/
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


$('form#frmReport').on('submit', function(event){
	var associate = $('select#users').val();
	var monthnum = $('select#rmonth option:selected').index() + 1;
	var yearnum = $('select#ryear').val();
	var cutofftype = $('select#rcutoff').val(); 
	
	if ( (associate != -1) && (associate != -2) && (associate != -3) ) 
		{
		event.preventDefault();
		$.ajax({
	        url : "/ERM/viewrep/", // the endpoint
	        type : "post", // http method
	        data : { associate:associate, monthnum: monthnum, yearnum: yearnum, cutofftype: cutofftype }, // data sent with the post request
			
			// handle a successful response
	        success : function(data) {
	        	$('#repdiv').html(data);
	        	},
	
	        // handle a non-successful response
	        error : function(data) {
	        	
	        	}
			 });
		/* 
		$('input#hmonth').val(monthnum);
		$('input#hyear').val(yearnum);
		$('input#hcutoff').val(cutofftype);
		*/
		}
	
});





////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
//INITIALIZATIONS
//show hide with Leave credits
if ( ($('select#users').val() != -1) && ($('select#users').val() != -2) && ($('select#users').val() != -3) ) {
		$('div#divwlc').hide();
	}
else{
		$('div#divwlc').show();
	}

$('select#cmbgenby').val('ID');
	


//on cmb change
$('select#users').on('change', function(event){
	if ( ($('select#users').val() != -1) && ($('select#users').val() != -2) && ($('select#users').val() != -3) ) {
		$('div#divwlc').hide();
	}
	else{
		$('div#divwlc').show();
	}
	
});

///////////////////////////////
//cmbsearchtype change
$('select#cmbgenby').on('change', function(event){
	var arrangeby = $(this).val();
	
	$.ajax({
        url : "/ERM/changecmbgenby/", // the endpoint
        type : "post", // http method
        data : { arrangeby: arrangeby }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#users').html(data);
        	$('div#divwlc').show();
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
});


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$("body").on("click","input.btnapprnoteprev",function(event) {
	var uid = $(this).attr('uid');
	var thedate= $(this).attr('thedate');
	
	$.ajax({
        url : "/ERM/apprnoteprev/", // the endpoint
        type : "post", // http method
        data : { uid:uid,thedate:thedate }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#apprnotemodal').html(data);
        	//$('#anotemodal').modal('show');
        	},

        // handle a non-successful response
        error : function(data) {
        	//alert(data);
        	}
		 });
});

//close button
$("body").on("click","button[id='btnNoteX']",function(event) {
	//alert("notemodal hidden");
	$('#anotemodal').modal('hide');
	//alert("bmodal hidden");
	$('#bmodal').modal('hide');
	//$('#bmodal').modal('show');
	setTimeout(function(){ $('#bmodal').modal('show'); }, 500);
	//alert("bmodal shown");
});


/**************************************************************************************/
/**************************************************************************************/
/**************************************************************************************/
	
	//AVOID 2 dots	
	$(".numdot").keydown(function (e) {
        var theVal = $(this).val().replace(/,/g, "");
        var dotctr = (theVal.match(/\./g) || []).length;
        
        if ((dotctr == 1 && e.keyCode == 110) || (dotctr == 1 && e.keyCode == 190))
        	{
        	e.preventDefault();
        	}
        else{
        	return;
        }
	});

/**************************************************************************************/
/**************************************************************************************/
/**************************************************************************************/

	//NUM ONLY and dots. only
	$(".numdot").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
             // Allow: Ctrl+A, Command+A
            (e.keyCode == 65 && ( e.ctrlKey === true || e.metaKey === true ) ) || 
             // Allow: home, end, left, right, down, up
            (e.keyCode >= 35 && e.keyCode <= 40)) {
                // let it happen, don't do anything
                return;
	            
                
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });

/**************************************************************************************/
/**************************************************************************************/
/**************************************************************************************/
	
	//NUM ONLY and dots. only
	$(".numonly").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13]) !== -1 ||
             // Allow: Ctrl+A, Command+A
            (e.keyCode == 65 && ( e.ctrlKey === true || e.metaKey === true ) ) || 
             // Allow: home, end, left, right, down, up
            (e.keyCode >= 35 && e.keyCode <= 40)) {
                // let it happen, don't do anything
                return;
	            
                
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });

/**************************************************************************************/
/**************************************************************************************/
/**************************************************************************************/
	
	$("body").on("change","input#id_avatar", function(event) {
		document.getElementById('filename').innerHTML = this.value;
	});

	/*
	$("body").on("click","input#up_avatar", function(event) {
		console.log('');
	});
	*/
	
/**************************************************************************************/
/**************************************************************************************/
/**************************************************************************************/

	$("body").on("input",".uppercase", function(e) {
	    if (e.which >= 97 && e.which <= 122) {
	        var newKey = e.which - 32;
	        // I have tried setting those
	        e.keyCode = newKey;
	        e.charCode = newKey;
	    }

	    $(this).val(($(this).val()).toUpperCase());
	});

/**************************************************************************************/
/**************************************************************************************/
/**************************************************************************************/

	//AMOUNT FORMATTER
	$("body").on("keyup","input.amts",function(event) {
    	var x = $(this).val();
    	$(this).val(x.toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
	});
	
	
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////




//csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
 
/*
The functions below will create a header with csrftoken
*/
 
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
 
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//DATE 
	$( ".datepicker" ).datepicker({
		 format: 'yyyy-mm-dd',
		 changeMonth: true,
         changeYear: true,
         showButtonPanel: true,
         yearRange: "-100:+0",
	});

	
	
//INPUTMASK
	
	$(".inputmask").inputmask({
		mask: '9hr 99min',
	});

	
});//end
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////









// PREDEFINED FUNCTIONS //
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

String.prototype.replaceAt=function(index, character) {
    return this.substr(0, index) + character + this.substr(index+character.length);
};

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////



