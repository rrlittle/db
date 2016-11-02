function write_err_message(message){
	$('#errs').show();
	$('#errs').append('<div class="alert alert-danger">' + message + '</div>');
	$("html, body").animate({ scrollTop: 0 }, "slow");
}

function clear_err_messages(){
	$('#errs').html("");
	$('#errs').hide();
}

function preliminary_err_checks(data){
	var errflag = 0;
	if(data['respondentid'] == -1){ // must select a valid respondent
		errflag++;
		write_err_message('You must include the Respondent');
	}
	if($('#subject').length > 0 && data['subjectid'] == -1){
		errflag++;
		write_err_message('You must select a Subject');
	}
	if(data['dateofresponse'] > new Date()){
		errflag++;
		write_err_message('Date of response is in the future');
	}
	return errflag;
}

/** can't think of any final checks to do...
**/
function final_err_checks(data){
	var errflag = 0;
	// run any checks you want to here. see preliminary_err_checks for 
	// setup
	return errflag;
}


/** returns a dict of all the checked choices and their values
	like so: { survequestid_choiceid: value of that choice,
		survequestid_choiceid: value of that choice,
		survequestid_choiceid: value of that choice,
	}
**/
function chk_radio_handler(choiceset){
	var ret = {};
	$(choiceset).find('.choice:checked').each(function(i){
		ret[this.id]= this.value;
	});
	console.log('in chk_radio_handler on', choiceset, 'return', ret);
	return ret;
}

function txt_handler(choiceset){
	ret = {};
	$(choiceset).find('.choice').each(function(i){
		ret[this.id] = this.value;
	});
	console.log('in txt_handler on', choiceset, 'return', ret);
	return ret;
}

/** goes through all the questions in the survey and 
	saves the answers in the value of all the choices
	using the handlers defined above
**/
function fill_data(data){
	var handlers = {
		'check': chk_radio_handler,
		'radio': chk_radio_handler,
		'box': txt_handler,
		'bigbox': txt_handler, 
	};
	// iterate through questions
	$('.survquestion').each(function(i){
		var choiceset = $(this).find('.choiceset')[0];
		var datatype = choiceset.dataset.datatype;
		var ui = choiceset.dataset.ui;
		// console.log(ui);
		$.extend(data, handlers[ui](choiceset, datatype, ui))
	});
	return data;
}


$(document).on('submit', '#post_survey', function(e){
	e.preventDefault();

	clear_err_messages();

	// initialize the data to be sent back 
	var data = {
		csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
		respondentid: $('#respondent').val(),
		dateofresponse: $('#dateofresponse').val(),
		surveyid: $('input[name=surveyid]').val(),
	};

	// the subject is only present if the survey is an observational report
	if($('#subject').length > 0){
		data['subjectid'] = $('#subject').val(); 
	}
	// if it's not observational it's self-report and subject == respondent 
	else{
		data['subjectid'] = data['respondentid'];	
	}

	// if there are any errors stop now. this prints err messages to the screen
	if (preliminary_err_checks(data) > 0){return}

	// fill in the responses to the questions
	data = fill_data(data);

	if(final_err_checks(data) > 0){return}

	// before sending it off check out the data
	console.log('sending ', data);
	// do the ajax to send it. if successful redirect to data page
	// if errors. display them 
	$.ajax({
		type: 'POST',
		url: '{% url "db:post_survey" %}',
		data: data,
		complete: function(resp, status){
			// for now. just print the response until the script is working
			console.log('recieved',resp);
			console.log(resp['status'])
			var data = resp.responseJSON;
			if(resp['status'] == 200){
				var string = 'Created ' 
					+ Object.keys(data).length 
					+ ' answers:\n\t';
				$.each(data, function(index, item){
					// console.log(i,j);
					string+= item + '\n\t'
				})
				alert(string);
				window.location = '{% url "db:survey" survey.id%}'
			}
			else{
				$.each(Object.keys(data), function(index,key){
					write_err_message(key + ' : ' + data[key])
				});
			}

			
		}
	}); // done with ajax
});
