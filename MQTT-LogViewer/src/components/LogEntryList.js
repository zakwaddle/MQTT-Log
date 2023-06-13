import React from "react";
import LogEntry from "./LogEntry";
import styled from 'styled-components';

const LogListContainer = styled.div`
  margin-top: 4em;
  width: 100%;
  overflow: hidden;
`

const LogEntryList = ({entries, onDelete, shouldScroll}) => {

    const logListRef = React.useRef(null);

    React.useEffect(() => {

        if (shouldScroll) {
            logListRef.current.scrollIntoView(false);
        }
    }, [entries]);


    return (
        <LogListContainer ref={logListRef}>
            {entries.map(entry => (
                <LogEntry key={entry.id} entry={entry} onDelete={onDelete}/>
            ))}
        </LogListContainer>
    );
};

export default LogEntryList;
