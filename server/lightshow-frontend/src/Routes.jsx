import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Redirect,
} from 'react-router-dom'
import SigninCard from './SigninCard';

const googleAuth = {
	isAuthenticated: false,
	profile: null,
}

const Public = () => <h3>Public</h3>
const Protected = () => <h3>Protected</h3>

class Login extends React.Component {
  constructor(props) {
    	super(props); 
    	console.log(this.props)
  }	
  state = {
    redirectToReferrer: false
  }
  login = () => {
    this.setState(() => ({
        redirectToReferrer: true
      })
    );
  }

  render() {
    const { from } = this.props.location.state || { from: { pathname: '/' } }
    const { redirectToReferrer } = this.state

    if (redirectToReferrer === true) {
      return <Redirect to='/lights' />
    }

    return (
       <SigninCard auth={googleAuth} login={this.login}/>
    )
  }
}

const PrivateRoute = ({ component: Component, auth=auth , ...rest }) => (
  <Route {...rest} render={(props) => (
    googleAuth.isAuthenticated === true
      ? <Component auth={auth} {...props} />
      : <Redirect to={{
          pathname: '/',
          state: { from: props.location }
        }} />
  )} />
)

export default function Routes (props) {
  return (
    <Router>
      <div>
        <Route path="/" component={Login}/>
        <PrivateRoute path='/lights' component={props.component} auth={googleAuth} />
      </div>
    </Router>
  )
}