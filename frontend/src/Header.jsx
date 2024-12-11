import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

export default function Header() {
  return (
    <Navbar expand="lg" className="justify-content-center">
      <Container>
        <Nav variant="underline" 
             className="justify-content-center"
             defaultActiveKey={window.location.pathname != "/" ? window.location.pathname : "/editor"}>
            <Row>
                <Col className='bg-primary-subtle'><Nav.Link href="/editor">Редактор</Nav.Link></Col>
                <Col className='bg-primary-subtle'><Nav.Link href="/analyser">Анализатор</Nav.Link></Col>
            </Row>
        </Nav>
      </Container>
    </Navbar>
  );
}