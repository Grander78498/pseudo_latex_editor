import Stack from 'react-bootstrap/Stack';
import Button from 'react-bootstrap/Button';
import { useRef } from 'react';

export default function EditorFooter({formulaRef}) {
  const nameInputRef = useRef(null);

  const sendData = () => {

  }

  return (
    <>
    <input ref={nameInputRef}></input>
    <Stack direction="horizontal" gap={3} className='justify-content-center'>
        <Button variant='primary' onClick={() => sendData()}>Сохранить</Button>
        <Button variant='danger'>Сбросить</Button>
    </Stack>
    </>
  );
}