import models
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.exceptions import MultipleObjectsReturned

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
        the first is a list of header strings for the survey temlate
        the second is a list of data elements to fill the data table

        returns 404 is no Questions found for the survey
    '''
    logger.info( 'in get_data_and_header_for_survey')
    headers = ['Respondent'] # first col will always be for people
    rows = {} # keys will be individuals, each respondent gets their own row
    
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
