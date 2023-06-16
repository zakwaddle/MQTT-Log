import React, {useState} from 'react';
import useApi from "../../hooks/useApi";
import styled from "styled-components";
import {FormContainer, FormInput, FormLabel} from "../../styles/FormStyles";

const AddWifiForm = ({addNew, hideForm}) => {
    const [ssid, setSSID] = useState('');
    const [password, setPassword] = useState('');
    const [isDefault, setIsDefault] = useState(false);

    const {addWifiNetwork} = useApi()
    const clearFields = () => {
        setSSID('');
        setPassword('');
        setIsDefault(false)
    }

    const handleSubmit = async (event) => {
        event.preventDefault();

        addWifiNetwork(ssid, password)
            .then(data => {
                console.log(data);
                if (data && data.success) {
                    clearFields();
                    addNew && addNew(data['wifi_network'])
                    hideForm && hideForm()
                }
            })
    };

    return (
        <FormContainer onSubmit={handleSubmit}>
            <FormLabel>
                SSID
                <FormInput type="text" value={ssid} onChange={e => setSSID(e.target.value)}/>
            </FormLabel>
            <FormLabel>
                Password
                <FormInput type="password" value={password} onChange={e => setPassword(e.target.value)}/>
            </FormLabel>
            {/*<FormLabel>*/}
            {/*    Default*/}
            {/*    <input type="checkbox" checked={isDefault} onChange={e => setIsDefault(e.target.checked)}/>*/}
            {/*</FormLabel>*/}

            <div>
                <button type="submit">Save</button>
            </div>
        </FormContainer>
    );
};

export default AddWifiForm;
