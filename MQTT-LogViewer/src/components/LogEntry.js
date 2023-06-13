import React from "react";
import styled from 'styled-components';
import useApi from "../hooks/useApi";

const LogContainer = styled.div`
  display: flex;
  justify-content: space-between;
  @media (max-width: 900px){
    margin-bottom: .5em;
  }
`
const LogId = styled.div`
  
  flex: 4 1;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  
  @media (max-width: 900px){
    flex-direction: column;
    flex: 3 1;
  }
  @media screen and (max-width: 700px){
    flex-direction: column;
    flex: 4 1;
  }
  @media screen and (max-width: 428px){
    flex-direction: column;
    flex: 4 1;
  }
`
const UnitId = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
`
const LogInfo = styled.div`
  margin-right: 1em;
`
const LogType = styled.div`
  flex: 1 1;
  justify-content: flex-end;
`
const LogMessage = styled.div`
  flex: 3 0;
  justify-content: flex-start;

  @media (max-width: 900px){
    flex: 4 0;
  }
  @media (max-width: 429px){
    flex: 4 0;
  }
`

const LogEntry = ({entry, onDelete}) => {
    const {time, log} = entry
    const {deleteLogEntry} = useApi()

    const handleDelete = () => {
        deleteLogEntry(entry.id)
            .then(()=> onDelete(entry.id))
    }

    return (
        <LogContainer>
            <LogId>
                <LogInfo>{time}</LogInfo>
                <UnitId>
                    <LogInfo><b>{log.unit_id}</b></LogInfo>
                    <LogInfo>{log.display_name}</LogInfo>
                </UnitId>
            </LogId>
            <LogMessage>{log && log.message}</LogMessage>
            <LogType>{log && log.type}</LogType>
            <button onClick={handleDelete}>Delete</button>
        </LogContainer>

    );
};

export default LogEntry;
