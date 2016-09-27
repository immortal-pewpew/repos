/**
 * @author fdypua
 * There are two views: a lot affection or not at all. The center serves to rejuvenate human race. Women for certain people nurtures and strengthen its vitality and spirit. Being single does the same to other people. I chose that second path.
 */

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


$(document).ready(function(){
	
	
////////////////////////////////////////////////////////////////////////
/////////////////////                              /////////////////////
/********************             ALL              ********************/
/////////////////////                              /////////////////////
////////////////////////////////////////////////////////////////////////

$(function() {
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	/*
	//FOR SOA Creation
    $("#dialogCreateSOA").dialog({
	  modal: true,
	  position: { my: 'top', at: 'top+150',of: window },
	  autoOpen: false,
	  buttons: {
	    Ok: function() {
	    	var nbu = $('select#nbu').val();
	    	$.ajax({
		        url : "/ECS/createSOA/", // the endpoint
		        type : "post", // http method
		        data : { nbu:nbu }, // data sent with the post request
				
				// handle a successful response
		        success : function(data) {
		        	alert(data);
		        	},
		
		        // handle a non-successful response
		        error : function(data) {
		        	
		        	}
				 });
	    	
	    	$(this).dialog( "close" );
	        
	    },
	    Cancel: function() {
	    	$(this).dialog("close");
      }
	  },
	  beforeClose: function(){
	    
	  }
	});
    */
	
	
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	
	//FOR SOA NOTES	    
    $("#dialognotes").dialog({
	  modal: true,
	  width:  700,
	  position: { my: 'top', at: 'top+125',of: window },
	  autoOpen: false,
	  buttons: {
	    Ok: function() {
	        $(this).dialog( "close" );
	    }
	    
	  },
	  beforeClose: function(){
	    
	  }
	});
	
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

	//FOR CONNECTION ERROR INFO	    
    $("#dialogConnerror").dialog({
	  modal: true,
	  position: { my: 'top', at: 'top+150',of: window },
	  autoOpen: false,
	  buttons: {
	    Ok: function() {
	        $(this).dialog( "close" );
	    }
	    
	  },
	  beforeClose: function(){
	    
	  }
	});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

	//FOR PAYMENT TERM ERROR INFO	    
    $("#dialogTermNotFoundError").dialog({
	  modal: true,
	  position: { my: 'top', at: 'top+150',of: window },
	  autoOpen: false,
	  buttons: {
	    Ok: function() {
	        $( this ).dialog( "close" );
	        
	    }
	    
	  },
	  beforeClose: function(){
	    
	  }
	});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

	

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	
	//FOR Create Confirmation
	$("#dialogconfirmcreate").dialog({
      modal: true,
      position: { my: 'top', at: 'top+150',of: window },
      autoOpen: false,
      buttons: {
        Ok: function() {
			$("#dialogconfirmcreate").dialog("close");
			$("form#frmCreate").unbind('submit').submit();
        },
        Cancel: function() {
        	//event.preventDefault();
            $("#dialogconfirmcreate").dialog("close");
        }
        
      },
      beforeClose: function(){
        //event.preventDefault();
        
      }
    });

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

	//DIALOG FOR INPUT IS REQUIRED
	$("#dialoginputerror").dialog({
	  modal: true,
	  position: { my: 'top', at: 'top+150',of: window },
	  autoOpen: false,
	  buttons: {
	    Ok: function() {
	        $(this).dialog( "close" );
	        
	    }
	    
	  },
	  beforeClose: function(){
	    
	  }
	});
	
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

	//DIALOG FOR CONFIRM UPDATE
		$("#dialogconfirmupdate").dialog({
	      modal: true,
	      position: { my: 'top', at: 'top+150',of: window },
	      autoOpen: false,
	      buttons: {
	        Ok: function() {
				$("#dialogconfirmupdate").dialog("close");
				$("form#updform").unbind('submit').submit();
				$('#susoadetailsmodal').modal('hide');
				
	        },
	        Cancel: function() {
	        	//event.preventDefault();
	            $("#dialogconfirmupdate").dialog("close");
	        }
	        
	      },
	      beforeClose: function(){
	        //event.preventDefault();
	        
	      }
	    });

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	
	//DELETE CHANGE PASSWORD
	$("#dialogchangepwd").dialog({
	      modal: true,
	      autoOpen: false,
	      position: { my: 'top', at: 'top+150',of: window },
	      buttons: {
	        Ok: function() {
				//ajax check for filters
				var oldpwd = $('input#oldpwd').val();
				var newpwd = $('input#newpwd').val();
				var confirmnewpwd = $('input#confirmnewpwd').val();
				
				$.ajax({
			        url : "/ECS/pwdcheck/", // the endpoint
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
				
				//$("#dialogchangepwd").dialog("close");
				//$("form#frmChangePwd").submit();
				
				//$("form#frmChangePwd").unbind('submit').submit();
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
	      position: { my: 'top', at: 'top+150',of: window },
	      closeOnEscape: false,
	      open: function(event, ui) { $(".ui-dialog-titlebar-close", ui.dialog | ui).hide();
	      			}, 
	      buttons: {
	        Ok: function() {
				$("#dialogpwdchngsuccess").dialog("close");
	        },
	        
	      },
	      beforeClose: function(){
	        //event.preventDefault();
	        
	      }
	      
	    });
	    
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	    
	    
	    
	    
	    
	    
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	    
	    $("#dialogaddholiday").dialog({
	      modal: true,
	      autoOpen: false,
	      position: { my: 'top', at: 'top+150',of: window },
	      buttons: {
	        Ok: function() {
				//ajax check for filters
				var dateOfHoliday = $('input#dateOfHoliday').val();
				var holidayDesc = $('textarea#holidayDesc').val();
				var typeOfHoliday = $('select#typeOfHoliday').val();
				var schemeOfHoliday = $('select#schemeOfHoliday').val();
				
				
				$.ajax({
			        url : "/ECS/addholiday/", // the endpoint
			        type : "post", // http method
			        data : { dateOfHoliday:dateOfHoliday, holidayDesc:holidayDesc, typeOfHoliday:typeOfHoliday, schemeOfHoliday:schemeOfHoliday }, // data sent with the post request
					
					// handle a successful response
			        success : function(data) {
			        	if (data == 'Holiday Success.'){
				        	$("#dialogaddholiday").dialog("close");
				        	window.location.reload();
				        	}
			        	else{
				        	document.getElementById('holidaynote').innerHTML = data;
				        	}
			        	},
			
			        // handle a non-successful response
			        error : function(data) {
			        	
			        	}
					 });
				
	        },
	        Cancel: function() {
	            $("#dialogaddholiday").dialog("close");
	        }
	        
	      },
	      beforeClose: function(){
	        //event.preventDefault();
	        
	      }
	    
	      
	    });
	    
	 
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	    
	    //CREATE ACCOUNT DIALOG
	    $("#dialogcreateacct").dialog({
	      modal: true,
	      autoOpen: false,
	      width: 320,
	      position: { my: 'top', at: 'top+80', of: window },
	      open: function( event, ui ) {
	    	  $('select#newaccttype').val(0);
	    	  $('div#vendorIDfield').show();
	    	  
	    	  $(".chosen-select").chosen({
	    		  placeholder_text_single: "Select Vendor ...",
	    		  no_results_text: "Vendor not found!",
	    			  });
	    	  
	      	},
	      buttons: {
	        Ok: function() {
				//ajax check for filters
	        	
	        	var newacctusername = $('input#newacctusername').val();
				var newacctfullname = $('input#newacctfullname').val();
				var newaccttype = $('select#newaccttype').val();
				
				if ((newacctusername === '') || (newacctfullname === '')){
					document.getElementById('newacctnote').innerHTML = 'Please enter required fields.';
				}
				else{
					if ((newaccttype === '0') && ($('input#newacctvendorID').val() === '')){
						document.getElementById('newacctnote').innerHTML = 'Please enter vendor ID.';
					}
					else{
						$("form#frmcreateacct").submit();
					}
				}
				
				
	        },
	        Cancel: function() {
	            $("#dialogcreateacct").dialog("close");
	        }
	        
	      },
	     
	    });

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////    
	    
	  //EDIT ACCOUNT DIALOG
	    $("#dialogeditacct").dialog({
	      modal: true,
	      autoOpen: false,
	      position: { my: 'top', at: 'top+150', of: window },
	      
	      buttons: {
	        Ok: function() {
	        	$("form#frmupdateacct").submit();
	        },
	        Cancel: function() {
	            $("#dialogeditacct").dialog("close");
	        }
	        
	      },
	     
	    });
	    
	    
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	    //DELETE SOA
		$("#dialogdel").dialog({
	    	modal: true,
	    	position: { my: 'top', at: 'top+150',of: window },
	    	autoOpen: false
		});	
	
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////	    
		//CREATE ACCESS DIALOG
	    $("#dialognewaccess").dialog({
	      modal: true,
	      autoOpen: false,
	      position: { my: 'top', at: 'top+150', of: window },
	      open: function( event, ui ) {
	    	  //$('select#newaccttype').val(0);
	    	  //$('div#vendorIDfield').show();
	      	},
	      buttons: {
	        Add: function() {
	        	$("form#frmaddaccess").submit();
	        	
	        },
	        Cancel: function() {
	            $(this).dialog("close");
	        }
	        
	      },
	     
	    });
	    
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
		
		//DELETE ACCESS
		$("#dialogdeleteaccess").dialog({
			modal: true,
			autoOpen: false,
			position: { my: 'top', at: 'top+150', of: window },
	      
			buttons: {
				Delete: function() {
					var id = $("#deleteID").val();
					
					$.ajax({
				        url : "/ECS/deleteaccess/", // the endpoint
				        type : "post", // http method
				        data : { id:id }, // data sent with the post request
				        success : function(data) {
				        	window.location.reload();
				        	},
				
				        // handle a non-successful response
				        error : function(data) {
				        	
				        	}
					});
					$(this).dialog("close");
				},
				Cancel: function() {
					$(this).dialog("close");
				}
	        
			},
		});
		
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////		
		
		//DIALOG REPORTS
		$("#dialogreports").dialog({
			modal: true,
			autoOpen: false,
			position: { my: 'top', at: 'top+150', of: window },
	      
			buttons: {
				Generate: function() {
					var reporttype = $('#reportype').val();
					var dt2 = $('#dt2').val();
					
					if ((reporttype == 1) || (reporttype == 2) || (reporttype == 4)){
						var dt1 = $('#dt1').val();
						
						if ((dt1 !== '') && (dt2 !== '')){
							$("form#frmgenreport").submit();
						}
						else{
							document.getElementById('reportnote').innerHTML = 'All fields required.';
						}
					}
					else{
						if (dt2 !== ''){
							$("form#frmgenreport").submit();
						}
						else{
							document.getElementById('reportnote').innerHTML = 'All fields required.';
						}
					$(this).dialog("close");
					}
				},
				Cancel: function() {
					$(this).dialog("close");
				}
	        
			},
		});
		

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////	    
	});//closing function

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

/*
//change vendor_lookup
$("body").on("keydown",".vendor_lookup",function(e) {
	var keyword = $(this).val();
	
	if((keyword.length === 1) || (keyword.length % 3 === 0)){
		$.ajax({
	        url : "/ECS/vendors/", // the endpoint
	        type : "post", // http method
	        data : { keyword:keyword, }, // data sent with the post request
			dataType: 'json',
	        
			// handle a successful response
	        success : function(data) {
	        	$(".vendor_lookup").autocomplete({
	        		source: function(request, response) {
	        			var results = $.ui.autocomplete.filter(data, request.term);//data is here
	        			response(results.slice(0, 4));//limit matches to 15
	        		},
	        		minLength: 0,
	        		select: function(event, ui) {
	        			$('#newacctvendorID').val(ui.item.value.substring(0,6));
				      	///////////////
	        			return false;
	        		},
	        		change: function(event, ui) {
	        			if ($("#newacctvendorID").val().length === 0) {
	        				$("#newacctvendorID").val('');
	        			}
	        		}
	        	});
	        	$('.vendor_lookup').autocomplete("search", keyword);
	        },

	        // handle a non-successful response
	    	error : function(data) {
	        	
	    	}
		});	
	}	
});
*/


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$('#reportlink').on('click', function(event){
	event.preventDefault();
	$("#dialogreports").dialog("open");
	$('select#reporttype').val('1');
	document.getElementById('date2').innerHTML = 'Date To:';
	$(".date1").show();
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
$('.pwdlink').on('click', function(event){
	event.preventDefault();
	$("#dialogchangepwd").dialog("open");
	$("input[type='password']").val('');
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
$('#holidaylink').on('click', function(event){
	event.preventDefault();
	$("#dialogaddholiday").dialog("open");
	$("textarea").val('');
	$("input[type='text']").val('');
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
$('#newacctlink').on('click', function(event){
	event.preventDefault();
	$("#dialogcreateacct").dialog("open");
	$("input[type='text']").val('');
	
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
$('.editlink').on('click', function(event){
	event.preventDefault();
	var userName = $(this).attr('id');
	
	$.ajax({
        url : "/ECS/getuserdata/", // the endpoint
        type : "post", // http method
        data : { userName:userName, }, // data sent with the post request
		
        
        
		// handle a successful response
        success : function(data) {
        	$("#dialogeditacct").dialog("open");
			
        	$('input#useracct').val(userName);
        	$('input#editacctusername').val(userName);
        	$('input#editacctfullname').val(data.FullName);
        	$('select#editacctstatus').val(data.Status);
        	
        	$('input#editacctpwd').val('');
        	},

        // handle a non-successful response
    	error : function(data) {
        	
        	}
		 });	
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
$('#accesslink').on('click', function(event){
	event.preventDefault();
	//$("#dialogcreateacct").dialog("open");
	$("#dialognewaccess").dialog("open");
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//hide loading initialization
$('#loading').hide();

////////////////////////////////////////////////////////////////////////
///////////////////////// PAGINATIONS //////////////////////////////////
////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////
//userpager
$('input#userpager').on('focusout', function(event){
	var page = $(this).val();
	window.location.replace("/ECS/users/?page=" + page);
});
//userpager
$('input#userpager').on('keydown', function(event){
	if(event.keyCode == 13){
		var page = $(this).val();
		window.location.replace("/ECS/users/?page=" + page);
	}
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
//SU
$('input#supager').on('focusout', function(event){
	var page = $(this).val();
	window.location.replace("/ECS/sumain/?page=" + page);
});
//SU
$('input#supager').on('keydown', function(event){
	if(event.keyCode == 13){
		var page = $(this).val();
		window.location.replace("/ECS/sumain/?page=" + page);
	}
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
//CA
$('input#capager').on('focusout', function(event){
	var page = $(this).val();
	window.location.replace("/ECS/camain/?page=" + page);
});
//CA
$('input#capager').on('keydown', function(event){
	if(event.keyCode == 13){
		var page = $(this).val();
		window.location.replace("/ECS/camain/?page=" + page);
	}
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
//PA
$('input#papager').on('focusout', function(event){
	var page = $(this).val();
	window.location.replace("/ECS/pamain/?page=" + page);
});
//PA
$('input#papager').on('keydown', function(event){
	if(event.keyCode == 13){
		var page = $(this).val();
		window.location.replace("/ECS/pamain/?page=" + page);
	}
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
//MU
$('input#mupager').on('focusout', function(event){
	var page = $(this).val();
	window.location.replace("/ECS/mumain/?page=" + page);
});
//MU
$('input#mupager').on('keydown', function(event){
	if(event.keyCode == 13){
		var page = $(this).val();
		window.location.replace("/ECS/mumain/?page=" + page);
	}
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
//Holiday Pager
$('input#hpager').on('focusout', function(event){
	var page = $(this).val();
	window.location.replace("/ECS/holidays/?page=" + page);
});
//Holidays Page
$('input#hpager').on('keydown', function(event){
	if(event.keyCode == 13){
		var page = $(this).val();
		window.location.replace("/ECS/holidays/?page=" + page);
	}
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
//Messages Pager
$('input#msgpager').on('focusout', function(event){
	var page = $(this).val();
	window.location.replace("/ECS/messagingadmin/?page=" + page);
});
//Messages Page
$('input#msgpager').on('keydown', function(event){
	if(event.keyCode == 13){
		var page = $(this).val();
		window.location.replace("/ECS/messagingadmin/?page=" + page);
	}
});
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//AUTO HIDE DATEPICKER
//$('.datepickerx').on('changeDate', function(event){
$("body").on("changeDate",".datepickerx",function(e) {
	$(this).datepicker('hide');
});

//LET DATEPICKER ACT AS READONLY
$("body").on("keydown","input.readonly",function(e) {
	if(e.keyCode == 8 || e.keyCode == 46){
        	$(this).val('');
        	$(this).datepicker('hide');
    }
    else{
    	e.preventDefault();
    }
});

//DATE INITIALIZATION
$('input.datepickerx').datepicker({
	format: 'mm/dd/yyyy',
	changeMonth: true,
    changeYear: true,
    showButtonPanel: true,
    yearRange: "-50:+0",
});


//AUTOHIDE POPOVER	
	$("body").on("click","input.POfield",function(event) {
		$(this).popover('hide');
	});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

/////SET NBU BUTTON//////////////	
	$("body").on("click","input#btnSetnbu",function(event) {
		$(this).prop('disabled',true);
		$('select#nbu').prop('disabled',true);
		$("input.disabler").prop('disabled',false);
		$('input.addInv').prop('disabled',false);
		var nbu = $('select#nbu').val();
		$('input#hnbu').val(nbu);
		$('input#vendorID').prop('disabled',false);
	});	
	
/////NBU CMB CHANGE EVENT//////////////
	$("body").on("change","select#nbu",function(event) {
		var nbu = $(this).val();
		if(nbu === ''){
			$('input#btnSetnbu').prop('disabled',true);
		}
		else{
			$('input#btnSetnbu').prop('disabled',false);
		}
	});


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//
$("body").on("click","input.delaccess",function(event) {
	event.preventDefault();
	
	var id = $(this).attr('id');
	
    $("#dialogdeleteaccess").dialog("open");
	$("#deleteID").val(id);
	
});
	





$("body").on("click","input.notes",function(event) {
	event.preventDefault();
	var SOANo = $(this).attr('SOANo');
	
	$.ajax({
        url : "/ECS/getremarks/", // the endpoint
        type : "post", // http method
        data : { SOANo:SOANo, }, // data sent with the post request
		
        
		// handle a successful response
        success : function(data) {
        	$("#dialognotes").dialog("open");
			//replace html
        	$('#remarksdiv').html(data);
        	},

        // handle a non-successful response
    	error : function(data) {
        	
        	}
		 });
	
	
});















//GO BUTTON FOR ALL
$('input#btnGo').on('click', function(event){
	var searchtype = $('select#searchtype').val();
	var keyword = $('input#txtKeyword').val();
	var bstatus = $('select#bstatus').val();
	
	$.ajax({
        url : "/ECS/SOASearch/", // the endpoint
        type : "post", // http method
        data : { searchtype:searchtype, keyword:keyword, bstatus:bstatus }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#soaviews').html(data);
			//$("span#stat").load(location.href + " span#stat");
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
	
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//DATE GO BUTTON FOR ALL
$('input#btnDTGo').on('click', function(event){
	var dtType = $('select#dtType').val();
	var dtFrom = $('input#dtFrom').val();
	var dtTo = $('input#dtTo').val();
	
	$.ajax({
        url : "/ECS/SOADTSearch/", // the endpoint
        type : "post", // http method
        data : { dtType:dtType, dtFrom:dtFrom, dtTo:dtTo }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#soaviews').html(data);
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//REFRESH ON MESSAGE MODAL HIDE
$('#msgmodal').on('hidden.bs.modal', function () {
  window.location.reload();
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

/*
//TANGGALON KAY MADAMAY ANG DESIGN SA UPDATE
//CLEAR MODAL DATA IF HIDDEN

$('.modal').on('hidden.bs.modal', function () {
  $('.modal-body').html('');
});
*/


////////////////////////////////////////////////////////////////////////
/////////////////////                              /////////////////////
/********************              SU              ********************/
/////////////////////                              /////////////////////
////////////////////////////////////////////////////////////////////////

/*
//TIKAS para mubaba ang scrollbar
$('#msgmodal').on('shown.bs.modal', function () {
	$('#focusfield').focus();
});
*/

//details for SU messages
$("body").on("click",".msglink",function(event) {
	event.preventDefault();
	var contact_username = $(this).attr('id'); 
	
	$.ajax({
        url : "/ECS/messaging/", // the endpoint
        type : "post", // http method
        data : { contact_username:contact_username }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#msgbody').html(data);
        	$('#focusfield').focus();
        	$('#comment').focus();
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
});


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//SOA creation for SU
$('#SOACreation').on('click', function(event){
	event.preventDefault();
	
	$.ajax({
        url : "/ECS/suSOACreation/", // the endpoint
        type : "post", // http method
        data : {  }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#bodycontent').html(data);
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
});



////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//delete SOA for SU
$('input.soadel').on('click', function(event){
	event.preventDefault();
	var SOANo = $(this).attr('SOANo'); 
	
	$("#dialogdel").dialog('option', 'buttons', {
        "Delete": function() {
            $(this).dialog("close");
            //DELETE CLICKED
            $.ajax({
	        url : "/ECS/SOAdeleteact/", // the endpoint
	        type : "post", // http method
	        data : { SOANo:SOANo }, // data sent with the post request
			
			// handle a successful response
	        success : function(data) {
	        	//alert(data);
	        	$('#deltext').text(data);
	        	  $(function() {
				    $( "#dialogdelsuc" ).dialog({
				      modal: true,
				      buttons: {
				        Ok: function() {
				        	$( this ).dialog( "close" );
				        	window.location.replace("/ECS/sumain/");
				        }
				        
				      },
				      beforeClose: function(){
				        window.location.replace("/ECS/sumain/");
				      }
				      
				    });
				  });
	        	},
	
	        // handle a non-successful response
	        error : function(data) {
	        	
	        	}
			 });
            
            
        },
        "Cancel": function() {
            $(this).dialog("close");
        }
    });
    $("#dialogdel").dialog("open");
    return false;
    
	
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//detail preview for SU
$('input.sudets').on('click', function(event){
	var SOANo = $(this).attr('SOANo');
	
	event.preventDefault();
	$.ajax({
        url : "/ECS/sudetprev/", // the endpoint
        type : "post", // http method
        data : { SOANo:SOANo }, // data sent with the post request
		
        
		// handle a successful response
        success : function(data) {
        	$('#sudetailsbody').html(data);
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

	/////DELETE BUTTON//////////////
	$("body").on("click","input.deleteInv",function(event) {
	//$('input.deleteInv').on('click',function(event){
		event.preventDefault();
		
		var fnum = parseInt($(this).attr('fnum'));
		var row = parseInt($(this).attr('rownum'));
		//var InvRowindex = parseInt($("input#InvRowindex" + fnum).val());
		var ctr = parseInt($('input#add' + fnum).attr('ctr'));
		
		$('#InvDate' + fnum + '-' + row).remove();
		$('#InvNo' + fnum + '-' + row).remove();
		$('#Amount' + fnum + '-' + row).remove();
		$('#ActBtn' + fnum + '-' + row).remove();
		
		
		$('input#add' + fnum).attr('ctr', ctr - 1);
		
		if (ctr <= 5){
			$('input#add' + fnum).prop('disabled',false);
			//$(this).show();
			}
		
			
	});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

	////ADDDDDDDDDD BUTTON///////
	$("body").on("click","input.addInv",function(event) {
    //$('input.addInv').on('click',function(event){
		event.preventDefault();
		var fnum = parseInt($(this).attr('fnum'));
		var row = parseInt($(this).attr('rownum'));
		var ctr = parseInt($(this).attr('ctr'));
		
		
		var InvRowindex = parseInt($("input#InvRowindex" + fnum).val());
		
		
		if (ctr<5){
			///////////////////////////////////////////////////////////////////////
			$("#multInvDate" + fnum).append(''+
				'<div id="InvDate' + fnum + '-' + (row+1) + '">'+
					'<input class="form-control input-sm datepickerx text-center disabler readonly InvDatefield fieldreq" type="text" placeholder="MM/DD/YYYY" name="InvDate' + fnum + '-' + (row+1) + '" fnum=' + fnum + ' rownum=' + (row+1) + ' />'+
				'</div>');
			$("#multInvNo" + fnum).append(''+
				'<div id="InvNo' + fnum + '-' + (row+1) + '">'+
					'<input class="form-control input-sm text-center disabler InvNofield fieldreq" type="text" placeholder="Invoice No." name="InvNo' + fnum + '-' + (row+1) + '" fnum=' + fnum + ' rownum=' + (row+1) + ' />'+
				'</div>');
			$("#multAmount" + fnum).append(''+
				'<div id="Amount' + fnum + '-' + (row+1) + '">' +
					'<input class="form-control input-sm text-right amts numdot disabler Amountfield fieldreq" type="text" placeholder="Amount" name="Amount' + fnum + '-' + (row+1) + '" fnum=' + fnum + ' rownum=' + (row+1) + ' />' +
					'<input id="holdamt' + fnum + '-' + (row+1) + '" type="hidden" value="0"/>'+
				'</div>');
			$("#multActBtn" + fnum).append('<div id="ActBtn' + fnum + '-' + (row+1) + '"><input type="image" src="/static/images/delete.png" style="height: 30px; padding-top: 5px; padding-bottom: 5px;" class="deleteInv" fnum=' + fnum + ' rownum=' + (row+1) + ' /><br /></div>');
			///////////////////////////////////////////////////////////////////////
			
			
			$( "input.datepickerx" ).datepicker({
				format: 'mm/dd/yyyy',
				changeMonth: true,
		        changeYear: true,
		        showButtonPanel: true,
		        yearRange: "-50:+0",
			});
			
			$("input#InvRowindex" + fnum).val(InvRowindex+1);
			
			$(this).attr('ctr', ctr + 1);
			//$().attr('ctr', ctr + 1);
			$(this).attr('rownum', row + 1);
			if (ctr == 4){
				$(this).prop('disabled',true);
				//$(this).hide();
			}
		}
		
		
	});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	
	//DISABLED
	//PO FIELD ON focusout
	$("body").on("focusout",".POfield",function(event) {
		var PONo = $(this).val();
		var fnum = $(this).attr('fnum');
		var Status = parseInt($("input#hStatus").val());
		var oldpo = $("input#holdpo" + fnum).val();
		var insertedpo = $("input#hponums").val().split(",").map(Number); 
		//var nbu = $("input#hnbu").val();
		var nbu = $("#nbu").val();
		var isadmin =  $("#hisadmin").val();
		
		//DELETE THE 0
		if ((insertedpo === 0) || (insertedpo === '0')){
			//Because we already know that index 0 is the index of the value 0
    		insertedpo.splice(0, 1);
		}
		
		var index = insertedpo.indexOf(parseInt(oldpo)); 
		if (index > -1)
			{
			insertedpo.splice(index,1);
			}
		
		
		if (PONo !== '') {
			$.ajax({
	        url : "/ECS/getPODate/", // the endpoint
	        type : "post", // http method
        	data : { PONo:PONo, nbu:nbu}, // data sent with the post request	
	    
	        
			beforeSend: function(xhr, settings) {
			        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
			            // Send the token to same-origin, relative URLs only.
			            // Send the token only if the method warrants CSRF protection
			            // Using the CSRFToken value acquired earlier
			            xhr.setRequestHeader("X-CSRFToken", csrftoken);
			        }
			        
			        //put loading bar here
			        $('#loading').show();
			        
			   	},
			
			// handle a successful response
	        success : function(data) {
	        	$('#loading').hide();
	        	var jElement;
	        	var errormsg;
	        	if (data.response === '' || data.response == 'Existed' || data.response == 'billto not same'){
	        		jElement = $("input#PONo" + fnum);
    				if(!jElement.hasClass('highlight')){
    					jElement.addClass('highlight');
    					$("input#hStatus").val(Status+1);
    					$("input.disabler").prop('disabled',true);
    					$("input#btnCreate").prop('disabled',true);
    					$("input#PONo" + fnum).prop('disabled',false);
    					$("input.addInv").prop('disabled',true);
    					$("input.deleteInv").prop('disabled',true);
    					
    					}
    				
    				$("input#podate" + fnum).val('');
    				$("input#hpodate" + fnum).val('');
    				
    				///////////////////////////////////////
    				//MESSAGE SETTING FOR POPOVER INVALID/IN DB	
					
    				if (data.response == 'Existed'){
						errormsg = 'PO already exists!';
					    }
					else if(data.response == 'billto not same'){
						errormsg = 'NBU not same!';
						}
			    	else{
					    errormsg = 'Invalid Entry!';
					    }
    				
    				$("input#PONo" + fnum).attr("data-content", errormsg);
    				$("input#PONo" + fnum).popover('show');
    				///////////////////////////////////////
	        		}
	        	else{
	        		if(insertedpo.indexOf(parseInt(PONo)) > -1)
	        			{
	        			//naay current sa taas dupe sya
	        			jElement = $("input#PONo" + fnum);
    					if(!jElement.hasClass('highlight')){
	    					jElement.addClass('highlight');
	    					$("input#hStatus").val(Status+1);
	    					$("input.disabler").prop('disabled',true);
	    					$("input#btnCreate").prop('disabled',true);
    						$("input#PONo" + fnum).prop('disabled',false);
    						$("input.addInv").prop('disabled',true);
    						$("input.deleteInv").prop('disabled',true);
    						}
    					
    					///////////////////////////////////////	
    					//MESSAGE SETTING FOR POPOVER DUPLICATE
    					errormsg = 'Duplicate entry not allowed.';
    					
    					$("input#PONo" + fnum).attr("data-content", errormsg);
    					$("input#PONo" + fnum).popover('show');
    					///////////////////////////////////////
	        			}
	        		
	        		else{	
		        		jElement = $("input#PONo" + fnum);
	    				if(jElement.hasClass('highlight')){
	    					jElement.removeClass('highlight');
	    					$("input#hStatus").val(Status-1);
	    					$("input.disabler").prop('disabled',false);
	    					$("input#btnCreate").prop('disabled',false);
	    					$("input.addInv").prop('disabled',false);
    						$("input.deleteInv").prop('disabled',false);
	    					}
	    			
		        		$("input#podate" + fnum).val(data.response);
		        		$("input#hpodate" + fnum).val(data.response);

		        		//hide popover
		        		$("input#PONo" + fnum).popover('hide');
		        		
		        		//
		        		insertedpo.push(PONo);
		        		$("input#holdpo" + fnum).val(PONo);
		        		$("input#hponums").val(insertedpo);
	        			}
	        		}
	        	},
	
	        // handle a non-successful response
	        error : function(data) {
	        	$('#loading').hide();
	        	$("#dialogConnerror").dialog("open");
	        	}      
		 	});
		}
		else{
			insertedpo = $.grep(insertedpo, function(value) {
			  return value != PONo;
			});
			

			var jElement = $("input#PONo" + fnum);
			if(jElement.hasClass('highlight')){
    			jElement.removeClass('highlight');
    			$("input#hStatus").val(Status-1);
    			$("input.disabler").prop('disabled',false);
    			$("input#btnCreate").prop('disabled',false);
    			$("input.addInv").prop('disabled',false);
    			$("input.deleteInv").prop('disabled',false);
    			}
			$("input#hponums").val(insertedpo);  			
			$("input#podate" + fnum).val('');
			$("input#hpodate" + fnum).val('');
			
			//unrequire fields	
			$("input#podate" + fnum).prop('required', false);
			$("input#PONo" + fnum).prop('required', false);
    	
		}
	});


////////////////////////////////////////////////////////////////////////
/////////////////////                              /////////////////////
/********************              CA              ********************/
/////////////////////                              /////////////////////
////////////////////////////////////////////////////////////////////////



////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//detail preview for CA
$('input.cadets').on('click', function(event){
	event.preventDefault();
	var SOANo = $(this).attr('SOANo');
	var SOAStatus = $(this).attr('Status');
	
	$.ajax({
	        url : "/ECS/cadetprev/", // the endpoint
	        type : "post", // http method
	        data : { SOANo:SOANo, SOAStatus:SOAStatus }, // data sent with the post request
			
			// handle a successful response
	        success : function(data) {
	        	$('#cadetailsbody').html(data);
	        	},
	
	        // handle a non-successful response
	        error : function(data) {
	        	
	        	}
			 });
	
});	

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////






////////////////////////////////////////////////////////////////////////
/////////////////////                              /////////////////////
/********************              PA              ********************/
/////////////////////                              /////////////////////
////////////////////////////////////////////////////////////////////////



////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


//detail preview for PA
$('input.padets').on('click', function(event){
	event.preventDefault();
	var SOANo = $(this).attr('SOANo');
	var SOAStatus = $(this).attr('Status');
	
	$.ajax({
        url : "/ECS/padetprev/", // the endpoint
        type : "post", // http method
        data : { SOANo:SOANo, SOAStatus:SOAStatus }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#padetailsbody').html(data);
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
});	

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	
////////////////////////////////////////////////////////////////////////
/////////////////////                              /////////////////////
/********************              MU              ********************/
/////////////////////                              /////////////////////
////////////////////////////////////////////////////////////////////////

//cmb report change
$("body").on("change","select#reporttype",function(event) {
	var reportnum = $(this).val();
	
	if((reportnum == 3) || (reportnum == 6)){
		document.getElementById('date2').innerHTML = 'Date:';
		$(".date1").hide();
	}
	else{
		document.getElementById('date2').innerHTML = 'Date To:';
		$(".date1").show();
	}
});


//cmb newaccttype change
$("body").on("change","select#newaccttype",function(event) {
	var isadmin = $(this).val();
	
	if(isadmin === '0'){
		$('div#vendorIDfield').show();
	}
	else{
		$('div#vendorIDfield').hide();
	}
	
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


//detail preview for MU
$('input.mudets').on('click', function(event){
	event.preventDefault();
	var SOANo = $(this).attr('SOANo');
	var SOAStatus = $(this).attr('Status');
	
	$.ajax({
        url : "/ECS/mudetprev/", // the endpoint
        type : "post", // http method
        data : { SOANo:SOANo, SOAStatus:SOAStatus }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#mudetailsbody').html(data);
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
});	

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//Message Search BUTTON FOR MU
$('input#btnMsgGo').on('click', function(event){
	var keyword = $('input#txtmsgkeyword').val();
	var msgby = $('select#msgby').val();
	
	$.ajax({
        url : "/ECS/MsgSearch/", // the endpoint
        type : "post", // http method
        data : { keyword:keyword, msgby:msgby }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#msgviews').html(data);
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
	
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//INPUT REQUIRE IF A FIELD IS TYPED	
	$("body").on("focusout","input.fieldreq",function(event) {
    	 var value = $(this).val();
    	 var fnum = $(this).attr('fnum');
    	 var row = $(this).attr('rownum');
    	 
    	 
    	 if((row !== null) && (value !== '')) {
    		 if( $('input#InvDate' + fnum + '-' + row).val() === '' && $('input#InvNo' + fnum + '-' + row).val() === '' && $('input#Amount' + fnum + '-' + row).val() === ''){
    	 		 $("input#podate" + fnum).prop('required', false);
		    	 $("input#PONo" + fnum).prop('required', false);
		    	 $('input#InvDate' + fnum + '-' + row).prop('required', false);
		    	 $('input#InvNo' + fnum + '-' + row).prop('required', false);
		    	 $('input#Amount' + fnum + '-' + row).prop('required', false);
		    	 }
	    	 else {
		    	 $("input#podate" + fnum).prop('required', true);
		    	 $("input#PONo" + fnum).prop('required', true);
		    	 $('input#InvDate' + fnum + '-' + row).prop('required', true);
		    	 $('input#InvNo' + fnum + '-' + row).prop('required', true);
		    	 $('input#Amount' + fnum + '-' + row).prop('required', true);
		    	 }
    		 }
    	 
    });
    
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//NUM ONLY with copy paste	
	$("body").on("keydown",".numonly",function(e) {
        // Allow: backspace, delete, tab, escape, enter and . is not allowed, allowed C & V
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13]) !== -1 ||
             // Allow: Ctrl+A, Command+A
            (e.keyCode == 65  && ( e.ctrlKey === true || e.metaKey === true ) ) || 
             // Allow: Ctrl+C, Command+C
            (e.keyCode == 67  && ( e.ctrlKey === true || e.metaKey === true ) ) ||
             // Allow: Ctrl+V, Command+V
            (e.keyCode == 86  && ( e.ctrlKey === true || e.metaKey === true ) ) ||
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

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//NUM ONLY and dots. only
	$("body").on("keydown",".numdot",function(e) {
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

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
	/*
	$(".numdot").keydown(function (e) {
        var theVal = $(this).val().replace(/,/g, "");
        var dotctr = (theVal.match(/\./g) || []).length;
        
        if ((dotctr == 1 && e.keyCode == 110) || (dotctr == 1 && e.keyCode == 190) || ((theVal == '') && (e.keyCode == 110)) || ((theVal == '') && (e.keyCode == 190))){
        	e.preventDefault();
        	}
        else{
        	return;
        	}
        });
	
	*/
	//AVOID 2 dots	
	$("body").on("keydown",".numdot",function(e) {
        var theVal = $(this).val().replace(/,/g, "");
        var dotctr = (theVal.match(/\./g) || []).length;
        
        if ((dotctr == 1 && e.keyCode == 110) || (dotctr == 1 && e.keyCode == 190) || ((theVal === '') && (e.keyCode == 110)) || ((theVal === '') && (e.keyCode == 190))){
        	e.preventDefault();
        	}
        else{
        	return;
        	}
        });

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

	//AMOUNT FORMATTER
	$("body").on("keyup","input.amts",function(event) {
    	var x = $(this).val();
    	$(this).val(x.toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
	});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

	//touppercase
	$("body").on("input",".uppercase", function(e) {
	    if (e.which >= 97 && e.which <= 122) {
	        var newKey = e.which - 32;
	        // I have tried setting those
	        e.keyCode = newKey;
	        e.charCode = newKey;
	    }

	    $(this).val(($(this).val()).toUpperCase());
	});


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
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



