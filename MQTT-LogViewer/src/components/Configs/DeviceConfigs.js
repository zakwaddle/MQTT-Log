import React from "react";
import styled from "styled-components";
import {useSelector} from "react-redux";
import AddWifiForm from "../Connections/AddWifiForm";
import AddMQTTBrokerForm from "../Connections/AddMQTTBrokerForm";
import useDeviceConfigs from "../../hooks/useDeviceConfigs";

const ConfigBox = styled.div`
  width: 48%;
  padding: 1em;
  display: flex;
  flex-direction: column;
`

const DeviceConfigsBox = styled.div`
  width: 100%;
  
`
const NoConfigBox = styled.div`
  width: 100%;
  justify-content: center;
`

const DeviceConfigs = () => {

    useDeviceConfigs()

    const wifiNetwork = useSelector(state => state['globalState']['wifiNetwork'])
    const mqttBroker = useSelector(state => state['globalState']['mqttBroker'])
    const ftpServer = useSelector(state => state['globalState']['ftpServer'])

    const needsConnections = !wifiNetwork && !mqttBroker

    if (needsConnections) {
        return (
            <ConfigBox>
                <NoConfigBox>
                    <h4>Configure Wifi</h4>
                    <AddWifiForm/>
                    <h4>Configure MQTT</h4>
                    <AddMQTTBrokerForm/>
                </NoConfigBox>
            </ConfigBox>
        )
    }
    return (
        <ConfigBox>
            <DeviceConfigsBox>
                Poo
            </DeviceConfigsBox>
        </ConfigBox>
    )
}

export default DeviceConfigs;