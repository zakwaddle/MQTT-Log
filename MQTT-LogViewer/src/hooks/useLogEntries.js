import React from "react";
const config = require('../../zrc')

// export default function useLogEntries(base_url){
export default function useLogEntries(){
    const [entries, setEntries] = React.useState([]);
    const [shouldScroll, setShouldScroll] = React.useState(true)

    const handleDelete = (id) => {
        setShouldScroll(false)
        setEntries(entries.filter(entry => entry.id !== id))
    }


    React.useEffect(() => {
        const url = `${config.apiHost}/logs`
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
        const url = `${config.apiHost}/stream`
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