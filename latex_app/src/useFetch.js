import { useEffect, useState } from "react";


export default function useFetch(url) {
    const [response, setResponse] = useState(null);
    const [isPending, setPending] = useState(true);
    const [isError, setError] = useState(true);

    useEffect(() => {
        fetch(url)
        .then(async (resp) => {
            let json = await resp.json();
            setResponse(json);
            setPending(false);
            setError(false);
            return json;
        })
        .catch(e => {
            console.log(e);
            setError(true);
            setPending(false);
        })
    }, [url]);

    return [response, isPending, isError];
}