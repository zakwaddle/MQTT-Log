import React, {useState} from "react";
import styled from "styled-components";
import {useSelector} from "react-redux";
import {Button, InfoBox} from "../../styles/SectionStyles";
import {PropStack} from "../UI/Property";

const Row = styled.div`
  width: available;
  display: flex;
  justify-content: space-around;
`
const DeviceSensors = ({setView, device}) => {
    const deviceSensors = device['sensors']
    if (!deviceSensors) {
        return (
            <Button onClick={() => setView('addSensor')}>Add Sensor</Button>
        )
    }
    return (
        <Row>
            poo
        </Row>
    )
}
const SectionContainer = styled.div`
  display: flex;
  flex-direction: column;
  padding: .5em;
`

const DeviceDetailsContainer = styled.div`
  width: 40%;
  height: available;
  background-color: white;
  display: flex;
  flex-direction: column;
  //justify-content: space-evenly;
  padding: 1em;

  border-style: solid;
  border-radius: 1em;
  border-width: 1px;
  border-color: darkgrey
`
const DeviceDetails = () => {
    const [view, setView] = useState('main')
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const menuSelection = useSelector(state => state['globalState']['menuSelection'])
    const isVisable = menuSelection === 'Devices'
    if (!selectedDevice || !isVisable) {
        return <InfoBox/>
    }

    const config = selectedDevice.config
    const wifi = config['wifi_network']
    const ftp = config['ftp_server']
    const mqtt = config['mqtt_broker']

    if (view === 'main') {
        return (
            <DeviceDetailsContainer>

                <SectionContainer>
                    <h4>Device Details:</h4>
                    <Row>
                        <PropStack label={"Name"}>{selectedDevice['display_name']}</PropStack>
                        <PropStack label={"DeviceID"}>{config['device_id']}</PropStack>
                        <PropStack label={"ConfigID"}>{config.id}</PropStack>
                    </Row>
                </SectionContainer>

                <SectionContainer>
                    <h4>Connections:</h4>
                    <Row>
                        <PropStack label={"Wifi"}>{wifi && wifi.ssid}</PropStack>
                        <PropStack label={"MQTT"}>{mqtt && mqtt.host_address}</PropStack>
                        <PropStack label={"FTP"}>{ftp && ftp.host_address}</PropStack>
                    </Row>
                </SectionContainer>

                <SectionContainer>
                    <h4>Sensors:</h4>
                    <DeviceSensors setView={setView} device={selectedDevice}/>
                </SectionContainer>

            </DeviceDetailsContainer>
        )
    }
    if (view === 'addSensor') {
        return (
            <DeviceDetailsContainer>
                <Button onClick={() => setView('main')}>Motion Sensor</Button>
                <Button onClick={() => setView('main')}>Weather Sensor</Button>
                <Button onClick={() => setView('main')}>Dimmable LED</Button>
                <Button onClick={() => setView('main')}>Cancel</Button>
            </DeviceDetailsContainer>
        )
    }
}

export default DeviceDetails;