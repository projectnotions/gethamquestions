#pylint: disable-msg=too-many-instance-attributes
from gethamquestionclasses import msg
from pathlib import Path
import json
import textwrap

def print_wrap(prefix, preferredWidth, message):
    #preferredWidth = 70
    wrapper = textwrap.TextWrapper(initial_indent=prefix, 
                    width=preferredWidth,
                    subsequent_indent=' '*len(prefix))
    print(wrapper.fill(message))

class Question:
    """
    A class to represent a question and multiple choice answers.

    ...

    Attributes
    ----------
    subelement : str
        Name of the subelement the question is in
    group : str
        The group the questio is in, i.e. A-F
    num : str
        The number of the question 1...n
    qid : str
        The FCC ID, i.e. T1A05
    correct : str
        The correct answer to the question A-D
    figure : str
        The figure identifier associated with the question, i.e. T-2
    answers : list
        The list of multiple choice answers.  There are four answers in the list
    fcc: str
        FCC references related to the question
    topics: list
        List of topics in the group relating to this question.

    """

    #pylint: disable-msg=too-many-arguments
    def __init__(self, subelement, group, num, qid, text, correct, figure, answers, \
                 fcc, topic_list):
        """
        Constructs the attributes for the Question object

        Parameters
        ----------
            subelement : str
                Name of the subelement the question is in.
            group : str
                The group the questio is in, i.e. A-F.
            num : str
                The number of the question 1...n
            qid : str
                The FCC ID, i.e. T1A05
            text : str
                The text of the question.
            correct : str
                The correct answer to the question A-D.
            figure : str
                The figure identifier associated with the question, i.e. T-2.
            answers : list
                The list of multiple choice answers.  There are four answers in the list.
            fcc: str
                FCC references related to the question
            topic_list
                A list of topics to make an assessment of relevance to this question.
                Relevant topics are added to the topic_list
        """
        self.subelement = subelement
        self.group = group
        self.num = num
        self.qid = qid                    # i.e. T1A05
        self.text = text                # Question text
        self.correct = correct
        self.figure = figure
        self.fcc = fcc
        self.answers = answers          # Array of Answers
        #self.topics = []               # deprecate, handle by AI
        #self.get_topics(topic_list)    
    #pylint: enable-msg=too-many-arguments

    def __str__(self):
        """
        Returns a short string description of the object

        """

        shortans = []
        shortlength = 10
        for i in self.answers:
            shortans.append(i[0:shortlength])
        return(
            f'Question("{self.subelement+self.group+self.num}", "{self.text[0:shortlength]}", '
            f'"{self.correct}", "{self.figure}", "{*shortans,}"'
        )

    def __repr__(self):
        """
        Returns a Question contructor.

        """

        return(
            f'Question("{self.subelement}", "{self.group}", "{self.num}", "{self.text}", '
            f'"{self.correct}", "{self.figure}", "{*self.answers,}"'
        )

    # def get_topics(self, topic_list):
    #     """
    #     DEPRECATE THIS FUNCION.... Question Topics are handled by AI
    #     Returns the topics contained in a question. EXPERIMENTAL

    #     """
    #     self.topics = []
    #     potential_topics = []
    #     self.topics = potential_topics

#pylint: enable-msg=too-many-instance-attributes

