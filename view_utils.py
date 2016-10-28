import models
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.exceptions import MultipleObjectsReturned
from datetime import datetime


import logging

logger = logging.getLogger(__name__)


def handle_quest_for_survey_view(survquest):
    ''' handles getting all the responses to a single survey question
        if this question allows multiple responses then it will
        produce mutiple columns. i.e one for each choice
        this returns a list of header strings
        and a dictionary of person: answer list where the answer list is 
        aligned with the header

        throws 404 if there are no choices available  
            if question allows muslitple
    '''
    logger.info('in handle_quest_for_survey_view for survquest %s'%survquest)
    headers = [] # to hold header strings
    rows = {} # to hold respomses 
    # using people as keys with header aligned lists as value
    question = survquest.question
    q_missing_val = question.get_missing_value() # save question missing value

    if question.allow_multiple_responses: # one column per possible responses
        logger.info(('this question allows multiple responses, '
            'making a column for each choice'))
        # then we need to create headers for each viable option
        choice_grp = question.choice_group
        # get all the choices for this question
        choices = get_list_or_404(
            models.Choice.objects.order_by('order'),
            group_id=choice_grp.id
        )
        logger.info( 'found these choices %s'%choices)
        for choice_num, choice in enumerate(choices):
            logger.info('\thandling choice %s'%choice)
            # save the header for this choice
            headers.append('%s (%s)'%(question.title, choice.name))
            # get all the answers to this responses 
            # to this choice for this question in this survey
            answers_for_this_choice = models.Answer.objects.filter(
                answer_id=choice.id,
                survey_question_id = survquest.id
            )
            logger.info('\tfound these answers %s'%answers_for_this_choice)
            # BUG: multiple responses from the same person for the same person 
            # will break this. they will add more than one column to this row
            # hopefully the database will be kept clean
            people_responded = []
            for ans in answers_for_this_choice:
                logger.info( '\t\thandling this answer %s'%ans)
                # save everyone that responded
                people_responded.append(ans.respondent) 
                
                # if they aren't already in rows, add them, 
                # be sure to pad with missing vals
                if ans.respondent not in rows:
                    logger.info (('\t\tnew respondent found. initializing '
                              'their row to %s')%([q_missing_val] * (choice_num)))
                    rows[ans.respondent] = [q_missing_val] * (choice_num)
                # put the value of their response in the data output
                rows[ans.respondent].append(
                    ans.answer.get_value(choice_grp.datatype)
                )
            # if people didn't respond we need to pad with missing values
            for no_response in [r for r in rows if r not in people_responded]:
                logger.info ('\t\tperson %s did not respond. adding %s to row'%(no_response, q_missing_val))
                rows[r].append(q_missing_val)
    else: # only one column 
        headers.append(question.title)
        logger.info( ('this question does not allow multiple responses',
                    'making only one column'))
        answers_to_this_quest = models.Answer.objects.filter(
            survey_question_id=survquest.id
        )
        for ans in answers_to_this_quest:
            logger.info( '\thandling this answer %s'%ans)
            if ans.respondent not in rows:
                logger.info (('\t\t new respondent found. '
                            'initializing their row to %s')%([]))
                rows[ans.respondent] = [] 
            
            rows[ans.respondent].append(ans.get_value())
                

    return headers, rows


def get_data_and_header_for_survey(survey):
    ''' turns the database representation of a survey into two lists
        the first is a list of header strings for the survey template
        the second is a list of data elements to fill the data table

        returns 404 if no Questions found for the survey
    '''
    logger.info('in get_data_and_header_for_survey')
    headers = ['Resp']  # define keys for all tables
    if survey.type == 'observational': headers.append('Subj')
    headers.append('Date Completed')
    
    rows = {}  # keys will be individuals, each respondent gets their own row
    
    # get all the questions in this survey in the correct order
    survquests = get_list_or_404(
        models.Survey_Question.objects.order_by('question_order'),
        survey_id=survey.id,
    )    
    logger.info('going through survquests %s'%survquests)

    # go through all the questions in the survey
    for survquest in survquests:
        question = survquest.question # get the actual question
        # get the headers and data columns for this question
        logger.info( 'handling %s'%survquest)
        headers_for_quest, \
        responses = handle_quest_for_survey_view(survquest)
        logger.info('got back %s %s'%(headers_for_quest, responses))
        # headers_for_quest = the headers for the table associated with question
        # columns_for_quest = the columns aligned with the headers

        # get a list of all the people that are currently in rows, but not in 
        # responses. i.e. they didn't provide an answer for these columns.
        resps_didnt_answer = [r for r in rows if r not in responses]
        for r in resps_didnt_answer:
            # recall rows contains one list per respondent
            rows[r] += [question.get_missing_value()]*len(headers_for_quest)
            # add a missing value for each header added. so they'll all be the 
            # same length always. 

        # update rows without overwriting what's already there
        for r in responses:
            if r not in rows: # this is the first time we've seen this person
                # initialize this respondent
                rows[r] = ['miss']*(len(headers)-1)
            rows[r] += responses[r] # add the current columns

        # add the headers
        headers += headers_for_quest

    # after we've totally filled rows. we need to reformat it to a list of lists
    # so that it's easier for the template
    logger.info('returning from get_data_and_header_for_survey with %s %s'%(headers, rows))
    return headers, rows


