#pylint: disable-msg=too-many-instance-attributes
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
        self.topics = []
        self.get_topics(topic_list)
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

    def get_topics(self, topic_list):
        """
        Returns the topics contained in a question. EXPERIMENTAL

        """
        self.topics = []
        potential_topics = []
        self.topics = potential_topics

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
        self.topics = self.get_topics(description)
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
        self.topics = self.get_topics(description)

    def get_topics(self, topic_string):
        """
        Returns an array with the topics for the object

        """
        #print(f'self.description = "{self.description}"')
        #print(f'self.description.split(";") = {self.description.split(";")}')
        topics = []
        for topic in topic_string.split(';'):
            topics.append(topic.strip())
        return topics

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
