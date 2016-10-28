from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime


class Person(models.Model):  # all people
	''' a list of all the people participating in the study
		some of them 
	'''
	firstName = models.CharField(max_length=60)
	lastName = models.CharField(max_length=60)
	birthdate = models.DateField()
	studyid = models.IntegerField(unique=True)
	
	def __str__(self): return str(self.studyid)


class Relation(models.Model):  # relationships between people
	''' this maps the relationships between subjects and the other people 
		in the People table.  
	'''
	subject = models.ForeignKey(Person, related_name='subject')
	relation = models.CharField(max_length=20)
	to = models.ForeignKey(Person, related_name='to')

	def __str__(self): 
		return '%s %s to %s' % (self.subject, 
			self.relation,
			self.to) 


class Measure(models.Model):  # what a question covers
	''' a type of measurement. each answer will be a measurement of something
		this is it's name. e.g. feet, miles, general anxiety etc
	'''
	name = models.CharField(max_length=60)
	
	def __str__(self): return self.name


class Choice(models.Model):
	''' this represents a singe choice availbale to a question. 
		the respondent may choose on of these.
		every choice will belong to a choice group. 
		i.e. yes belongs to yes/no
		a different yes might belong to yes/no/maybe
	'''
	name = models.CharField(max_length=60)  # what is this choice called?
	# e.g. Yes / No / Strongly Agree / Ambivalent / Disagree etc
	order = models.IntegerField(blank=True, null=True) 
	# if it matters what order the choices appear in

	default_boolean_resp = models.NullBooleanField(blank=True, null=True)
	default_date_resp = models.DateField(blank=True, null=True)
	default_text_resp = models.CharField(max_length=60, blank=True, null=True)
	default_int_resp = models.IntegerField(blank=True, null=True)
	default_float_resp = models.FloatField(blank=True, null=True)

	def __str__(self): return self.name

	def get_value(self, datatype):

		if datatype == 'int': return self.default_int_resp
		elif datatype == 'float': return self.default_float_resp
		elif datatype == 'bool': return self.default_boolean_resp
		elif datatype == 'date': return self.default_date_resp
		elif datatype == 'text': return self.default_text_resp
		else: raise LookupError('%s not a recognised datatype' % datatype)


class Choice_Group(models.Model):  # 
	''' questions often have multiple possible responses. yes/no, 1-5 etc
		this allows multiple questions to point to one group, which contains 
		multiple allowable choices.
	'''
	name = models.CharField(max_length=60)  # what is this group called? 
	# 	# e.g. yes-no. strongly agree to disagree

	ui = models.CharField(max_length=20, 
		choices=[('radio', 'radio'), 
			('check', 'check'), 
			('box', 'box'), 
			('bigbox', 'bigbox')]
	)
	# this determines how all the chocices will appear
	# radio - the default value will be used. user cannot overwrite
	# check - they will be able to select a number of options
	# box - small textbox
	# bigbox - multiline resizable textbox
	# if this is checkbox a column for each option will be created when
	# viewing the data

	datatype = models.CharField(max_length=20, 
		choices=([('int', 'int'), 
			('text', 'text')])
	)

	choices = models.ManyToManyField(Choice, related_name='choice_groups')
	
	def __str__(self): return self.name

	def choice_defs(self):
		''' to populate the choice template we need to get the
			default values from the choice for this group. 
			that's complicated because each choice can belong to multiple 
			groups.
			so each choice can have multiple default values depending on which 
			group they are a part of. 

			this function will create a more useful list of of choices
			with their default values and associated stuffs available in 
			templates 
		''' 
		choices = []
		for choice in self.choices.order_by('order').all():
			choices.append({
				'def_value': choice.get_value(self.datatype),
				'name': choice.name,
				'id': choice.id,
				})
		return choices


class Question(models.Model):
	''' this is the actual question including the prompt and possible 
		answers people are allowed to provide
	''' 
	title = models.CharField(max_length=60)
	prompt = models.CharField(max_length=200)
	choice_group = models.ForeignKey(Choice_Group)
	allow_multiple_responses = models.BooleanField()
	
	# if you are missing an answer to this question display it like so
	missing_value_int = models.IntegerField(blank=True, null=True, default=999)
	missing_value_float = models.FloatField(blank=True, null=True)
	missing_value_boolean = models.NullBooleanField(blank=True, null=True)
	missing_value_date = models.DateField(blank=True, null=True)
	missing_value_text = models.CharField(max_length=60, blank=True, null=True)

	def __str__(self): return self.prompt

	def get_missing_value(self):
		datatype = self.choice_group.datatype
		if datatype == 'int': return self.missing_value_int
		elif datatype == 'float': return self.missing_value_float
		elif datatype == 'bool': return self.missing_value_boolean
		elif datatype == 'date': return self.missing_value_date
		elif datatype == 'text': return self.missing_value_text
		else: raise LookupError('%s not a recognised datatype' % datatype)


