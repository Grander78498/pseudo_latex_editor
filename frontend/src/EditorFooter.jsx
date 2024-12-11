import Stack from 'react-bootstrap/Stack';

export default function EditorFooter() {
  return (
    <Stack direction="horizontal" gap={3} className='justify-content-center'>
      <div className="p-2">First item</div>
      <div className="p-2">Second item</div>
      <div className="p-2">Third item</div>
    </Stack>
  );
}