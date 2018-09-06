import React from 'react';
import PropTypes from 'prop-types';
import Avatar from '@material-ui/core/Avatar';
import CssBaseline from '@material-ui/core/CssBaseline';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import withStyles from '@material-ui/core/styles/withStyles';
import GoogleLogin from 'react-google-login';


const styles = theme => ({
  layout: {
    width: 'auto',
    display: 'block', // Fix IE11 issue.
    marginLeft: theme.spacing.unit * 3,
    marginRight: theme.spacing.unit * 3,
    [theme.breakpoints.up(400 + theme.spacing.unit * 3 * 2)]: {
      width: 400,
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
  paper: {
    marginTop: theme.spacing.unit * 8,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: `${theme.spacing.unit * 2}px ${theme.spacing.unit * 3}px ${theme.spacing.unit * 3}px`,
  },
  avatar: {
    backgroundColor: theme.palette.primary.main,
  },
  typography : {
  	marginTop: theme.spacing.unit * 3,
  },
  form: {
    marginTop: theme.spacing.unit * 4,
  },
  submit: {
    marginTop: theme.spacing.unit * 3,
  },
});


class SignInCard extends React.Component {
	constructor(props) {
    	super(props); 
    	console.log(this.props)
    	this.onSignIn = this.onSignIn.bind(this);
	}

	onSignIn(googleUser) {
	  const profile = googleUser.getBasicProfile();
	  console.log(this.props)
	  this.props.auth.profile = googleUser.getBasicProfile();
	  this.props.auth.isAuthenticated = true;
	  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
	  console.log('Name: ' + profile.getName());
	  console.log('Image URL: ' + profile.getImageUrl());
	  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
	  this.props.login();
	  console.log("signed")
	}


	 render() {
	  const { classes } = this.props;

	  return (
	    <React.Fragment>
	      <CssBaseline />
	      <main className={classes.layout}>
	        <Paper className={classes.paper}>
	          <Avatar className={classes.avatar}>
		       L   
		      </Avatar>
	          <Typography variant="headline" className={classes.typography}>One Account. All of Lightshow.</Typography>
	          <form className={classes.form}>
				<GoogleLogin
				    clientId="494838513648-oci760cft84811ttcpmahjvndo19a56o.apps.googleusercontent.com"
				    buttonText="Login with Google"
				    onSuccess={this.onSignIn}
				  />          
				  </form>
	        </Paper>
	      </main>
	    </React.Fragment>
	  );
	}
}

SignInCard.propTypes = {
	classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SignInCard);

