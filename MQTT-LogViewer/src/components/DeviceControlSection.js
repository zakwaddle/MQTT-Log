import React, {useState} from "react";
import useApi from "../hooks/useApi"
import {useDispatch, useSelector} from "react-redux";
import styled from "styled-components";
import {globalStateActions} from "../store/globalStateSlice";
import AddMQTTBrokerForm from "./Configs/AddMQTTBrokerForm";
import AddFTPServerForm from "./Configs/AddFTPServerForm";
import AddWifiForm from "./Configs/AddWifiForm";
import useDeviceConfigs from "../hooks/useDeviceConfigs";

const Button = styled.button`
  font-family: monospace;
  font-size: inherit;
  background-color: inherit;
  border-radius: .3em;
  border-width: 1px;
`
const InfoBox = styled.div`
  width: 40%;
  background-color: white;
  display: flex;
  flex-direction: column;
`
const ControlSectionBox = styled.div`
  width: 100%;
  height: 20em;
  display: flex;
`
const MenuBox = styled.div`
  height: 100%;
  width: 10em;
  display: flex;
  flex-direction: column;
`
const MenuItemBox = styled.div`

`
const MenuItem = ({children}) => {
    const dispatch = useDispatch()
    const handleSelection = () => {
        dispatch(globalStateActions.updateMenuSelection(children))
    }
    return (
        <MenuItemBox onClick={handleSelection}>
            {children}
        </MenuItemBox>
    )
}
const PropertyRow = styled.div`
  width: 90%;
  display: flex;
  justify-content: space-between;
  padding-left: 2em;
  padding-right: 2em;
`
const PropertyName = styled.div`

`
const PropertyValue = styled.div`

`
const Property = ({name, value}) => {
    return (
        <PropertyRow>
            <PropertyName><b>{name}</b></PropertyName>
            <PropertyValue>{value}</PropertyValue>
        </PropertyRow>
    )
}

const Section = styled.div`
  padding: .5em;
  display: flex;
  flex-direction: column;
`
const SectionTitle = styled.div`
  padding: .25em;
  font-weight: bold;
  font-size: medium;
`
const CenteredRow = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
`
const WifiSection = ({wifi}) => {
    const dispatch = useDispatch()
    const handleClick = () => dispatch(globalStateActions.updateShowConnectionForm("WIFI"))
    if (!wifi) {
        return (
            <Section>
                <SectionTitle>Wifi Network</SectionTitle>
                <CenteredRow>
                    <div>
                        <Button onClick={handleClick}>Configure Wifi</Button>
                    </div>
                </CenteredRow>
            </Section>
        )
    }
    return (
        <Section>
            <SectionTitle>Wifi Network</SectionTitle>
            <Property name={'ssid'} value={(wifi ? wifi.ssid : '')}/>
            <Property name={'password'} value={(wifi ? wifi.password : '')}/>
        </Section>
    )
}
const MQTTSection = ({mqtt}) => {
    const dispatch = useDispatch()
    const handleClick = () => dispatch(globalStateActions.updateShowConnectionForm("MQTT"))
    if (!mqtt) {
        return (
            <Section>
                <SectionTitle>MQTT Broker</SectionTitle>
                <CenteredRow>
                    <div>
                        <Button onClick={handleClick}>Configure MQTT</Button>
                    </div>
                </CenteredRow>
            </Section>
        )
    }
    return (
        <Section>
            <SectionTitle>MQTT Broker</SectionTitle>
            <Property name={'host'} value={(mqtt ? mqtt.host_address : '')}/>
            <Property name={'port'} value={(mqtt ? mqtt.port : '')}/>
            <Property name={'username'} value={(mqtt ? mqtt.username : '')}/>
            <Property name={'password'} value={(mqtt ? mqtt.password : '')}/>
        </Section>
    )
}
const FTPSection = ({ftp}) => {
    const dispatch = useDispatch()
    const handleClick = () => dispatch(globalStateActions.updateShowConnectionForm("FTP"))
    if (!ftp) {
        return (
            <Section>
                <SectionTitle>FTP Server</SectionTitle>
                <CenteredRow>
                    <div>
                        <Button onClick={handleClick}>Configure FTP</Button>
                    </div>
                </CenteredRow>
            </Section>
        )
    }
    return (
        <Section>
            <SectionTitle>FTP Server</SectionTitle>
            <Property name={'host'} value={(ftp ? ftp.host_address : '')}/>
            <Property name={'username'} value={(ftp ? ftp.username : '')}/>
            <Property name={'password'} value={(ftp ? ftp.password : '')}/>
        </Section>
    )
}
const ConnectionSection = () => {
    const dispatch =  useDispatch()
    const wifi = useSelector(state => state['globalState']['wifiNetwork'])
    const ftp = useSelector(state => state['globalState']['ftpServer'])
    const mqtt = useSelector(state => state['globalState']['mqttBroker'])
    const connectionKey = useSelector(state => state['globalState']['showConnectionForm'])
    const handleCancel = () => dispatch(globalStateActions.updateShowConnectionForm('None'))
    if (connectionKey === 'None') {
        return (
            <InfoBox>
                <WifiSection wifi={wifi}/>
                <MQTTSection mqtt={mqtt}/>
                <FTPSection ftp={ftp}/>
            </InfoBox>
        )
    }
    if (connectionKey === 'MQTT') {
        return (
            <InfoBox>
                <SectionTitle>MQTT Broker</SectionTitle>

                <AddMQTTBrokerForm handleCancel={handleCancel}/>
            </InfoBox>
        )
    }
    if (connectionKey === 'WIFI') {
        return (
            <InfoBox>
                <SectionTitle>Wifi Network</SectionTitle>

                <AddWifiForm handleCancel={handleCancel}/>
            </InfoBox>
        )
    }
    if (connectionKey === 'FTP') {
        return (
            <InfoBox>
                <SectionTitle>FTP Server</SectionTitle>

                <AddFTPServerForm handleCancel={handleCancel}/>
            </InfoBox>
        )
    }


}
const DeviceControlSection = () => {
    useDeviceConfigs()
    const devices = useSelector(state => state['globalState']['devices'])
    const newDevices = useSelector(state => state['globalState']['newDevices'])


    return (
        <ControlSectionBox>
            <MenuBox>
                <MenuItem>Devices</MenuItem>
                <MenuItem>Connections</MenuItem>
            </MenuBox>
            <ConnectionSection/>
        </ControlSectionBox>
    )

}

export default DeviceControlSection;