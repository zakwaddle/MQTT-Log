import React, {useState, useEffect} from "react";
import styled from "styled-components";
import useApi from "../../hooks/useApi";
import AddWifiForm from "../Connections/AddWifiForm";
import AddFTPServerForm from "../Connections/AddFTPServerForm";
import AddMQTTBrokerForm from "../Connections/AddMQTTBrokerForm";
import {useDispatch, useSelector} from "react-redux";
import {globalStateActions} from "../../store/globalStateSlice";

const ConfigSectionContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;

  padding: .5em;
  margin: .5em;
`
const ConfigContainer = styled.div`
  display: flex;
  flex-direction: column;
  padding: .5em;
  margin: .5em;
  //flex: 1 0;
  //justify-content: center;
  //align-items: center;
`

const ConfigPropContainer = styled.div`
  display: flex;
  justify-content: space-around;
`
// const ConfigPropValue = styled.div`
//
// `

const WifiNetwork = ({ssid, password}) => {
    return (
        <ConfigPropContainer>
            <div><b>SSID</b></div>
            <div>{ssid}</div>
            {/*<div>{password}</div>*/}
        </ConfigPropContainer>
    )
}
const FtpServer = ({hostAddress, username, password}) => {
    return (
        <ConfigPropContainer>
            <div><b>Host Address</b></div>
            <div>{hostAddress}</div>
            {/*<div>{username}</div>*/}
            {/*<div>{password}</div>*/}
        </ConfigPropContainer>
    )
}
const MqttBroker = ({hostAddress, port, username, password}) => {
    return (
        <ConfigPropContainer>
            <div><b>Host Address</b></div>
            <div>{hostAddress}</div>
            {/*<div>{port}</div>*/}
            {/*<div>{username}</div>*/}
            {/*<div>{password}</div>*/}
        </ConfigPropContainer>
    )
}

const ConfigsSection = () => {
    // const [wifiNetworks, setWifiNetworks] = useState([])
    // const [ftpServers, setFtpServers] = useState([])
    // const [mqttBrokers, setMqttBrokers] = useState([])

    // const [showWifiForm, setShowWifiForm] = useState(false)
    // const [showFtpForm, setShowFtpForm] = useState(false)
    // const [showMqttForm, setShowMqttForm] = useState(false)

    // const showAddWifiForm = () => setShowWifiForm(true)
    // const hideWifiForm = () => setShowWifiForm(false)
    // const showAddFtpForm = () => setShowFtpForm(true)
    // const hideFtpForm = () => setShowFtpForm(false)
    // const showAddMqttForm = () => setShowMqttForm(true)
    // const hideMqttForm = () => setShowMqttForm(false)

    // const addNewWifiNetwork = (network) => {
    //     setWifiNetworks(oldEntries => [...oldEntries, network])
    // }
    // const addNewFtpServer = (server) => {
    //     setFtpServers(oldEntries => [...oldEntries, server])
    // }
    // const addNewMqttBroker = (broker) => {
    //     setMqttBrokers(oldEntries => [...oldEntries, broker])
    // }
    // const dispatch = useDispatch()
    const wifiNetwork = useSelector(state => state['globalState']['wifiNetwork'])
    const ftpServer = useSelector(state => state['globalState']['ftpServer'])
    const mqttBroker = useSelector(state => state['globalState']['mqttBroker'])
    // const {
    //     fetchWifiNetworks,
    //     fetchFtpServers,
    //     fetchMqttBrokers,
    // } = useApi()
    //
    // useEffect(() => {
    //     fetchWifiNetworks().then(data => {
    //         dispatch(globalStateActions.updateWifiNetwork(data[0]))
    //     })
    //     fetchFtpServers().then(data => {
    //         dispatch(globalStateActions.updateFtpServer(data[0]))
    //     })
    //     fetchMqttBrokers().then(data => {
    //         dispatch(globalStateActions.updateMqttBroker(data[0]))
    //     })
    // }, [])

    return (
        <ConfigSectionContainer>
            <ConfigContainer>
                <h3>Wifi Network</h3>
                {wifiNetwork &&
                    <WifiNetwork ssid={wifiNetwork.ssid} password={wifiNetwork.password}/>}
                {/*<div>*/}
                {/*    <button onClick={showAddWifiForm}>add network</button>*/}
                {/*</div>*/}
                {/*{showWifiForm && <AddWifiForm addNew={addNewWifiNetwork} hideForm={hideWifiForm}/>}*/}
            </ConfigContainer>
            <ConfigContainer>
                <h3>FTP Server</h3>
                {ftpServer && <FtpServer hostAddress={ftpServer.host_address}
                                         username={ftpServer.username}
                                         password={ftpServer.password}
                />}
                {/*<div>*/}
                {/*    <button onClick={showAddFtpForm}>add ftp server</button>*/}
                {/*</div>*/}
                {/*{showFtpForm && <AddFTPServerForm addNew={addNewFtpServer} hideForm={hideFtpForm}/>}*/}
            </ConfigContainer>
            <ConfigContainer>
                <h3>MQTT Broker</h3>
                {mqttBroker && <MqttBroker hostAddress={mqttBroker.host_address}
                                           port={mqttBroker.port}
                                           username={mqttBroker.username}
                                           password={mqttBroker.password}
                />}
                {/*<div>*/}
                {/*    <button onClick={showAddMqttForm}>add mqtt broker</button>*/}
                {/*</div>*/}
                {/*{showMqttForm && <AddMQTTBrokerForm addNew={addNewMqttBroker} hideForm={hideMqttForm}/>}*/}
            </ConfigContainer>

        </ConfigSectionContainer>
    )
}

export default ConfigsSection;