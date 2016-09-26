from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime

datatypes = [
	'int',
	'float',
	'date',
	'bool',
	'text',
]


class Person(models.Model):
	''' a list of all the people participating in the study
		some of them 
	'''
	firstName = models.CharField(max_length=60)
	lastName = models.CharField(max_length=60)
	birthdate = models.DateField()
	def __str__(self): return self.firstName + ' ' + self.lastName


class Measure(models.Model):
	''' a type of measurement. each answer will be a measurement of something
		this is it's name. e.g. feet, miles, general anxiety etc
	'''
	name = models.CharField(max_length=60)
	def __str__(self): return self.name


class Choice_Group(models.Model):
	''' questions often have multiple possible responses. yes/no, 1-5 etc
		this allows multiple questions to point to one group, which contains 
		multiple allowable choices.
	'''
	name = models.CharField(max_length=60) # what is this group called? 
	# 	# e.g. yes-no. strongly agree to disagree

	ui = models.CharField(max_length=20)  # how does the choices appear	
	# this determines how all the chocices will appear
	#	# radio - the default value will be used. user cannot overwrite
	#	# text - they will be able to enter characters in any fields
	#	# checkbox - they will be able to enter a number of options
	# if this is checkbox a column for each option will be created when
	# viewing the data

	datatype = models.CharField(max_length=20) # bool/int/phone/id/email/etc
	# this is used to validate the data passed along

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
	group = models.ForeignKey(Choice_Group)  # each choice belongs to a group 
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

class Question(models.Model):
	''' this is the actual question including the prompt and possible 
		answers people are allowed to provide
	''' 
	title = models.CharField(max_length=60)
	prompt = models.CharField(max_length=200)
	choice_group = models.ForeignKey(Choice_Group)
	
	def __str__(self): return self.prompt


class Survey(models.Model):
	''' surveys are questionaires
	'''
	name = models.CharField(max_length=60) # the name of the survey
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
	
	boolean_response = models.NullBooleanField(blank=True, null=True)
	date_response = models.DateField(blank=True, null=True)
	text_response = models.CharField(max_length=60, blank=True, null=True)
	int_response = models.IntegerField(blank=True, null=True)
	float_response = models.FloatField(blank=True, null=True)
	
	def __str__(self): return '%s [%s=%s]' % (
		self.respondent, 
		self.survey_question, self.answer)

	def clean(self):
		''' used to validate Answer entries. 
			self.answer must belong to the the choice_group
			in the self.survey_question.question.choice_group
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

		if self.booleanresponse is None: 
			self.booleanresponse = self.answer.default_boolean_resp
		if self.dateresponse is None: 
			self.dateresponse = self.answer.default_date_resp
		if self.textresponse is '': 
			self.textresponse = self.answer.default_text_resp
		if self.intresponse is None: 
			self.intresponse = self.answer.default_int_resp
		if self.floatresponse is None: 
			self.floatresponse = self.answer.default_float_resp