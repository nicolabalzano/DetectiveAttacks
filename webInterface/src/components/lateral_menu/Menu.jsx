import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import { Link } from 'react-router-dom';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import github from "../../assets/github.svg";
import linkedin from "../../assets/linkedin.png";
import search from "../../assets/search_lens.png";
import MenuIcon from "../../assets/MenuIcon.jsx";
import './menu.scss';
import LogoSvg from '../../assets/LogoSvg';
import QuestionMark from '../../assets/QuestionMark';

const Menu = () => {
    const [state, setState] = React.useState({
        top: false,
        left: false,
        bottom: false,
        right: false,
    });

    const toggleDrawer = (anchor, open) => (event) => {
        if (
            event.type === 'keydown' &&
            (event.key === 'Tab' || event.key === 'Shift')
        ) {
            return;
        }

        setState({ ...state, [anchor]: open });
    };

    const list = (anchor) => (
        <Box
            sx={{ width: anchor === 'top' || anchor === 'bottom' ? 'auto' : 300 }}
            role="presentation"
            onClick={toggleDrawer(anchor, false)}
            onKeyDown={toggleDrawer(anchor, false)}
            >
            
            {/* Page */}
            <List className='mt-2 text-decoration-none'>
                {/* Home */}
                <Link to="/" className='text-decoration-none text-color'>
                    <ListItemButton>
                        <ListItemIcon> <LogoSvg w={'40px'} h={'40px'}/> </ListItemIcon>
                        <ListItemText primary='Home' />
                    </ListItemButton>
                </Link>
                {/* Searching option */}
                <Link to="/searching_choice" className='text-decoration-none text-color'>
                    <ListItemButton>
                        <ListItemIcon> <QuestionMark/> </ListItemIcon>
                        <ListItemText primary='Searching option' />
                    </ListItemButton>
                </Link>
                {/* Search page */}
                <Link to="/manual_search" className='text-decoration-none text-color'>
                    <ListItemButton>
                        <ListItemIcon> <img src={search} alt='search' width={'30px'} height={'30px'} /> </ListItemIcon>
                        <ListItemText primary='Search page' />
                    </ListItemButton>
                </Link>
                {/* Attack Patterns by phase */}
                <Link to="/attack_patterns_by_phase" className='text-decoration-none text-color'>
                    <ListItemButton>
                        <ListItemIcon> 
                            <div className='m-0 text-center fs-6'>
                                <p style={{ color: '#c9482e' }} className='m-0 font-logo'>ATT&CK</p>
                                <p className='text-color text-center font-logo plus-logo'>+</p>
                                <p style={{ color: '#83d3f7' }} className='m-0 font-logo'>ATLAS</p> 
                            </div>
                        </ListItemIcon>
                        <ListItemText primary='Attack Patterns by phase' />
                    </ListItemButton>
                </Link>
            </List>

            <hr className='mx-4 border-2 border-primary'/>
            
            {/* About */}
            <List>
                <p className='ms-4 fw-bold fs-4'>About</p>
                {/* Github */}
                <ListItemButton onClick={() => window.open("https://github.com/nicolabalzano")}>
                        <ListItemIcon> <img src={github} alt='github' width={'30px'} height={'30px'} /> </ListItemIcon>
                        <ListItemText primary='github' />
                </ListItemButton>
                {/* Linkedin */}
                <ListItemButton onClick={() => window.open("https://www.linkedin.com/in/nicola-balzano-1668a0272/")}>
                    <ListItemIcon> <img src={linkedin} alt='linkedin' width={'30px'} height={'30px'} /> </ListItemIcon>
                    <ListItemText primary='linkedin' />
                </ListItemButton>
            </List>
        </Box>
    );

    return (
        <div>
            {
                <React.Fragment key={'right'}>
                    <Button className='color-primary' onClick={toggleDrawer('right', true)}><MenuIcon/></Button>
                    <Drawer
                        anchor={'right'}
                        open={state['right']}
                        onClose={toggleDrawer('right', false)}
                    >
                        {list('right')}
                    </Drawer>
                </React.Fragment>
            }
        </div>
    );
}
export default Menu;
