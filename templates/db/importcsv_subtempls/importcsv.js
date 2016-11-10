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

var files = []; // save the files
var filetext = null; // save the text of the file

// save the files and print the to the screen
function handleFileSelect(evt){
	files = evt.target.files; // FileList object
	
	// files is a FileList of File objects. List some properties.
	var output = [];
	// add the files with properties to output list
	for (var i = 0, f; f = files[i]; i++) {
		output.push('<li><strong>', 
			escape(f.name), 
			'</strong> (', 
			f.type || 'n/a', ') - ',
			f.size, 
			' bytes, last modified: ',
			f.lastModifiedDate ? 
				f.lastModifiedDate.toLocaleDateString() : 'n/a',
			'</li>'
		);
	}

	// read the file and save it's text to filetext
	var f = new FileReader();
	f.onload = function(thefile){
		// runs when the file is loaded after read

		filetext = thefile.srcElement.result

		if (filetext != null){
			$('#submit_button').prop('disabled',false);
		}
		else{
			alert('something in this file did not work')
		}
	};
	f.readAsText(files[0]);
	// read happens asynchonously. 

	document.getElementById('list').innerHTML = '<ul>' + 
		output.join('') + '</ul>';
};

// when the files change
document.getElementById('files').addEventListener('change',  // on change 
	handleFileSelect,  // use this callback
	false  // at most once
); 

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
		surveyid: 1,
		importsourceid: 1,
		csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
	};

	$.ajax({
		type: 'POST',
		url: '{% url "db:post_csv" %}',
		data: data,
		complete: handle_ajax_complete
	});
});




