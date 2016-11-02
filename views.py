from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, get_list_or_404
import models
from django.http import Http404, HttpResponse, HttpResponseBadRequest
import json
from django.core.urlresolvers import reverse
import view_utils
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def index(request):  # lab main page
    ''' main lab page. we can decide what we want people to see'''
    return render(request, 'db/index.html')


@login_required(login_url='/index')
def respondents(request):  # list of all people
    ''' list of all respondents with some associated info'''
    context = {'respondents': models.Person.objects.all()}
    return render(request, 'db/respondents.html', context)


@login_required(login_url='/index')
def respondent(request, respondentid):  # person details
    ''' veiw a single person'''
    respondent = get_object_or_404(models.Person, pk=respondentid)
    logger.info(respondent.firstName)
    context = {'respondent': respondent}
    return render(request, 'db/respondent.html', context)


@login_required(login_url='/index')
def surveys(request):  # list of all surveys
    '''view list of all surveys'''
    surveys = models.Survey.objects.all()
    context = {'surveys': surveys}
    return render(request, 'db/surveys.html', context)


@login_required(login_url='/index')
def survey(request, surveyid):  # details of a single survey
    ''' view a sigle survey
        a table of all the data respondents have given
        the template expects a dictionary with:
            survey => a survey object
            headers => a list of strings that end up being the col headers
            survey_responses => a list of lists that contain all the 
                data for the table cells

            every list in survey_responses should be the same length as 
            headers so that alignment is correct

            if the surveyid is bad raise 404
            if the survey is not represented properly in the database
            just sort of fails
    '''
    survey = get_object_or_404(models.Survey, pk=surveyid)
    context = {'survey': survey}
    headers, rows = view_utils.structure_survey_view(survey)
    logger.info('creating view for %s' % survey)
    
    logger.info('headers (%s col wide):' % len(headers))
    for h in headers: logger.info('\t' + str(h))
    context['headers'] = headers

    logger.info('rows (%s rows):' % len(rows))
    for r in rows: logger.info('\t(%s col wide):' % len(r) + str(r))
    context['rows'] = rows
    return render(request, 'db/survey.html', context)


@login_required(login_url='/index')
def submit_survey(request, surveyid):  # fill in a specific survey
    ''' pospulates a form to submit a survey.
        requires that:
        - you be logged in
        - provide a valid surveyid
        - survey is properly formed in the database

    '''
    context = {
        'survey': None,  # give the survey to the template for title and id
        'questions': [],  # to pass all the question objects to the template
        'respondents': [],  # to pass all the respondents to the template
        'errors': [],  # any errors that occur. this is also used during submit
    }

    # get the survey. if it can't be found 404
    survey = get_object_or_404(models.Survey, pk=surveyid)
    context['survey'] = survey  # save for the templates to use

    # get all the respondents for filling the respondents section
    context['respondents'] = models.Person.objects.all()
    # if it's empty. they can add a respondent through the 
    # respondents section of template

    # get the questions in this survey. by ordering the questions
    surv_quests = models.Survey_Question.objects.order_by('question_order')
    # then filtering out ones not related to this survey
    surv_quests = surv_quests.filter(survey_id=surveyid)
    context['questions'] = surv_quests

    return render(request, 'db/submit_survey.html', context)


@login_required(login_url='/index')
def import_survey(request, surveyid):  # import a csv and create answers
    survey = get_object_or_404(models.Survey, pk=surveyid)
    context = {
        'survey': survey
    }
    return render(request, 'db/import_survey.html', context)


@login_required(login_url='/index')
def post_survey(request):
    ''' this is the point that recieves the data for a single respondent
        i.e. it creates one record for a given survey. 
        this should be the entry point for all survey data either from the
        submit_survey view or an import

        data comes in a flat dictionary that looks like this:
        {   surveyid:#,
            csrfmiddlewaretoken: key,
            dateofresponse: "yyyy-mm-dd",
            respondentid:#,
            subjectid:#,
            choice_choiceid_surveyquestion_id:value
        }   

        if the choice_id allows custom values the value provided should be 
        saved otherwise the default should be used. 
        
        if any errors occur they will appear in the response json. 
        this is primarily designed for ajax interaction. and returns json data

    '''
    date_format = '%Y-%m-%d'  # define a local standard date format. 
    # this should actually go somewhere else. so that it's global 

    # check the request has all the required stuff. 
    #  this does not check that the id's passed in are valid or anything
    status = view_utils.check_post_survey_request(request, 
        DATE_FORMAT=date_format)
    if status is not None:
        return HttpResponseBadRequest(json.dumps(status), 
            content_type='application/json')
    
    errors = {}  # prepare a container for any critical errors that arise
    data = request.POST  # get the data supplied

    def try_to_get_obj_or_save_to_err(model, pk, errkey):
        obj = None
        try:
            obj = get_object_or_404(model, pk=pk)
        except Http404 as e:    
            errors[errkey] = e
        return obj

    # strip all the infor passed from request. 
    # this has all been checked
    respondent = try_to_get_obj_or_save_to_err(models.Person, 
        data['respondentid'], 'err_bad_respondentid')    
    subject = try_to_get_obj_or_save_to_err(models.Person, 
        data['subjectid'], 'err_bad_subjectid')    
    survey = try_to_get_obj_or_save_to_err(models.Survey, 
        data['surveyid'], 'err_bad_surveyid')
    dateofresponse = datetime.strptime(data['dateofresponse'], date_format)

    # get the choices selected from the request
    choices = {c: data[c] for c in data if c.startswith('choice_')}

    # create the answers to save
    answers_to_save = []
    for choice, value in choices.items():
        try:
            new_ans = view_utils.create_answer_from_post(choice, value,
                date=dateofresponse, 
                respondent=respondent,
                subject=subject,
                survey=survey)
            answers_to_save.append(new_ans)
        except Exception as e: 
            logger.info('answer not created because %s' % e)
            errors['err_bad_answer_creation_' + choice] = str(e)

    if len(errors) > 0:
        logger.warning('Errs creating answers returning Http500: %s' % errors)
        return HttpResponseBadRequest(json.dumps(errors), 
            content_type='application/json')

    for ans in answers_to_save:
        logger.info(ans)
        logger.info('saving ans %s'%ans)
        ans.save()

    ans_created = {i : str(ans) for i, ans in enumerate(answers_to_save)}
    return HttpResponse(json.dumps(ans_created), 
        content_type='application/json')



