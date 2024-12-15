import { MathJax } from "better-react-mathjax";
import { useState, useRef, useEffect, useCallback } from "react";
import Buttons from "./Buttons.jsx";
import UploadPhoto from "./UploadPhoto.jsx";
import Button from "react-bootstrap/Button";
import Stack from "react-bootstrap/Stack";
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import debounce from './utils.js';
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";

const maxHistoryLength = 100;

const MathEditor = ({showSave, textareaRef, index, upload}) => {
    if (!textareaRef) textareaRef = useRef(null);
    const [formula, setFormula] = useState("");
    const [history, setHistory] = useState([""]);
    const [_, setCurrentPos] = useState(0);
    
    let result;
    const getSelections = (text) => {
        if (result) return result;
        
        const stack = [];
        result = [];

        for (let i = 0; i < text.length; i++) {
            if (text[i] === '{') {
                stack.push(i);
            } else if (text[i] === '}') {
                if (stack.length > 0) {
                    const start = stack.pop() + 1;
                    const end = i;
                    result.push({ start, end });
                }
            }
        }
        
        result.sort((a, b) => a.end - b.end);
        result.push({start: text.length, end: text.length});
        result.unshift({start: 0, end: 0});
        return result;
    }

    const updateHistory = useCallback(debounce((f) => {
        if (history) setHistory(old => {
            let res = old.concat(f.replaceAll(/\?/g, ""));
            if (res.length > maxHistoryLength) res.shift();
            setCurrentPos(res.length - 1);
            return res;
        });
        else setHistory([f]);
    }, 500), []);

    const changeFormula = (f) => {
        updateHistory(f);
        setFormula(f);
    }

    const insertTextAtCursor = (text) => {
        const textarea = textareaRef.current;
        if (textarea) {
            const startPos = textarea.selectionStart;
            const endPos = textarea.selectionEnd;
            const currentText = textarea.value;
            
            const newText = currentText.substring(0, startPos) + text + currentText.substring(endPos, currentText.length);
            
            textarea.value = newText;
            textarea.selectionStart = startPos;
            textarea.selectionEnd = startPos + text.length;
            textarea.focus();
            setTimeout(() => {
                textarea.selectionStart = startPos;
                textarea.selectionEnd = startPos;
            }, 500);
            
            changeFormula(newText);
        }
        };

    const handleButtonClick = (text) => {
        insertTextAtCursor(text);
    };

    const undoRedo = (e) => {
        e.preventDefault();
        if (e.shiftKey) {
            setCurrentPos(old => {
                let val = Math.min(history.length - 1, old + 1);
                setFormula(history[val]);
                textareaRef.current.value = history[val];
                return val;
            });
        }
        else {
            setCurrentPos(old => {
                let val = Math.max(0, old - 1);
                setFormula(history[val]);
                textareaRef.current.value = history[val];
                return val;
            });
        }
    }

    const moveCursor = (e) => {
        e.preventDefault();
        const textarea = textareaRef.current;
        const selections = getSelections(textarea.value);
        if (textarea) {
            const startPos = textarea.selectionStart;
            const endPos = textarea.selectionEnd;
            let index;
            if (!e.shiftKey) {
                index = 0;
                while (index < selections.length && selections[index].end <= endPos) index++;
                if (index >= selections.length) index = selections.length - 1;
            }
            else {
                index = selections.length - 1;
                while (index >= 0 && selections[index].end >= endPos) index--;
                if (index < 0) index = 0;
            }
            textarea.selectionStart = selections[index].start;
            textarea.selectionEnd = selections[index].end;
            textarea.focus();
        }
    }

    const handleKeyEvent = (e) => {
        //console.log(e);
        if (e.ctrlKey && e.key.toLowerCase() === 'z') {
            undoRedo(e);
        }
        else if (e.key.toLowerCase() === 'tab') {
            moveCursor(e);
        }
    }

    return (
        <Form as={Stack} gap={1} className="w-75 mx-auto justify-content-center"
              style={{maxWidth: showSave ? "100%" : "75%"}}>
        <Form.Group className="mb-3">
          <Form.Label>
            <Container direction="horizontal" className="d-flex jusitfy-content-between">
                <Row>
                    <Col>Формула{index ? " " + index: ""}</Col>
                    <Col>{upload && <UploadPhoto setFormula={insertTextAtCursor}/>}</Col>
                </Row>
            </Container>
            </Form.Label>
          <Form.Control
            as={"textarea"}
            ref={textareaRef}
            rows={upload ? 3: 5}
            cols={showSave ? 50 : 30} // Уменьшаем ширину в зависимости от showSave
            placeholder="Введите вашу формулу..."
            className={showSave ? "" : "col-md-6"} // Уменьшаем ширину в зависимости от showSave
            onChange={(e) => {
              changeFormula(e.target.value);
            }}
            onKeyDown={(e) => {
              handleKeyEvent(e);
            }}
            style={{ maxWidth: showSave ? "100%" : "100%" }} // Уменьшаем максимальную ширину
          />
        </Form.Group>
      
        <Buttons handleButtonClick={handleButtonClick} />
      
        <MathJax dynamic>
          <span>{`$$${formula.replaceAll(/\{\}/g, "{?}")}$$`}</span>
        </MathJax>
      
        {showSave && (
          <>
            <Form.Group as={Row} className="d-flex flex-column align-items-center">
              <Form.Label>Название формулы</Form.Label>
              <Form.Control className={showSave ? "w-50" : "w-25"} /> {/* Уменьшаем ширину в зависимости от showSave */}
            </Form.Group>
            <Stack direction="horizontal" gap={3} className="justify-content-center">
              <Button variant="primary" size="sm">
                Сохранить
              </Button>
              <Button variant="danger" size="sm">
                Сбросить
              </Button>
            </Stack>
          </>
        )}
      </Form>
    );
};

export default MathEditor;
