from django.shortcuts import render, get_object_or_404, get_list_or_404
import models
from django.http import Http404, HttpResponse, HttpResponseBadRequest
import json


def index(request):  # lab main page
    ''' main lab page. we can decide what we want people to see'''
    return render(request, 'db/index.html')


def respondents(request):  # list of all people
    ''' list of all respondents with some associated info'''
    context = {'respondents': models.Person.objects.all()}
    return render(request, 'db/respondents.html', context)


def respondent(request, respondentid):  # person details
    ''' veiw a single person'''
    respondent = get_object_or_404(models.Person, pk=respondentid)
    print respondent.firstName
    context = {'respondent': respondent}
    return render(request, 'db/respondent.html', context)


def surveys(request):  # list of all surveys
    '''view list of all surveys'''
    surveys = models.Survey.objects.all()
    context = {'surveys': surveys}
    return render(request, 'db/surveys.html', context)


def survey(request, surveyid):  # details of a single survey
    ''' view a sigle survey
        a table of all the data respondents have given
    '''
    survey = get_object_or_404(models.Survey, pk=surveyid)
    context = {'survey': survey}
    try:
        # get the questions for the table header
        surv_quest_objs = get_list_or_404(
            models.Survey_Question.objects.order_by('question_order'),
            survey_id=surveyid)  # in order by appearance in the survey

        question_headers = ['Respondent']
        question_headers += [q.question.title for q in surv_quest_objs]
        context['survey_questions'] = question_headers

        resps = {}
        # go through all the answers to this survey
        for i, surv_quest in enumerate(surv_quest_objs):
            try:
                # get all the answers to this question
                ans_to_this_surv_quest = get_list_or_404(
                    models.Answer,
                    survey_question=surv_quest)
                # go through all the answers to this question
                for ans in ans_to_this_surv_quest:
                    # if this is a new respondent
                    if ans.respondent not in resps:
                        # add them and set previous responses to Not Found
                        resps[ans.respondent] = [ans.respondent]
                        resps[ans.respondent] += [Http404('Not Found')] * len(surv_quest_objs)
                    # then add this response
                    resps[ans.respondent][i + 1] = ans
            except Http404:  # no answers found for this question
                print('no answers fround for survey Question %s' % surv_quest)

        # convert responses to a list of lists
        responses_as_lists = [resps[person] for person in resps]
        context['survey_responses'] = responses_as_lists

        # e.g.
        # context['survey_questions'] = ['resp','c1','c2','c3']
        # context['survey_responses'] = [['r1','r1c1','r1c2','r1c3'],
        #                                ['r2','r2c1','r2c2','r2c3']]
    except Http404 as e:
        print('No questions found for %s survey: %s' % (survey, e))
    print context
    return render(request, 'db/survey.html', context)


def submit_survey(request, surveyid):  # fill in a specific survey
    '''view of a single survey that allows you to add answers for a single
        respondent. for the whole survey at once.

        use the surveyid to get the survey_questions for the specific survey
        - add the title of the survey to the context.
        - create a list of questions that make up the survey.
            each question needs to be defined.  
            with a title (what the header is in the data table)
            with a prompt (what does the choice look like, can be empty.)
            with a type (what is ui should be used?)
                the types that are allowed will be... UNDEFINED
                __So far we have radio... just stick to that for now.__
    '''
    context = {}
    survey_dict = {}
    survey = get_object_or_404(models.Survey, pk=surveyid)
    
    context['surveytitle'] = survey.name
    context['surveyid'] = surveyid
    
    resp_objs = None
    try:
        resp_objs = get_list_or_404(models.Person)
    except Http404: 
        context['NoRespondents'] = True
        return render(request, 'db/submit_survey.html', context)
    context['respondents'] = []
    for resp in resp_objs: 
        context['respondents'].append({'id': resp.id, 'display': str(resp)}) 
        

    try:
        surv_quest_objs = get_list_or_404(
            models.Survey_Question.objects.order_by('question_order'),
            survey_id=surveyid)  # in order by appearance in the survey

        questions = []
        for surv_quest in surv_quest_objs:
            quest = surv_quest.question
            question_dict = {}
            question_dict['surveyquestionid'] = surv_quest.id
            question_dict['title'] = quest.title
            question_dict['prompt'] = quest.prompt
            question_dict['handlingflag'] = quest.choice_group.ui
            # get all the choices associated with this question
            choice_group = quest.choice_group
            choices = []
            try:
                # get all the choices for this question
                choice_objs = get_list_or_404(
                    models.Choice.objects.order_by('order'), 
                    group_id=choice_group.id)
                for choice in choice_objs:
                    # get the description and type for each choice
                    choice_dict = {
                        'description': choice.name,
                        'ui': choice_group.ui,
                        'id': choice.id,
                        'defaultvalue': choice.get_value(choice_group.datatype)
                    } 
                    # add the correct default value based on the datatype

                    choices.append(choice_dict)

            except Http404 as e: 
                print 'No choices found for question %s: %s' % (quest, e)

            question_dict['choices'] = choices
            questions.append(question_dict)
        survey_dict['questions'] = questions
    except Http404 as e:
        print 'No Questions associated with survey %s: %s' % (survey, e)

    context['survey'] = survey_dict 
    return render(request, 'db/submit_survey.html', context)


