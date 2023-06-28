/** Class containing the Amateur Radio Element Question Pool
 * Generated from the question pooly by gethamquestions.py
 * More methods will be added as development proceeds
*/
class ElementPool {
    /**
     * Create the ElementPool with an precreated object (see gethamquestions.py)
     * @param {object} element - element pool object
     */
	constructor(element) {
		this.element = element;
		
	}
    /**
     * Get an array of questions corresponding to an input of question ID's
     * @param {array} qIds an array of strings containing the question id's in form SeGXx, i.e. "T1A02"
     * @param {string} options  - a string containing: 'strip-answer-prefix' - the answer prefix should be removed, i.e. A. Answer
     * @returns {array} - an array of Question objects
	 */
	//  /***  @enum
	//  *         where Question has the properties:
	//  *         .figure - str with the name of the associated figure/diagram,
	//  *         .correct - str, on of ['A', 'B', 'C', 'D'] that is the correct answer,
	//  *         .title - str, the question in this format: 'Question #T1A03 What is the ...',
	//  *         .answers - an array of str containing the answer strings, i.e. ,
	//  *            A. All of these answers are correct ,
	//  *            Note: if options has the string 'strip-answer-prefix' the prefix is removed. ,
    //  */
	getQuestionsByIds(qIds, options='') {
		debug(`getQuestionsById()`, 'Enter', `${qIds}`);
		let result = [];
		let e = this.element;
		let se = e.subelements;
		for (let seI=0; seI<se.length; seI++) {
			//debug('getQuestionsByIds()', 'Info', `Subelement = "${se[seI].sub_el}", description ="${se[seI].description}"`);
			let g = se[seI].groups;
			for (let gI=0; gI<g.length; gI++) {
				//debug('getQuestionsByIds()', 'Info', `    Group = "${g[gI].group_id}", description ="${g[gI].description}"`);
				let q = g[gI].questions;
				for (let qI=0; qI<q.length; qI++) {
					//debug('getQuestionsByIds()', 'Info', `        Question = "${q[qI].qid}", text ="${q[qI].text}"`);
					let indx = qIds.indexOf(q[qI].qid);
					if (indx != -1)	{
						let question = {};
						question.figure = q[qI].figure;
						if (question.figure) {
							//debug('getQuestionsByIds()', 'Info', `        Question = "${q[qI].qid}", figure ="${q[qI].figure}"`);	
						}
						let correct = ['A', 'B', 'C', 'D'].indexOf(q[qI].correct);
						question.title = `Question #${q[qI].qid} ${q[qI].text}`;
						let start = 0;
						if (options.indexOf('strip-answer-prefix') != -1) {
						   start = 3;	
						}
						question.answers = [];
						for (let i=0; i<q[qI].answers.length; i++) {
							question.answers[i] = q[qI].answers[i].substr(start);
						}	
						question.correct = correct;
						result[indx] = question;
					}
				}
			}
		}
		let resultError = false;
		for (let i=0; i<result.length; i++) {
		    if (!result[i]) {
				debug(`getQuestionsById()`, 'Error', `result is empty at index ${i}`)
				debugger;
			}	
		}
		return result;
		debug(`getQuestionsById()`, 'Exit', `${qIds}`);
	}
}
