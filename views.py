from django.shortcuts import render, get_object_or_404, get_list_or_404
import models
from django.http import Http404, HttpResponse, HttpResponseBadRequest
import json
from django.core.urlresolvers import reverse
import view_utils
import logging

logger = logging.getLogger(__name__)


def index(request):  # lab main page
    ''' main lab page. we can decide what we want people to see'''
    return render(request, 'db/index.html')


def respondents(request):  # list of all people
    ''' list of all respondents with some associated info'''
    if not request.user.is_authenticated(): return index(request)
    context = {'respondents': models.Person.objects.all()}
    return render(request, 'db/respondents.html', context)


def respondent(request, respondentid):  # person details
    ''' veiw a single person'''
    if not request.user.is_authenticated(): return index(request)
    respondent = get_object_or_404(models.Person, pk=respondentid)
    logger.info(respondent.firstName)
    context = {'respondent': respondent}
    return render(request, 'db/respondent.html', context)


def surveys(request):  # list of all surveys
    '''view list of all surveys'''
    if not request.user.is_authenticated(): return index(request)
    logger.info('salfjsdlfjaslfjdla')
    surveys = models.Survey.objects.all()
    context = {'surveys': surveys}
    return render(request, 'db/surveys.html', context)


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
    if not request.user.is_authenticated(): return index(request)
    survey = get_object_or_404(models.Survey, pk=surveyid)
    context = {'survey': survey}
    headers, rows = view_utils.get_data_and_header_for_survey(survey)
    # before: rows = {
    #     r1: [ans1, ans2, ans3.1, ans3.2, ans3.3],
    #     r2: [ans1, ans2, ans3.1, ans3.2, ans3.3],
    #     r3: [ans1, ans2, ans3.1, ans3.2, ans3.3],
    #     r4: [ans1, ans2, ans3.1, ans3.2, ans3.3],
    # }
    rows = view_utils.dict_rows_to_list_of_lists_for_survey(rows)
    context['rows'] = rows
    # after: rows = [
    #  [r1      ,   ans1,   ans2, ans3.1,   ans3.2,     ans3.3]
    #  [r2      ,   ans1,   ans2, ans3.1,   ans3.2,     ans3.3]
    #  [r3      ,   ans1,   ans2, ans3.1,   ans3.2,     ans3.3]
    #  [r4      ,   ans1,   ans2, ans3.1,   ans3.2,     ans3.3]
    # ]

    context['headers'] = headers
    # [respondent,  q1,     q2, q3 choice1, q3 choice2, q3 choice3]

    return render(request, 'db/survey.html', context)


def submit_survey(request, surveyid):  # fill in a specific survey
    ''' pospulates a form to submit a survey.
        requires that:
        - you be logged in
        - provide a valid surveyid
        - survey is properly formed in the database

    '''
    if not request.user.is_authenticated(): return index(request)
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


