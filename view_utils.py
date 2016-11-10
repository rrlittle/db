import models
from django.shortcuts import render, get_object_or_404, get_list_or_404
# from django.core.exceptions import MultipleObjectsReturned
import datetime
import csv
import logging

logger = logging.getLogger(__name__)


class table(object):
    ''' defines a table object for use in structuring_survey_view '''

    # defines the keys for this table
    rowkeys = [
        ('Resp', models.Person),
        ('Subj', models.Person), 
        ('Date', datetime.date),
    ]
    
    class col(object):
        '''defines a single column in the table'''

        # defines recognized header types 
        h_types = [
            tuple,  # allowed to provide (Survey_Question, Choice) sets
            models.Survey_Question,  # allowed to just provide Survey_Question
        ]
        
        def __init__(self, header):
            self.rows = {}  # holds the rows for
            if type(header) not in self.h_types: 
                raise NotImplementedError('%s not recognized type' % header)

            if type(header) is tuple:
                assert (type(header[0]) is models.Survey_Question and
                    type(header[1]) is models.Choice), ('set headers must be '
                    '(Survey_Question, Choice)')
                self.survey_question = header[0]
                self.choice = header[1]
                self.type_ = 'choicecolumn'
                self.question = header[0].question
            else:  # header must given as a survey_question
                self.survey_question = header
                self.question = header.question
            self.header = {
                'question': self.question,
                'survey_question': self.survey_question
            }
            if hasattr(self, 'choice'):
                self.header['choice'] = self.choice

        def __setitem__(self, rowkey, answer):
            ''' expects a tuple of keys, as specified by self.keys
                as therow key, there should be one unique rowkey for
                each row in the table'''
            errstring = 'rowkey must be %s' % str(self.rowkeys) 
            assert len(rowkey) == len(self.rowkeys), errstring + ': len'
            assert type(rowkey) is tuple, errstring + ': type'
            for i, k in enumerate(rowkey):
                assert type(k) is self.rowkeys[i][1], errstring + ': %s' % k
            logger.info('adding %s to %s' % (answer, self))
            self.rows[rowkey] = answer
        
        def keys(self):
            '''returns all the keys usd in this column'''
            return set(self.rows.keys())
        
        def __contains__(self, key):
            ''' does this row existin in this column?'''
            return self.rows.__contains__(key)

        def __getitem__(self, key):
            '''gets a pointer to a cell using the rowkey provided'''
            return self.rows[key]

        def __str__(self):
            return str(self.question)

    # give both col and table the same rowkeys
    col.rowkeys = rowkeys

    def __init__(self):
        # holds the columns of data
        # keys are not included as columns. but done differently
        self.columns = []
        
    def add_col(self, header):
        ''' creates a column object in self.columns
            accepts strings, Survey_Question and (Survey_Questions, Choice)'''
        self.columns.append(self.col(header))

    def __getitem__(self, survey_question, choice=None):
        # import ipdb; ipdb.set_trace()
        for c in self.columns:
            # if we need to specify the choice
            if survey_question == c.survey_question:
                # if the survey_question matches
                if hasattr(c, 'choice'):  # need to match choice as well
                    if choice == c.choice: return c  # match both
                else: return c  # match and no choice
        raise KeyError('column %s %s not found in table' % (survey_question, 
            choice))

    def add_cols(self, *headers):
        for h in headers:
            self.add_col(h)

    def header(self):
        ''' returns the header of the table in its current state'''
        return [c.header for c in self.columns] 

    def body(self):
        ''' returns the body of the table in it's current state'''
        rows = {}
        for k in self.keys():
            rows[k] = []
            for c in self.columns:
                if k in c:
                    rows[k].append(c[k])
                else:
                    missing_val = c.question.get_missing_value()
                    rows[k].append(missing_val)
        return rows

    def keys(self):
        '''returns the keys for the whole table'''
        keys = set()
        for c in self.columns:
            keys |= c.keys()
        return keys

    def __str__(self):
        ''' returns string representation of this'''
        return (
            'headers: ' + str(self.header()) + 
            'body: ' + str(self.body())
        ) 

    def make_key_cols(self, key):
        ''' key should be a key from the column or from self.body key
            this splits them apart and returms them as a list
            for use in compplete_table
        '''
        return list(key)

    def key_headers(self):
        ''' returms a list of the keys used by this table, 
            for use in the header
            where normal rows use question/choice as their dicts
            this uses key
            i.e. [{key: rowkey1}, {key: rowkey2},] 
        '''
        return [{'key': k[0]} for k in self.rowkeys]

    def complete_table(self):
        ''' returns the whole table including key columns. 
            which are not internally represented. 
            this returns two lists 
            headers, a list of dicts
            rows, a list of lists, each representing a row in the table
        '''
        headers = self.key_headers()  # create the headers for the column keys
        headers += self.header()
        rows = []
        for k, row in self.body().items():
            rows.append(self.make_key_cols(k) + row)

        return headers, rows


def structure_survey_view(survey):
    ''' converts the database representation of a survey into something for the
        template
    '''
    logger.info('getting questions and answers for %s' % survey)
    # define the keys for the table
    t = table()

    # get the questions for this survey
    surv_quests = models.Survey_Question.objects.filter(survey=survey)
    logger.info('found %s questions for this survey' % len(surv_quests))
    # add all the questions from this survey to the headers
    for sq in surv_quests:
        logger.info('adding headers for %s' % sq)
        choice_group = sq.question.choice_group 
        logger.info('q ui: %s' % choice_group.ui)
        if choice_group.ui == 'check':
            choices = choice_group.choices.order_by('order')
            for c in choices:
                logger.info('adding %s to header' % c)
                t.add_col((sq, c))
        else:
            logger.info('creating one column for question')
            t.add_col(sq)

    logger.info('completed header: %s' % t.header())
    # HEADER COMPLETED

    # collect all the answers to this survey
    answers = models.Answer.objects.filter(survey_question__survey=survey)
    logger.info('found %s answers' % len(answers))

    # fill table rows
    for ans in answers:
        logger.info('adding answer %s' % ans)
        rowkey = (ans.respondent, ans.subject, ans.date_of_response)
        if ans.survey_question.question.choice_group.ui == 'check':
            col = t.__getitem__(ans.survey_question, ans.answer) 
            col[rowkey] = ans.get_value()
        else:
            t[ans.survey_question][rowkey] = ans
    # logger.info(t)

    return t.complete_table()


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
        datetime.datetime.strptime(data['dateofresponse'], DATE_FORMAT)
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
    

def handle_import_csv(text):  #, survey, importsource): 
    ''' this does the actual parsing of the text based on importsource
    '''
    # parse the csv reader as csv dict... this should allow easy manipulation
    reader = csv.DictReader(text.splitlines())
    # logger.info('headers (%s) : %s' % (len(reader.fieldnames), 
        # reader.fieldnames))
    for i, row in enumerate(reader):
        logger.info('row %s (%s): %s' % (i, len(row), row.values())) 


def check_post_csv_request(request):
    ''' checks that the post_csv request is a post and has all 
        the required keys.
        beyond that is someone else's responsibility
    '''
    if request.method != 'POST':
        return {'err_bad_method': 'must be a post'}

    errors = {}  # container for any errors that arise. 
    data = request.POST  # get the data from the request

    # these must be in the data
    required_keys = [
        'surveyid',
        'importsourceid',
        'text',
    ]

    for k in required_keys:
        if k not in data:
            errors['err_%s_not_present' % k] = '%s is a required key' % k 

    if len(errors) > 0: return errors
    else: return None 