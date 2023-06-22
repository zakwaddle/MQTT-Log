import React from "react";
import styled from "styled-components";
import UpdateConfigJsonForm from "./updateConfigJsonForm";
import useApi from "../../../../hooks/useApi";
import {useDispatch, useSelector} from "react-redux";
import {globalStateActions} from "../../../../store/globalStateSlice";
// import {Button} from "../../../../styles/SectionStyles";

const Box = styled.div`
`

export default function UpdateConfigJsonView (){
    const {sendMessage} = useApi()
    const dispatch = useDispatch()
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const deviceDetailsView = () => dispatch(globalStateActions.updateDetailsSectionView('main'))

    const handleSubmit = (host, name, wifiSSID, wifiPassword) => {
        sendMessage(selectedDevice.id, {
            command: "update_config",
            new_config: {
                host: host,
                name: name,
                wifi_ssid: wifiSSID,
                wifi_password: wifiPassword
            }}).then(data => {
            console.log(data)
            deviceDetailsView()
        })
    }

    return (

            <UpdateConfigJsonForm submitHandler={handleSubmit} cancelHandler={deviceDetailsView}/>
    )
}