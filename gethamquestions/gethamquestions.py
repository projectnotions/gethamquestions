"""
Process the Amateur Radio Element Question Pool and return a JSON representation
The following question pools have been tested:

Classes:

    Element
    Subelement
    Group
    Question

Functions:
    _parse_line
    get_element

Misc variables:
    regex_dict

References
    https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
    https://www.vipinajayakumar.com/parsing-text-with-python/
    stackoverflow.com/questions/55933956/what-does-a-star-asterisk-do-in-f-string/55934921
    https://docs.python.org/3/howto/unicode.html#introduction-to-unicode

Notes
    pylint is used for style checking
    see function _parse_line() notes for Question Pool anomolies

Change Log
    2023-06-29 v10 - adding openai routine to identify topics for question
    2023-06-30 v10 - tried to resolve use of u\uf0b4 for "x", could not fix
    2023-06-29 v09 - fixed unusal characters for +', etc
    2023-06-28 v08 - added case for "E3B08 (DELETED)"
    2023-06-27 v07 - removed match statement for wls python 3.8
    2023-06-22 v06 - cleaned up pylint
    2023-06-13 v05 - Added source file name to
    2023-05-24 v04 - Work for all elements as of now.  Added Question id attribute
    2023-05-22 v03 - Wrks for element 2 and element 3. State base for better error detection
    2023-05-21 v02 = Works for Question Pool only. Not for total file. Is not state based.
"""

#-*- coding: utf-8 -*-
import re
import json
import sys
import datetime
import os, os.path
import docx
import magic
from gethamelementclasses import *


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
    def __init__ (self, state, cur_element, cur_subelement, cur_group):
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
            # If windows doc file, write out txt file
            if (self.cur_element.filetype == 'Microsoft Word'):
                # write out text file
                out_lines = get_file(self.cur_element.filename)
                #out_lines = Filelines(out_lines)
                outpath3 = f'./output/element{self.cur_element.elem}.txt'
                os.makedirs(os.path.dirname(outpath3), exist_ok=True)
                with open(outpath3, 'w', encoding='utf-8-sig') as file3:
                    line_num = 0
                    for line in out_lines:
                        line_num +=1
                        line = fix_line(line)
                        if (not line.isascii()):
                            msg('Warning', 'W002', 
                                'Non ASCII in out txt', line_num, json.dumps(line))
                        file3.write(line)
                msg('Info', 'I201', 
                    f'text written to element{self.cur_element.elem }.txt, lines={len(out_lines)}')
            # Writing element JSON to file
            # https://stackoverflow.com/questions/23793987/write-a-file-to-a-directory-that-doesnt-exist
            outpath = f'./output/element{self.cur_element.elem }.json'
            os.makedirs(os.path.dirname(outpath), exist_ok=True)
            #TODO: add Try exception
            with open(outpath, 'w', encoding='utf-8-sig') as file2:
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
            f'*** Summary - Element {self.cur_element.elem } - {self.cur_element.timestamp} '
              f'{el_namefmt}{self.cur_element.yrvalid["begin"]}-'
              f'{self.cur_element.yrvalid["end"]} ***')
        subelnum = 0
        groupnum = 0
        questionsnum = 0
        msg('Info', 'I301', f'Subelements: {len(self.cur_element.subelements)}')
        for sube in self.cur_element.subelements:
            subelnum += 1
            msg('Info', 'I302', f'  Sub element: {sube.sub_el }, Groups: {sube.numg}')
            for grp in sube.groups:
                groupnum += 1
                questionsnum += len(grp.questions)
                msg('Info', 'I303', f'    Group: {grp.group_id}, questions: {len(grp.questions)}')
        msg('Info', 'I304', 
            f'Subelements: {subelnum}, groups: {groupnum}, questions: {questionsnum}')
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

    def __init__ (self, listobj):
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

    #def __str__(self):
        """
        Returns a short string description of the object

        """

        #return f'Filelines Object("{self.list}", "Length{len(self.list)}"'

    def __repr__(self):
        """
        Returns an Filelines contructor.

        """
        return f'Filelines("{self.list}")'

