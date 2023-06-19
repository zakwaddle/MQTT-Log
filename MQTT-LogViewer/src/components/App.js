import React from "react";
import GlobalStyle from "../styles/GlobalStyles";
import styled from 'styled-components';
import LogSection from "./Logs";
import ControlSection from "./Controls/ControlSection";
import useSSE from "../hooks/useSSE";


const AppContainer = styled.div`
  height: 100%;
  width: 100%;
  font-family: monospace;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
`

export default function App() {
    useSSE();

    return (
        <AppContainer>
            <GlobalStyle/>
            <ControlSection/>
            <LogSection/>
        </AppContainer>
    );
};