import React, {useState} from "react";
import styled from "styled-components";
import useApi from "../../../../hooks/useApi";
import {useDispatch, useSelector} from "react-redux";
import {globalStateActions} from "../../../../store/globalStateSlice";
import {PropStack} from "../../../UI/Property";

const DeviceSectionContainer = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 1em;
  margin: 1em;
`

const DeviceListContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 8em;
  width: 100%;
  //border-radius: 0 0 1em 1em;
`

const DeviceContainer = styled.div`
  background-color: ${props => props['selected'] ? 'grey' : undefined};
  display: flex;
  justify-content: space-evenly;
  border: 1px solid black;
  border-radius: 1em;
  padding: .25em;
  margin: .25em;
  align-items: center;
  cursor: pointer;
`
const Button = styled.button`
  font-family: monospace;
  font-size: inherit;
  background-color: inherit;
  border-radius: .3em;
  border-width: 1px;
`

const Device = ({deviceData}) => {
    const dispatch = useDispatch()
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const isSelected = selectedDevice === deviceData
    const handleClick = () => {
        if (isSelected){
            dispatch(globalStateActions.updateSelectedDevice(null))
        } else {
            dispatch(globalStateActions.updateSelectedDevice(deviceData))

        }
    }
    const platform = (deviceData.platform === 'rp2' ? 'PicoW' : 'ESP32')
    return (
        <DeviceContainer selected={isSelected}
                         onClick={handleClick}>
            <PropStack label={'Name'}>{deviceData.display_name}</PropStack>
            <p><b>{platform}</b></p>
        </DeviceContainer>
    )
}
export const DeviceList = ({devices, selectedDevice, setSelectedDevice}) => {
    return (
        <DeviceListContainer>
            {devices.map(device => <Device key={device.id}
                                           deviceData={device}
                                           selected={selectedDevice}
                                           setSelected={setSelectedDevice}/>)}
        </DeviceListContainer>
    )
}
const NewDevice = ({deviceData, setSetupDevice, setShowSetup}) => {
    const handleClick = () => {
        setSetupDevice(deviceData)
        setShowSetup(true)
    }
    return (
        <DeviceContainer>
            <p>{deviceData.id}</p>
            <p>{deviceData.platform}</p>
            <Button onClick={handleClick}>Setup Device</Button>
        </DeviceContainer>
    )
}
export const NewDeviceList = ({newDevices, setSetupDevice, setShowSetup}) => {

    return (
        <DeviceListContainer>
            {newDevices.map(device => <NewDevice key={device.id}
                                                 deviceData={device}
                                                 setShowSetup={setShowSetup}
                                                 setSetupDevice={setSetupDevice}/>)}
        </DeviceListContainer>
    )
}
const DeviceSetupBox = styled.div`
  width: 95%;
  display: flex;
  flex-direction: column;
`
const DeviceSetupRow = styled.div`
  width: 95%;
  display: flex;
  justify-content: space-evenly;
`
export const DeviceSetup = ({device, setShowSetup}) => {
    const [newName, setNewName] = useState("")

    const {updateDeviceName} = useApi()

    const handleCancel = () => setShowSetup(false)
    const handleSetup = () => {
        updateDeviceName(device.id, newName).then(setShowSetup(false))
    }
    return (
        <DeviceSetupBox>
            <DeviceSetupRow>
                {device.platform}
                {device.id}
            </DeviceSetupRow>
            <DeviceSetupRow>
                Display Name
                <input value={newName} onChange={event => setNewName(event.target.value)}/>
            </DeviceSetupRow>
            <DeviceSetupRow>
                <Button onClick={handleCancel}>Cancel</Button>
                <Button onClick={handleSetup}>Save</Button>
            </DeviceSetupRow>
        </DeviceSetupBox>
    )
}