def dict_rows_to_list_of_lists_for_survey(rows):
    ''' get_data_and_header_for_survey returns a list of headers and 
        a dictionary of rows using the respondent as a key. 
        like so:
        {
            r1: [ans1, ans2, ans3.1, ans3.2, ans3.3],
            r2: [ans1, ans2, ans3.1, ans3.2, ans3.3],
            r3: [ans1, ans2, ans3.1, ans3.2, ans3.3],
            r4: [ans1, ans2, ans3.1, ans3.2, ans3.3],

        }

        the template wants this a list of lists like so:
        [[r1, ans1, ans2, ans3.1, ans3.2, ans3.3],
         [r2, ans1, ans2, ans3.1, ans3.2, ans3.3],
         [r3, ans1, ans2, ans3.1, ans3.2, ans3.3],
         [r4, ans1, ans2, ans3.1, ans3.2, ans3.3],
        ]
        this function does that
    '''
    ret_rows = []
    for r in rows:
        ret_rows.append([r] + rows[r])
    return ret_rows


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
                logger.info( 'No choices found for question %s: %s' % (quest, e))

            question_dict['choices'] = choices
            questions.append(question_dict)
        survey_dict['questions'] = questions
    except Http404 as e:
        logger.info( 'No Questions associated with survey %s: %s' % (survey, e))

    context['survey'] = survey_dict 
    return render(request, 'db/submit_survey.html', context)


def check_post_survey_request(request, DATE_FORMAT='%Y-%m-%d'):
    ''' this ensures that the request sent to post_survey is filled 
        appropriately. 
        if it is: return None
        if there are errors, return a dictionary appropriate to be sent back 
        in JSON.
    '''

    if request.method != 'POST':
        return {'err_bad_method': 'must be a post'}

    errors = {}  # container for any errors that arise. 
    data = request.POST  # get the data from the request

    # these must be in the data
    required_keys = [
        'respondentid',
        'subjectid',
        'dateofresponse',
        'surveyid',
    ]
    
    for k in required_keys:
        if k not in data:
            errors['err_%s_not_present' % k] = '%s is a required key' % k 

    try:
        datetime.strptime(data['dateofresponse'], DATE_FORMAT)
    except ValueError as e: 
        errors['err_bad_dateofresponse_format'] = e

    for c_id in [c_id for c_id in data if c_id.startswith('choice_')]:
        try:
            assert len(c_id.split('_')) == 3
        except AssertionError:
            errors['err_badchoicekey_%s'] = ('malformed choice key should '
                'be choice_<choiceid>_<surveyquestionid>')

    if len(errors) > 0: return errors
    else: return None


def create_answer_from_post(html_choiceid, value, 
        date=None, respondent=None, subject=None,
        survey=None):
    ''' html_choiceid is the string from the template:
            choice_choiceid_surveyquestionid
        value is the string passed in. if allow custom value is True, then use 
        that. else use the default value of the choice.
        this should return an unsaved answer object or raise an error
    '''
    html_choiceid_split = html_choiceid.split('_')
    choiceid = html_choiceid_split[1]
    surveyquestid = html_choiceid_split[2]

    choice = get_object_or_404(models.Choice, pk=choiceid)
    surveyquestion = get_object_or_404(models.Survey_Question, 
        pk=surveyquestid)
    datatype = surveyquestion.question.choice_group.datatype

    val_to_save = None
    if choice.allow_custom_responses: val_to_save = value
    else: 
        val_to_save = choice.get_value(datatype)

    # create the answer
    ans = models.Answer(
        respondent=respondent, 
        subject=subject,
        date_of_response=date,
        survey_question=surveyquestion,
        answer=choice,
        **{datatype + '_response': val_to_save}
    )
    ans.clean()
    return ans
    