class Survey(models.Model):
	''' surveys are questionaires
	'''
	name = models.CharField(max_length=60)  # the name of the survey
	
	def __str__(self): return self.name


class Survey_Question(models.Model):
	''' this maps specific questions to specific surveys. that way individual 
		questions can belong to multiple surveys.
	'''
	survey = models.ForeignKey(Survey)
	question = models.ForeignKey(Question)
	question_order = models.PositiveIntegerField()
	unit_of_measure = models.ForeignKey(Measure, blank=True, null=True)  
	# what this answer measures

	def __str__(self): 
		return '%s[%s]=>%s' % (
			self.survey, 
			self.question_order, 
			self.question)

	class Meta:
		unique_together = (('survey', 'question_order'),)


class Answer(models.Model):
	''' this model holds the actual values users supply
		the values suppled might be either, string, int, float, bool, or date
	'''

	respondent = models.ForeignKey(Person)  # person providing this answer
	answer = models.ForeignKey(Choice) 
	# one of the possible choices they went with 
	survey_question = models.ForeignKey(Survey_Question) 
	# what survey and question this answer belongs to. 
	date_of_response = models.DateField(default=datetime.now)

	# value:  
	# #	save the actual value for their resonse. 
	# #	all, none, or anywhere in between may be filled. depending on what
	# #	type of question this is.  
	
	int_response = models.IntegerField(blank=True, null=True)
	float_response = models.FloatField(blank=True, null=True)
	date_response = models.DateField(blank=True, null=True)
	boolean_response = models.NullBooleanField(blank=True, null=True)
	text_response = models.CharField(max_length=60, blank=True, null=True)
	
	def __str__(self): return '%s [%s=%s]' % (
		self.respondent, 
		self.survey_question, self.answer)

	def clean(self):
		''' used to validate Answer entries. 
			self.answer must belong to the the choice_group
			in the self.survey_question.question.choice_group

			also not allowed to save duplicate entries
			duplicate meaning same 
		'''
		question = Survey_Question.objects.get(pk=self.survey_question_id)
		question_id = question.question_id
		choice_group = Question.objects.get(pk=question_id)
		proper_choice_group_id = choice_group.choice_group_id

		selected_choice = Choice.objects.get(pk=self.answer_id)
		selected_choice_group_id = selected_choice.group_id

		if proper_choice_group_id != selected_choice_group_id:
			raise ValidationError(('Selected choice is not part of'
				' proper group for this question.'))

		if self.boolean_response is None: 
			self.boolean_response = self.answer.default_boolean_resp
		if self.date_response is None: 
			self.date_response = self.answer.default_date_resp
		if self.text_response is '': 
			self.text_response = self.answer.default_text_resp
		if self.int_response is None: 
			self.int_response = self.answer.default_int_resp
		if self.float_response is None: 
			self.float_response = self.answer.default_float_resp

		# get any duplicates for this answer i.e.
		# same respondent, 
		# same survey question
		# same choice
		duplicates = Answer.objects.filter(
			respondent_id=self.respondent.id,
			survey_question_id=self.survey_question.id,
			answer_id=self.answer.id)
		print 'cleaning answer %s' % self
		print 'foud duplicates %s' % duplicates
		if len(duplicates) > 0: 
			raise ValidationError(('this is a duplicate '
				'to these %s') % duplicates)

	def get_value(self):
		'''
			depending on the choice_group this choice is a part of
			the value of this answer will be stored in one of several fields. 
			so we need to retrieve the value from the correct field.
		'''
		
		datatype = self.answer.group.datatype  # get the datatype of ths answer
		if datatype == 'int': return self.int_response
		elif datatype == 'float': return self.float_response
		elif datatype == 'date': return self.date_response
		elif datatype == 'bool': return self.boolean_response
		elif datatype == 'text': return self.text_response
		else: raise LookupError('%s not a recognised datatype' % datatype)
