import React, {useEffect} from "react";
import styled from "styled-components";
import {useDispatch, useSelector} from "react-redux";
import useApi from "../../hooks/useApi";
import Menu from "./Menu/Menu";
import useDeviceConfigs from "../../hooks/useDeviceConfigs";
import {globalStateActions} from "../../store/globalStateSlice";
import DetailSection from "./DetailsSection";
import InfoSection from "./InfoSection";

const ControlSectionBox = styled.div`
  width: 100%;
  min-height: 22em;
  display: flex;
  justify-content: space-around;
  margin: 1em 1em 0 1em;
`

const InfoWindow = styled.div`
  width: 30%;
  background-color: white;
  display: flex;
  flex-direction: column;
  padding: 1em;

  border-style: solid;
  border-radius: 1em;
  border-width: 1px;
  border-color: darkgrey;
`

const DetailsWindow = styled.div`
  width: 50%;
  height: available;

  display: flex;
  flex-direction: column;

  background-color: white;
  padding: 1em;

  border-style: solid;
  border-radius: 1em;
  border-width: 1px;
  border-color: darkgrey
`
const ControlSection = () => {
    useDeviceConfigs()
    const dispatch = useDispatch();
    const {fetchDevices} = useApi();
    // const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    // const menuSelection = useSelector(state => state['globalState']['menuSelection'])

    useEffect(() => {
        fetchDevices().then(data => {
            const newDevices = data.filter(device => device.display_name === null)
            const devices = data.filter(device => device.display_name !== null)
            dispatch(globalStateActions.updateDevices(devices));
            dispatch(globalStateActions.updateNewDevices(newDevices));
        });
    }, []);

    // const detailsVisible = menuSelection === 'Devices'
    // if (!selectedDevice || !detailsVisible) {
    //     return <DetailsWindow/>
    // }
    return (
        <ControlSectionBox>
            <Menu/>
            <InfoWindow>
                <InfoSection/>
            </InfoWindow>
            <DetailsWindow>
                <DetailSection/>
            </DetailsWindow>
        </ControlSectionBox>
    )
}

export default ControlSection;