import { MathJax } from "better-react-mathjax";
import Button from 'react-bootstrap/Button';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import useFetch from "./useFetch";
import Spinner from 'react-bootstrap/Spinner';
import env from './env.json';

export default function Buttons({handleButtonClick}) {
    let host = process.env.REACT_APP_API_HOST ? process.env.REACT_APP_API_HOST : env.API_HOST;
    let port = process.env.REACT_APP_API_PORT ? process.env.REACT_APP_API_PORT : env.API_PORT;
    const [buttons, isPending, isError] = useFetch(`http://${host}:${port}/api/expressions`);

    return (
        <div className="d-flex justify-content-center gap-1 mb-2">
            {isPending && <Spinner animation="border" role="status">
                            <span className="visually-hidden">Загрузка...</span>
                          </Spinner>
            }
            {!isPending && !isError && buttons.map((f, index) => {
                return <OverlayTrigger
                        placement="bottom"
                        overlay={<Tooltip id="button-tooltip-2" placement={"bottom"}>{f.name}</Tooltip>}
                        key={index}
                    >
                        {({ ref, ...triggerHandler }) => (
                        <Button
                            variant="light"
                            {...triggerHandler}
                            className="d-inline-flex align-items-center"
                            onClick={() => handleButtonClick(f.expr)}
                            ref={ref}
                            ke
                        >
                            <MathJax>
                                <span className="sm">{`$$${f.expr.replaceAll(/\{\}/g, "{?}")}$$`}</span>
                            </MathJax>
                            {/* <Image
                            ref={ref}
                            roundedCircle
                            src="holder.js/20x20?text=J&bg=28a745&fg=FFF"
                            />
                            <span className="ms-1">Hover to see</span> */}
                        </Button>
                        )}
                    </OverlayTrigger>
                return <Button variant="success" size="sm" onClick={() => handleButtonClick(f.expr)} key={index}>
                            <MathJax>
                                <span className="sm">{`$$${f.expr.replaceAll(/\{\}/g, "{?}")}$$`}</span>
                            </MathJax>
                        </Button>
            })}
        </div>
    )
}