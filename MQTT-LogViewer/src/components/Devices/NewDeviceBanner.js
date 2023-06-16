import styled from "styled-components";
import {useSelector} from "react-redux";
import React from "react";

const NewDeviceBannerContainer = styled.div`
  width: 100%;
  height: 3em;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
`

const NewDeviceBanner = () => {
    const newDevices = useSelector(state => state['globalState'].newDevices)
    if (newDevices){
        return (
            <NewDeviceBannerContainer>
                You have {newDevices.length} unconfigured device{(newDevices.length > 1 ? 's' : '')}
            </NewDeviceBannerContainer>
        )
    }
}

export default NewDeviceBanner;