# set up regular expressions
# use https://regexper.com to visualise these if required
regex_dict = {
    """
    Examples:
        subelement
            element 4 SUBELEMENT E1 - COMMISSION RULES [6 Exam Questions - 6 Groups]
    """

    'element_onel' : re.compile(
        r'(?P<begin>\d\d\d\d)-(?P<end>\d\d\d\d)\s+'
        r'(?P<elname>[a-zA-z]+)\s+Class.*FCC Element '
        r'(?P<elnum>\d)\sQuestion Pool\s-\sEffective\s(?P<effbegin>\w+\s\d+,\s\d\d\d\d).*'),
    'el_name'    : re.compile(
        r'(?P<yrbegin>\d\d\d\d)-(?P<yrend>\d\d\d\d)\s+(?P<elname>[a-zA-z]+)\s+Class.*'),
    'el_effective': re.compile(r'Effective (?P<begin>\d+\/\d+/\d+)...(?P<end>\d+\/\d+\/\d+)'),
    'el_eff_short': re.compile(r'Effective (?P<begin>[JFMASOND].*\s\d+\,\s\d\d\d\d).*$'),
    'el_num'   : re.compile(r'FCC Element (?P<elnum>\d)\sQuestion Pool\s*$'),
    'subelement': re.compile(r'SUBELEMENT (?P<subelement>[TGE]\d)\s.?\s?(?P<description>.*)'
                  r'-?\s?\[(?P<numq>\d+)\s[Ee]xam\s[Qq]uestions?\s.*\s(?P<numg>\d+)\s[Gg]roups?\]'),
    'subelement2': re.compile(r'(?P<subelement>[TGE]\d)\s.\s(?P<description>.*)'
                   r'\s.?\[(?P<numq>\d+)\sExam\sQuestions\s.\s(?P<numg>\d+)\s[Gg]roups\].*'),
    'group'     : re.compile(
        r'(?P<subelem>[TGE]\d)(?P<group_id>[A-H])\s-?\s?(?P<description>.*)'),
    'question'  : re.compile(
        r'(?P<subelem>[TGE]\d)(?P<group>[A-H])(?P<qnum>\d\d)\s?\((?P<ans>[A-D])\)\s?(?P<fcc>.*)'),
    #'question'  : re.compile(
    # r'(?P<subelem>T\d)(?P<group>[A-F])(?P<qnum>\d\d).+\((?P<ans>[A-D])\)\s?(?P<fcc>.*)'),
    'removed'   :
        re.compile(r'(?P<subelem>[TGE]\d)(?P<group>[A-F])(?P<qnum>\d\d)\s? Question Removed.?'),
    'removed2'  : re.compile(r'(?P<subelem>[TGE]\d)(?P<group>[A-F])(?P<qnum>\d\d)\s? \(DELETED\).?'),
    'end'      : re.compile(r'~~~~?.*~~~~?'),
    'blank'    : re.compile(r'~~'),
}