class Group:
    """
    A class to represent a group of question.

    ...

    Attributes
    ----------
    subelement : str
        Name of the subelement the question is in
    group_id : str
        The group id the questions are in, i.e. A-F
    description : str
        A discription of the question group.  Can be several sentences or sentence fragments
    topics : list
        A list of the topics in this group.
    questions : list
        The list of Question objects in the group.

    """
    def __init__(self, subelement, group_id, description, questions):
        """
        Constructs the attributes for the Group object

        Parameters
        ----------
            subelement : str
                Name of the subelement the question is in
            group_id : str
                The group id the questions are in, i.e. A-F
            description : str
                A discription of the question group.  Can be several sentences or sentence fragments
            questions : list
                The list of Question objects in the group.
        """

        self.subelement = subelement
        self.group_id = group_id
        self.description = description
        self.topics, self.subtopics = self.get_topics(description)
        self.questions = questions      # Array of Question

    def __str__(self):
        """
        Returns a short string description of the object

        """

        return(
            f'Group("{self.subelement+self.group_id}", "{self.description[0:20]}" '
        )

    def __repr__(self):
        """
        Returns a Group contructor.

        """
        return(
            f'Group("{self.subelement}", "{self.group_id}", '
            f'"{self.description}", "{*self.questions,}")'
        )
    def set_description(self, description):
        """
        Sets the description of the object

        """
        self.description = description
        self.topics, self.subtopics = self.get_topics(description)
        msg('Info', 'I999', f'set_description: self.topics = "{self.topics}"\n')
        msg('Info', 'I999', f'set_description: self.topics = "{self.subtopics}"\n')

    def get_topics(self, topic_string):
        """
        Returns an array with the topics for the object

        """
        #print(f'self.description = "{self.description}"')
        #print(f'self.description.split(";") = {self.description.split(";")}')
        # If the topic is too long it throws off the AI, for now will skip
        #TODO Fix the "long topic situation"
        topics = []
        sub_topics = []
        for topic in topic_string.split(';'):
            topic = topic.strip()
            if len(topic.split(':'))<=1:
                topics.append(topic)
            else:
                new_sub_topics = []
                top_sub_topic = topic.split(':')[0].strip()
                topics.append(top_sub_topic)
                new_sub_topics = topic.split(':')[1].split(',')
                for st in new_sub_topics:
                    sub_topics.append(top_sub_topic + ': ' + st.strip())

        return topics, sub_topics

class Subelement:
    """
    A class to represent a subelement of the question pool.

    ...

    Attributes
    ----------
    elem : str
        Name of the element the subelement is in, i.e. 2 or 3 or 4
    sub_el : str
        Identifier of the subelement
    description : str
        A discription of the subelement.  Can be several sentences or sentence fragments
    numq : number
        The number of questions in the subelement
    numg : number
        The number of groups in the subelement
    groups : list of Group objects
        The list of Group objects in the subelement.

    """

    #pylint: disable-msg=too-many-arguments
    def __init__(self, elem, sub_el, description, numq, numg, groups):
        self.elem = elem
        self.sub_el = sub_el
        self.description = description
        self.numq = numq
        self.numg = numg
        self.groups = groups            # Array of Group
    #pylint: enable-msg=too-many-arguments

    def __str__(self):
        """
        Returns a short string description of the object

        """

        return(
            f'Group("{self.sub_el}", "{self.description[0:20]}" '
        )

    def __repr__(self):
        """
        Returns a Subelement contructor.

        """
        return (
            f'sub_element("{self.elem}", "{self.sub_el}", "{self.description}", '
            f'"{self.numq}", "{self.numg}", "{self.groups}")'
        )

class Element:
    """
    A class to represent a element question pool. i.e Element 2, (Technician Class)

    ...

    Attributes
    ----------
    timestamp : str
        datetime.datetime.now() at the time of creation of instance
    elem : str
        Name of the element, i.e. 2 or 3 or 4
    elname : str
        Identifier of the element, i.e. Technician, General, Extra
    valid : object
        .begin - the beginning date for the element question pool
        .end - the ending date for the element question pool
    effective : date, first use of the pool, i.e. July 1, 2016
    subelements : list of Subelement objects
        The list of Subelement objects in the Element.

    """
    def __init__(self, elem, elname, yrvalid, effective, subelements, timestamp,
                 filename, filetype):
        """
        Constructs the attributes for the Element object

        Parameters
        ----------
        timestamp : str
            datetime.datetime.now() at the time of creation of instance
        elem : str
            Name of the element, i.e. 2 or 3 or 4
        elname : str
            Identifier of the element, i.e. Technician, General, Extra
        yrvalid : object
            .begin - the beginning date for the element question pool
            .end - the ending date for the element question pool
        effective : date, first use of the pool, i.e. July 1, 2016
        subelements : list of Subelement objects
            The list of Subelement objects in the Element.

    """
        self.filename = filename
        self.filetype = filetype
        self.timestamp = str(timestamp)
        self.elem = elem
        self.elname = elname
        self.yrvalid = yrvalid             # {'begin' : date, 'end' : date}
        self.effective = effective         # {'begin' : date, 'end' : date}
        self.subelements = subelements

    def __str__(self):
        """
        Returns a short string description of the object

        """

        return(
            f'Element("{self.elem}", "{self.elname}")'
            )

    def __repr__(self):
        """
        Returns an Element contructor.

        """
        return f'Element("{self.elem }","","","","{self.subelements},")'
    
