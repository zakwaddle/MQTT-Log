import React, {useState} from "react";
import useLogEntries from "../hooks/useLogEntries";
import LogEntryList from "./Logs/LogEntryList";
import LogHeader from "./Logs/LogHeader";
import GlobalStyle from "../styles/GlobalStyles";
import styled from 'styled-components';
import DeviceSection from "./Devices/DeviceSection";


const AppContainer = styled.div`
  width: 100%;
  font-family: monospace;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`
const LogSection = styled.div`
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`

export default function App() {
    const [unitId, setUnitId] = useState('');
    const [type, setType] = useState('');
    const {entries, handleDelete, shouldScroll} = useLogEntries();

    const handleUnitIdChange = (event) => setUnitId(event.target.value)
    const handleTypeChange = (event) => setType(event.target.value)


    const unitIds = [...new Set(entries.map(entry => entry['log']['unit_id']))];
    const types = [...new Set(entries.map(entry => entry['log']['type']))];
    const filteredLogEntries = entries.filter(entry =>
        (unitId === '' || entry['log']["unit_id"] === unitId) &&
        (type === '' || entry['log']["type"] === type));


    return (
        <AppContainer>
            <GlobalStyle/>
            <DeviceSection/>
            <LogSection>
                <LogHeader logTypes={types}
                           unitIds={unitIds}
                           handleIdFilter={handleUnitIdChange}
                           handleTypeFilter={handleTypeChange}/>
                <LogEntryList entries={filteredLogEntries}
                              onDelete={handleDelete}
                              shouldScroll={shouldScroll}/>
            </LogSection>
        </AppContainer>
    )
}