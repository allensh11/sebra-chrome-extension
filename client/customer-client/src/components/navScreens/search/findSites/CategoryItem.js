import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import ShareIcon from '@material-ui/icons/Share';
import CreditCardIcon from '@material-ui/icons/CreditCard';
import MailOutlineIcon from '@material-ui/icons/MailOutline';
import SmartphoneIcon from '@material-ui/icons/Smartphone';


const useStyles = makeStyles(theme => ({
    listItemAvatar: {
        minWidth: '45px'
    },
    avatar: {
        fontSize: '20px',
        width: '30px',
        height: '30px'
    },
    listItemText:{
        fontSize:'12px'
    }
}));

const CategoryItem = ({ name }) => {
    const classes = useStyles();

    let iconComponent = null;
    if(name === 'Trending Sites') iconComponent = <ShareIcon fontSize='inherit'/>;
    else if(name === 'Money') iconComponent = <CreditCardIcon fontSize='inherit'/>;
    else if(name === 'Productivity') iconComponent = <MailOutlineIcon fontSize='inherit'/>;
    else if(name === 'Technology') iconComponent = <SmartphoneIcon fontSize='inherit'/>;
    
    return(
        <ListItem>
            <ListItemAvatar className={classes.listItemAvatar}>
                <Avatar className={classes.avatar}>
                    { iconComponent }
                </Avatar>
            </ListItemAvatar>
            <ListItemText classes={{ primary: classes.listItemText }} primary={name}/>
        </ListItem>
    )
}


export default CategoryItem;