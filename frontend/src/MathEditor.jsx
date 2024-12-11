import { MathJax } from "better-react-mathjax";
import { useState, useRef } from "react";
import Buttons from "./Buttons.jsx";
import EditorFooter from "./EditorFooter.jsx";
import Stack from "react-bootstrap/Stack";

const maxHistoryLength = 100;

const MathEditor = () => {
    const textareaRef = useRef(null);
    const [formula, setFormula] = useState("");
    const [history, setHistory] = useState([""]);
    const [currentPos, setCurrentPos] = useState(0);

    const changeFormula = (f) => {
        if (history) setHistory(old => {
            let res = old.concat(f.replaceAll(/\?/g, ""));
            if (res.length > maxHistoryLength) res.shift();
            setCurrentPos(res.length - 1);
            return res;
        });
        else setHistory([f]);
        setFormula(f);
    }

    const insertTextAtCursor = (text) => {
        const textarea = textareaRef.current;
        if (textarea) {
            const startPos = textarea.selectionStart;
            const endPos = textarea.selectionEnd;
            const currentText = textarea.value;
            
            const newText = currentText.substring(0, startPos) + text + currentText.substring(endPos, currentText.length);
            changeFormula(newText);

            textarea.value = newText;
            textarea.selectionStart = startPos + text.length - 1;
            textarea.selectionEnd = startPos + text.length - 1;
            textarea.focus();
        }
        };

    const handleButtonClick = (text) => {
        insertTextAtCursor(text);
    };

    const handleKeyEvent = (e) => {
        // console.log(e);
        if (e.ctrlKey && e.key.toLowerCase() === 'z') {
            e.preventDefault();
            if (e.shiftKey) {
                setCurrentPos(old => {
                    let val = Math.min(history.length - 1, old + 1);
                    setFormula(history[val]
                        .replaceAll(/\{\}/g, "{?}")
                    );
                    textareaRef.current.value = history[val];
                    return val;
                });
            }
            else {
                setCurrentPos(old => {
                    let val = Math.max(0, old - 1);
                    setFormula(history[val]
                        .replaceAll(/\{\}/g, "{?}")
                    );
                    textareaRef.current.value = history[val];
                    return val;
                });
            }
        }
    }

    return (
    <Stack gap={3}>
        <textarea
        ref={textareaRef}
        rows={10}
        cols={50}
        placeholder="Введите вашу формулу..."
        onChange={e => {
            changeFormula(e.target.value);
        }}
        onKeyDown={e => {
            handleKeyEvent(e)
        }}
        />
        <div>
        <Buttons handleButtonClick={handleButtonClick}/>
        </div>
        <MathJax dynamic>
            <span>{`$$${formula.replaceAll(/\{\}/g, "{?}")}$$`}</span>
        </MathJax>
        <EditorFooter />
    </Stack>
    );
};

export default MathEditor;
