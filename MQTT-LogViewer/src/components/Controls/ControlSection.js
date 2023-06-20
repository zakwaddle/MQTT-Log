import React from "react";
import styled from "styled-components";
// import {useDispatch, useSelector} from "react-redux";
// import useApi from "../../hooks/useApi";
import Menu from "./Menu/Menu";
import useConnections from "../../hooks/useConnections";
// import {globalStateActions} from "../../store/globalStateSlice";
import DetailSection from "./DetailsSection";
import InfoSection from "./InfoSection";
import useDevices from "../../hooks/useDevices";

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
    useConnections()
    useDevices()

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