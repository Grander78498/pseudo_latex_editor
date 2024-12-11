import Stack from "react-bootstrap/Stack";
import MathEditor from "./MathEditor.jsx";

export default function MathAnalyser() {
    return (
        <Stack direction="horizontal" gap={5}>
            <MathEditor/>
            <MathEditor/>
        </Stack>
    )
}