def post_survey(request):
    ''' this handles the submission of a filled survey.
        that involves creating answers for all the data provided
        and doing error checking so bad info can't get in. 
    '''
    # endure it's a post method.
    if request.method != 'POST': 
        return HttpResponseBadRequest(
            {'error': 'Not a post'}, 
            content_type='application/json')
    
    # declare the errors container
    errors = {
        'personNotFound':None, # bad personid
        'invalidSurveyQuestions':[], # list of bad survey Question ids
        'badSurveyQuestionIdForThisSurvey':[], 
        # list of surveyquestions not for this survey
        'badChoices':{}, # survquestid: list of bad choice ids
        'badAnswerCreation':[], # list of answers that couldn't be created
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
    except Http404: errors['personNotFound'] = respondentid 
    
    # get the date of response
    date_of_response_raw = rdata['dateofresponse']

    answers = [] # container for all answers created. save either all or none. 

    # get the actual questions
    # they should be supplied with key survquest_{survquestid}_choiceid = ansval
    for k in {k: rdata[k] for k in rdata if k.startswith('survquest_')}:
        print 'processing key', k # display the raw
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
                errors['badSurveyQuestionIdForThisSurvey'].append(survquestid)
                # go to next choice
                continue
        except Http404: 
            if surveyquestid not in errors['invalidSurveyQuestions']:
                errors['invalidSurveyQuestions'].append(surveyquestid)
            continue # go to next choice

        choiceid = k_split[2] # access choiceid
        choice = None
        try:
            choice = get_object_or_404(models.Choice, pk=choiceid)
        except Http404:
            if surveyquestid not in errors['badChoices']:
                errors['badChoices'][surveyquestid] = [] 
            errors['badChoices'][surveyquestid].append(choiceid)
            continue # go to next choice    
        
        # get value provided
        value_raw = rdata[k]

        # we need to figure out what to save the value as...
        # that's defined by the type_field in the choice_group
        datatype = surv_quest.question.choice_group.datatype
        response_val = {datatype:value_raw}

        # passed all checks make an answer
        new_ans = None
        try:
            new_ans = models.Answer(
                respondent=respondent, 
                survey_question=surv_quest,
                date_of_response=date_of_response_raw,
                answer=choice,
                **response_val)
        except Exception as e: # can't create the answer
            errors['badAnswerCreation'].append(
                ('sq',survquestid, 'c',choiceid, e)
            ) # save the error
            continue # go to next choice
        print 'created answer:', new_ans
    
    # if errors stay on same page
    if (errors['personNotFound'] 
        or len(errors['invalidSurveyQuestions']) > 0
        or len(errors['badSurveyQuestionIdForThisSurvey']) > 0
        or len(errors['badChoices'].keys()) > 0
        or len(errors['badAnswerCreation']) > 0):
        return HttpResponse(
            json.dumps(errors), 
            content_type='application/json'
        )
    
    # for ans in answers: ans.save()
    return survey(surveyid)
