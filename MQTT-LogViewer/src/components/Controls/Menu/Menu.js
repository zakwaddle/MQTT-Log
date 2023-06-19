import React from "react";
import {useDispatch} from "react-redux";
import {Button} from "../../../styles/SectionStyles";
import {globalStateActions} from "../../../store/globalStateSlice";
import styled from "styled-components";


// const MenuItemBox = styled.div`
//
// `
const MenuItem = ({children}) => {
    const dispatch = useDispatch()
    const handleSelection = () => {
        dispatch(globalStateActions.updateMenuSelection(children))
    }
    return (
        <Button onClick={handleSelection}>
            {children}
        </Button>
    )
}

const MenuBox = styled.div`
  height: 100%;
  width: 10em;
  display: flex;
  flex-direction: column;
`
const Menu = () => {

    return (
        <MenuBox>
            <MenuItem>Devices</MenuItem>
            <MenuItem>Connections</MenuItem>
        </MenuBox>
    )
}

export default Menu;