import React, {useState} from "react";
import styled from "styled-components";
import {Button} from "../../../../styles/SectionStyles";

const Box = styled.div`
  width: 100%;
`

const Form = styled.form`
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 1em;
`

const UpdateConfigJsonForm = ({submitHandler, cancelHandler}) => {
    const [host, setHome] = useState('')
    const [name, setName] = useState('')
    const [wifiSSID, setWifiSSID] = useState('')
    const [wifiPassword, setWifiPassword] = useState('')

    const handleSubmit = async (event) => {
        event.preventDefault()
        submitHandler(host, name, wifiSSID, wifiPassword)
    }
    return (
        <Box>
            <Form onSubmit={handleSubmit}>
                <label>Host
                    <input type={'text'} value={host} onChange={event => setHome(event.target.value)}/>
                </label>
                <label>Display Name
                    <input type={'text'} value={name} onChange={event => setName(event.target.value)}/>
                </label>
                <label>Wifi SSID
                    <input type={'text'} value={wifiSSID} onChange={event => setWifiSSID(event.target.value)}/>
                </label>
                <label>Wifi Password
                    <input type={'text'} value={wifiPassword} onChange={event => setWifiPassword(event.target.value)}/>
                </label>
                <button type={'submit'} style={{display: 'None'}}>submit</button>
            </Form>
            <div>
                <Button onClick={cancelHandler}>Cancel</Button>
                <Button onClick={handleSubmit}>Save</Button>
            </div>
        </Box>

    )

}

export default UpdateConfigJsonForm;