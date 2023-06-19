import React, {useState} from 'react';
import useApi from "../../../hooks/useApi";
import styled from "styled-components";
import {FormContainer, FormInput, FormLabel} from "../../../styles/FormStyles";
import {useDispatch} from "react-redux";
import {globalStateActions} from "../../../store/globalStateSlice";
import {Button} from "../../../styles/SectionStyles";


export const MotionSensorForm = ({deviceConfigId, handleCancel}) => {
    const dispatch = useDispatch()
    const {addSensor} = useApi()
    const [name, setName] = useState('');
    const [pin, setPin] = useState(null);
    const [retrigDelay, setRetrigDelay] = useState(120000);
    const clearFields = () => {
        setName('')
        setPin(null)
        setRetrigDelay(120000)
    }
    const handleSubmit = async (event) => {
        event.preventDefault();

        addSensor("motion", name, deviceConfigId,
            {
                pin: pin,
                retrigger_delay_ms: retrigDelay
            }).then(data => {
            if (data && data.success) {
                clearFields();
                handleCancel && handleCancel()
            }
        })
    };
    return (
        <FormContainer onSubmit={handleSubmit}>
            <FormLabel>
                Name
                <FormInput type="text" value={name} onChange={e => setName(e.target.value)}/>
            </FormLabel>
            <FormLabel>
                Pin
                <FormInput type="number" value={pin} onChange={e => setPin(Number(e.target.value))}/>
            </FormLabel>
            <FormLabel>
                Re-Trigger Delay (ms)
                <FormInput type="number" value={retrigDelay} onChange={e => setRetrigDelay(Number(e.target.value))}/>
            </FormLabel>

            <div>
                <Button onClick={handleCancel && handleCancel}>Cancel</Button>
                <Button type="submit">Save</Button>
            </div>
        </FormContainer>
    );
}

export const WeatherSensorForm = ({deviceConfigId, handleCancel}) => {
    const dispatch = useDispatch()
    const {addSensor} = useApi()
    const [name, setName] = useState('');
    const [pin, setPin] = useState(null);
    const [measurementInterval, setMeasurementInterval] = useState(10000);
    const clearFields = () => {
        setName('')
        setPin(null)
        setMeasurementInterval(10000)
    }
    const handleSubmit = async (event) => {
        event.preventDefault();

        addSensor("weather", name, deviceConfigId,
            {
                pin: pin,
                measurement_interval_ms: measurementInterval
            }).then(data => {
            if (data && data.success) {
                clearFields();
                handleCancel && handleCancel()
            }
        })
    };
    return (
        <FormContainer onSubmit={handleSubmit}>
            <FormLabel>
                Name
                <FormInput type="text" value={name} onChange={e => setName(e.target.value)}/>
            </FormLabel>
            <FormLabel>
                Pin
                <FormInput type="number" value={pin} onChange={e => setPin(Number(e.target.value))}/>
            </FormLabel>
            <FormLabel>
                Measurement Interval (ms)
                <FormInput type="number" value={measurementInterval} onChange={e => setMeasurementInterval(Number(e.target.value))}/>
            </FormLabel>

            <div>
                <Button onClick={handleCancel && handleCancel}>Cancel</Button>
                <Button type="submit">Save</Button>
            </div>
        </FormContainer>
    );
}
export const DimmableLEDForm = ({deviceConfigId, handleCancel}) => {
    const dispatch = useDispatch()
    const {addSensor} = useApi()
    const [name, setName] = useState('');
    const [pin, setPin] = useState(null);
    const [freq, setFreq] = useState(300);
    const [fadeTimeMS, setFadeTimeMS] = useState(4);
    const [brightnessScale, setBrightnessScale] = useState(255);
    const clearFields = () => {
        setName('')
        setPin(null)
        setFreq(300)
        setFadeTimeMS(4)
        setBrightnessScale(255)
    }
    const handleSubmit = async (event) => {
        event.preventDefault();

        addSensor("led", name, deviceConfigId,
            {
                pin: pin,
                freq: freq,
                fade_time_ms: fadeTimeMS,
                brightness_scale: brightnessScale
            }).then(data => {
            if (data && data.success) {
                clearFields();
                handleCancel && handleCancel()
            }
        })
    };
    return (
        <FormContainer onSubmit={handleSubmit}>
            <FormLabel>
                Name
                <FormInput type="text" value={name} onChange={e => setName(e.target.value)}/>
            </FormLabel>
            <FormLabel>
                Pin
                <FormInput type="number" value={pin} onChange={e => setPin(Number(e.target.value))}/>
            </FormLabel>
            <FormLabel>
                Frequency
                <FormInput type="number" value={freq} onChange={e => setFreq(Number(e.target.value))}/>
            </FormLabel>
            <FormLabel>
                Fade Time (ms)
                <FormInput type="number" value={fadeTimeMS} onChange={e => setFadeTimeMS(Number(e.target.value))}/>
            </FormLabel>
            <FormLabel>
                Brightness Scale
                <FormInput type="number" value={brightnessScale} onChange={e => setBrightnessScale(Number(e.target.value))}/>
            </FormLabel>

            <div>
                <Button onClick={handleCancel && handleCancel}>Cancel</Button>
                <Button type="submit">Save</Button>
            </div>
        </FormContainer>
    );
}

