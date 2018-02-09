import React, { Component } from 'react'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import AppBar from 'material-ui/AppBar';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect,
  withRouter
} from 'react-router-dom'
import axios from 'axios';

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
  margin: 12,
};


function hello() {
  console.log("hello")
}

export default class LoginScreen extends React.Component {
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
                    <div style={{width: '45%', }}>
                        <RaisedButton label="Login" primary={true}  fullWidth={true} style={style} />
                    </div>
                    <div style={{width: '45%', }}>
                        <RaisedButton label="Sign up" onClick={this.props.signupClick} primary={true} fullWidth={true} style={style} />
                    </div>
                    <RaisedButton onClick={this.props.guestClick} label={"Continue as guest"} primary={true} fullWidth={true}  style={style} />
                </div>
            </Card>
        </div>
        </div>
        </MuiThemeProvider>
    </div>);
  }
}