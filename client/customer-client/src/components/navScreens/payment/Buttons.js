import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { updateOrder } from '../../../store/actions/orders';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';


const useStyles = makeStyles(theme => ({
    button: {
      width: '202px',
      height: '56px',
      marginTop: '60px',
      fontSize: '13px',
      padding: '10px 20px'
    },
    redirectLink: {
      textDecoration: 'none',
      color: 'white'
    }
}))


const Buttons = ({ pathname, history, params, setOpen, setLoading, setError }) => {
    const classes = useStyles();
    const dispatch = useDispatch();

    const auth = useSelector(store => store.auth);

    let itemUrl = null;
    if(params && params.itemUrl) itemUrl = 'https://' + params.itemUrl;
  
    const handlePayClick = e => {
        e.preventDefault();
        setOpen(true);
        setLoading(true);
        return (
          dispatch(updateOrder(auth, history, params))
            .then(() => setLoading(false))
            .catch(() => {
              setLoading(false);
              setError('Payment error!');
            })
        )
    }

    const handleSearchClick = () => history.push('/account/search');
    
    return (
      itemUrl   
        ? pathname !== '/payment-completed' 
          ? <Button onClick={handlePayClick} className={classes.button} variant="contained" color="primary" >
              Pay with Libra
            </Button>
          : <a className={classes.redirectLink} href={ itemUrl } rel="noopener noreferrer" target="_blank">
              <Button className={classes.button} variant="contained" color="primary" >
                  Proceed to Article!
              </Button>
            </a>
        : <Button onClick={handleSearchClick} className={classes.button} variant="contained" color="primary" >
              Click here to search
          </Button>
    )
}


export default Buttons;