import React, {useState, useEffect} from "react";
import styled from "styled-components";
import useApi from "../../hooks/useApi";
import AddDeviceForm from "./AddDeviceForm";
import DeviceConfigs from "../Configs/DeviceConfigs";
import {useSelector} from "react-redux";

const DeviceSectionContainer = styled.div`
  width: 100%;
  display: flex;
 
`

const DeviceListContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 8em;
  width: 48%;
  padding: .5em;
  margin: .5em;
  background-color: white;
  border-radius: 1em;
`
const ConfigContainer = styled.div`
  display: flex;
  flex-direction: column;
  flex: 2 1;
`
const DeviceContainer = styled.div`
  background-color: ${props=> props['selected'] ? 'grey' : undefined};
`
const Button = styled.button`
  font-family: monospace;
  font-size: inherit;
  background-color: inherit;
  border-radius: .3em;
  border-width: 1px;
`
const Device = ({deviceData, selected, setSelected}) => {

    return (
        <DeviceContainer selected={selected === deviceData.id} onClick={() => setSelected(deviceData.id)}>
            <p>{deviceData.display_name}</p>
        </DeviceContainer>
    )
}

const DeviceSection = () => {
    const [selectedDevice, setSelectedDevice] = useState([])
    // const [showForm, setShowForm] = useState(false)
    // const hideAddDevice = () => setShowForm(false)
    // const showAddDevice = () => setShowForm(true)
    const devices = useSelector(state => state['globalState'].devices)

    return (
        <DeviceSectionContainer>
            <DeviceListContainer>
                <h3>Devices</h3>
                {devices.map(device => <Device key={device.id} deviceData={device}
                                               selected={selectedDevice} setSelected={setSelectedDevice}/>)}
            {/*<Button onClick={showAddDevice}>add device</Button>*/}
            </DeviceListContainer>
            {/*{showForm && <AddDeviceForm hideForm={hideAddDevice}/>}*/}
            <DeviceConfigs/>
        </DeviceSectionContainer>
    )
}

export default DeviceSection;