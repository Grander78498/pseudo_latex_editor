import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import { MathJax } from 'better-react-mathjax';
import OverlayButton from './OverlayButton.jsx';


export default function OverlayDropdown({buttons, handleButtonClick, title}) {

    return (
        <DropdownButton title={title}>
            <Dropdown.Item className='w-auto'>
            <Container className="p-0">
                <Row className='g-0'>
            {buttons.map((button, index) => {
                if (index % 2 == 0)
                    return <Col key={index} className="d-flex justify-content-center align-items-center">
                        <OverlayButton  tip={button.name} 
                                        handleButtonClick={() => handleButtonClick(button.expr)}
                                        buttonContent={<MathJax>
                                        <span className="sm">{`\\(${button.expr.replaceAll(/\{\}/g, "{?}")}\\)`}</span>
                                        </MathJax>}/>
                        </Col>
            })}
                </Row>
                <Row className='g-0'>
            {buttons.map((button, index) => {
                if (index % 2 == 1)
                    return <Col key={index} className="d-flex justify-content-center align-items-center">
                        <OverlayButton  tip={button.name} 
                                        handleButtonClick={() => handleButtonClick(button.expr)}
                                        buttonContent={<MathJax>
                                        <span className="sm">{`\\(${button.expr.replaceAll(/\{\}/g, "{?}")}\\)`}</span>
                                        </MathJax>}/>
                        </Col>
            })}
                </Row>
            </Container>
            </Dropdown.Item>
        </DropdownButton>
    )
}