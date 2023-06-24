import React from 'react';
import Button from '@mui/material/Button'; // Import Button component from @mui/material
import { Link } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';



const Navbar = () => {
    return (
        <AppBar position="static">
            <Toolbar>
                <Button color="inherit" component={Link} to="/DailyReport">Create Daily Report</Button>

            </Toolbar>
        </AppBar>
    );
};

export default Navbar;