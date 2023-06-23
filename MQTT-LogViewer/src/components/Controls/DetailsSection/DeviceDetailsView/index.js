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
  width: 100%;
`

const DeviceTitle =styled.h1`
  margin: .25em 0 .5em 1.5em;
`
const Box = styled.div`
  
  width: 100%;
  height: 100%;
  
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  
`
const Property = styled.div`
  display: flex;
  justify-content: space-between;
  margin-left: 2em;
  margin-right: 2em;
  @media (max-width: 700px) {
    flex-direction: row;
  }
`
const PropertyTitle = styled.div`
  margin-left: 2em;
  font-weight: bold;
  @media (max-width: 700px) {
    margin-left: 1em;
  }
`
const PropertyValue = styled.div`
  margin-right: 2em;
  @media (max-width: 700px) {
    margin-right: 1em;
  }
`

const HalfColumn = styled.div`
  display: flex;
  flex-direction: column;
  width: 50%;
`

const Form = styled.form`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
`
const FormLabel = styled.form`
  display: flex;
  justify-content: space-between;
`

const DeviceDetailsView = () => {
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const config = selectedDevice.config
    const deviceSettings = config["device_settings"]

    const [usePing, setUsePing] = useState(true)
    const [ledOn, setLedOn] = useState(true)

    const {deviceId, sensors} = config
    const wifi = config['wifi_network']
    const ftp = config['ftp_server']
    const mqtt = config['mqtt_broker']
    const dispatch = useDispatch()

    React.useEffect(() => {
        if (deviceSettings){
            // console.log(deviceSettings['use_ping'] !== undefined)
            // console.log(deviceSettings['led_on_after_connect'] !== undefined)
            if (deviceSettings['use_ping'] !== undefined){
                setUsePing(deviceSettings['use_ping'])
            }
            if (deviceSettings['led_on_after_connect'] !== undefined){
                setLedOn(deviceSettings['led_on_after_connect'])
            }
        }
        // const ping = (deviceSettings && !!deviceSettings['use_ping'] ? deviceSettings['use_ping'] : true)
        // const ledOnAfterConnect = (deviceSettings && !!deviceSettings['led_on_after_connect'] ? deviceSettings['led_on_after_connect'] : true)
    })

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
        <Box>
            <DeviceTitle>{selectedDevice['display_name']}</DeviceTitle>
            <Row>
                <div><Button onClick={handleRestartClick}>Restart Device</Button></div>
                <div><Button onClick={updateConfigJsonView}>Update Start Configs</Button></div>
                <div><Button onClick={handleUpdateSettings}>Save Settings</Button></div>
            </Row>
            <SectionContainer>
                <h4>Device Details:</h4>
                    {/*<PropStack label={"Name"}>{selectedDevice['display_name']}</PropStack>*/}
                    {/*<PropStack label={"DeviceID"}>{config['device_id']}</PropStack>*/}
                    {/*<PropStack label={"ConfigID"}>{config.id}</PropStack>*/}
                    {/*<PropStack label={"Platform"}>{selectedDevice['platform']}</PropStack>*/}
                    <Property>
                        <PropertyTitle>Name</PropertyTitle>
                        <PropertyValue>{selectedDevice['display_name']}</PropertyValue>
                    </Property>
                    <Property>
                        <PropertyTitle>DeviceID</PropertyTitle>
                        <PropertyValue>{config['device_id']}</PropertyValue>
                    </Property>
                    <Property>
                        <PropertyTitle>ConfigID</PropertyTitle>
                        <PropertyValue>{config.id}</PropertyValue>
                    </Property>
                    <Property>
                        <PropertyTitle>Platform</PropertyTitle>
                        <PropertyValue>{selectedDevice['platform']}</PropertyValue>
                    </Property>

            </SectionContainer>

            <SectionContainer>
                <HalfColumn>
                    <Form onSubmit={handleUpdateSettings}>
                        <FormLabel>Use Ping
                            <input type={'checkbox'}
                                   checked={usePing}
                                   onChange={event => setUsePing(event.target.checked)}/>
                        </FormLabel>
                        <FormLabel>LED On After Connect
                            <input type={'checkbox'}
                                   checked={ledOn}
                                   onChange={event => setLedOn(event.target.checked)}/>
                        </FormLabel>
                        <button type={'submit'} style={{display: 'None'}}>submit</button>
                    </Form>
                </HalfColumn>
                <HalfColumn>

                </HalfColumn>
            </SectionContainer>

            <SectionContainer>
                <h4>Connections:</h4>
                    <Property>
                        <PropertyTitle>Wifi Network</PropertyTitle>
                        <PropertyValue>{wifi && wifi.ssid}</PropertyValue>
                    </Property>
                    <Property>
                        <PropertyTitle>MQTT Broker</PropertyTitle>
                        <PropertyValue>{mqtt && mqtt.host_address}</PropertyValue>
                    </Property>
                    <Property>
                        <PropertyTitle>FTP Server</PropertyTitle>
                        <PropertyValue>{ftp && ftp.host_address}</PropertyValue>
                    </Property>
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

        </Box>
    )
}

export default DeviceDetailsView;