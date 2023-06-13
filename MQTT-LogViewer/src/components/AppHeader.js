import React from "react";
import useApi from "../hooks/useApi";
import styled from 'styled-components';

const AppHeaderContainer = styled.header`
  position: fixed;
  top: 0;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  background-color: whitesmoke;
  
  @media (max-width: 700px) {
    flex-direction: column;
  } 
`
// const HeaderTitle = styled.div

const AppHeader = ({handleIdFilter, unitIds, handleTypeFilter, logTypes}) => {
    const {checkIn} = useApi()
    const handleCheckIn = () => {
        checkIn().then(data => console.log(data))
    }
    return (
        <AppHeaderContainer>
            <div>
                <h1>Log Entries</h1>
            </div>
            <div>
                <select onChange={handleIdFilter}>
                    <option value="">All</option>
                    {unitIds.map(id => (
                        <option key={id} value={id}>{id}</option>
                    ))}
                </select>
                <select onChange={handleTypeFilter}>
                    <option value="">All</option>
                    {logTypes.map(t => (
                        <option key={t} value={t}>{t}</option>
                    ))}
                </select>
                <button onClick={handleCheckIn}>check in</button>
            </div>
        </AppHeaderContainer>
    )
}


export default AppHeader;