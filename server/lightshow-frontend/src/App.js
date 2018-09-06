import React from 'react';
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles';
import blue from '@material-ui/core/colors/blue';
import orange from '@material-ui/core/colors/orange';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Routes from './Routes'
import CardStream from './CardStream'

const theme = createMuiTheme({
  palette: {
    primary: blue,
    secondary: orange,
  },
});

export default class App extends React.Component {
  constructor(props) {
      super(props); 
      console.log(this.props)
  }

  componentDidMount() {
    const s = document.createElement('script');
    s.async = true;
    s.src = "https://apis.google.com/js/platform.js";
    document.head.appendChild(s);
    const m = document.createElement('meta');
    m.name ="google-signin-client_id";
    m.content="494838513648-cas9l973201ht48gb9pgo0p1j2elql5c.apps.googleusercontent.com";
    document.head.appendChild(m);
  }

  render() {
    return (
      <MuiThemeProvider theme={theme}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="title" color="inherit">
            Lightshow
          </Typography>
        </Toolbar>
      </AppBar>
      <Routes component={CardStream}/>
      </MuiThemeProvider>)
  }
}
  
