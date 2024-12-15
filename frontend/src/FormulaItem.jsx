import Card from 'react-bootstrap/Card';
import { MathJax } from "better-react-mathjax";

export default function FormulaItem({name, formula}) {
    return (
        <Card style={{ width: '100%' }}>
          <Card.Body>
            <Card.Title>{name}</Card.Title>
            <Card.Text>
              <MathJax dynamic>
                <span>{`$$${formula.replaceAll(/\{\}/g, "{?}")}$$`}</span>
              </MathJax>
            </Card.Text>
          </Card.Body>
        </Card>
      );
}