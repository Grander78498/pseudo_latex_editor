import { useEffect, useState } from "react";


export default function useFetch({url, method, body}) {
    const [response, setResponse] = useState(null);
    const [isPending, setPending] = useState(true);
    const [isError, setError] = useState(true);

    useEffect(() => {
        let interval = setInterval(() => {
            fetch(url, {method, body})
            .then(async (resp) => {
                let json = await resp.json();
                setResponse(json);
                setPending(false);
                setError(false);
                clearInterval(interval);
                return json;
            })
            .catch(e => {
                console.log(e);
                setError(true);
                setPending(false);
            })
        },
        1000
        );
    }, [url]);

    return [response, isPending, isError];
}