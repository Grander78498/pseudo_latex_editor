import { MathJax } from "better-react-mathjax";
import useFetch from "./useFetch";
import Spinner from 'react-bootstrap/Spinner';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import env from './env.json';
import OverlayButton from "./OverlayButton.jsx";
import OverlayDropdown from "./OverlayDropdown.jsx";
import Stack from "react-bootstrap/Stack";

export default function Buttons({handleButtonClick}) {
    const host = import.meta.env.VITE_API_HOST ? import.meta.env.VITE_API_HOST : env.API_HOST;
    const port = import.meta.env.VITE_API_PORT ? import.meta.env.VITE_API_PORT : env.API_PORT;
    const url = `http://${host}:${port}/api/expressions`;
    const method = 'GET';
    const [result, isPending, isError] = useFetch({url});
    const exprs = result ? result.expressions : null;
    const groups = result ? result.groups : null;

    return (
        <div className="justify-content-center gap-1 mb-2">
            {(isPending || isError) && <Spinner animation="border" role="status">
                            <span className="visually-hidden">Загрузка...</span>
                          </Spinner>
            }
            {!isPending && !isError && exprs.map((f, index) => {
                return <OverlayButton
                                        tip={f.name}
                                        handleButtonClick={() => handleButtonClick(f.expr)}
                                        key={index}
                                        buttonContent={<MathJax>
                                            <span className="sm">{`$$${f.expr.replaceAll(/\{\}/g, "{?}")}$$`}</span>
                                        </MathJax>}
                                    />
            })}
            {!isPending && !isError && <Stack direction="horizontal" className="justify-content-center">
                {groups.map((f, index) => {
                    return <OverlayDropdown buttons={f.expressions}
                                            handleButtonClick={handleButtonClick}
                                            key={index}
                                            title={<MathJax>
                                                <span className="sm">{`\\(${f.main_expr.replaceAll(/\{\}/g, "")}\\)`}</span>
                                            </MathJax>}
                            />
                })}
            </Stack>}
        </div>
    )
}