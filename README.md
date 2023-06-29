# gethamquestions
Parse the official Amateur Radio FCC question pools and get the Element Questios in a JSON object

## Installation
Download the getquestions.py file. 

## Overview
With the advent of accessible AI infrastructure, Amateur Radio seems a perfect domain in which to experiment with value add functions that AI API's might provide.
To get started though, requires accurate question pools.  Fortunately these are publically available from [http://www.ncvec.org/page.php?id=338](http://www.ncvec.org/page.php?id=338).
You can run gethamquestions.py specifying the docx file as input.  It will create a JSON file as output, and also a text version (UTF-8 encoding) of the docx file.  If you prefer, you can specifiy a text file as input (recommended UTF-8 encoding.)

A javascript class is also provided, elementpool.js (class ElementPool) that supports the method "getQuestionsByIds".  Additional methods will be added as use cases emerge.

The next phase of development will experiment with AI input on topics, and explainations of the questions and answers. Also provide full package support.

A rudimentary deployment of gethamquestions can be seen at [projectnotions.com - Technician Ham Class](https://projectnotions.com/blog1/2023/05/technician-ham-class)

## Usage

```python
python gethamquestions.py "C:\Users\kb\onedrive\HamTest\QuestionPools\Technician Pool and Syllabus 2022-2026 Public Release Errata March 7 2022.utf8.txt"

# returns json file, txt file (if the input was docx), and summary (abbreviated below)
Info I9999 C:\Users\kenwb\onedrive\HamTest\QuestionPools\Technician Pool and Syllabus 2022-2026 Public Release Errata March 7 2022.utf8.txt 0 nond
timestamp = 2023-06-22 16:13:45.848043
JSON written to Element2.json
*** Summary - Element 2 - self.cur_element.timestamp (Technician Class) 2022-2026 ***
Subelements: 10
  Sub element: T1, Groups: 6
    Group: A, questions: 11
    Group: B, questions: 12
    Group: C, questions: 11
    Group: D, questions: 11
    Group: E, questions: 11
    Group: F, questions: 11
  Sub element: T2, Groups: 3

 etc. etc.

   Sub element: T0, Groups: 3
    Group: A, questions: 12
    Group: B, questions: 11
    Group: C, questions: 13
Subelements: 10, groups: 35, questions: 411 
```
The javascript class ElementPool is provided for methods of getting guestions based on various criteria.

## Output

A JSON file is created with the name of "ElementX.json" where X is 2, 3, or 4.  A sample is below:

```javascript
{
  "filename": "C:\\Users\\kenwb\\onedrive\\HamTest\\QuestionPools\\Technician Pool and Syllabus 2022-2026 Public Release Errata March 7 2022.utf8.txt",
  "timestamp": "2023-06-22 16:13:45.848043",
  "elem": "2",
  "elname": "Technician",
  "yrvalid": {
    "begin": "2022",
    "end": "2026"
  },
  "effective": {
    "begin": "7/01/2022",
    "end": "6/30/2026"
  },
  "subelements": [
    {
      "elem": "2",
      "sub_el": "T1",
      "description": "COMMISSION'S RULES",
      "numq": "6",
      "numg": "6",
      "groups": [
        {
          "subelement": "T1",
          "group_id": "A",
          "description": "Purpose and permissible use of the Amateur Radio Service; Operator/primary station license grant; Meanings of basic terms used in FCC rules; Interference; RACES rules; Phonetics; Frequency Coordinator",
          "topics": [
            "Purpose and permissible use of the Amateur Radio Service",
            "Operator/primary station license grant",
            "Meanings of basic terms used in FCC rules",
            "Interference",
            "RACES rules",
            "Phonetics",
            "Frequency Coordinator"
          ],
          "questions": [
            {
              "subelement": "T1",
              "group": "A",
              "num": "01",
              "qid": "T1A01",
              "text": "Which of the following is part of the Basis and Purpose of the Amateur Radio Service?",
              "correct": "C",
              "figure": "",
              "fcc": "[97.1]",
              "answers": [
                "A. Providing personal radio communications for as many citizens as possible",
                "B. Providing communications for international non-profit organizations",
                "C. Advancing skills in the technical and communication phases of the radio art",
                "D. All these choices are correct"
              ],
              "topics": [
                "Purpose and permissible use of the Amateur Radio Service"
              ]
            },
```
