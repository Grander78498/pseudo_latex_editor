import { MathJax } from "better-react-mathjax";
import Button from 'react-bootstrap/Button';
import useFetch from "./useFetch";
import Spinner from 'react-bootstrap/Spinner';
import env from './env.json';

export default function Buttons({handleButtonClick}) {
    console.log(`http://${env.API_HOST}:${env.API_PORT}/api/expressions`);
    const [buttons, isPending, isError] = useFetch(`http://${env.API_HOST}:${env.API_PORT}/api/expressions`);

    return (
        <div className="d-flex justify-content-center gap-1 mb-2">
            {isPending && <Spinner animation="border" role="status">
                            <span className="visually-hidden">Загрузка...</span>
                          </Spinner>
            }
            {!isPending && !isError && buttons.map((f, index) => {
                return <Button variant="success" size="sm" onClick={() => handleButtonClick(f.expr)} key={index}>
                            <MathJax>
                                <span className="sm">{`$$${f.expr.replaceAll(/\{\}/g, "{?}")}$$`}</span>
                            </MathJax>
                        </Button>
            })}
        </div>
    )
}