class ElementPool:
    """
    """
    #TODO: add fileFN parameter, obj=element_pool, i.e. ElementHelp
    def __init__(self, element_pool):
        self.element_pool = element_pool

    def get_questions_by_ids(self, qids, options=''):
        """
        returns:
        [{
            'qid': 'T1A01', 
            'topics': [
                'Purpose and permissible use of the Amateur Radio Service', 
                'Operator/primary station license grant', 
                'Meanings of basic terms used in FCC rules', 
                'Interference', 
                'RACES rules', 
                'Phonetics', 
                'Frequency Coordinator'
                ], 
            'question': '#T1A01 Which of the following is part of the Basis and Purpose of the Amateur Radio Service?', 
            'answers': [
                'A. Providing personal radio communications for as many citizens as possible', 
                'B. Providing communications for international non-profit organizations', 
                'C. Advancing skills in the technical and communication phases of the radio art', 
                'D. All these choices are correct'
                ], 
            'correct answer': 'C. Advancing skills in the technical and communication phases of the radio art'
        }, 
        {question}, 
        {question}
        }]
        """
        result = []
        e = self.element_pool
        for se in e['subelements']:
            for g in se['groups']:
                topics = g['topics']
                for q in g['questions']:
                    if q['qid'] in qids:
                        question = {}
                        question['qid'] = q['qid']
                        question['topics'] = topics
                        if q['figure']:
                            question['figure'] = q['figure']
                        question['question'] = f'#{q["qid"]} {q["text"]}'
                        start = 0
                        if options.find('strip-answer-prefix') != -1:
                            start = 3
                        question['answers'] = []
                        for answer in q['answers']:
                            question['answers'].append(answer[start:])
                        question['correct answer'] = \
                            q['answers'][['A', 'B', 'C', 'D'].index(q['correct'])][start:]
                        result.append(question)
        return result

