import React from "react";
// import styled from 'styled-components';
import {Devices} from "../Devices/Devices";
import ConnectionSection from "./Connections";
import {useSelector} from "react-redux";

const Wrapper = ({children}) => {
    return ({...children})
}
export default function InfoWindow (){
    const menuSelection = useSelector(state => state['globalState']['menuSelection'])

    const infoSection = {
        "Devices": <Devices/>,
        "Connections": <ConnectionSection/>
    }

    return (
        <Wrapper>
            {infoSection[menuSelection]}
        </Wrapper>
    )
}