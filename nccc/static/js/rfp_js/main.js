/**
 * @author fdypua
 */

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
/*
function printDiv(divName) {      
	var printContents = document.getElementById(divName).innerHTML;      
	var originalContents = document.body.innerHTML;      
	document.body.innerHTML = printContents;      
	window.print();      
	document.body.innerHTML = originalContents;
}
*/

        
function printDiv(divId) {
	//printDivCSS = new String ('<link href="/static/css/print.css" rel="stylesheet" type="text/css">');
	window.frames.print_frame.document.body.innerHTML=document.getElementById(divId).innerHTML;                 
	//window.frames["print_frame"].window.focus();                 
	window.frames.print_frame.window.print();             
	}

 
      

$(document).ready(function(){

	
$(function() {
	//////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////
		
	$('table.tablesorter').tablesorter({
	    // *** APPEARANCE ***
	    // Add a theme - try 'blackice', 'blue', 'dark', 'default'
	    //  'dropbox', 'green', 'grey' or 'ice'
	    // to use 'bootstrap' or 'jui', you'll need to add the "uitheme"
	    // widget and also set it to the same name
	    // this option only adds a table class name "tablesorter-{theme}"
	    theme: 'blue',
	    
	    // fix the column widths
	    widthFixed: false,
	    
	    // Show an indeterminate timer icon in the header when the table
	    // is sorted or filtered
	    showProcessing: false,

	    // header layout template (HTML ok); {content} = innerHTML,
	    // {icon} = <i/> (class from cssIcon)
	    headerTemplate: '{content}',

	    // return the modified template string
	    onRenderTemplate: null, // function(index, template){ return template; },

	    // called after each header cell is rendered, use index to target the column
	    // customize header HTML
	    onRenderHeader: function (index) {
	        // the span wrapper is added by default
	        $(this).find('div.tablesorter-header-inner').addClass('roundedCorners');
	    },

	    // *** FUNCTIONALITY ***
	    // prevent text selection in header
	    cancelSelection: true,

	    // other options: "ddmmyyyy" & "yyyymmdd"
	    dateFormat: "mmddyyyy",

	    // The key used to select more than one column for multi-column
	    // sorting.
	    sortMultiSortKey: "shiftKey",

	    // key used to remove sorting on a column
	    sortResetKey: 'ctrlKey',

	    // false for German "1.234.567,89" or French "1 234 567,89"
	    usNumberFormat: true,

	    // If true, parsing of all table cell data will be delayed
	    // until the user initializes a sort
	    delayInit: false,

	    // if true, server-side sorting should be performed because
	    // client-side sorting will be disabled, but the ui and events
	    // will still be used.
	    serverSideSorting: false,

	    // *** SORT OPTIONS ***
	    // These are detected by default,
	    // but you can change or disable them
	    // these can also be set using data-attributes or class names
	    headers: {
	        // set "sorter : false" (no quotes) to disable the column
	        0: {
	            sorter: "text"
	        },
	        1: {
	            sorter: "digit"
	        },
	        2: {
	            sorter: "text"
	        },
	        3: {
	            sorter: "url"
	        }
	    },

	    // ignore case while sorting
	    ignoreCase: true,

	    // forces the user to have this/these column(s) sorted first
	    sortForce: null,
	    // initial sort order of the columns, example sortList: [[0,0],[1,0]],
	    // [[columnIndex, sortDirection], ... ]
	    
	    
	    /*
	    sortList: [
	        [0, 0],
	        [1, 0],
	        [2, 0]
	    ],
	    */
	    
	    
	    // default sort that is added to the end of the users sort
	    // selection.
	    sortAppend: null,

	    // starting sort direction "asc" or "desc"
	    sortInitialOrder: "asc",

	    // Replace equivalent character (accented characters) to allow
	    // for alphanumeric sorting
	    sortLocaleCompare: false,

	    // third click on the header will reset column to default - unsorted
	    sortReset: false,

	    // restart sort to "sortInitialOrder" when clicking on previously
	    // unsorted columns
	    sortRestart: false,

	    // sort empty cell to bottom, top, none, zero
	    emptyTo: "bottom",

	    // sort strings in numerical column as max, min, top, bottom, zero
	    stringTo: "max",

	    // extract text from the table - this is how is
	    // it done by default
	    textExtraction: {
	        0: function (node) {
	            return $(node).text();
	        },
	        1: function (node) {
	            return $(node).text();
	        }
	    },

	    // use custom text sorter
	    // function(a,b){ return a.sort(b); } // basic sort
	    textSorter: null,
	    
	    
	    
	    // *** WIDGETS ***
	    
	    // apply widgets on tablesorter initialization
	    initWidgets: true,

	    // include zebra and any other widgets, options:
	    // 'columns', 'filter', 'stickyHeaders' & 'resizable'
	    // 'uitheme' is another widget, but requires loading
	    // a different skin and a jQuery UI theme.
	    
	    
	    widgets: ['filter'],

	    widgetOptions: {

	        // zebra widget: adding zebra striping, using content and
	        // default styles - the ui css removes the background
	        // from default even and odd class names included for this
	        // demo to allow switching themes
	        // [ "even", "odd" ]
	        zebra: [
	            "ui-widget-content even",
	            "ui-state-default odd"],

	        // uitheme widget: * Updated! in tablesorter v2.4 **
	        // Instead of the array of icon class names, this option now
	        // contains the name of the theme. Currently jQuery UI ("jui")
	        // and Bootstrap ("bootstrap") themes are supported. To modify
	        // the class names used, extend from the themes variable
	        // look for the "$.extend($.tablesorter.themes.jui" code below
	        theme: 'jui',

	        // columns widget: change the default column class names
	        // primary is the 1st column sorted, secondary is the 2nd, etc
	        
	        columns: [
	            "primary",
	            "secondary",
	            "tertiary"],
			
	        
	        // columns widget: If true, the class names from the columns
	        // option will also be added to the table tfoot.
	        columns_tfoot: true,

	        // columns widget: If true, the class names from the columns
	        // option will also be added to the table thead.
	        columns_thead: true,

	        // filter widget: If there are child rows in the table (rows with
	        // class name from "cssChildRow" option) and this option is true
	        // and a match is found anywhere in the child row, then it will make
	        // that row visible; default is false
	        filter_childRows: false,

	        // filter widget: If true, a filter will be added to the top of
	        // each table column.
	        filter_columnFilters: true,

	        // filter widget: css class applied to the table row containing the
	        // filters & the inputs within that row
	        filter_cssFilter: "tablesorter-filter",

	        // filter widget: Customize the filter widget by adding a select
	        // dropdown with content, custom options or custom filter functions
	        // see http://goo.gl/HQQLW for more details
	        
	        filter_functions: null,
	        /*
	        filter_functions: {
	        	4: {
	        		"LTS Supermarket, INC" :   
	        			function(e, n, f, i, $r, c, data) { 
	        				return e === f; 
	        				}
	        	},
	        	
	        	
	        },
	        */

	        // filter widget: Set this option to true to hide the filter row
	        // initially. The rows is revealed by hovering over the filter
	        // row or giving any filter input/select focus.
	        filter_hideFilters: false,

	        // filter widget: Set this option to false to keep the searches
	        // case sensitive
	        filter_ignoreCase: true,

	        // filter widget: jQuery selector string of an element used to
	        // reset the filters.
	        filter_reset: null,

	        // Delay in milliseconds before the filter widget starts searching;
	        // This option prevents searching for every character while typing
	        // and should make searching large tables faster.
	        filter_searchDelay: 300,

	        // Set this option to true if filtering is performed on the server-side.
	        filter_serversideFiltering: false,

	        // filter widget: Set this option to true to use the filter to find
	        // text from the start of the column. So typing in "a" will find
	        // "albert" but not "frank", both have a's; default is false
	        filter_startsWith: false,

	        // filter widget: If true, ALL filter searches will only use parsed
	        // data. To only use parsed data in specific columns, set this option
	        // to false and add class name "filter-parsed" to the header
	        filter_useParsedData: false,

	        // Resizable widget: If this option is set to false, resized column
	        // widths will not be saved. Previous saved values will be restored
	        // on page reload
	        resizable: true,

	        // saveSort widget: If this option is set to false, new sorts will
	        // not be saved. Any previous saved sort will be restored on page
	        // reload.
	        saveSort: true,

	        // stickyHeaders widget: css class name applied to the sticky header
	        stickyHeaders: "tablesorter-stickyHeader"

	    },

	    // *** CALLBACKS ***
	    // function called after tablesorter has completed initialization
	    initialized: function (table) {},

	    // *** CSS CLASS NAMES ***
	    tableClass: 'tablesorter',
	    cssAsc: "tablesorter-headerSortUp",
	    cssDesc: "tablesorter-headerSortDown",
	    cssHeader: "tablesorter-header",
	    cssHeaderRow: "tablesorter-headerRow",
	    cssIcon: "tablesorter-icon",
	    cssChildRow: "tablesorter-childRow",
	    cssInfoBlock: "tablesorter-infoOnly",
	    cssProcessing: "tablesorter-processing",

	    // *** SELECTORS ***
	    // jQuery selectors used to find the header cells.
	    selectorHeaders: '> thead th, > thead td',

	    // jQuery selector of content within selectorHeaders
	    // that is clickable to trigger a sort.
	    selectorSort: "th, td",

	    // rows with this class name will be removed automatically
	    // before updating the table cache - used by "update",
	    // "addRows" and "appendCache"
	    selectorRemove: "tr.remove-me",

	    // *** DEBUGING ***
	    // send messages to console
	    debug: false
	    

	}).tablesorterPager({

	    // target the pager markup - see the HTML block below
	    container: $(".pager"),
	    //
	    savePages : false,
	    //
	    
	    

	    // use this url format "http:/mydatabase.com?page={page}&size={size}" 
	    ajaxUrl: null,

	    // process ajax so that the data object is returned along with the
	    // total number of rows; example:
	    // {
	    //   "data" : [{ "ID": 1, "Name": "Foo", "Last": "Bar" }],
	    //   "total_rows" : 100 
	    // } 
	    ajaxProcessing: function(ajax) {
	        if (ajax && ajax.hasOwnProperty('data')) {
	            // return [ "data", "total_rows" ]; 
	            return [ajax.data, ajax.total_rows];
	        }
	    },

	    // output string - default is '{page}/{totalPages}';
	    // possible variables:
	    // {page}, {totalPages}, {startRow}, {endRow} and {totalRows}
	    output: '{startRow} to {endRow} ({totalRows})',

	    // apply disabled classname to the pager arrows when the rows at
	    // either extreme is visible - default is true
	    updateArrows: true,

	    // starting page of the pager (zero based index)
	    page: 0,//<-0

	    // Number of visible rows - default is 10
	    size: 25,//<-10

	    // if true, the table will remain the same height no matter how many
	    // records are displayed. The space is made up by an empty 
	    // table row set to a height to compensate; default is false 
	    fixedHeight: false,

	    // remove rows from the table to speed up the sort of large tables.
	    // setting this to false, only hides the non-visible rows; needed
	    // if you plan to add/remove rows with the pager enabled.
	    removeRows: true,

	    // css class names of pager arrows
	    // next page arrow
	    cssNext: '.next',
	    // previous page arrow
	    cssPrev: '.prev',
	    // go to first page arrow
	    cssFirst: '.first',
	    // go to last page arrow
	    cssLast: '.last',
	    // select dropdown to allow choosing a page
	    cssGoto: '.gotoPage',
	    // location of where the "output" is displayed
	    cssPageDisplay: '.pagedisplay',
	    // dropdown that sets the "size" option
	    cssPageSize: '.pagesize',
	    // class added to arrows when at the extremes 
	    // (i.e. prev/first arrows are "disabled" when on the first page)
	    // Note there is no period "." in front of this class name
	    cssDisabled: 'disabled'

	});

	// Extend the themes to change any of the default class names ** NEW **
	$.extend($.tablesorter.themes.jui, {
	    // change default jQuery uitheme icons - find the full list of icons
	    // here: http://jqueryui.com/themeroller/ (hover over them for their name)
	    table: 'ui-widget ui-widget-content ui-corner-all', // table classes
	    header: 'ui-widget-header ui-corner-all ui-state-default', // header classes
	    icons: 'ui-icon', // icon class added to the <i> in the header
	    sortNone: 'ui-icon-carat-2-n-s',
	    sortAsc: 'ui-icon-carat-1-n',
	    sortDesc: 'ui-icon-carat-1-s',
	    active: 'ui-state-active', // applied when column is sorted
	    hover: 'ui-state-hover', // hover class
	    filterRow: '',
	    even: 'ui-widget-content', // even row zebra striping
	    odd: 'ui-state-default' // odd row zebra striping
	});
	
	
	
	//////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////

	//loading bar
	$("#dialogloadingbar").dialog({
	      modal: true,
	      autoOpen: false,
	      position: { my: 'top', at: 'top+200',of: window },
	      open: function() { $('#dialogloadingbar').dialog('option', 'dialogClass', 'noTitle'); },
	    });
	//loading bar end
	
	//////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////
	
	//dialogactionevent notif
	$("#dialogactionevent").dialog({
	      modal: true,
	      autoOpen: false,
	      position: { my: 'top', at: 'top+100',of: window },
	      width: 350,
	      buttons: {
	        Ok: function() {
	        	$(this).dialog("close");
	        	window.location.replace("/RFP/main/");
	        },
	      },
	     
	    });
	//dialogactionevent notif end
	
	//////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////
	
	//dialognotes
	$("#dialognotes").dialog({
	      modal: true,
	      autoOpen: false,
	      position: { my: 'top', at: 'top+100',of: window },
	      width: 350,
	      height: 250,
	      close: function(event, ui) {
			
	      },
	      
	      buttons: {
	        Attach: function() {
	        	var rfpno = $('#hrfp_no').val();
	        	var nbu_id = $('#nbu').val();
		    	var savednotes = $('#savednotes').val();
	        	
	        	//update notes
	        	$.ajax({
	                url : "/RFP/attachnotes/", // the endpoint
	                type : "post", // http method
	                data : { rfpno:rfpno, nbu_id:nbu_id, savednotes:savednotes }, // data sent with the post request
	        		
	        		// handle a successful response
	                success : function(data) {
	                	$('#dialognotes').dialog("close");
	                	},

	                // handle a non-successful response
	                error : function(data) {
	                	
	                	}
	        		 });
	        	
	        },
	        
	      },
	      
	     
	    });
	//dialognotes end
	
	//////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////
	
	//vendor does not exist notif
	$("#dialogvendornotif").dialog({
	      modal: true,
	      autoOpen: false,
	      position: { my: 'top', at: 'top+100',of: window },
	      
	      buttons: {
	        Ok: function() {
	        	$(this).dialog("close");
	        	$('#vendor_id').val('');
	        	$('#vendor_name').val('');
	        	$('#check_payee').val('');
	        	$('#vendor_id').focus();
	        },
	      },
	     
	    });
	//vendor notif end
	
	//////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////
	
	//add request dialog
	$("#dialogprocessrequest").dialog({
	      modal: true,
	      autoOpen: false,
	      width: 1100,
	      //height: 5000,
	      closeOnEscape: false,
	      position: { my: 'top', at: 'top+50',of: window },
	      open: function(event, ui) {
	    	  $("#nbu option[value='']").prop('disabled',true);
	    	  $("input.aaid").val('');
	    	  
	    	  $('#nature_of_req').val('');
	    	  $('input.reqdet').prop('disabled',true);
	    	  $('select.reqdet').prop('disabled',true);
	    	  $('textarea').prop('disabled',true);
	    	  
	    	  $('select#nbu').attr('disabled',true);
	    	  //$("#nbu option[value='']").prop('disabled',true);
	    	  
	    	  $('select.calculate').prop('selectedIndex', 0);
	    	  $('.tag').hide();
	    	  
	    	  $('.coa_lookup').show();
	    	  
	    	  $('#notes').hide();
	    	  
	    	  $('.actbtns').hide();
	    	  $('.saveaction').hide();
			}, 
		  close: function(event, ui) {
			  
			  $('span#rfp_no').val('-----------------');
			  $('input#hrfp_no').val('');
			  
			  $('#bank_clps_div').collapse('hide');
			  
			  $("input.calculate").attr('disabled',true);
			  $("input.amts").val('').attr('disabled',true);
			  
			  $("select.calculate").attr('disabled',true).prop('selectedIndex', 0);
			  $('.tag').hide();
			  $('.coa_lookup').prop('disabled',false);
			  $('.coa_lookup').val('').show();
			  
			  $("input.aaid").val('');
			  /////////
	    	  
			},
	
	});//add request dialog end
	
	//////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////
	
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
		        url : "/RFP/pwdcheck/", // the endpoint
		        type : "post", // http method
		        data : { oldpwd:oldpwd, newpwd:newpwd, confirmnewpwd:confirmnewpwd }, // data sent with the post request
				
				// handle a successful response
		        success : function(data) {
		        	if (data == 'Successful.'){
			        	$("#dialogchangepwd").dialog("close");
			        	$("#dialogpwdchngsuccess").dialog("open");
			        	}
		        	else{
			        	//document.getElementById('pwdnote').innerHTML = data;
			        	$('#pwdnote').html(data);
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
	
	
	//CHANGE PWD NOTIF
    $("#dialogpwdchngsuccess").dialog({
      modal: true,
      autoOpen: false,
      closeOnEscape: false,
      position: { my: 'top', at: 'top+100',of: window },
      open: function(event, ui){ 
    	  $(".ui-dialog-titlebar-close", ui.dialog | ui).hide();
    	  }, 
      buttons: {
    	  Ok: function() {
    		  $("#dialogpwdchngsuccess").dialog("close");
    		  window.location.replace('/RFP/main/');
    		  },
        
      },
      beforeClose: function(){
        //event.preventDefault();
        
      }
      
    });
	
	
////////////////////////////////////////////////////////////////////////
	
	});//dialog function end 


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////////

//ADD REQUEST
$("body").on("click","#processrequestlink", function(event) {
	event.preventDefault();
	$("#dialogprocessrequest").dialog("open");
	//kaso walay glyphicons
	$("#dialogprocessrequest").dialog('option', 'title', 'Create New Request');
	
	$("select#nbu").prop('selectedIndex', 0);
	$("select#dept").prop('selectedIndex', 0);
	//$("select#location").prop('selectedIndex', 0);
	//document.getElementById('rfp_no').innerHTML = '-----------------';
	$('#rfp_no').html('-----------------');
	$('#hrfp_no').val('');	
	$("input[type='text']").val('');
	
	//disable all except nbu
	$("input.calculate").attr('disabled',true);
	$("input.amts").attr('disabled',true);
	$("input.coa_lookup").attr('disabled',true);
	$("select.calculate").attr('disabled',true);
	$("select#nbu").attr('disabled',false);
	
	//show Clear button
	$('#btnClear').show();
	//replace Request button text as Update
	//$('#btnRequest').show();//gibalhin sa nbu focusout
	$("#btnRequest").html('<span class="glyphicon glyphicon-floppy-disk"></span> Save');
	$("#btnRequest").attr('title','Save Request');
	//Submit Button with Post
	$('#btnSavePost').html('<span class="glyphicon glyphicon-floppy-saved"></span> <span id="btn-label">Save & Post</span>');
	$('#btnSavePost').attr('title','Save & Post Request');
	//$('#btnSavePost').show();//gibalhin sa nbu focusout
	
	//////////////////////////////////////////////////////////////////////////////////////////////////
	////////////// GIBALHIN SA TAAS USING APPROPRIATE OPTION TO CHANGE TITLE//////////////////////////
	//////////////////////////////////////////////////////////////////////////////////////////////////
	//change ui-dialog-title
	//document.getElementById('ui-id-5').innerHTML = '<span class="glyphicon glyphicon-plus-sign"></span> Create New Request';
	//$('#ui-id-5').html('<span class="glyphicon glyphicon-plus-sign"></span> Create New Request');
	//$('.ui-dialog-title').html('<span class="glyphicon glyphicon-plus-sign"></span> Create New Request');
	//$('#ui-id-6').html('<span class="glyphicon glyphicon-plus-sign"></span> Create New Request');
	//////////////////////////////////////////////////////////////////////////////////////////////////
	
	//coa_lookup show -> tag hide
	$('.coa_lookup').show();
	$('.tag').hide();
	$('.coa_lookup').attr('disabled',true);
	$('.clearAALine').attr('disabled',true);
	$('.dept_lookup').attr('disabled',true);
	$('.locs_lookup').attr('disabled',true);
	//set totals to 0.00
	$('.totals').html('0.00');

});

////////////////////////////////////////////////////////////////////////

//PROCESS BUTTON
$("body").on("click",".processbtn", function(event) {
	var rfp_no = $('#hrfp_no').val();
	var nbu_id = $("select#nbu").val();
	var nbu_text = $("select#nbu option:selected").text();
	var action;
	
	if($(this).attr('id') == 'btnCancel'){
		action = 'Cancel';
	}
	else if($(this).attr('id') == 'btnSendback'){
		action = 'Sendback';
	}
	else if($(this).attr('id') == 'btnReceive'){
		action = 'Receive';
	} 
	else{
		action = $('#btn-label').html();
	}
	
	$.ajax({
        url : "/RFP/actionevent/", // the endpoint
        type : "post", // http method
        data : { rfp_no:rfp_no, nbu_id:nbu_id, action:action }, // data sent with the post request
		
		// handle a successful response
        success : function(response) {
        	$('#dialogprocessrequest').dialog("close");
        	$("#dialogactionevent").dialog("open");
        	//document.getElementById('actmessage').innerHTML = '<b class="text-info">' + rfp_no + '</b> from <b class="text-danger"><i>' + nbu_text + '</i></b>' + response;
        	$('#actmessage').html('<b class="text-info">' + rfp_no + '</b> from <b class="text-danger"><i>' + nbu_text + '</i></b>' + response);
        	},

        // handle a non-successful response
        error : function(response) {
        	
        	}
		 });
	
});

////////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////////

//EDIT REQUEST
$("body").on("click",".rfpeditlink", function(event) {
	event.preventDefault();
	var rfp_no = $(this).attr('rfp_no');
	var nbu_id = $(this).attr('nbu_id');
	
	$("input[type='text']").val('');
	//coa_lookup show -> tag hide
	$('.coa_lookup').show();
	$('.tag').hide();
	//
	
	//set totals to 0.00
	$('.totals').html('0.00');
	$("input.amts").attr('disabled',true);
	$("select.calculate").attr('disabled',true);
	
	$('.clearAALine').attr('disabled',false);
	$('.dept_lookup').attr('disabled',false);
	$('.locs_lookup').attr('disabled',false);
	
	$('.dept_lookup').attr('readonly',false);
    $('.locs_lookup').attr('readonly',false);
	
	$('.coa_lookup').attr('disabled',true);
	
	//get rfp data
	$.ajax({
        url : "/RFP/getrfpdata/", // the endpoint
        type : "post", // http method
        data : { rfp_no:rfp_no, nbu_id:nbu_id }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$("#dialogprocessrequest").dialog("open");
        	//kaso walay glyphicons
        	$("#dialogprocessrequest").dialog('option', 'title', 'Request Information');
        	
        	$("select#nbu").val(nbu_id);
        	        	
			//SET RFP NO
        	//document.getElementById('rfp_no').innerHTML = rfp_no;
        	$('#rfp_no').html(rfp_no);
        	$('#hrfp_no').val(rfp_no);
        	
        	
        	//SET FIELD VALUES
        	$('#doc_no').val(data.docnumber);
        	$('#inv_date').val(data.invoicedate);
        	
        	$('#vendor_id').val(data.vendorid);
        	$('#vendor_name').val(data.vendorname);
        	$('#check_payee').val(data.checkpayee);
        	//set vendor details to readonly
        	$('.vendor_dets').attr('readonly','readonly');
        	$('#btnLookup').prop('disabled',true);
        	
        	//BANK DETAILS
        	if (data.bankaccountno !== ''){
        		$('#bank_clps_div').collapse('show');
        		$('#bankaccountno').val(data.bankaccountno);
        		$('#bankaccountname').val(data.bankaccountname);
        		$('#bankaccounttype').val(data.bankaccounttype);
        		$('#bankname').val(data.bankname);
        	}
        	else{
        		$('#bank_clps_div').collapse('hide');
        		$('#bankaccountno').val('');
        		$('#bankaccountname').val('');
        		$('#bankaccounttype').prop('selectedIndex', 0);
        		$('#bankname').val('');
        	}
        	
        	$('#expense_type').val(data.expensetype_id);
        	$('#grossamt').val(data.grossamount);
        	$('#netamount').val(data.netamount);
        	
        	$('#ers_no').val(data.ersnumber);
        	$('#ejo_no').val(data.ejonumber);
        	$('#epromos_no').val(data.epromosnumber);
        	
        	$('#cwo').val(data.cwo);
        	
        	
        	//$('#status_id').val(data['status_id']);
        	$('#nature_of_req').val(data.natureofreq);
        	
        	$('input.reqdet').prop('disabled',false);
    		$('select.reqdet').prop('disabled',false);
    		$('textarea').prop('disabled',false);
        	
    		
        	//disabled #nbu
        	$('select#nbu').attr('disabled',true);
        	
        	//set to hidden field
        	$('#nbucode').val(nbu_id);

        	//hide Clear button
        	$('#btnClear').hide();
        	
        	//iterate AA Details
			for (var key in data.aadata) {
				  if (data.aadata.hasOwnProperty(key)) {
					  key=parseInt(key);
					  $('#aa_id' + (key+1)).val(data.aadata[key][0]);
					  $('#dept' + (key+1)).val(pad(data.aadata[key][10],3));
					  $('#locs' + (key+1)).val(pad(data.aadata[key][11],5));
					  $('#coa_text' + (key+1)).val(pad(data.aadata[key][1],3) + ' - ' + data.aadata[key][2]); 
					  $("#coa_text" + (key+1)).hide();
					  $("#coa_text" + (key+1)).attr('disabled',false);
					  ////////////LABEL HERE//////////////
					  //document.getElementById('coa_span' + (key+1)).innerHTML = data.aadata[key][1] + ' - ' + data.aadata[key][2];
					  $('#coa_span' + (key+1)).html(pad(data.aadata[key][1],3) + ' - ' + data.aadata[key][2]);
					  $('#label-btn' + (key+1)).show();
					  
		              //enable same line
		              $('#grossamt' + (key+1)).attr('disabled',false);
		              //
		              $('#dept' + (key+1)).attr('disabled',false);
		              $('#locs' + (key+1)).attr('disabled',false);
		              //
		              $('#dept' + (key+1)).attr('readonly',true);
		              $('#locs' + (key+1)).attr('readonly',true);
		              //
		              $('#tax' + (key+1)).attr('disabled',false);
		              $('#vatamt' + (key+1)).attr('disabled',false);
		              $('#wtax' + (key+1)).attr('disabled',false);
		              $('#wtaxamt' + (key+1)).attr('disabled',false);
		              $('#netamt' + (key+1)).attr('disabled',false);
		              
		              //SET VALUES
					  $('#grossamt' + (key+1)).val(data.aadata[key][3].toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
					  $('#tax' + (key+1)).val(data.aadata[key][4]);
					  $('#vatamt' + (key+1)).val(data.aadata[key][5].toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
					  
					  $('#wtax' + (key+1)).val(data.aadata[key][6]+'|'+data.aadata[key][7]);
					  $('#wtaxamt' + (key+1)).val(data.aadata[key][8].toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
					  $('#netamt' + (key+1)).val(data.aadata[key][9].toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
					  
				  }
				}
			calc_totals();
			//end iterate
        	
        	
        	/////////////////////////////////////////////////
        	//show Request/Update - Print - Submit button
        	
        	if(data.userclass == 'PREPARER'){
        		if (data['status.desc'] == 'WORK'){
	        		$('#btnAction').html('<span class="glyphicon glyphicon-send"></span> <span id="btn-label">Post</span>');
	        		$('#btnAction').attr('title','Send for Checking');
	            	$('#btnAction').show();
	            	//replace Request button text as Update
	            	$('#btnRequest').show();
	    			$("#btnRequest").html('<span class="glyphicon glyphicon-check"></span> Update');
	    			$('#btnRequest').attr('title','Update RFP');
        			}
        		else if(data['status.desc'] == 'OPEN'){
        			$('#btnCancel').show();
        			}
        		else if(data['status.desc'] == 'APPROVED'){
        			$('#btnPrint').show();
        			}

        		}
        	else if(($.inArray(data['status.desc'], ["OPEN","PRINTED"]) !== -1) && (data.userclass == 'CHECKER')){
        		$('#btnSendback').show();
        		$('#btnAction').html('<span class="glyphicon glyphicon-check"></span> <span id="btn-label">Check</span>');
        		$('#btnAction').attr('title','Mark as Checked');
        		$('#btnAction').show();
        		}
        	else if(($.inArray(data['status.desc'], ["OPEN","PRINTED","CHECKED"]) !== -1) && (data.userclass == 'APPROVER')){
        		$('#btnSendback').show();
        		$('#btnAction').html('<span class="glyphicon glyphicon-thumbs-up"></span> <span id="btn-label">Approve</span>');
        		$('#btnAction').attr('title','Mark as Approved');
        		$('#btnAction').show();
        		//DISABLE - ENABLE APPROVE BUTTON DEPENDS ON AMOUNT
        		var NETTOTAL = $('#totalnet').html().replace(/,/g , "");
        		if (parseFloat(data.amount_limit) < NETTOTAL){
        			$('#btnAction').attr('disabled',true);
        			}
        		else{
        			$('#btnAction').attr('disabled',false);
        			}
        		}
        	else if(($.inArray(data['status.desc'], ["APPROVED","RECEIVED"]) !== -1) && (data.userclass == 'PAYASSOC')){
        		if(data['status.desc'] == "APPROVED"){
        			//DAPAT DUHA DIRI
        			$('#btnSendback').show();
        			$('#btnReceive').show();
        			//$('#btnAction').html('<span class="glyphicon glyphicon-send"></span> <span id="btn-label">Disbursement</span>');
        			//$('#btnAction').attr('title','Send to Disbursement');
        			//$('#btnAction').show();
        			}
        		else if(data['status.desc'] == "RECEIVED"){
        			$('#btnAction').html('<span class="glyphicon glyphicon-send"></span> <span id="btn-label">Disbursement</span>');
        			$('#btnAction').attr('title','Send to Disbursement');
        			$('#btnAction').show();
        			}
        		
        		}
        	
        	//////////////////////////////////////////////////////////////////////////////////////////////////
        	////////////// GIBALHIN SA TAAS USING APPROPRIATE OPTION TO CHANGE TITLE//////////////////////////
        	//////////////////////////////////////////////////////////////////////////////////////////////////
			//change ui-dialog-title
			//document.getElementById('ui-id-5').innerHTML = '<span class="glyphicon glyphicon-info-sign"></span> Request Information';
			//$('#ui-id-5').html('<span class="glyphicon glyphicon-info-sign"></span> Request Information');
			//$('.ui-dialog-title').html('<span class="glyphicon glyphicon-info-sign"></span> Request Information');
			//$('#ui-id-6').html('<span class="glyphicon glyphicon-info-sign"></span> Request Information');
        	//////////////////////////////////////////////////////////////////////////////////////////////////
			
        	
			//focus on dept (changed to focus on doc number)
        	//$('#dept').focus();
        	$('#doc_no').focus();
        	
        	
        	//////////////////////////////
        	//     UPDATE LIST START    //
        	//////////////////////////////
        	//update_dept
        	update_dept();
        	
        	//update_locs
        	update_locs(nbu_id);
        	
        	//update_coa
        	//update_coa(nbu_id);
        	//update_coa(nbu_id, data.department, data.location);
        	//////////////////////////////
        	//     UPDATE LIST END      //
        	//////////////////////////////
			
			
			//set rfpno/nbu_id on note
			$('#notes').show();
			$('#notes').attr('rfpno',rfp_no);
			$('#notes').attr('nbu_id',nbu_id);
			
			
			
        	},

        // handle a non-successful response
    	error : function(data) {
    		alert("Error!" + data.toString());
        	}
		});
	
});



////////////////////////////////////////////////////////////////////////

//BANK DETAILS COLLAPSE DIV
	//enabled
$("#bank_clps_div").on("hide.bs.collapse", function(){
	$('#bankclpslink').removeClass('btn-success');
	$('#bankclpslink').addClass('btn-danger');
	$("#bankclpslink").html('<span class="glyphicon glyphicon-remove-circle"></span> Bank Details');
	//setting of fields not required
	$("#bankaccountno").attr("required", false).val('');
	$("#bankaccountname").attr("required", false).val('');
	$("#bankaccounttype").attr("required", false).prop('selectedIndex', 0);
	$("#bankname").attr("required", false).val('');
});
	//disabled
$("#bank_clps_div").on("show.bs.collapse", function(){
	$('#bankclpslink').removeClass('btn-danger');
	$('#bankclpslink').addClass('btn-success');
	$("#bankclpslink").html('<span class="glyphicon glyphicon-ok-circle"></span> Bank Details');
	//setting of fields must be required
	$("#bankaccountno").attr("required", true);
	$("#bankaccountname").attr("required", true);
	$("#bankaccounttype").attr("required", true);
	$("#bankname").attr("required", true);
	
});
  
////////////////////////////////////////////////////////////////////////
  


//NOTE LINK
$('.notelink').on('click', function(event){
	event.preventDefault();
	var rfpno = $(this).attr('rfpno');
	var nbu_id = $(this).attr('nbu_id');
	
	$.ajax({
        url : "/RFP/getnotes/", // the endpoint
        type : "post", // http method
        data : { rfpno:rfpno, nbu_id:nbu_id }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$("#dialognotes").dialog("open");
        	
        	$('#savednotes').val(data);
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
});

////////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////////


$('.pwdlink').on('click', function(event){
	event.preventDefault();
	$("#dialogchangepwd").dialog("open");
});

////////////////////////////////////////////////////////////////////////

//Print Button
$("body").on("click","#btnPrint", function(event) {
	var nbu_id = $('#nbu').val();
	var rfpno = $('#rfp_no').html();
	
	
	//ajax to new html file get data returned and replace printarea div
	$.ajax({
        url : "/RFP/printRFP/", // the endpoint
        type : "post", // http method
        data : { nbu_id:nbu_id, rfpno:rfpno }, // data sent with the post request
        
		// handle a successful response
        success : function(data) {
        	$('#printarea').html(data);
        	printDiv('printarea');
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });	
});



////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////







//CLEAR BUTTON CLICKED
$('#btnClear').on('click', function(event){
	$('input[type="text"]').val('');
	$('#nature_of_req').val('');
	$('#hrfp_no').val('');
	
	$('input.reqdet').prop('disabled',true);
	$('select.reqdet').prop('disabled',true);
	$('textarea').prop('disabled',true);
	$('#nbu').prop('disabled',false);
	
	$('#nbu').focus();
	$("select#nbu").prop('selectedIndex', 0);
	//document.getElementById('rfp_no').innerHTML = '-----------------';
	$('#rfp_no').html('-----------------');
	/////////
	$("input.calculate").attr('disabled',true);
	$("input.amts").attr('disabled',true);
	$("input.coa_lookup").attr('disabled',true);
	$("select.calculate").attr('disabled',true).prop('selectedIndex', 0);
	$('.tag').hide();
	$('.coa_lookup').show();
	
	$("input.aaid").val('');
	///////////
	$('#location').prop('selectedIndex', 0);
	$('#dept').prop('selectedIndex', 0);
	
	calc_totals();
	
	
});


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//CALCULATE
$("body").on("keyup",".calculate", function(event) {
	var entryno = $(this).attr('entryno');
	var grossamt = $('#grossamt' + entryno).val().replace(/,/g , "");
	var taxsched = $('#tax' + entryno).val();
	var wtaxstr = $('#wtax' + entryno).val().split('|');
	
	//var wtaxsched = wtaxstr[0];//unused variable
	var rate = parseFloat(wtaxstr[1]);
	var VATamt;
	var WTaxamt;
	var NETamt; 
	
		
	if (grossamt !== ''){
		//FOR VAT
		if (taxsched == '1'){	
			VATamt = parseFloat(grossamt) * 0.12;
			WTaxamt = parseFloat(grossamt) * rate;
		}
		else if(taxsched == '2'){
			VATamt = 0.00;
			WTaxamt = parseFloat(grossamt) * rate;
		}
		else if(taxsched == '3'){
			VATamt = 0.00;
			WTaxamt = 0.00;
			$('#wtax' + entryno).prop('selectedIndex', 5);
		}
		
		//FOR NET
		NETamt = parseFloat(grossamt) + VATamt - WTaxamt; 
		
		//SET VALUES
		$('#vatamt' + entryno).val(VATamt.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
		$('#wtaxamt' + entryno).val(WTaxamt.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
		$('#netamt' + entryno).val(NETamt.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
		
	}
	else{
		//SET VALUES
		$('#vatamt' + entryno).val('');
		$('#wtaxamt' + entryno).val('');
		$('#netamt' + entryno).val('');
	}
	calc_totals();
	
	
});

$("body").on("change",".calculate", function(event) {
	var entryno = $(this).attr('entryno');
	var grossamt = $('#grossamt' + entryno).val().replace(/,/g , "");
	var taxsched = $('#tax' + entryno).val();
	var wtaxstr = $('#wtax' + entryno).val().split('|');
	
	//var wtaxsched = wtaxstr[0];//unused variable
	var rate = parseFloat(wtaxstr[1]);
	var VATamt;
	var WTaxamt;
	var NETamt; 
	
	
	if (grossamt !== ''){
		//FOR VAT
		if (taxsched == '1'){	
			VATamt = parseFloat(grossamt) * 0.12;
			WTaxamt = parseFloat(grossamt) * rate;
		}
		else if(taxsched == '2'){
			VATamt = 0.00;
			WTaxamt = parseFloat(grossamt) * rate;
		}
		else if(taxsched == '3'){
			VATamt = 0.00;
			WTaxamt = 0.00;
			$('#wtax' + entryno).prop('selectedIndex', 5);
		}
		
		//FOR NET
		NETamt = parseFloat(grossamt) + VATamt - WTaxamt; 
		
		//SET VALUES
		$('#vatamt' + entryno).val(VATamt.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
		$('#wtaxamt' + entryno).val(WTaxamt.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
		$('#netamt' + entryno).val(NETamt.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
	}
	else{
		//SET VALUES
		$('#vatamt' + entryno).val('');
		$('#wtaxamt' + entryno).val('');
		$('#netamt' + entryno).val('');
	}
	calc_totals();
});

//     CALCULATE TOTAL AMOUNT     //
function calc_totals(){
	var NEWTOTALGROSS = 0;
	var NEWTOTALVAT = 0;
	var NEWTOTALWTAX = 0;
	var NEWTOTALNET = 0;
	var gross;
	
	for (var x=1;x<=10;x++){
		gross = $('#grossamt' + x).val().replace(/,/g , "");
		/*
		vat = $('#vatamt' + x).val().replace(/,/g , "");
		tax = $('#wtaxamt' + x).val().replace(/,/g , "");
		net = $('#netamt' + x).val().replace(/,/g , "");
		*/
		if (gross !== ''){
			NEWTOTALGROSS += parseFloat($('#grossamt' + x).val().replace(/,/g , ""));
			NEWTOTALVAT += parseFloat($('#vatamt' + x).val().replace(/,/g , ""));
			NEWTOTALWTAX += parseFloat($('#wtaxamt' + x).val().replace(/,/g , ""));
			NEWTOTALNET += parseFloat($('#netamt' + x).val().replace(/,/g , ""));
		}
		
	}
	/*
	document.getElementById('totalgross').innerHTML = NEWTOTALGROSS.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	document.getElementById('totalvat').innerHTML = NEWTOTALVAT.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	document.getElementById('totalwtax').innerHTML = NEWTOTALWTAX.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	document.getElementById('totalnet').innerHTML = NEWTOTALNET.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	*/
	$('#totalgross').html(NEWTOTALGROSS.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
	$('#totalvat').html(NEWTOTALVAT.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
	$('#totalwtax').html(NEWTOTALWTAX.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
	$('#totalnet').html(NEWTOTALNET.toFixed(2).toString().replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
	
	
}


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////





////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//ON NBU FOCUSOUT
$("body").on("focusout","#nbu", function(e) {
	var nbu_id = $(this).val();
	var hrfp_no = $('input#hrfp_no').val();
	
	
	if ((nbu_id !== null)&&(nbu_id !== '') && (hrfp_no === '')&&(hrfp_no === '')){
		$.ajax({
	        url : "/RFP/getrfp_no/", // the endpoint
	        type : "post", // http method
	        data : { nbu_id:nbu_id }, // data sent with the post request
			
			// handle a successful response
	        success : function(rfpno) {
	        	$('#btnRequest').show();
	        	$('#btnSavePost').show();
	        	
	        	$('input.reqdet').prop('disabled',false);
	    		$('select.reqdet').prop('disabled',false);
	    		$('textarea').prop('disabled',false);
	        	
	        	//set rfp_no
	        	//document.getElementById('rfp_no').innerHTML = rfpno;
	        	$('#rfp_no').html(rfpno);
	        	$('input#hrfp_no').val(rfpno);
	        	
	        	$('.clearAALine').attr('disabled',false);
	        	$('.dept_lookup').attr('disabled',false);
	        	$('.locs_lookup').attr('disabled',false);
	        	//disabled #nbu
	        	$('#nbu').prop('disabled',true);
	        	
	        	
	        	//set to hidden field
	        	//var nbu = $('#nbu').val();
	        	$('#nbucode').val(nbu_id);
	        	
	        	$('#btnLookup').attr('disabled',false);
	        	
	        	//focus on dept (changed to focus on doc number)
	        	//$('#dept').focus();
	        	$('#doc_no').focus();
	        	
	        	//update department
	        	update_dept();
	        	
	        	//update locations
	        	update_locs(nbu_id);
	        	
	        	//set rfpno/nbu_id on note
	        	$('#notes').show();
				$('#notes').attr('rfpno',rfpno);
				$('#notes').attr('nbu_id',nbu_id);
				
	        	},

	        // handle a non-successful response
	    	error : function(data) {
	    		alert("Oops! Something went wrong! Please Try Again!");
	        	}
			});
		
	}
	else{
		//pop up notification (No NBU Selected. Please Select NBU.)
		
		//after that, focus on #nbu cmb
		//document.getElementById("nbu").focus();
		$('#nbu').focus();
		//document.getElementById('hrfp_no').innerHTML = '';
		//$('#hrfp_no').val('');
		//$('input#rfp_no').val('-----------------');
	}
	
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//kuhaon ang name sa MMS
$('#vendor_id').on('focusout', function(event){
	var vendorid = $(this).val();
	var locked = $(this).attr('readonly');
	
	if((vendorid!=='') && (locked === undefined)){
		$.ajax({
	        url : "/RFP/getvendorname/", // the endpoint
	        type : "post", // http method
	        data : { vendorid:vendorid }, // data sent with the post request
			
	        beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
		            // Send the token to same-origin, relative URLs only.
		            // Send the token only if the method warrants CSRF protection
		            // Using the CSRFToken value acquired earlier
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		        
		        //put loading bar here
		        $('#dialogloadingbar').dialog("open");
		        
		   	},
	        complete: function() {
	        	$('#dialogloadingbar').dialog("close");
	        },
		   	
			// handle a successful response
	        success : function(data) {
	        	var vendorname = data.vendorname; 
	        	var asvoth = data.asvoth;
	        	var afname = data.afname;
	        	
	        	$('#vendor_name').val(vendorname);
	        	
	        	if (asvoth=='0'){
	        		$('#check_payee').val(vendorname);
	        	}
	        	else{
	        		$('#check_payee').val(afname);
	        	}
	        	//set vendor details to readonly
	        	$('.vendor_dets').attr('readonly','readonly');
	        	$('#btnLookup').prop('disabled',true);
	        	},
	
	        // handle a non-successful response
	    	error : function(data) {
	    		//alert('Vendor does not exist.');
	    		$("#dialogvendornotif").dialog("open");
	    		
	        	}
        	
			});
	}
});




////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////



////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$("body").on("click","#btnClearVDets", function(event) {
	//set vendor details to readonly
	$('.vendor_dets').attr('readonly',false);
	$('.vendor_dets').val('');
	$('#btnLookup').prop('disabled',false);
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//Search Name of Vendor
$("body").on("click","#btnLookup", function(event) {
	var keyword = $('#vendor_name').val();
	$("#vendor_id").val('');
	$("#check_payee").val('');
	
	//if greater than 2 char and divisible by 3
	if(keyword !== ''){
		$.ajax({
	        url : "/RFP/getvendordetails/", // the endpoint
	        type : "post", // http method
	        data : { keyword:keyword }, // data sent with the post request
	        dataType: 'json',
			// handle a successful response
	        success : function(data) {
	        	$(".vname_lookup").autocomplete({
		    		source: function(request, response) {
	        	        var results = $.ui.autocomplete.filter(data, request.term);//data is here
	        	        //console.log(results.length);
	        	        response(results.slice(0, 15));//limit matches to 15
	        	    },
		    		minLength: 0,
		            select: function(event, ui) {
		            	$('#vendor_name').val(ui.item.value);
		            	
		            	///////////////////////////
		            	//ajax to get id and check payee
		            	$.ajax({
		        	        url : "/RFP/getvendorid/", // the endpoint
		        	        type : "post", // http method
		        	        data : { vendorname:ui.item.value }, // data sent with the post request
		        			
		        			// handle a successful response
		        	        success : function(data) {
		        	        	var vendorid = data.vendorid; 
		        	        	var asvoth = data.asvoth;
		        	        	var afname = data.afname;
		        	        	
		        	        	$('#vendor_id').val(vendorid);
		        	        	
		        	        	if (asvoth=='0'){
		        	        		$('#check_payee').val(ui.item.value);
		        	        	}
		        	        	else{
		        	        		$('#check_payee').val(afname);
		        	        	}
		        	        	
		        	        	//set vendor details to readonly
		        	        	$('.vendor_dets').attr('readonly','readonly');
		        	        	
		        	        	$('#btnLookup').prop('disabled',true);
		        	        	},
		        	
		        	        // handle a non-successful response
		        	    	error : function(data) {
		        	    		
		        	    		},
		        	    		
		                	
		        			});
		            	///////////////
		            	
		            	return false;
		            },
		            change: function(event, ui) {
		            	if ($("#vendor_name").val().length === 0) {
		            		$("#vendor_id").val('');
		            		$("#vendor_name").val('');
		            		$("#check_payee").val('');
		            		
		            	}
	            	
		            }
	            });
	        	
	        	$('#vendor_name').autocomplete("search", "");
	        	},
	
	        // handle a non-successful response
	        error : function(data) {
	        	
	        	}
			 });	
	
	}
	
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

$('.remove-label').on('click', function(event){
	var entryno = $(this).attr('entryno');
	var nbu_id = $('#nbu').val();
	var dept = $('#dept' + entryno).val(); 
	var locs = $('#locs' + entryno).val();
	
	remove_line_data(entryno);
	
	update_coa(entryno,nbu_id,dept,locs);
	$("#coa_text" + entryno).focus();
	
	
	//CONVERTED TO FUNCTION remove_line_data
	/*
	$("#coa_text" + entryno).val('');
	$("#coa_hidden" + entryno).val('');
	
	$("#coa_text" + entryno).show();
    document.getElementById('coa_span' + entryno).innerHTML = '';
    $('#label-btn' + entryno).hide();
    
    $("#coa_text" + entryno).focus();
    //disable same line if closed & delete all values
    $('#grossamt' + entryno).attr('disabled',true).val('');
    $('#tax' + entryno).attr('disabled',true).prop('selectedIndex', 0);
    $('#vatamt' + entryno).attr('disabled',true).val('');
    $('#wtax' + entryno).attr('disabled',true).prop('selectedIndex', 0);
    $('#wtaxamt' + entryno).attr('disabled',true).val('');
    $('#netamt' + entryno).attr('disabled',true).val('');
    
    calc_totals();
    */
});

$('.clearAALine').on('click', function(event){
	var entryno = $(this).attr('entryno');
	if (entryno==='1'){
		$('.dept_lookup').val('').attr('readonly',false);
		$('.locs_lookup').val('').attr('readonly',false);		
		$('.coa_lookup').val('').attr('disabled',true);
	}
	else{
		$('#dept' + entryno).val('').attr('readonly',false);
		$('#locs' + entryno).val('').attr('readonly',false);
		$('#coa_text' + entryno).val('').attr('disabled',true);
	}
	
	remove_line_data(entryno);
	$('#dept' + entryno).focus();
	
});



////////////////////////////////////////////////////////////////////////

function remove_line_data(entryno){
	if (entryno=='1'){
		$(".coa_lookup").val('');
		//$("#coa_hidden" + entryno).val('');
		
		$("#coa_text" + entryno).show();
	    //document.getElementById('coa_span' + entryno).innerHTML = '';
	    $('#coa_span' + entryno).html('');
	    $('#label-btn' + entryno).hide();
	    
	    //disable same line if closed & delete all values
	    $('#grossamt' + entryno).attr('disabled',true).val('');
	    $('#tax' + entryno).attr('disabled',true).prop('selectedIndex', 0);
	    $('#vatamt' + entryno).attr('disabled',true).val('');
	    $('#wtax' + entryno).attr('disabled',true).prop('selectedIndex', 0);
	    $('#wtaxamt' + entryno).attr('disabled',true).val('');
	    $('#netamt' + entryno).attr('disabled',true).val('');
	}
	else{
		$("#coa_text" + entryno).val('');
		//$("#coa_hidden" + entryno).val('');
		
		$("#coa_text" + entryno).show();
	    //document.getElementById('coa_span' + entryno).innerHTML = '';
	    $('#coa_span' + entryno).html('');
	    $('#label-btn' + entryno).hide();
	    
	    //disable same line if closed & delete all values
	    $('#grossamt' + entryno).attr('disabled',true).val('');
	    $('#tax' + entryno).attr('disabled',true).prop('selectedIndex', 0);
	    $('#vatamt' + entryno).attr('disabled',true).val('');
	    $('#wtax' + entryno).attr('disabled',true).prop('selectedIndex', 0);
	    $('#wtaxamt' + entryno).attr('disabled',true).val('');
	    $('#netamt' + entryno).attr('disabled',true).val('');
	}
    
    calc_totals();
}


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

function update_dept(){
	$.ajax({
        url : "/RFP/get_dept_list/", // the endpoint
        type : "post", // http method
        data : { }, // data sent with the post request
        dataType: 'json',
		// handle a successful response
        success : function(data) {
        	
        	$(".dept_lookup").autocomplete({
        		source: function(request, response) {
        	        var results = $.ui.autocomplete.filter(data, request.term);//data is here
        	        //console.log(results.length);
        	        response(results.slice(0, 15));//limit matches to 15
        	    },
	            select: function(event, ui) {
	            	var entryno = $(this).attr('entryno');
	                //$("#dept" + entryno).val(ui.item.value.substring(0, 3));
	            	//set to all dept fields by default
	            	if (entryno === '1'){
	            		$('.dept_lookup').val(ui.item.value.substring(0, 3));
	            		$('.dept_lookup').attr('readonly',true);
	            	}
	            	else{
	            		$('#dept' + entryno).val(ui.item.value.substring(0, 3));
	            		$('#dept' + entryno).attr('readonly',true);
	            	}
	            	
	            	$('#locs' + entryno).focus();
	            	validate_check_coalist(entryno);
	                return false;
	            },
	            change: function(event, ui) {
	            	var entryno = $(this).attr('entryno');
	            	if ($("#dept" + entryno).val().length === 0) {
	            		$("#dept" + entryno).val('');
	            		
	            	}
            	
	            }
            });
        	
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });	
}

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

function update_locs(nbu_id){
	$.ajax({
        url : "/RFP/get_locs_list/", // the endpoint
        type : "post", // http method
        data : { nbu_id:nbu_id }, // data sent with the post request
        dataType: 'json',
		// handle a successful response
        success : function(data) {
        	
        	$(".locs_lookup").autocomplete({
        		//source: data,
        		source: function(request, response) {
        	        var results = $.ui.autocomplete.filter(data, request.term);
        	        //console.log(results.length);
        	        response(results.slice(0, 15));//limit matches to 15
        	    },
	            select: function(event, ui) {
	            	var entryno = $(this).attr('entryno');
	            	//set to all locs fields by default if entry is 1
	            	if (entryno == '1'){
	            		$(".locs_lookup").val(ui.item.value.substring(0, 5));
	            		$(".locs_lookup").attr('readonly',true);
	            	}
	            	else{
	            		$('#locs' + entryno).val(ui.item.value.substring(0, 5));
	            		$('#locs' + entryno).attr('readonly',true);
	            	}
	            	
	            	validate_check_coalist(entryno);
	            	return false;
	            },
	            change: function(event, ui) {
	            	var entryno = $(this).attr('entryno');
	            	if ($("#locs" + entryno).val().length === 0) {
	            		$("#locs" + entryno).val('');
	            	}
            	
	            }
            });
        	
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });	
}


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


//validate and check coa_list
function validate_check_coalist(entryno){
	var dept = $('#dept' + entryno).val();
	var locs = $('#locs' + entryno).val();
	
	if((dept!=='')&&(locs!=='')){
		var nbu_id = $('#nbu').val();
		if (entryno == '1'){
			$('.coa_lookup').attr('disabled',false);
		}
		else{
			$('#coa_text' + entryno).attr('disabled',false);
		}
		
		$('#coa_text' + entryno).focus();
		update_coa(entryno,nbu_id,dept,locs);
		
	}
}

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

//function update_coa(nbu_id){
function update_coa(entryno,nbu_id,dept,locs){
	$.ajax({
        url : "/RFP/get_coa_list/", // the endpoint
        type : "post", // http method
        data : { nbu_id:nbu_id,dept:dept,locs:locs }, // data sent with the post request
        dataType: 'json',
		// handle a successful response
        success : function(data) {
        	var coasetting;
        	if (entryno === '1'){
        		coasetting = '.coa_lookup'; 
        	}
        	else{
        		coasetting = '#coa_text' + entryno;
        	}
        	
        	//$("#coa_text" + entryno).autocomplete({
        	$(coasetting).autocomplete({
        		//source: data,
        		source: function(request, response) {
        	        var results = $.ui.autocomplete.filter(data, request.term);
        	        //console.log(results.length);
        	        response(results.slice(0, 15));//limit matches to 15
        	    },
        	    minLength: 0,
	            select: function(event, ui) {
	            	var entryno = $(this).attr('entryno');
	                $("#coa_text" + entryno).val(ui.item.value);
	                $("#coa_text" + entryno).hide();
	                $('#coa_span' + entryno).html(ui.item.value);
	                $('#label-btn' + entryno).show();
	                //enable same line
	                $('#grossamt' + entryno).attr('disabled',false);
	                $('#tax' + entryno).attr('disabled',false);
	                $('#vatamt' + entryno).attr('disabled',false);
	                $('#wtax' + entryno).attr('disabled',false);
	                $('#wtaxamt' + entryno).attr('disabled',false);
	                $('#netamt' + entryno).attr('disabled',false);
	                
	                $('#grossamt' + entryno).focus();
	                
	                return false;
	            },
	            change: function(event, ui) {
	            	var entryno = $(this).attr('entryno');
	            	if ($("#coa_text" + entryno).val().length === 0) {
	            		//$("#coa_hidden" + entryno).val('');
	            		
	            		$("#coa_text" + entryno).show();
		                //document.getElementById('coa_span' + entryno).innerHTML = '';
		                $('#coa_span').html('');
		                $('#label-btn' + entryno).hide();
	            	}
            	
	            }
            });
        	//
        	$('#coa_text' + entryno).autocomplete("search", "");
        	
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });	
	

}

////////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////////
///////////////////// USER ACCOUNT CONTROLS ////////////////////////////
////////////////////////////////////////////////////////////////////////

//POPULATE CLERK
function populate_clerk(){
	$.ajax({
        url : "/RFP/populate_clerk/", // the endpoint
        type : "post", // http method
        data : {  }, // data sent with the post request
        dataType: 'json',
		// handle a successful response
        success : function(data) {
        	$("#clerk_lookup").autocomplete({
	    		source: function(request, response) {
        	        	var results = $.ui.autocomplete.filter(data, request.term);//data is here
	        	        //console.log(results.length);
	        	        response(results.slice(0, 10));//limit matches to 10
        	    },
	    		minLength: 0,
	            select: function(event, ui) {
	            		$('#clerk_lookup').val(ui.item.value.toString().substring(0, 3));
	            		$('#clerk_lookup').hide();
	            		console.log(ui.item.value);
	            		
	            		$('#clerktag').show();
	            		$('#clerktag_value').html(ui.item.value);
	            		///////////////
	            		return false;
	            },
	            change: function(event, ui) {
	            	if ($("#clerk_lookup").val().length === 0) {
	            		$("#clerk_lookup").val('');
	            		
	            	}
	            }
            });
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });	
}

//RESET CLERK (X BUTTON)
$("body").on("click","#resetclerk", function(event) {
	$('#clerk_lookup').val('');
	$('#clerk_lookup').show();
	
	$('#clerktag_value').html('');
	$("#clerktag").hide();
});


//ACCOUNT LINK
$("body").on("click",".usercreatelink", function(event) {
	$("#dialogaccountinfo").dialog("open");
	
	$('#loa_applimit').hide();
	$('#locstag').hide();
	$('#userlocs_lookup').show();
	
	$('.approver_group').hide();
	$('.clerk_group').hide();
	$('#clerktag').hide();
	
	$('#btnPopulateLocs').attr('disabled',false);//disable PopulateLocs Button
	$('#processaction').val('Create');
	$('#actiontext').html('Create');
});


//CREATE ACCOUNT DIALOG
$("#dialogaccountinfo").dialog({
  modal: true,
  autoOpen: false,
  width: 550,
  position: { my: 'top', at: 'top+100', of: window },
  open: function( event, ui ) {
	  $("#userclass option[value='']").prop('disabled',true);
	  $("#userrole option[value='']").prop('disabled',true);
	  $("#usernbu option[value='']").prop('disabled',true);
	  $("#userdept option[value='']").prop('disabled',true);
	  
	  $("input[type='text']").val('');
	  $('select').prop('selectedIndex', 0);
	  $('#locstag_value').html('');
	  $('#clerktag_value').html('');
	  $('#amount_limit').attr('required',false);
	  $('#pwdreset').hide();
	  populate_clerk();
  	},
});

//LIMIT TRIGGER CHANGE
$("body").on("change","#limit_trigger", function(event) {
	var selctd = $(this).val();
	if(selctd === 'N'){
		$('#loa_applimit').hide();
		$('#amount_limit').attr('required',false);
	}
	else if(selctd === 'Y'){
		$('#loa_applimit').show();
		$('#amount_limit').attr('required',true);
	}
});

//USER CLASS CHANGED
$("body").on("change","#userclass", function(event) {
	var selctd = $(this).val();
	if(selctd === '3'){
		$('.approver_group').show();
		$('#userrole').attr('required',true);
		//$('#limit_trigger').attr('required',true);
		$('.clerk_group').hide();
		$('#clerk_lookup').attr('required',false);

	}
	else if(selctd === '4'){
		$('.approver_group').hide();
		$('#userrole').attr('required',false);
		$('.clerk_group').show();
		$('#clerk_lookup').attr('required',true);
	}
	else{
		$('.approver_group').hide();
		$('#userrole').attr('required',false);
		//$('#limit_trigger').attr('required',false);
		$('.clerk_group').hide();
		$('#clerk_lookup').attr('required',false);

	}
});

//POPULATE USER LOCATION
$("body").on("click","#btnPopulateLocs", function(event) {
	var usernbu = $('#usernbu').val();
	
	if((usernbu !== null) && (usernbu!=='')){
		$.ajax({
	        url : "/RFP/populate_locs/", // the endpoint
	        type : "post", // http method
	        data : { usernbu:usernbu }, // data sent with the post request
	        dataType: 'json',
			// handle a successful response
	        success : function(data) {
	        	$("#userlocs_lookup").autocomplete({
		    		source: function(request, response) {
	        	        	var results = $.ui.autocomplete.filter(data, request.term);//data is here
		        	        //console.log(results.length);
		        	        response(results.slice(0, 10));//limit matches to 10
	        	    },
		    		minLength: 0,
		            select: function(event, ui) {
		            		$('#userlocs_lookup').val(ui.item.value.toString().substring(0, 5));
		            		$('#userlocs_lookup').hide();
		            		
		            		$('#locstag_value').html(ui.item.value);
		            		$("#locstag").show();
		            		$('#btnPopulateLocs').attr('disabled',true);//disable PopulateLocs Button
		            		///////////////
		            		return false;
		            },
		            change: function(event, ui) {
		            	if ($("#userlocs_lookup").val().length === 0) {
		            		$("#userlocs_lookup").val('');
		            		
		            	}
		            }
	            });
	        	
	        	$('#userlocs_lookup').autocomplete("search", "").focus();
	        	},
	
	        // handle a non-successful response
	        error : function(data) {
	        	
	        	}
			 });	
	}
});

//RESET LOCATION (X BUTTON)
$("body").on("click","#resetlocs", function(event) {
	$('#userlocs_lookup').val('');
	$('#userlocs_lookup').show();
	
	$('#locstag_value').html('');
	$("#locstag").hide();
	$('#btnPopulateLocs').attr('disabled',false);//enable PopulateLocs Button
});

//CREATE ACCOUNT BUTTON
$("body").on("click","#btnCreateAcct", function(event) {
	var locsvalue = $('#locstag_value').html();
	var clerkvalue = $('#clerktag_value').html();
	
	if(locsvalue === ''){
		event.preventDefault();
		$('#userlocs_lookup').val('').focus();
		//$('#btnCreateAcct').attr('disabled',true);
	}
	else if(clerkvalue === ''){
		event.preventDefault();
		$('#clerk_lookup').val('').focus();
	}
		
});

//EDIT ACCOUNT LINK
$("body").on("click",".editacctlink", function(event) {
	var theuser = $(this).attr('id');
	
	$("#dialogaccountinfo").dialog("open");
	$('#pwdreset').show();
	$('#actiontext').html('Update');
	
	$.ajax({//ajax to get user info
        url : "/RFP/getuserinfo/", // the endpoint
        type : "post", // http method
        data : { theuser:theuser }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	$('#usertoupdate').val(theuser);
        	$('#fname').val(data.fname);
        	$('#mname').val(data.mname);
        	$('#lname').val(data.lname);
        	$('#userstatus').val(data.userstatus);
        	$('#userclass').val(data.userclass_id);
        	
        	if(data.userclass_id === '3'){//if userclass is APPROVER
        		$('.approver_group').show();//show role
        		$('.clerk_group').hide();//hide clerk
        		$('#userrole').val(data.userrole_id);
        		
        		if((data.useramount_limit !== 'None') && (data.userrole !== '7')){//if approving amount is override
            		$('#limit_trigger').val('Y');
            		$('#loa_applimit').show();
            		$('#amount_limit').val(data.useramount_limit.replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","));
            	}
        		else{
        			$('#limit_trigger').val('N');
        			$('#loa_applimit').hide();
        			$('#amount_limit').val('');
        		}
        	}
        	else if(data.userclass_id === '4'){
        		$('.approver_group').hide();//hide approver group
        		$('.clerk_group').show();//show clerk
        		$('#clerk_lookup').attr('required',true);
        		$('#clerktag').show();
        		$('#clerk_lookup').val(data.userclerknum).hide();
        		$('#clerktag_value').html(data.userclerknum + ' - ' + data.fname + ' ' + data.lname);
        	}
        	else{
        		$('.approver_group').hide();
        		$('.clerk_group').hide();
        		console.log('a');
        	}
        	
        	
        	$('#usernbu').val(data.nbu_id);
        	$('#userdept').val(data.department);
        	$('#locstag_value').html(data.location);//set locstag_value
        	$('#locstag').show();//show locstag
        	$('#btnPopulateLocs').attr('disabled',true);//disable PopulateLocs Button
        	$('#userlocs_lookup').val(data.location);//set userlocs_lookup value
        	$('#userlocs_lookup').hide();//hide userlocs_lookup
        	
        	$('#processaction').val('Update');
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
	
});



////////////////////////////////////////////////////////////////////////
//////////////////////// ACCESS CONTROLS ///////////////////////////////
////////////////////////////////////////////////////////////////////////

//ACCESS LINK
$("body").on("click","#accesslink", function(event) {
	$("#dialognewaccess").dialog("open");
	
	$("#usertag").hide();
	$("#locstag").hide();
	
	$('#userlocs_lookup').show();
	$('#user_lookup').show();
});

//NEW ACCESS DIALOG
$("#dialognewaccess").dialog({
  modal: true,
  autoOpen: false,
  width: 550,
  position: { my: 'top', at: 'top+100', of: window },
  open: function( event, ui ) {
	  $("#usernbu option[value='']").prop('disabled',true);
	  $("#userdept option[value='']").prop('disabled',true);
	  
	  $("input[type='text']").val('');
	  $('select').prop('selectedIndex', 0);
	  $('#usertag_value').html('');
	  $('#locstag_value').html('');
  	},
});

//POPULATE USER LOCATION
$("body").on("click","#btnPopulateUser", function(event) {
	var userkey = $('#user_lookup').val();
	
	if((userkey !== null) && (userkey!=='')){
		$.ajax({
	        url : "/RFP/populate_user/", // the endpoint
	        type : "post", // http method
	        data : { userkey:userkey }, // data sent with the post request
	        dataType: 'json',
			// handle a successful response
	        success : function(data) {
	        	$("#user_lookup").autocomplete({
		    		source: function(request, response) {
	        	        	var results = $.ui.autocomplete.filter(data, request.term);//data is here
		        	        //console.log(results.length);
		        	        response(results.slice(0, 10));//limit matches to 10
	        	    },
		    		minLength: 0,
		            select: function(event, ui) {
		            		$('#user_lookup').val(ui.item.value);
		            		$('#user_lookup').hide();
		            		
		            		$('#usertag_value').html(ui.item.value);
		            		$('#usertag').show();
		            		
		            		var userdata = ui.item.value.split('|'); 
		        			
		            		$('#theuser').val(userdata[0]);
		            		$('#fname').val(userdata[1]);
		            		$('#mname').val(userdata[2]);
		            		$('#lname').val(userdata[3]);
		            		
		            		///////////////
		            		return false;
		            },
		            change: function(event, ui) {
		            	if ($("#user_lookup").val().length === 0) {
		            		$("#user_lookup").val('');
		            		
		            	}
		            }
	            });
	        	
	        	$('#user_lookup').autocomplete("search", "").focus();
	        	},
	
	        // handle a non-successful response
	        error : function(data) {
	        	
	        	}
			 });	
	}
});

//RESET USER (X BUTTON)
$("body").on("click","#resetuser", function(event) {
	$('#user_lookup').val('');
	$('#theuser').val('');
	$('#fname').val('');
	$('#mname').val('');
	$('#lname').val('');
	
	$('#user_lookup').show();
	
	$('#usertag_value').html('');
	$('#usertag').hide();
});

//GRANT ACCESS BUTTON
$("body").on("click","#btnGrantAccess", function(event) {
	var uservalue = $('#usertag_value').html();
	var locsvalue = $('#locstag_value').html();
	
	if(uservalue === ''){
		event.preventDefault();
		$('#user_lookup').focus();
		}
	else if (locsvalue === ''){
		event.preventDefault();
		$('#userlocs_lookup').focus();
		}
	
});

//REVOKE ACCESS
$("body").on("click",".delaccess", function(event) {
	var revokeid = $(this).attr('id');

	$("#dialogrevokeaccess").dialog("open");
	$('#revokeid').val(revokeid);
});

//REVOKE ACCESS DIALOG
$("#dialogrevokeaccess").dialog({
  modal: true,
  autoOpen: false,
  position: { my: 'top', at: 'top+100',of: window },
  buttons: {
    Revoke: function() {
		var revokeid = $('#revokeid').val();
		console.log(revokeid);
		
		$.ajax({
	        url : "/RFP/revokeaccess/", // the endpoint
	        type : "post", // http method
	        data : { revokeid:revokeid }, // data sent with the post request
			
			// handle a successful response
	        success : function(data) {
	        	$("#dialogrevokeaccess").dialog("close");
	        	window.location.replace("/RFP/access/");
	        	},
	
	        // handle a non-successful response
	        error : function(data) {
	        	
	        	}
			 });
    },
    Cancel: function() {
    	//event.preventDefault();
        $(this).dialog("close");
    }
  },
 
});

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////



////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////



////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////



////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////




////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////

/**************************************************************************************/
/**************************************************************************************/
/**************************************************************************************/

	//NO INPUT
	$("body").on("keydown","input.noinput",function(event) {
		event.preventDefault();
	});
	
/**************************************************************************************/
/**************************************************************************************/
/**************************************************************************************/
	
	//AVOID 2 dots	
	$(".numdot").keydown(function (e) {
        var theVal = $(this).val().replace(/,/g, "");
        var dotctr = (theVal.match(/\./g) || []).length;
        
        if ((dotctr === 1 && e.keyCode === 110) || (dotctr === 1 && e.keyCode === 190) || ((theVal === '') && (e.keyCode === 110)) || ((theVal === '') && (e.keyCode == 190))){
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

//DATE 
	$( ".datepickerx" ).datepicker({
		 //format: 'yyyy-mm-dd',
		 changeMonth: true,
         changeYear: true,
         //showButtonPanel: true, //TODAY - DONE BUTTON
         yearRange: "-10:+0",
         
	});

	
	


	
});//end
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

function pad(num, size) {
    var s = "000000000" + num;
    return s.substr(s.length-size);
}







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





/*
function update_locations(nbu, locs){
	$.ajax({
        url : "/RFP/select_locations/", // the endpoint
        type : "post", // http method
        data : { nbu:nbu }, // data sent with the post request
		
		// handle a successful response
        success : function(data) {
        	document.getElementById('locations').innerHTML = data;

        	$('#location').val(locs);
        	
        	},

        // handle a non-successful response
        error : function(data) {
        	
        	}
		 });
}
*/













