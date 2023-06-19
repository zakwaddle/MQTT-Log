import React, {useState} from "react";
// import styled from 'styled-components';
import {useSelector} from "react-redux";
import DeviceDetails from "../Devices/DeviceDetails";
//
// const Window = styled.div`
//   width: 50%;
//   height: available;
//
//   display: flex;
//   flex-direction: column;
//
//   background-color: white;
//   padding: 1em;
//
//   border-style: solid;
//   border-radius: 1em;
//   border-width: 1px;
//   border-color: darkgrey
// `

const Wrapper = ({children}) => {
    return ({...children})
}

export default function DetailSection (){
    // const [view, setView] = useState('main')
    const selectedDevice = useSelector(state => state['globalState']['selectedDevice'])
    const menuSelection = useSelector(state => state['globalState']['menuSelection'])

    const isVisible = menuSelection === 'Devices'
    if (!selectedDevice || !isVisible) {
        return null
    }
    return (
        <Wrapper>
            <DeviceDetails/>
        </Wrapper>
    )
}