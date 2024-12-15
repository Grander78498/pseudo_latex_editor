import './App.css';
import MathEditor from './MathEditor.jsx';
import Header from './Header.jsx';
import { MathJaxContext } from 'better-react-mathjax';
import { Route, Routes } from 'react-router';
import MathAnalyser from './MathAnalyser.jsx';
import Stack from 'react-bootstrap/Stack';

function App() {
  return (
    <MathJaxContext>   
      <div className="App">
        <Stack gap={3} className='justify-content-center'>
          <Header />
          <Routes>
            <Route index element={<MathEditor showSave={true}/>}/>
            <Route path='/editor' element={<MathEditor showSave={true}/>}/>
            <Route path='/analyser' element={<MathAnalyser/>}/>
          </Routes>
        </Stack>
      </div>
    </MathJaxContext>
  );
}

export default App;
