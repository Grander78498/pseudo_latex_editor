import { useState } from "react";
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import env from './env.json';


export default function AddButton() {
    const [show, setShow] = useState(false);
    const [name, setName] = useState(null);
    const [expr, setExpr] = useState(null);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    
    const host = import.meta.env.VITE_API_HOST ? import.meta.env.VITE_API_HOST : env.API_HOST;
    const port = import.meta.env.VITE_API_PORT ? import.meta.env.VITE_API_PORT : env.API_PORT;
    const url = `http://${host}:${port}/api/post/expr`;
    const method = 'POST';

    const sendExpression = (e) => {
        e.preventDefault();
        const body = JSON.stringify({name, expr});
        fetch(url, {method, body, headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }})
        .then(async (resp) => {
                let json = await resp.json();
                console.log(json.msg);
                return json;
            })
        .catch(e => {
                console.log(e);
            });
        setShow(false);
    }
    
    return (
        <>
        <Button variant="primary" size="sm" onClick={handleShow}>
            Добавить кнопку
        </Button>

        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
            <Modal.Title>Добавить кнопку</Modal.Title>
            </Modal.Header>
            <Modal.Body>
            <Form encType="multipart/form-data" onSubmit={sendExpression} method="POST">
                <Form.Group controlId="form_expr_name" className="mb-3">
                    <Form.Label>Название кнопки</Form.Label>
                    <Form.Control type="text" onChange={(e) => setName(e.target.value)}/>
                </Form.Group>
                <Form.Group controlId="form_expression" className="mb-3">
                    <Form.Label>Выражение</Form.Label>
                    <Form.Control type="text" placeholder="Например, \\frac{}{}" onChange={(e) => setExpr(e.target.value)}/>
                </Form.Group>
                <Button variant="primary" type="submit">
                    Отправить
                </Button>
            </Form>
            </Modal.Body>
            <Modal.Footer>
            </Modal.Footer>
        </Modal>
        </>
    )
}