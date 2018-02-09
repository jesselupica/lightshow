import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import CardStream from './CardStream';
import LoginScreen from './LoginScreen'
import Signup from './Signup' 
import AppBar from 'material-ui/AppBar';
import ClientJS from 'clientjs/dist/client.min.js';
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect,
  withRouter,
  Switch,
} from 'react-router-dom'
import axios from 'axios';

const base_url = 'http://jesselupica.com/';

function setCookie(cname, cvalue) {
    var d = new Date();
    document.cookie = cname + "=" + cvalue + ";" + "path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
  }

const userAuth = {
  isAuthenticated: false,
  callbacks: [],
  registerChange(fn) {
    this.callbacks.push(fn);
  },
  callCallbacks() {
    this.callbacks.forEach(cb => cb(this));
  },

  auth_token: null, 

  authenticate(cb) {
    var username = getCookie('username')
    this.auth_token = getCookie('auth')
    console.log("b")

    if (this.auth_token != "" && username != '') {
      var url = base_url + 'auth/validate'
      axios.get(url, {
        auth_token: this.auth_token,
        username: username,
      }).then( (res) => {
          console.log(res.status)
          if(res.status == 200 ) {
            this.isAuthenticated = true
            this.callCallbacks();
          } else {
            this.isAuthenticated = false
            this.callCallbacks();
          }
        }).catch( (res) => {
          console.log("error")
          this.isAuthenticated = false
          this.callCallbacks();
        });
    }
    cb()
  },

  guestAuthenticate(cb) {
    this.auth_token = getCookie('auth')
    if (this.auth_token != '') {
      var url = base_url + 'auth/guest/' + this.auth_token
      axios.get(url).then( (res) => {
        this.isAuthenticated = true
      }).catch((res) => {
        this.isAuthenticated = false
      })
    } 
    else {
      var client = new ClientJS();
      var url = base_url + 'auth/guest/init'
        axios.get(url, {
          os: client.getOS(),
          browser: client.getBrowser()
        }).then( (res) => {
            console.log(res.status)
            if(res.status == 200 ) {
              this.auth_token = res.data
              setCookie('auth', this.auth_token)
              this.isAuthenticated = true
              this.callCallbacks();
            } else {
              this.isAuthenticated = false
              this.callCallbacks();
            }
          }).catch( (res) => {
            console.log("error")
            this.isAuthenticated = false
            this.callCallbacks();
          });
    }
    
  },

  signout(cb) {
    this.isAuthenticated = false
    cb()
  },

  signup(cb) {
    var url = base_url + 'auth/init'
  }
}

const Home = () => (
  <div className="App">
    <MuiThemeProvider>
     <AppBar
        title="Lightshow"
        iconClassNameRight="muidocs-icon-navigation-expand-more"
      />
    <CardStream auth={userAuth}/>
    </MuiThemeProvider>
  </div>
)

const PrivateRoute = ({ component: Component, ...rest }) => (
  <Route {...rest} render={(props) => (
    userAuth.isAuthenticated === true
      ? <Component {...props} />
      : <Redirect to='/' />
  )} />
)


////////////////////////////////////////////////////////////
// 1. Click the public page
// 2. Click the protected page
// 3. Log in
// 4. Click the back button, note the URL each time

const App = () => (
    <Router>
      <div>
        <Switch>
          <Route exact path='/' component={Login} auth={userAuth}/>
          <Route path='/signup' component={Signup} />
          <PrivateRoute path='/lights' component={Home}/>
        </Switch>
        </div>
    </Router> 
)

class Login extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      redirectToReferrer: userAuth.isAuthenticated,
      redirectToSignin: false
    }
    userAuth.registerChange((auth) => this.setState({redirectToReferrer: auth.isAuthenticated}))
    userAuth.authenticate(() => {})
    console.log("hello")
  }

  loginAsGuest = () => {
    userAuth.guestAuthenticate(() => {})
  }

  signUp = () => {
    userAuth.signup(() => {})
  }

  userLogin = () => {
    this.setState({redirectToSignin: true})
  }

  render() {  

    if( this.state.redirectToSignin) {
      return (
        <Redirect to={"/signup"}/>
      )
    }

    if (this.state.redirectToReferrer) {
      return (
        <Redirect to={"/lights"}/>
      )
    }
    
    return (
      <div>
      <MuiThemeProvider>
        <LoginScreen guestClick={this.loginAsGuest} signupClick={this.userLogin}/>
      </MuiThemeProvider>
      </div>
    )
  }
}



export default App;
