import React, { Component } from 'react'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import AppBar from 'material-ui/AppBar';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import axios from 'axios';
import md5 from 'md5';

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

const style1 = {
  margin: '0px 0px',
};

const style2 = {
  margin: '12px 0px',
};

export default class Signin extends React.Component {
  constructor(props) {
    super(props)
        console.log(this.props.history)

    this.state = {
      username: '',
      password: '',
      usernameErrorMessage: '',
      passErrorMessage: '',
    }
  }

  update_pass = (event, newValue) => {
    console.log(newValue)
    this.setState({password: newValue})
  }

  update_username = (event, newValue) => {
    console.log(newValue)
    this.setState({username: newValue})

  }

  authenticate_user = () => {

    const url = 'http://jesselupica.com/auth/verify';
    axios.post(url, {
        username: this.state.username,
        password: md5(this.state.password),
      }).then( (res) => {
          if(res.status == 200 ) {
            this.props.auth.isAuthenticated = true
            this.props.auth.auth_token = res.data
            console.log(this.props.history)
            this.props.history.push("/lights");
          } else {
            console.log("why u like dis?")
            this.props.auth.isAuthenticated = false
            this.setState({passErrorMessage: 'The username or password you entered is not valid'})
            this.setState({usernameErrorMessage: ' '})
          }
        }).catch( (res) => {
          console.log("why u like dis 2?")
          console.log("error")
          this.setState({passErrorMessage: 'The username or password you entered is not valid'})
          this.setState({usernameErrorMessage: ' '})
        });
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
                <CardTitle title="Lightshow Login" titleStyle={{'fontFamily': 'HelveticaNeue-Light','fontSize': 30, textAlign: 'center', marginTop: '30px', fontWeight: 20}}/>
                <div style={buttonContainerStyle}>
                    <TextField floatingLabelText="Username" fullWidth={true} style={style1} onChange={this.update_username} errorText={this.state.usernameErrorMessage}/>
                    <TextField floatingLabelText="Password" type="password" fullWidth={true} style={style2} onChange={this.update_pass} errorText={this.state.passErrorMessage}/>
                    <RaisedButton onClick={this.authenticate_user} label={"Log in"} primary={true} fullWidth={true}  style={style2} />
                </div>
              <div style={{height: '50px'}}/>
            </Card>
        </div>
        </div>
        </MuiThemeProvider>
    </div>);
  }
}