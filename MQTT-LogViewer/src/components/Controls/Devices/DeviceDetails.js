import React, {useState} from "react";
import styled from "styled-components";
import {useSelector} from "react-redux";
import {Button} from "../../../styles/SectionStyles";
import {PropStack} from "../../UI/Property";
import {DimmableLEDForm, MotionSensorForm, WeatherSensorForm} from "../Forms/AddSensorForm";

const Row = styled.div`
  width: available;
  display: flex;
  justify-content: space-around;
`
const SensorContainer = styled.div`
  border: 1px solid grey;
  border-radius: 1em;
  padding: .5em;
  margin: .25em;
`

const Sensor = ({sensorDetails}) => {
    const {name, sensor_type, sensor_config} = sensorDetails
    const title = () => {
        switch (sensor_type) {
            case "motion": {
                return "Motion Sensor"
            }
            case "led": {
                return "LED Dimmer"
            }
            case "weather": {
                return "Weather Sensor"
            }
            default: {
                return null
            }
        }
    }

    return (
        <SensorContainer>
            <h4>{title()}</h4>
            <p><b>{name}</b></p>
            <p>Pin: {sensor_config.pin}</p>
        </SensorContainer>
    )
}

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

const DeviceSensors = ({setView, deviceConfig}) => {
    const deviceSensors = deviceConfig['sensors']

    return (
        <SensorSection>
            <SensorRow>
                {deviceSensors.map(sensor => <Sensor sensorDetails={sensor}/>)}
            </SensorRow>
            <Button onClick={() => setView('addSensor')}>Add Sensor</Button>
        </SensorSection>
    )
}

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
const AddSensorContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
`
const Wrapper = ({children}) => {
    return [...children]
}
const AddSensor = ({deviceConfigId, handleCancel}) => {
    const [sensorType, setSensorType] = useState('motion');
    const handleChange = (event) => setSensorType(event.target.value)

    const sensorForms = {
        "motion": <MotionSensorForm deviceConfigId={deviceConfigId} handleCancel={handleCancel}/>,
        "weather": <WeatherSensorForm deviceConfigId={deviceConfigId} handleCancel={handleCancel}/>,
        "led": <DimmableLEDForm deviceConfigId={deviceConfigId} handleCancel={handleCancel}/>,
    }
    return (
        <AddSensorContainer>
            <div>
                <select onChange={handleChange}>
                    <option value={'motion'}>Motion Sensor</option>
                    <option value={'weather'}>Weather Sensor</option>
                    <option value={'led'}>LED Dimmer</option>
                </select>
            </div>
            {sensorForms[sensorType]}

        </AddSensorContainer>

    );
};

const DeviceDetails = () => {
    const [view, setView] = useState('main')
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const menuSelection = useSelector(state => state['globalState']['menuSelection'])
    const isVisible = menuSelection === 'Devices'
    if (!selectedDevice || !isVisible) {
        return <DeviceDetailsContainer/>
    }
    console.log(selectedDevice)
    const config = selectedDevice.config
    const wifi = config['wifi_network']
    const ftp = config['ftp_server']
    const mqtt = config['mqtt_broker']

    const mainView = () => setView("main")
    if (view === 'main') {
        return (
            <Wrapper>
            {/*<DeviceDetailsContainer>*/}
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
                    <h4>Sensors:</h4>
                    <DeviceSensors setView={setView} deviceConfig={config}/>
                </SectionContainer>

                {/*</DeviceDetailsContainer>*/}
            </Wrapper>
        )
    }
    if (view === 'addSensor') {
        return (
            <DeviceDetailsContainer>
                <AddSensor handleCancel={mainView} deviceConfigId={config.id}/>
            </DeviceDetailsContainer>
        )
    }
}

export default DeviceDetails;