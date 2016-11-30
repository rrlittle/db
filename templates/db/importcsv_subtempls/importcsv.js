/**
this page has 2 funcitonalities. 
1. when you select a file using the select file button. 
	this 
	- gets the file objects and populates a list on the screen
	- saves the file objects for later use 
2. when you click the submit button to submit the file.
	- reads the file selected and posts it to the server's 
		{% url 'db:post_csv'%}
	- then handles the return value 
**/

var files = null; // save the files
var filetext = null; // save the text of the file
var lastmodified = null; // save when file last modified as mm/dd/YYYY
// todays date for use if the file doesn't have a date
var today = new Date(Date.now()).toLocaleString(); 


///////////////////////////////////
// Get files from user
///////////////////////////////////


// on change of the file selection. update the text box
$(document).on('change',':file', function(){
	// retrieve the files
	var input = $(this).get(0); // get input node
	files = input.files // get the files
	if (files == null){return} // break. no files selected
	// else continue
	
	// update the feedback box
	var output = []; // container to hold file names
	for (var i = 0, f; f = files[i]; i++) {
		console.log(f.name, f.type);
		output.push( 
			'<label id="sel_disp', i, '" class="form-control">',
				escape(f.name), '\t\t',
			'(', f.type || 'n/a', ')',
			'<span style="float:right">', f.size, ' bytes, last modified: ',
			f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
			'</span></label>' 
		);
	}
	$('#selected_files')[0].innerHTML = output.join('');

	// actually read the files
	var f = new FileReader();
	f.onload = function(thefile){
		// runs when the file is loaded after read


		filetext = thefile.srcElement.result
		// save the filetext as a string
		lastmodified = f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : new Date(Date.now()).toLocaleString();
		// save the last moified date if available or todays date as a backup.

		if (filetext != null){
			$('#submit_button').prop('disabled',false);
		}
		else{
			alert('something in this file did not work')
		}
	};
	f.readAsText(files[0]);
	

});


///////////////////////////////////
// do upload and handle response
///////////////////////////////////

// when ajax finishes
function handle_ajax_complete(resp, status){
	console.log(status, resp);
}

// submit button
// just send filetext to the server
$(document).on('submit', '#post_csv', function(e){
	e.preventDefault();
	console.log('sending ', filetext);
	data = {
		text: filetext,
		surveyid: $('input[name=surveyid]').val(),
		importsourceid: $('#importsource')[0].value,
		csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
	};

	$.ajax({
		type: 'POST',
		url: '{% url "db:post_csv" %}',
		data: data,
		complete: handle_ajax_complete
	});
});





