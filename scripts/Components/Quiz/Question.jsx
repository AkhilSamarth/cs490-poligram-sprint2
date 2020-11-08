import React from "react";

function Question(props) {
    
    const answerBlockStyle = {
        display: "inline-block",
        textAlign: "center",
        width: "7em",
        verticalAlign: "top",
        fontFamily: "verdana"
    };
    
    const questionTextStyle = {
        paddingBottom: "1em",
        fontFamily: "verdana",
        fontSize: "1.1em"
    };
    
    return (
        <div style={{textAlign: "center"}}>
            <div style={questionTextStyle}>
                {props.text}
            </div>
            <div>
                <div style={answerBlockStyle}>
                    <input type="radio" name={"quiz_answer_" + props.index} id="d3" value="d3" /><br />
                    <label for="d3">Strongly Disagree</label>
                </div>
                <div style={answerBlockStyle}>
                    <input type="radio" name={"quiz_answer_" + props.index} id="d2" value="d2" /><br />
                    <label for="d2">Disagree</label>
                </div>
                <div style={answerBlockStyle}>
                    <input type="radio" name={"quiz_answer_" + props.index} id="d1" value="d1" /><br />
                    <label for="d1">Somewhat Disagree</label>
                </div>
                <div style={answerBlockStyle}>
                    <input type="radio" name={"quiz_answer_" + props.index} id="a1" value="a1" /><br />
                    <label for="a1">Somewhat Agree</label>
                </div>
                <div style={answerBlockStyle}>
                    <input type="radio" name={"quiz_answer_" + props.index} id="a2" value="a2" /><br />
                    <label for="a2">Agree</label>
                </div>
                <div style={answerBlockStyle}>
                    <input type="radio" name={"quiz_answer_" + props.index} id="a3" value="a3" /><br />
                    <label for="a3">Strongly Agree</label>
                </div>
            </div>
        </div>
    );
}

export default Question;