import useFetch from "./useFetch";
import Spinner from 'react-bootstrap/Spinner';
import env from './env.json';
import Stack from "react-bootstrap/Stack";
import FormulaItem from "./FormulaItem.jsx";

export default function Formulas() {
    const host = import.meta.env.VITE_API_HOST ? import.meta.env.VITE_API_HOST : env.API_HOST;
    const port = import.meta.env.VITE_API_PORT ? import.meta.env.VITE_API_PORT : env.API_PORT;
    const url = `http://${host}:${port}/api/formulas`;
    const [result, isPending, isError] = useFetch({url});
    const formulas = result ? result.formulas : null;

    return (
        <div className="justify-content-center gap-1 mb-2">
            {(isPending || isError) && <Spinner animation="border" role="status">
                            <span className="visually-hidden">Загрузка...</span>
                          </Spinner>
            }
            <Stack gap={1}>
            {!isPending && !isError && formulas.map((f, index) => {
                return (
                    <FormulaItem name={f.name} formula={f.formula} key={index} />
                )
            })}

            </Stack>
        </div>
    )
}