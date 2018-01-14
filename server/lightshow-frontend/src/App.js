import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import CardStream from './CardStream';
import AppBar from 'material-ui/AppBar';


class App extends Component {
  render() {
    return (
      <div className="App">
          <MuiThemeProvider>
           <AppBar
              title="Lightshow"
              iconClassNameRight="muidocs-icon-navigation-expand-more"
            />
          </MuiThemeProvider>
          <MuiThemeProvider>
          <CardStream items={["Brightness","Hue","Contrast"]}/>
          </MuiThemeProvider>
      </div>
    );
  }
}

export default App;
