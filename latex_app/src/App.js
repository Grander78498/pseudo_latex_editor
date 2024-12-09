import './App.css';
import MathEditor from './MathEditor'; 
import { MathJaxContext } from 'better-react-mathjax';

function App() {
  return (
    <MathJaxContext>   
      <div className="App">
        <p>Формула</p>
        <MathEditor />
      </div>
    </MathJaxContext>
  );
}

export default App;