# an example ElementHelp file is aianswers.history.json
class ElementHelp:
    def __init__(self, help_FN='', help_obj=''):
        self.version = "0.15ex"
        self.version_date = "2023-07-23"
        self.element_help = {}
        if help_FN:
            path = Path(help_FN)
            if path.is_file():
                el_help = ''
                try:
                    #open(file, mode='r', buffering=- 1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
                    with path.open(mode='rt', encoding='UTF-8') as f:
                        el_help = json.load(f)
                except:
                    print("An exception occurred, path.open")       
        if help_obj:
            el_help = help_obj
        # sort the keys
        el_help_sort_keys = list(el_help.keys())
        el_help_sort_keys.sort()
        # import "current" aihelp
        for key in el_help_sort_keys:
            help = {}
            cur = el_help[key]['current']
            help["topics"] = cur.get("topics") if cur.get("topics_valid") else ''
            help["explanation"] = cur.get("explanation") if cur.get("explanation_valid") else ''
            help["memory_aid"] = cur.get("memory_aid") if cur.get("memory_aid_valid") else ''
            help["topics_valid"] = cur.get("topics_valid")
            help["explanation_valid"] = cur.get("explanation_valid")
            help["memory_aid_valid"] = cur.get("memory_aid_valid")
            help["topics_edited"] = cur.get("topics_edited") if cur.get("topics_edited") else ''
            help["explanation_edited"] = cur.get("explanation_edited") if cur.get("explanation_edited") else ''
            help["memory_aid_edited"] = cur.get("memory_aid_edited") if cur.get("memory_aid_edited") else ''
            self.element_help.update({key: help})

    def get_version(self):
        return self.version
    
    def print_summary(self):
        items_num = 0
        topics_valid = 0
        topics_edited = 0
        explanations_valid = 0
        explanations_edited = 0
        memory_aids_valid = 0
        memory_aids_edited = 0
        no_explanation = []
        no_memory_aids = []
        for qid, helps in self.element_help.items():
            items_num += 1
            topics_valid += 1 if (helps["topics_valid"] == True) else 0
            topics_edited += 1 if (helps["topics_edited"] == True) else 0
            #explanations_valid += 1 if (helps["explanation_valid"] == True) else 0
            if helps["explanation_valid"] == True:
                explanations_valid += 1
            else:
                no_explanation.append(qid)
            explanations_edited += 1 if (helps["explanation_edited"] == True) else 0
            #memory_aids_valid += 1 if (helps["memory_aid_valid"] == True) else 0
            if helps["memory_aid_valid"] == True:
                memory_aids_valid += 1
            else:
                no_memory_aids.append(qid)
            memory_aids_edited += 1 if (helps["memory_aid_edited"] == True) else 0

        print(f'helps:               {items_num}')
        print(f'topics valid:        {topics_valid}')
        print(f'topics edited:       {topics_edited}')
        print(f'explanations valid:  {explanations_valid}')
        print(f'explanations edited: {explanations_edited}')
        print(f'memory aids valid:   {memory_aids_valid}')
        print(f'memory aids edited:  {memory_aids_edited}')
        if no_explanation:
            print(f'questions with no explanation:')
            for qid in no_explanation:
                print(f'    {qid}')
        if no_memory_aids:
            print(f'questions with no memory aids:')
            for qid in no_memory_aids:
                print(f'    {qid}')

    def print_help_by_ids(self, qids):
        PREF_WIDTH = 80
        h = self.element_help
        for qid in qids.split():
            helps = h.get(qid)
            if helps:
                print('\n')
                print_wrap(f'Ham Question:    ', PREF_WIDTH, f'{qid}')
                print_wrap(f'    Topics:      ', PREF_WIDTH, f'{helps["topics"]}')
                print_wrap(f'    Explanation: ', PREF_WIDTH, f'{helps["explanation"]}')
                print_wrap(f'    Memory aid:  ', PREF_WIDTH, f'{helps["memory_aid"]}')

    def get_help_by_ids(self, qids, include_keys='ALL'):
        """
        Returns help information for a list of questions

        Parameters
            qids - a string with blank separated question ids:
                   'T1A01 T3B06'
                   or
                   'ALL' - all questions should be selected

        Return
            object with key = qid, and 'topics', 'explanation' and 'memory_aid' object
            { 'T1A01': {
                'topics': 'topics separated with; Another topic',
                'explanation': 'A block of sentences with an explanation',
                'memory_aid': 'A block of sentences with a memory aid'
            }}
        """
        result = {}
        e = self.element_help
        for qid in e:
            if qid in qids or qids.upper() == 'ALL':
                if include_keys == 'ALL':
                    result.update({qid: e[qid]})
                else:
                    pass
                    #TODO: implement include_keys = 'topics explanation memory_aid" etc
                    #{'topics': e[qid]['topics'], 
                    # 'explanation': e[qid]['explanation'], 
                    # 'memory_aid': e[qid]['memory_aid']}})
        return result
    
    def export_help(self, help_FN):
        export_help = {}
        for qid, h in self.element_help.items():
            export_help.update({qid: {"topics": h["topics"], "explanation": h["explanation"], "memory_aid": h["memory_aid"]}})
        path = Path(help_FN)
        with open(help_FN, 'w', encoding='utf-8') as file:
            file.write(json.dumps(export_help, default=vars, indent=2))