def _parse_line(line, pool_state):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    Question heading formats:
      Element 2: 2022-2026: 2022-2026 Technician Class
                          : FCC Element 2 Question Pool
                          : Effective 7/01/2022 - 6/30/2026
      Element 3: 2019-2023: General Class - FCC Element 3 Question Pool - Effective July 1, 2019
      Element 3: 2023-2027: 2023-2027 General Class
                          : FCC Element 3 Question Pool
                          : Effective 7/01/2023 - 6/30/2027
      Element 4: 2020-2024: 2020-2024 Extra Class
                          : FCC Element 4 Question Pool
                          : Effective July 1, 2020
    Anomolies:
      Element 4: E3B08 (DELETED)
      Element 4: 2020-2024: E7C09 (D) - Missing a ~~ line at the end of the question
                 (~~ at end of answer D, line wrap disguises error in word)
      Element 4: 2020-2024: E8C10 (C) - Missing a ~~ line at the end of the question
      Element 4: file: 2020ExtraClassPoolJan22.txt
                  ----------------------------------------------------------------------
                  E2B08 (A)
                    What technique allows commercial analog TV receivers to be used for fast-scan
                        TV operations on the 70 cm band?
                    A. Transmitting on channels shared with cable TV
                    B. Using converted satellite TV dishes
                    C. Transmitting on the abandoned TV channel 2
                    D. Using USB and demodulating the signal with a computer sound card

                    ~~
                  ----------------------------------------------------------------------
                  ~~~~End of question pool text~~~~
                  ----------------------------------------------------------------------
    """
    if not line:
        return 'end', ''
    for key, regex in regex_dict.items():
        match = regex.search(line)
        #print(key + ", match='" + match + "'")
        if match:
            if key == 'element_onel':
                # print('element_one1 match')
                pool_state.el_name = match.group('elname')
                pool_state.el_effective = {'begin' : match.group('effbegin'), 'end' : ''}
                pool_state.el_yrvalid = {'begin' : match.group('begin'), \
                                       'end'   : match.group('end')}
                pool_state.el_num = match.group('elnum')
                key = 'element'
            if key == 'el_name':
                # print('el_name match')
                # print('begin="' + match.group('yrbegin') + '", end="' + match.group('yrend') + '"')
                pool_state.el_name = match.group('elname')
                pool_state.el_yrvalid = {'begin' : match.group('yrbegin'), \
                                       'end'   : match.group('yrend')}
                key = 'data'
            if key == 'el_effective':
                # print('el_effective match')
                pool_state.el_effective = {'begin' : match.group('begin'), \
                                         'end'   : match.group('end')}
                key = 'data'
                if pool_state.el_num:
                    key = 'element'
            if key == 'el_eff_short':
                # print('el_eff_short match')
                # print('el begin="' + match.group('begin') + '"')
                pool_state.el_effective = {'begin' : match.group('begin'), \
                                         'end'   : ''}
                key = 'data'
                if pool_state.el_num:
                    key = 'element'

            if key == 'el_num':
                pool_state.el_num = match.group('elnum')
                key = 'data'
            if key == 'subelement2':
                key = 'subelement'

            return key, match
    # if there are no matches
    return None, None

def get_file_type(file_name):
    """
    Determine the file type and return:
    - "ASCII text" if it is a text file
    - "Microsoft Word" if it is a docx
    - "anything else" - not ASCII text or Microsoft Word

    """
    
    tokens = magic.from_file(file_name).split()
    result = ''
    sep = ''
    i = 0
    while (i < len(tokens)) and (i < 2):
        result += sep + tokens[i]
        sep = ' '
        i += 1
    return result

def get_file(file_name):
    """
    Read a file and return an iterable object list of all lines

    """
    
    file_type = get_file_type(file_name)
    if (file_type == 'ASCII text') or (file_type == 'UTF-8 Unicode'):
        try:
            with open(file_name, 'r', encoding='UTF-8') as file:
                lines = file.readlines()
            return lines

        except IOError as err:
            print(f'I/O error({err.errno}): {err.strerror} for: "{file_name}"')
            return ''

        except: #handle other exceptions such as attribute errors
            print("Unexpected error:", sys.exc_info()[0])
            return ''
    elif (file_type == 'Microsoft Word'):
        doc = docx.Document(file_name)
        lines = []
        line_num = 0
        for para in doc.paragraphs:
            #try:
            #    line = para.text.decode('UTF-8', 'strict')
            #except UnicodeDecodeError:
            #    print('*** Error, line has non UTF-8 characters: "' + para.text + '"')
            line = para.text
            line_num += 1
            if (not line.isascii()):
                msg('Warning', 'W402', 'line has non-ascii characters', line_num, json.dumps(line))
                line = fix_line(line)
            lines.append(line + '\n')
        msg('Info', 'I400', 'get_file(' + file_name + ')' + 
            'returned len(lines)= ' + str(len(lines)))  
        return lines
    else:
        msg('Error', 'E401', 'Unknown file type "' + file_type + '"')
        return ''

def fix_line(line, index=''):

    line = line.replace(u"\u2013", '-')
    line = line.replace(u"\u2019", "'")
    line = line.replace(u"\u2018", "'")
    line = line.replace(u"\u201c", '"')
    line = line.replace(u"\u201d", '"') 
    line = line.replace(u"\uf0b4", 'x')
    return line
    
def read_fline(filelines, skip_blank=True):
    """
    Read the next non-blank line of the iterable

    """

    try:
        line, index = next(filelines)
        if (not line.isascii()):
            msg('Warning', 'W403', 'line has non-ascii characters', index, json.dumps(line))
            line = fix_line(line)
        while line and (len(line.strip()) == 0 and skip_blank):
            line, index = next(filelines)
            if (not line.isascii()):
                msg('Warning', 'W403', 'line has non-ascii characters', index, json.dumps(line))
                line = fix_line(line)
        return line, index

    except StopIteration:
        line = ''
        return line, len(filelines)

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
    if (not msg_type in types):
        print('Error   : E001: Invalid Message Type:     : "' + msg_type + '"')
    else:
        pri = types.index(msg_type)
        if pri < 4:
            print(f'{msg_type:8}: {msg_num:4}: {message:20} {line_num} {line}\n', end='')
  

def get_element_pool (file_name):
    """
    Extract the element pool from the source file

    """
    #State __init__(self, state, cur_element, cur_subelement, cur_group):
    #state.elname = ''
    pool_state = State('initial', None, None, None)
    file_lines = get_file(file_name)
    file_lines = Filelines(file_lines)  # convert to Filelines iterable
    while pool_state.state != 'end':
        line, count = read_fline(file_lines)
        key, match = _parse_line(line, pool_state)
        begin_state = pool_state.state

        if key == 'removed' or key == 'removed2' or key == 'blank':
            continue
        #match pool_state.state:
            #case 'initial':
        if pool_state.state == 'initial':
                #match key:
                    #case 'element':
            if key == 'element':
                # Can be ended by end of input
                # Not currently allowed more than one element, so it can't end anything else
                subelements = []
                timestamp = datetime.datetime.now()
                pool_state.cur_element = Element(pool_state.el_num , pool_state.el_name, \
                    pool_state.el_yrvalid, pool_state.el_effective, subelements, \
                    timestamp, file_name, get_file_type(file_name))
                pool_state.state = 'element'
                    #case 'end':
            elif key == 'end':
                msg('Error', 'E001', 'Premature end', count, line)
                pool_state.state = 'end'
                    #case 'data':
            elif key == 'data':
                msg('Debug', 'D002', 'Data line', count, line)
                    #case _:
            else:
                msg('Debug', 'D004', 'Line b4 Element', count, line)

            #case 'element':
        elif pool_state.state == 'element':
                #match key:
                    #case 'subelement':
            if key == 'subelement':
                # Can be ended by subelement, end of input
                # Can end group, subelement
                #                        pool_state.close_group()
                #                        pool_state.close_subelement()
                # New subelement
                description = match.group('description').strip().rstrip('-').strip()
                pool_state.cur_subelement = \
                    Subelement(pool_state.cur_element.elem, match.group('subelement'), \
                                description, match.group('numq'), match.group('numg'), [])
                pool_state.state = 'subelement'
                    #case 'end':
            elif key == 'end':
                msg('Error', 'E003', 'Unexpected "end"', count, line)
                pool_state.state = 'end'
                    #case _:
            else:
                msg('Error', 'E004', '{key} from {pool_state.state}', count, line)
                pool_state.state = 'end'
            #case 'subelement':
        elif pool_state.state == 'subelement':
                #match key:
                    #case 'group':
            if key == 'group':
                # Can be ended by subelement, group, end of input
                # Can end group
                pool_state.close_group()
                # New group
                subelem = match.group('subelem')
                group_id = match.group('group_id')
                description = match.group('description')
                description = description.strip().rstrip('-').strip()
                questions = []
                pool_state.cur_group = Group(subelem, group_id, description, questions)
                pool_state.state = 'group'
                    #case 'end':
            elif key == 'end':
                msg('Error', 'E004', 'Unexpected "end"', count, line)
                pool_state.state = 'end'
                    #case _:
            else:
                msg('Error', 'E007', '{key} from {pool_state.state}', count, line)
                msg('Error', 'D008', f'{begin_state}:{pool_state.state}', count, line)
                pool_state.state = 'end'
            #case 'group':
        elif pool_state.state == 'group':
                #match key:
                    #case 'group':
            if key == 'group':
                # Can be ended by subelement, group, end of input
                # Can end group
                pool_state.close_group()
                # New group
                subelem = match.group('subelem')
                group_id = match.group('group_id')
                description = match.group('description')
                questions = []
                pool_state.cur_group = Group(subelem, group_id, description, questions)
                pool_state.state = 'group'
                    #case 'subelement':
            elif key == 'subelement':
                # Can be ended by subelement?, end of input
                # Can end group, subelement?
                pool_state.close_group()
                pool_state.close_subelement()
                sub_el = match.group('subelement')
                description = match.group('description')
                # couldn't get regex to elminiate final - in some cases
                description = description.strip().rstrip('-').strip()
                numq = match.group('numq')
                numg = match.group('numg')
                groups = []
                pool_state.cur_subelement = \
                    Subelement(pool_state.cur_element.elem, sub_el, \
                                description, numq, numg, groups)
                pool_state.state = 'subelement'
                    #case 'question':
            elif key == 'question':
                #'T(?P<subelem>\d)(?P<group>[A-F])(?P<qnum>\d\d).
                #\((?P<ans>[A-D])\).(?P<fcc>.*)'
                #metastate = 'question'
                #print(f'{metastate:8} : {count:04d}:{line}', end='')
                msg('Debug', 'D002', f'{begin_state}:{pool_state.state}', count, line)
                subelem = match.group('subelem')
                group = match.group('group')
                qnum = match.group('qnum')
                qid = f'{subelem}{group}{qnum}'
                ans = match.group('ans')
                fcc = match.group('fcc')
                # Get question lines from the file
                text, count = read_fline(file_lines)      # read line 1 Question
                figure = ''
                regex_figure = re.compile(r'(^|\s)[fF]igure\s+(?P<fig>[TGE]\d?-\d+).?')
                match = regex_figure.search(text)
                if match:
                    figure = match.group('fig')
                answers = []

                line, count = read_fline(file_lines)      # read line 2 Ans A.
                answers.append(line.strip())
                line, count = read_fline(file_lines)      # read line 3 Ans B.
                answers.append(line.strip())
                line, count = read_fline(file_lines)      # read line 4 Ans C.
                answers.append(line.strip())
                line, count = read_fline(file_lines)      # read line 5 Ans D.
                answers.append(line.strip())
                # ignore this line, ~~ at end of question
                # Read line 6 Question End ~~, don't skip blank lines
                line, count = read_fline(file_lines, False)
                if line.strip() != '~~':
                    msg('Error', 'E005', 'Missing quest end ~~', count, line)
                cur_question = \
                    Question(subelem, group, qnum, \
                                qid, text.strip(), ans, figure, answers, fcc, \
                                pool_state.cur_group.topics)
                # Add question to Group
                pool_state.cur_group.questions.append(cur_question)
                    #case 'end':
            elif key == 'end':
                # Can end group, subelement
                pool_state.close_group()
                pool_state.close_subelement()
                pool_state.close_element()
                pool_state.state = 'end'
                pool_state.print_summary()
                    #case _:
            else:
                #print(f'Error: {key} is not valid in state "{pool_state.state}" ', end='')
                msg('Error', 'E010', f'{key} not valid', count, line)
                msg('Info', 'I003', f'{begin_state}:{pool_state.state}', count, line)
                pool_state.state = 'end'
            #case 'end':
        elif pool_state.state == 'end':
            pass
            #case _:
        else:
            pass
        if begin_state != pool_state.state:
            msg('Debug','D005', f'{begin_state}:{pool_state.state}', count, line)

    return pool_state.cur_element


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        msg('Debug', 'D001', sys.argv[1], 0, 'nond')
        if (os.path.isfile(sys.argv[1])):
            element = get_element_pool(sys.argv[1])
        else:
            msg('Error', 'E002', 'File not found: "' + sys.argv[1] + '"' )
    else:
        msg('Error', 'E999', 'Not enough arguments')
        #element = get_element_pool('element2.txt')
        #element = get_element('input.txt')
