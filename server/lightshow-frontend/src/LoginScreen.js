import React, { Component } from 'react'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import AppBar from 'material-ui/AppBar';
import {Card, CardHeader, CardTitle, CardText} from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
import axios from 'axios';
import FacebookLogin from 'react-facebook-login';


const styles = {
  headline: {
    fontSize: 24,
    paddingTop: 16,
    marginBottom: 12,
    fontWeight: 400,
    },
  chip: {
    margin: 4,
  },
  chipWrapper: {
    display: 'flex',
    flexWrap: 'wrap',
  },
};

const cardContainerStyle = {
  display: 'flex',
  flexWrap: 'wrap',
  marginTop: '12px',
  justifyContent: 'center',
}

const buttonContainerStyle = {
  display: 'flex',
  flexWrap: 'wrap',
  marginTop: '12px',
  minWidth: '200px',
  maxWidth: '400px',
  justifyContent: 'space-between',
  marginLeft: 'auto',
   marginRight: 'auto',
  paddingRight: 10,
  paddingLeft: 10,
  border: '0px'
}

const cardsStyle = {
  flexGrow: 1,
  flexShrink: 1,
  margin: '0 10px 12px',
  width: '100wh',
  minWidth: '100px',
  maxWidth: '500px',
  minHeight: '300px',
}

const cardContentStyle = {
    padding: '12px',
}

const style = {
  margin: "12px 0px",
  /*minWidth: '20%'*/
};

export default class LoginScreen extends React.Component {

  constructor(props) {
    super(props)
        console.log("this is the history" + this.props.history)

    this.state = {
      username: '',
      password: '',
      usernameErrorMessage: '',
      passErrorMessage: '',
    }
  }


  responseFacebook(response, history) {
    console.log(response);

    //this.props.auth.isAuthenticated = true
    //this.props.auth.auth_token = response
    history.push("/lights");
  }

    render() {
    return (<div>
      <MuiThemeProvider>
      <div>
     <AppBar
        title="Lightshow"
        iconClassNameRight="muidocs-icon-navigation-expand-more"
      />
        <div style={cardContainerStyle}>
            <Card style={cardsStyle}>
                <CardTitle title="One Account. All of Lightshow" titleStyle={{'fontFamily': 'HelveticaNeue-Light','fontSize': 30, textAlign: 'center', marginTop: '30px', fontWeight: 20}}/>
                <div style={{height: 30}}/>
                <div style={buttonContainerStyle}>
                    <FacebookLogin
                      appId="416422595462913"
                      autoLoad={true}
                      cookie={true}
                      fields="name,email,picture"
                      callback={(resp) => {this.responseFacebook(resp, this.props.history)}} />
                </div>
            </Card>
        </div>
        </div>
        </MuiThemeProvider>
    </div>);
  }
}