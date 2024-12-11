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
            <Container>
                <Row>
            {buttons.map((button, index) => {
                return <Col key={index}>
                    <Dropdown.Item className='w-100'>
                    <OverlayButton  tip={button.name} 
                                    handleButtonClick={() => handleButtonClick(button.expr)}
                                    buttonContent={<MathJax>
                                    <span className="sm">{`\\(${button.expr.replaceAll(/\{\}/g, "{?}")}\\)`}</span>
                                    </MathJax>}/>
                    </Dropdown.Item>
                    </Col>
            })}
                </Row>
            </Container>
        </DropdownButton>
    )
}