import React, {useEffect} from "react";
import GlobalStyle from "../styles/GlobalStyles";
import styled from 'styled-components';
// import DeviceSection from "./Devices/DeviceSection";
import Logs from "./Logs";
import useApi from "../hooks/useApi";
import {useDispatch, useSelector} from "react-redux";
import {globalStateActions} from "../store/globalStateSlice";
import useSSE from "../hooks/useSSE";
import useLogEntries from "../hooks/useLogEntries";
// import NewDeviceBanner from "./Devices/NewDeviceBanner";
import DeviceControlSection from "./DeviceControlSection";


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
    useLogEntries();

    const dispatch = useDispatch();
    const {fetchDevices} = useApi();
    // const numNew = useSelector(state => state['globalState']['newDevices']).length

    useEffect(() => {
        fetchDevices().then(data => {
            const newDevices = data.filter(device => device.display_name === null)
            const devices = data.filter(device => device.display_name !== null)
            dispatch(globalStateActions.updateDevices(devices));
            dispatch(globalStateActions.updateNewDevices(newDevices));
        });
    }, []);


    return (
        <AppContainer>
            <GlobalStyle/>
            {/*{numNew > 0 &&*/}
            {/*    <NewDeviceBanner/>*/}
            {/*}*/}
            {/*<DeviceSection/>*/}
            <DeviceControlSection/>
            <Logs/>
        </AppContainer>
    );
};