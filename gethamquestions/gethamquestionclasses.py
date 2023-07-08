import os
import json

def msg(msg_type, msg_num, message, line_num='', line=''):
    """
    Print messages in a consistant way

    Parameters
    ----------
    msg_type: str
        Type of message: 'Info', 'Warning', 'Error'
    msg_num : str
        Identifier of the message, I001, W005, E006, etc
    message : str
        A short message to display
    line_num : str
        The line number
    line : str
        The line in the file being processed
    """
    if line:
        line = f': {line.strip():20}'
    if line_num:
        line_num = f': {line_num:-4d}'
    types = ['zero', 'Error', 'Warning', 'Info', 'Debug']
    if not msg_type in types:
        print('Error   : E001: Invalid Message Type:     : "' + msg_type + '"')
    else:
        pri = types.index(msg_type)
        if pri < 4 and msg_num not in 'W403':
            print(f'{msg_type:8}: {msg_num:4}: {message:20} {line_num} {line}\n', end='')

class State:
    """
    A class to represent internal states and element pool class objects
    while parsing a question pool

    ...

    Attributes
    ----------
    state: str
        state name "initial", "element", "subelement", "group", "end"
    cur_element : Element object
        The instance of the current Element
    cur_subelement: Submlement object
        The instance of the current Subelement
    group : Group object
        The instance of the current Group

    """
    def __init__(self, state, cur_element, cur_subelement, cur_group,
                 source_lines):
        """
        Constructs the attributes for the State object

        Parameters
        ----------
        state: str
            state name "initial", "element", "subelement", "group", "end"
        cur_element : Element object
            The instance of the current Element
        cur_subelement: Submlement object
            The instance of the current Subelement
        group : Group object
            The instance of the current Group

    """
        self.state = state
        self.cur_element = cur_element
        self.cur_subelement = cur_subelement
        self.cur_group = cur_group
        self.el_name = ''
        self.el_yrvalid = ''             #{'begin': yyyy, 'end': yyyy}
        self.el_effective = ''           #{'begin' : July 1, 2019, 'end' : date}
        self.el_num = ''
        self.source_lines = source_lines

    def close_group(self):
        """
        closes the current Group object

        """
        if self.cur_group:
            self.cur_subelement.groups.append(self.cur_group)
            self.cur_group = None

    def close_subelement(self):
        """
        closes the current Subelement object

        """
        if self.cur_subelement:
            self.cur_element.subelements.append(self.cur_subelement)
            self.cur_subelement = None

    def close_element(self):
        """
        closes the current Element object

        """
        if self.cur_element:
            str_out = json.dumps(self.cur_element, default=vars, indent=2)
            #print(self.cur_element.filetype)
            # Writing element JSON to file
            # stackoverflow.com/questions/23793987/write-a-file-to-a-directory-that-doesnt-exist
            outpath = f'./output/element{self.cur_element.elem }.json'
            os.makedirs(os.path.dirname(outpath), exist_ok=True)
            #TODO: add Try exception
            with open(outpath, 'w', encoding='utf-8') as file2:
                file2.write(str_out)
            msg('Info', 'I200', f'JSON written to element{self.cur_element.elem}.json')

    def print_summary(self):
        """
        Prints a summary of the element question pool

        """
        # Print Summary
        el_namefmt = ''
        if self.el_name:
            el_namefmt = f'({self.el_name} Class) '
        #TODO: convert to Info msg
        msg('Info', 'I300',
            f'*** Summary - Element {self.cur_element.elem } - {self.cur_element.timestamp} '\
              f'{el_namefmt}{self.cur_element.yrvalid["begin"]}-'\
              f'{self.cur_element.yrvalid["end"]} ***')
        subelnum = 0
        groupnum = 0
        questionsnum = 0
        topicsnum = 0
        subtopicsnum = 0
        msg('Info', 'I301', f'Subelements: {len(self.cur_element.subelements)}')
        for sube in self.cur_element.subelements:
            subelnum += 1
            msg('Info', 'I302', f'  Sub element: {sube.sub_el }, Groups: {sube.numg}')
            for grp in sube.groups:
                groupnum += 1
                questionsnum += len(grp.questions)
                topicsnum += len(grp.topics)
                subtopicsnum += len(grp.subtopics)
                msg('Info', 'I303', f'    Group: {grp.group_id}, questions: {len(grp.questions)},'
                    f' topics: {len(grp.topics)}, subtopics: {len(grp.subtopics)}')
        msg('Info', 'I304',
            f'Subelements: {subelnum}, groups: {groupnum}, questions: {questionsnum}'
            f' topics: {topicsnum}, subtopics: {subtopicsnum}' )
        msg('Info', 'I305', '*** End of Processing ***\n')


class Filelines:
    """
    A class to represent tile contents in an iterable object

    ...

    Attributes
    ----------
    list : list
        The list object to iterate
    current_index : number
        The current index into list for iterable functions

    """

    def __init__(self, listobj):
        """
        Constructs the attributes for the Filelines object

        Parameters
        ----------
        list : list
            Name of the list object to iterate

        """
        self.list = listobj
        self.current_index = 0

    def __iter__(self):
        """
        The iter function

        """
        self.current_index = 0
        return self

    def __len__(self):
        """
        The length of the iterable (iterables normally don't have lengths.)

        """
        return len(self.list)

    def __next__(self):
        """
        Returns the next iteration and the item number (counting from 1).
        The first iterate past the end of the list returns null, line number.
        The next iteration will raise StopIteration


        """
        if self.current_index <= len(self.list):
            if self.current_index < len(self.list):
                line, num = self.list[self.current_index], self.current_index +1
            else:
                line, num = '', self.current_index + 1
            self.current_index += 1
            return line, num
        raise StopIteration

    def __str__(self):
        """
        Returns a short string description of the object

        """

        return f'Filelines Object("{self.list}", "Length{len(self.list)}"'

    def __repr__(self):
        """
        Returns an Filelines contructor.

        """
        return f'Filelines("{self.list}")'