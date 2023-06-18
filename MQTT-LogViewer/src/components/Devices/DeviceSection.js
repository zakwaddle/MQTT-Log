// import React, {useState} from "react";
// import styled from "styled-components";
// import useApi from "../../hooks/useApi";
// import DeviceConfigs from "../Configs/DeviceConfigs";
// import {useSelector} from "react-redux";
//
// const DeviceSectionContainer = styled.div`
//   width: 100%;
//   display: flex;
//   justify-content: center;
//   padding: 1em;
//   margin: 1em;
// `
//
// const DeviceListContainer = styled.div`
//   display: flex;
//   flex-direction: column;
//   min-height: 8em;
//   width: 100%;
//   border-radius: 0 0 1em 1em;
// `
//
// const DeviceContainer = styled.div`
//   background-color: ${props => props['selected'] ? 'grey' : undefined};
//   display: flex;
//   justify-content: space-evenly;
// `
// const Button = styled.button`
//   font-family: monospace;
//   font-size: inherit;
//   background-color: inherit;
//   border-radius: .3em;
//   border-width: 1px;
// `
// const Device = ({deviceData, selected, setSelected}) => {
//
//     return (
//         <DeviceContainer selected={selected === deviceData.id} onClick={() => setSelected(deviceData.id)}>
//             <p>{deviceData.display_name}</p>
//         </DeviceContainer>
//     )
// }
// const DeviceList = ({devices, selectedDevice, setSelectedDevice}) => {
//     return (
//         <DeviceListContainer>
//             {devices.map(device => <Device key={device.id}
//                                            deviceData={device}
//                                            selected={selectedDevice}
//                                            setSelected={setSelectedDevice}/>)}
//         </DeviceListContainer>
//     )
// }
// const NewDevice = ({deviceData, setSetupDevice, setShowSetup}) => {
//     const handleClick = () => {
//         setSetupDevice(deviceData)
//         setShowSetup(true)
//     }
//     return (
//         <DeviceContainer>
//             <p>{deviceData.id}</p>
//             <p>{deviceData.platform}</p>
//             <Button onClick={handleClick}>Setup Device</Button>
//         </DeviceContainer>
//     )
// }
// const NewDeviceList = ({newDevices, setSetupDevice, setShowSetup}) => {
//
//     return (
//         <DeviceListContainer>
//             {newDevices.map(device => <NewDevice key={device.id}
//                                                  deviceData={device}
//                                                  setShowSetup={setShowSetup}
//                                                  setSetupDevice={setSetupDevice}/>)}
//         </DeviceListContainer>
//     )
// }
// const StackedTabContainer = styled.div`
//   display: flex;
//   flex-direction: column;
//   width: 100%;
// `
// const TabAreaContainer = styled.div`
//   display: flex;
//   margin: .5em 0 0 0;
//
// `
// const TabContainer = styled.div`
//   height: 2em;
//   background-color: ${props => props['selected'] ? 'white' : 'grey'};
//   box-shadow: ${props => props['selected'] ? '3px -2px 2px rgba(0,0,0,0.3)' : 0};
//   z-index: ${props => props['selected'] ? 1 : 0};
//   display: flex;
//   justify-content: center;
//   align-items: center;
//   flex: 1 0;
//   border-radius: 1em 1em 0 0;
// `
//
// const Tab = ({label, selectedTab, setSelectedTab}) => {
//     return (
//         <TabContainer selected={selectedTab === label} onClick={() => setSelectedTab(label)}>
//             <h3>{label}</h3>
//         </TabContainer>
//     )
// }
//
// const TabContentContainer = styled.div`
//   min-height: 8em;
//   width: 100%;
//   background-color: white;
//   box-shadow: ${props => props['selected'] ? '3px -2px 2px rgba(0,0,0,0.3)' : 0};
// `
//
// const TabContent = ({label, selectedTab, children}) => {
//     if (selectedTab !== label) {
//         return null
//     }
//     return (
//         <TabContentContainer selected={selectedTab === label}>
//             {children}
//         </TabContentContainer>
//     )
// }
//
// const DeviceSetupBox = styled.div`
//   width: 95%;
//
//   display: flex;
//   flex-direction: column;
// `
// const DeviceSetupRow = styled.div`
//   width: 95%;
//   display: flex;
//   justify-content: space-evenly;
// `
// const DeviceSetup = ({device, setShowSetup}) => {
//     const [newName, setNewName] = useState("")
//
//     const {updateDeviceName} = useApi()
//
//     const handleCancel = () => setShowSetup(false)
//     const handleSetup = () => {
//         updateDeviceName(device.id, newName).then(setShowSetup(false))
//     }
//     return (
//         <DeviceSetupBox>
//             <DeviceSetupRow>
//                 {device.platform}
//                 {device.id}
//             </DeviceSetupRow>
//             <DeviceSetupRow>
//                 Display Name
//                 <input value={newName} onChange={event => setNewName(event.target.value)}/>
//             </DeviceSetupRow>
//             <DeviceSetupRow>
//                 <Button onClick={handleCancel}>Cancel</Button>
//                 <Button onClick={handleSetup}>Save</Button>
//             </DeviceSetupRow>
//         </DeviceSetupBox>
//     )
// }
// const StackedTabs = () => {
//     const [selectedTab, setSelectedTab] = useState("Devices")
//     const [selectedDevice, setSelectedDevice] = useState([])
//     const [showDeviceSetup, setShowDeviceSetup] = useState(false)
//     const [setupDevice, setSetupDevice] = useState({})
//
//     const devices = useSelector(state => state['globalState']['devices'])
//     const newDevices = useSelector(state => state['globalState']['newDevices'])
//
//     return (
//         <StackedTabContainer>
//             <TabAreaContainer>
//                 <Tab label={"Devices"} selectedTab={selectedTab} setSelectedTab={setSelectedTab}/>
//                 <Tab label={"New Devices"} selectedTab={selectedTab} setSelectedTab={setSelectedTab}/>
//             </TabAreaContainer>
//             <TabContent label={"Devices"} selectedTab={selectedTab}>
//                 <DeviceList devices={devices} selectedDevice={selectedDevice} setSelectedDevice={setSelectedDevice}/>
//             </TabContent>
//             <TabContent label={"New Devices"} selectedTab={selectedTab}>
//                 {showDeviceSetup && <DeviceSetup device={setupDevice} setShowSetup={setShowDeviceSetup}/>}
//                 {!showDeviceSetup && <NewDeviceList newDevices={newDevices}
//                                                     setShowSetup={setShowDeviceSetup}
//                                                     setSetupDevice={setSetupDevice}/>}
//             </TabContent>
//         </StackedTabContainer>
//     )
// }
//
//
// const DeviceSection = () => {
//
//
//     return (
//         <DeviceSectionContainer>
//             <StackedTabs/>
//             <DeviceConfigs/>
//         </DeviceSectionContainer>
//     )
// }
//
// export default DeviceSection;