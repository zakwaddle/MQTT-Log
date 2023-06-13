import React from "react";

export default function useLogEntries(base_url){
    const [entries, setEntries] = React.useState([]);
    const [shouldScroll, setShouldScroll] = React.useState(true)

    const handleDelete = (id) => {
        setShouldScroll(false)
        setEntries(entries.filter(entry => entry.id !== id))
    }


    React.useEffect(() => {
        const url = `${base_url}/logs`
        fetch(url)
            .then(response => response.json())
            .then(data => {
                setEntries(data)
                console.log(`API: ${url}`)
                console.log(data)
            })
            .catch(error => console.error(error));
    }, []);

    React.useEffect(() => {
        const url = `${base_url}/stream`
        console.log(`SSE Stream: ${url}`)
        const eventSource = new EventSource(url);

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            // console.log(data);
            data.log && setShouldScroll(true)
            data.log && setEntries(oldEntries => [...oldEntries, data.log]);
            // const shouldAutoScroll = (Date.now() - lastScroll) >= 15000;
        };

        return () => {
            eventSource.close();
        };
    }, []);

    return { entries, handleDelete, shouldScroll };
}