import React, {useState} from "react";
import styled from "styled-components";
import {Button} from "../../../../styles/SectionStyles";
import {globalStateActions} from "../../../../store/globalStateSlice";
import {useDispatch, useSelector} from "react-redux";
import useApi from "../../../../hooks/useApi";
import {Property} from "../../../UI/Property";

const SensorDetailsContainer = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;

`
const Header = styled.div`

`
const ConfigSection = styled.div`

`
const ButtonRow = styled.div`

`
const DeleteConfirmContainer = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`

const SensorDetails = () => {
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
    const dispatch = useDispatch()
    const selectedSensor = useSelector(state => state['globalState']['selectedSensor'])
    const sensorConfig = selectedSensor.sensor_config
    const setDetailsView = () => dispatch(globalStateActions.updateDetailsSectionView('main'))
    const {deleteSensor} = useApi()

    const openDeleteConfirm = () => setShowDeleteConfirm(true)
    const closeDeleteConfirm = () => setShowDeleteConfirm(false)

    const handleDelete = () => {
        deleteSensor(selectedSensor.id)
            .then(() => {
                dispatch(globalStateActions.updateShouldUpdateDevices(true))
                setDetailsView()
            })
    }

    if (showDeleteConfirm){
        return (
            <DeleteConfirmContainer>
                <h2>Delete {selectedSensor.name}?</h2>
                <br/>
                <ButtonRow>
                    <Button onClick={closeDeleteConfirm}>Cancel</Button>
                    <Button onClick={handleDelete}>Delete</Button>
                </ButtonRow>
            </DeleteConfirmContainer>
        )
    }

    const allConfigKeys = Object.keys(sensorConfig)
    const topicKeys = Object.keys(sensorConfig.topics)
    const configKeys = allConfigKeys.filter(i => i !== 'topics')
    console.log(configKeys)
    return (
        <SensorDetailsContainer>
            <Header>
                <h3>{selectedSensor.name}</h3>
                <h4>type: {selectedSensor.sensor_type}</h4>
            </Header>
            <ConfigSection>
                <h4>Sensor Configs</h4>
                {configKeys.map(k => {
                    // const prettyName = k.replace('_', ' ').replace('_', ' ')
                    return <Property key={k} name={k} value={sensorConfig[k]}/>
                })}
            </ConfigSection>
            <ConfigSection>
                <h4>Sensor Topics</h4>
                {topicKeys.map(k => {
                    // const prettyName = k.replace('_', ' ').replace('_', ' ')
                    return <Property key={k} name={k} value={sensorConfig.topics[k]}/>
                })}
            </ConfigSection>
            <ButtonRow>
                <Button onClick={openDeleteConfirm}>Delete</Button>
                <Button onClick={setDetailsView}>Back</Button>
            </ButtonRow>
        </SensorDetailsContainer>
    )
}

export default SensorDetails;