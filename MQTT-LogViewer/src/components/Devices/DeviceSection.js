import React, {useState, useEffect} from "react";
import styled from "styled-components";
import useApi from "../../hooks/useApi";
import AddDeviceForm from "./AddDeviceForm";

const DeviceSectionContainer = styled.div`
  width: 100%;
  display: flex;
  //flex-direction: column;
  //justify-content: center;
  //align-items: center;
`

const DeviceListContainer = styled.div`
  //width: 100%;
  display: flex;
  flex-direction: column;
  flex: 1 0;

  //justify-content: center;
  //align-items: center;
`
const ConfigContainer = styled.div`
  //width: 100%;
  display: flex;
  flex-direction: column;
  flex: 1 0;

  //justify-content: center;
  //align-items: center;
`
const DeviceContainer = styled.div`
  background-color: ${props=> props.selected ? 'grey' : undefined};
`

const Device = ({deviceData, selected, setSelected}) => {
    // const [isSelected, setIsSelected] = useState(false)

    return (
        <DeviceContainer selected={selected === deviceData.id} onClick={() => setSelected(deviceData.id)}>
            <p>{deviceData.display_name}</p>
        </DeviceContainer>
    )
}

const DeviceSection = () => {
    const [devices, setDevices] = useState([])
    const [selectedDevice, setSelectedDevice] = useState([])
    const [showForm, setShowForm] = useState(false)
    const hideAddDevice = () => setShowForm(false)
    const showAddDevice = () => setShowForm(true)
    const {fetchDevices} = useApi()
    useEffect(() => {
        fetchDevices().then(data=> {
            console.log(data)
            setDevices(data)
        })
    },[])

    return (
        <DeviceSectionContainer>
            <DeviceListContainer>
                <h3>Devices</h3>
                {devices.map(device => <Device key={device.id} deviceData={device}
                                               selected={selectedDevice} setSelected={setSelectedDevice}/>)}
            <div><button onClick={showAddDevice}>add device</button></div>
            </DeviceListContainer>
            {showForm && <AddDeviceForm hideForm={hideAddDevice}/>}
            <ConfigContainer>
                <div>WiFi</div>
                <div>MQTT</div>
                <div>FTP</div>
                <div>Sensors</div>
            </ConfigContainer>
        </DeviceSectionContainer>
    )
}

export default DeviceSection;