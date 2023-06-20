import React, {useState} from "react";
import {useDispatch, useSelector} from "react-redux";

import {DeviceList, DeviceSetup, NewDeviceList} from "./DeviceList";


const Wrapper = ({children}) => {
    return [...children]
}
export const Devices = () => {
    const devices = useSelector(state => state['globalState']['devices'])
    const newDevices = useSelector(state => state['globalState']['newDevices'])
    const [showDeviceSetup, setShowDeviceSetup] = useState(false)
    const [setupDevice, setSetupDevice] = useState(null)
    if (showDeviceSetup){
        return (
            <DeviceSetup setShowSetup={setShowDeviceSetup}
                         device={setupDevice}/>
        )
    }
    return (
        <Wrapper>
            <DeviceList devices={devices}/>
            <NewDeviceList setSetupDevice={setSetupDevice}
                           setShowSetup={setShowDeviceSetup}
                           newDevices={newDevices}/>
        </Wrapper>
    )
}