def post_survey(request):
    ''' this handles the submission of a filled survey.
        that involves creating answers for all the data provided
        and doing error checking so bad info can't get in. 
    '''
    if not request.user.is_authenticated(): 
        return HttpResponseBadRequest(
            {'error': 'Not Logged in!'}, 
            content_type='application/json')

    # ensure it's a post method.
    if request.method != 'POST': 
        return HttpResponseBadRequest(
            {'error': 'Not a post'}, 
            content_type='application/json')
    
    # declare the return container
    respdat = {
        'status':None, # error/success if the request is erroneous or 
        # if theres an error, if we successfully process the survey is success  
        'personNotFound':None, # bad personid
        'invalidSurveyQuestions':[], # list of bad survey Question ids
        'badSurveyQuestionIdForThisSurvey':[], 
        # list of surveyquestions not for this survey
        'badChoices':{}, # survquestid: list of bad choice ids
        'badAnswerCreation':[], # list of answers that couldn't be created
        'answers':[]
    }

    # get the data supplied.
    rdata = request.POST # request data

    # get surveyid
    surveyid = rdata['surveyid']

    
    # get the respondent
    respondentid = rdata['respondentid']
    respondent = None
    try:
        respondent = get_object_or_404(models.Person, pk=respondentid)
    except Http404: respdat['personNotFound'] = respondentid 
    
    # get the date of response
    date_of_response_raw = rdata['dateofresponse']

    answers = [] # container for all answers created. save either all or none. 

    logger.info(rdata)
    logger.info('about to try creating answers')
    logger.info('going through these')
    logger.info({k: rdata[k] for k in rdata if k.startswith('survquest_')}) 

    # get the actual questions
    # they should be supplied with key survquest_{survquestid}_choiceid = ansval
    for k in {k: rdata[k] for k in rdata if k.startswith('survquest_')}:
        logger.info('processing key', k) # display the raw
        k_split = k.split('_') # split up
        
        # get the survey_question
        survquestid = k_split[1] # access surveyquestid
        survquest = None
        try:
            # get the surveyQuestion object
            surv_quest = get_object_or_404(
                models.Survey_Question, 
                pk=survquestid)

            # if this question should not belong to this survey
            if surv_quest.survey.id != int(surveyid):
                # flag an error
                respdat['badSurveyQuestionIdForThisSurvey'].append(survquestid)
                # go to next choice
                continue
        except Http404: 
            if surveyquestid not in respdat['invalidSurveyQuestions']:
                respdat['invalidSurveyQuestions'].append(surveyquestid)
            continue # go to next choice

        choiceid = k_split[3] # access choiceid
        choice = None
        try:
            choice = get_object_or_404(models.Choice, pk=choiceid)
        except Http404:
            if surveyquestid not in respdat['badChoices']:
                respdat['badChoices'][surveyquestid] = [] 
            respdat['badChoices'][surveyquestid].append(choiceid)
            continue # go to next choice    
        
        # get value provided
        value_raw = rdata[k]

        # we need to figure out what to save the value as...
        # that's defined by the type_field in the choice_group
        recognised_datatypes = {
            'int': 'int_response',
            'float': 'float_response',
            'date': 'date_response',
            'bool': 'boolean_response',
            'text': 'text_response',
        }

        datatype = surv_quest.question.choice_group.datatype
        if datatype not in recognised_datatypes:
            respdat['badAnswerCreation'].append(
                ('survquestid', survquestid, 'choice', choiceid, 
                    'Datatype [%s] unrecognised'%datatype)
            )
            logger.info('unrecognised datatype %s'%datatype)
            continue
        savefield = recognised_datatypes[datatype] 
        response_val = {savefield:value_raw}

        logger.info(response_val)
        # passed all checks make an answer
        new_ans = None
        try:
            new_ans = models.Answer(
                respondent=respondent, 
                survey_question=surv_quest,
                date_of_response=date_of_response_raw,
                answer=choice,
                **response_val)
            new_ans.clean()
        except Exception as e: # can't create the answer
            respdat['badAnswerCreation'].append(
                ('surveyquestid',survquestid, 'choice',choiceid, str(e))
            ) # save the error

            continue # go to next choice
        logger.info('created answer:' + str(new_ans))
        answers.append(new_ans)
    
    # if respdat stay on same page
    if (respdat['personNotFound'] 
        or len(respdat['invalidSurveyQuestions']) > 0
        or len(respdat['badSurveyQuestionIdForThisSurvey']) > 0
        or len(respdat['badChoices'].keys()) > 0
        or len(respdat['badAnswerCreation']) > 0):
        respdat['status'] = 'error'
        logger.info('responding error')
        logger.info('respdat' + str(respdat))
        return HttpResponse(
            json.dumps(respdat), 
            content_type='application/json'
        )
    
    for ans in answers: 
        logger.info('saving answer %s'%ans) 
        respdat['answers'].append(str(ans))
        ans.save()

    respdat['status'] = 'success'
    respdat['surveypage'] = reverse(
        'db:survey', 
        kwargs={'surveyid':surveyid}
    )
    logger.info('responding successful going to page %s'%respdat['surveypage'])
    return HttpResponse(
        json.dumps(respdat),
        content_type='application/json')
