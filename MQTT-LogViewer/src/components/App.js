import React, {useEffect, useState} from "react";
import useLogEntries from "../hooks/useLogEntries";
import LogEntryList from "./LogEntryList";
import AppHeader from "./AppHeader";
import GlobalStyle from "../styles/GlobalStyles";
import styled from 'styled-components';

const AppContainer = styled.div`
  width: 100%;
  font-family: monospace;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`

// const BASE_URL = `http://localhost:5000/api/home`
const BASE_URL = `http://yawntsum.local/api/home`


export default function App() {
    const [unitId, setUnitId] = useState('');
    const [type, setType] = useState('');
    const { entries, handleDelete, shouldScroll } = useLogEntries(BASE_URL);

    const handleUnitIdChange = (event) => setUnitId(event.target.value)
    const handleTypeChange = (event) => setType(event.target.value)


    const unitIds = [...new Set(entries.map(entry => entry['log']['unit_id']))];
    const types = [...new Set(entries.map(entry => entry['log']['type']))];
    const filteredLogEntries = entries.filter(entry =>
        (unitId === '' || entry['log']["unit_id"] === unitId) &&
        (type === '' || entry['log']["type"] === type));

    useEffect(() => {
        console.log(window.outerWidth)
    }, [window.outerWidth])

    return (
        <AppContainer>
            <GlobalStyle/>
            <AppHeader logTypes={types}
                       unitIds={unitIds}
                       handleIdFilter={handleUnitIdChange}
                       handleTypeFilter={handleTypeChange}/>
            <LogEntryList entries={filteredLogEntries}
                          onDelete={handleDelete}
                          shouldScroll={shouldScroll}/>
        </AppContainer>
    )
}