import React, {useState} from "react";
import styled from "styled-components";
import {useDispatch, useSelector} from "react-redux";
import {Button} from "../../../../styles/SectionStyles";
import {PropStack} from "../../../UI/Property";
import {globalStateActions} from "../../../../store/globalStateSlice";
import SensorCard from "./SensorCard";
import useApi from "../../../../hooks/useApi";

const Row = styled.div`
  width: available;
  display: flex;
  justify-content: space-around;
`

const SensorSection = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
`
const SensorRow = styled.div`
  width: 100%;
  display: flex;
  margin: .5em;

`

const SectionContainer = styled.div`
  display: flex;
  flex-direction: column;
  padding: .5em;
`

const DeviceDetailsContainer = styled.div`
  width: 50%;
  height: available;

  display: flex;
  flex-direction: column;

  background-color: white;
  padding: 1em;

  border-style: solid;
  border-radius: 1em;
  border-width: 1px;
  border-color: darkgrey
`

const Wrapper = ({children}) => {
    return [...children]
}

const DeviceDetailsView = () => {
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const config = selectedDevice.config
    const deviceSettings = config["device_settings"]
    const ping = (deviceSettings && !!deviceSettings['use_ping'] ? deviceSettings['use_ping'] : true)
    const ledOnAfterConnect = (deviceSettings && !!deviceSettings['led_on_after_connect'] ? deviceSettings['led_on_after_connect'] : true)
    const [usePing, setUsePing] = useState(ping)
    const [ledOn, setLedOn] = useState(ledOnAfterConnect)
    const menuSelection = useSelector(state => state['globalState']['menuSelection'])
    const isVisible = menuSelection === 'Devices'
    if (!selectedDevice || !isVisible) {
        return <DeviceDetailsContainer/>
    }
    const deviceId = config['device_id']
    const sensors = config['sensors']
    const wifi = config['wifi_network']
    const ftp = config['ftp_server']
    const mqtt = config['mqtt_broker']
    const dispatch = useDispatch()

    const addSensorView = () => dispatch(globalStateActions.updateDetailsSectionView('addSensor'))
    const updateConfigJsonView = () => dispatch(globalStateActions.updateDetailsSectionView('updateConfigJson'))
    const {restartDevice, updateDeviceSettings} = useApi()
    const handleRestartClick = () => {
        restartDevice(deviceId).then(data => console.log(data))
    }
    const handleUpdateSettings = () => {
        updateDeviceSettings(deviceId, {'use_ping': usePing, 'led_on_after_connect': ledOn})
            .then(data => console.log(data))
    }
    return (
        <Wrapper>
            <Row>
                <div><Button onClick={handleRestartClick}>Restart Device</Button></div>
                <div><Button onClick={updateConfigJsonView}>Update Start Configs</Button></div>
                <div><Button onClick={handleUpdateSettings}>Save Settings</Button></div>
            </Row>
            <SectionContainer>
                <h4>Device Details:</h4>
                <Row>
                    <PropStack label={"Name"}>{selectedDevice['display_name']}</PropStack>
                    <PropStack label={"DeviceID"}>{config['device_id']}</PropStack>
                    <PropStack label={"ConfigID"}>{config.id}</PropStack>
                    <PropStack label={"Platform"}>{selectedDevice['platform']}</PropStack>
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
                <Row>
                    <form onSubmit={handleUpdateSettings}>
                        <label>Use Ping
                            <input type={'checkbox'} checked={usePing} onChange={event => setUsePing(event.target.checked)}/>
                        </label>
                        <label>LED On After Connect
                            <input type={'checkbox'} checked={ledOn} onChange={event => setLedOn(event.target.checked)}/>
                        </label>
                        <button type={'submit'} style={{display: 'None'}}>submit</button>
                    </form>
                </Row>
            </SectionContainer>
            <SectionContainer>

                <h4>Sensors:</h4>
                <SensorSection>
                    <SensorRow>
                        {sensors.map(sensor => <SensorCard sensorDetails={sensor}/>)}
                    </SensorRow>
                    <Button onClick={addSensorView}>Add Sensor</Button>
                </SensorSection>
            </SectionContainer>

        </Wrapper>
    )
}

export default DeviceDetailsView;