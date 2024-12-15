import { useState } from "react";
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import env from './env.json';


export default function UploadPhoto({setFormula}) {
    const [show, setShow] = useState(false);
    const [file, setFile] = useState(null);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
          setFile(selectedFile);
        }
    };
    
    const host = import.meta.env.VITE_API_HOST ? import.meta.env.VITE_API_HOST : env.API_HOST;
    const port = import.meta.env.VITE_API_PORT ? import.meta.env.VITE_API_PORT : env.API_PORT;
    const url = `http://${host}:${port}/api/upload_photo`;
    const method = 'POST';

    const sendPhoto = (e) => {
        e.preventDefault();
        const data = new FormData();
        data.append('file', file);
        fetch(url, {method, body: data, headers: {
            'Accept': 'application/json'
            }})
        .then(async (resp) => {
                let json = await resp.json();
                setFormula(json.result);
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
            Загрузить фото
        </Button>

        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
            <Modal.Title>Загрузка</Modal.Title>
            </Modal.Header>
            <Modal.Body>
            <Form encType="multipart/form-data" onSubmit={sendPhoto} method="POST">
                <Form.Group controlId="formFile" className="mb-3">
                    <Form.Label>Фотография формулы</Form.Label>
                    <Form.Control type="file" onChange={handleFileChange}/>
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