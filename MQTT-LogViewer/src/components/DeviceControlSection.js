import React, {useState} from "react";
// import useApi from "../hooks/useApi"
import {useDispatch, useSelector} from "react-redux";
// import styled from "styled-components";
import {globalStateActions} from "../store/globalStateSlice";
import useDeviceConfigs from "../hooks/useDeviceConfigs";
import {DeviceList, NewDeviceList} from "./Devices/DeviceList";
import {Button, InfoBox, MenuBox} from "../styles/SectionStyles";
import ConnectionSection from "./Connections";
import DeviceDetails from "./Devices/DeviceDetails";
import styled from "styled-components";

const MenuItem = ({children}) => {
    const dispatch = useDispatch()
    const handleSelection = () => {
        dispatch(globalStateActions.updateMenuSelection(children))
    }
    return (
        <Button onClick={handleSelection}>
            {children}
        </Button>
    )
}

// const Wrapper = ({children}) => {
//     return (
//         {...children}
//     )
// }
const Devices = () => {
    const devices = useSelector(state => state['globalState']['devices'])
    const newDevices = useSelector(state => state['globalState']['newDevices'])
    return (
        <InfoBox>
            <DeviceList devices={devices}/>
            <NewDeviceList newDevices={newDevices}/>
        </InfoBox>
    )
}

export const ControlSectionBox = styled.div`
  width: 100%;
  height: 20em;
  display: flex;
  justify-content: space-around;
  margin: 1em 1em 0 1em;
  //padding: .5em;
`

const DeviceControlSection = () => {
    useDeviceConfigs()

    const menuSelection = useSelector(state => state['globalState']['menuSelection'])

    const infoSection = {
        "Devices": <Devices/>,
        "Connections": <ConnectionSection/>
    }

    return (
        <ControlSectionBox>
            <MenuBox>
                <MenuItem>Devices</MenuItem>
                <MenuItem>Connections</MenuItem>
            </MenuBox>
            {infoSection[menuSelection]}
            <DeviceDetails/>
        </ControlSectionBox>
    )

}

export default DeviceControlSection;