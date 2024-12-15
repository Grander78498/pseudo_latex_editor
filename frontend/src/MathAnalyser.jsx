import Stack from "react-bootstrap/Stack";
import Button from 'react-bootstrap/Button';
import MathEditor from "./MathEditor.jsx";
import { useState, useRef } from "react";
import useFetch from "./useFetch.jsx";
import env from './env.json';
import { MathJax } from "better-react-mathjax";

export default function MathAnalyser() {
    const firstRef = useRef(null);
    const secondRef = useRef(null);
    const [analyseResult, setResult] = useState(null);
    const [score, setScore] = useState(null);
    const host = import.meta.env.VITE_API_HOST ? import.meta.env.VITE_API_HOST : env.API_HOST;
    const port = import.meta.env.VITE_API_PORT ? import.meta.env.VITE_API_PORT : env.API_PORT;
    const url = `http://${host}:${port}/api/analyse`;
    const method = 'POST';

    const sendData = () => {
        let body = {'first_formula': firstRef.current.value,
                        'second_formula': secondRef.current.value
        }
        body = JSON.stringify(body);
        fetch(url, {method, body, headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }})
        .then(async (resp) => {
            let json = await resp.json();
            setResult(json.diff);
            setScore(json.score);
            return json;
        })
        .catch(e => {
            console.log(e);
        });
    }

    return (
        <>
        <Stack direction="horizontal" gap={3}>
            <MathEditor index={1} showSave={false} textareaRef={firstRef}/>
            <MathEditor index={2} showSave={false} textareaRef={secondRef} upload={true}/>
        </Stack>
        <Button onClick={() => sendData()}>Сравнить</Button>
        <div>
            <h3>Результат:</h3>
            {analyseResult && <MathJax dynamic>
                <span>{`$$${analyseResult.replaceAll(/\{\}/g, "{?}")}$$`}</span>
                </MathJax>}
            <p><strong>Процент совпадения:</strong> {score}%</p>
        </div>
        </>
    )
}