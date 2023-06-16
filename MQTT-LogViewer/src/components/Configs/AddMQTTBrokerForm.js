import React, {useState} from 'react';
import useApi from "../../hooks/useApi";
import {FormContainer, FormInput, FormLabel} from "../../styles/FormStyles";



const AddMQTTBrokerForm = ({hideForm}) => {
    const [hostAddress, setHostAddress] = useState('');
    const [port, setPort] = useState(1883);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isDefault, setIsDefault] = useState(false);


    const {addMqttBroker} = useApi()
    const clearFields = () => {
        setHostAddress('');
        setPort(null);
        setUsername('');
        setPassword('');
        setIsDefault(false)
    }

    const handleSubmit = async (event) => {
        event.preventDefault();

        addMqttBroker(hostAddress, port, username, password)
            .then(data => {
                console.log(data);
                if (data && data.success) {
                    clearFields();
                    hideForm && hideForm()
                }
            })
    };

    return (
        <FormContainer onSubmit={handleSubmit}>
            <FormLabel>
                Host Address
                <FormInput type="text" value={hostAddress} onChange={e => setHostAddress(e.target.value)}/>
            </FormLabel>
            <FormLabel>
                Port
                <FormInput type="number" value={port} onChange={e => setPort(Number(e.target.value))}/>
            </FormLabel>
            <FormLabel>
                Username
                <FormInput type="text" value={username} onChange={e => setUsername(e.target.value)}/>
            </FormLabel>
            <FormLabel>
                Password
                <FormInput type="password" value={password} onChange={e => setPassword(e.target.value)}/>
            </FormLabel>

            <div>
                <button type="submit">Save</button>
            </div>
        </FormContainer>
    );
};

export default AddMQTTBrokerForm;
