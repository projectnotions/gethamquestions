/** Class containing the Amateur Radio Element Question Pool
 * Generated from the question pooly by gethamquestions.py
 * More methods will be added as development proceeds
*/
//console.log('elementpool2.js begin')
//
/*********************************************/
/*** WPCode snippet name: elementpool.js   ***/
/*********************************************/
class ElementPool {
	/**
     * Create the ElementPool with an precreated object (see gethamquestions.py)
	 * or use the method getElementByFileName to load an object
     * @param {object} element - element pool object, or null
	 * @property {object} element - an element pool object, created by gethamquestions.py
	 * @property {function} getFileSuccess - a function called by getElementByFileName on success
	 * @property {function} getFileFail - a function called by GetElementByFileName on fail
     */
	constructor(element=null) {
		this.element = element;
		this.getFileSuccess =null;
		this.getFileFail = null
	}

	EpSuccess(json) {
		this.element = json;
	}

	EpFail(evt) {
		this.element = '';
	}
	/**
	 * Get an Element from a file.  The element is in JSON format.  
	 * gethamquestions.py can produce the file
	 * 
	 * @param {string} fileUrl - The url of the file.  Relative or absolute
	 * @param {function} [success] - function to be called if loading the file is successfull
	 * @param {function} [fail] - function to be called if loading the file fails
	 */
    getElementByFileName(fileUrl, success, fail) {
		debug(`getElementByFileName()`, 'Enter', `${fileUrl}`);
		if (typeof success == 'function') {
			this.getFileSuccess = success;
		}
		if (typeof fail == 'function') {
			this.getFileFail = fail;
		}
		let self = this;
		this.element = '';
		jQuery.getJSON(fileUrl, function(json) {	
		    self.EpSuccess(json);
			if (self.getFileSuccess) {
				self.getFileSuccess(json);
			}

		})
		    .fail(function(evt) {
                self.EpFail(evt);
				if (self.getFileFail) {
					self.getFileFail(evt);
				}

			})
		    //.always(function(evt) {
			//	self.EpAlways(evt);
			//})  
			debug(`getElementByFileName()`, 'Exit', `${fileUrl}`);     
    }
	/**
	 * Get Questions by their ID, i.e. T1A01, T3C04, etc.
	 * 
	 * @param {Array} qIds - An array with the question ids
	 * @param {string} [options=''] options - 'strip-answer-prefix' - Strip 'Question T1A01'
	 * @return [[{questions}], [errorMessages]] - returns question array and Msg array
	 */
	//  /***  @enum
	//  *         where Question has the properties:
	//  *         .qid - the question id, i.e. 'T1A01'
	//  *         .figure - str with the name of the associated figure/diagram,
	//  *         .correct - str, on of ['A', 'B', 'C', 'D'] that is the correct answer,
	//  *         .title - str, the question in this format: 'Question #T1A03 What is the ...',
	//  *         .answers - an array of str containing the answer strings, i.e. ,
	//  *            A. All of these answers are correct ,
	//  *            Note: if options has the string 'strip-answer-prefix' the prefix is removed. ,
    //  */
	getQuestionsByIds(qIds, options='') {
		debug(`getQuestionsById()`, 'Enter', `${qIds}`);
		let resultMsgs = [];
		if (!this.element) {
			resultMsgs.push("this.element is empty")
			return [[''], resultMsgs];
		}
		if (!Array.isArray(qIds)) {
			resultMsgs.push("input is not an array")
			return [[''], resultMsgs];
		}
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
						question.qid = q[qI].qid;
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
						resultMsgs[indx] = 'question found';
					}
				}
			}
		}
		for (let i=0; i<result.length; i++) {
		    if (!result[i]) {
				result[i] = {};
				let errMsg = `result is empty at index ${i}`
				resultMsgs[i] = errMsg;
				debug('getQuestionById()', 'Error', errMsg);
			}	
		}
		debug(`getQuestionsById()`, 'Exit', `${qIds}`);
		return [result, resultMsgs];
	}
}
