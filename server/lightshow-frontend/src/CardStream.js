 /*eslint-env jquery*/
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Card } from 'material-ui/Card'
import Dialog from 'material-ui/Dialog';
import Slider from 'material-ui/Slider'
import Divider from 'material-ui/Divider'
import {Tabs, Tab} from 'material-ui/Tabs';
import Avatar from 'material-ui/Avatar';
import {List, ListItem} from 'material-ui/List';
import Chip from 'material-ui/Chip';
import ImageBrightness1 from 'material-ui/svg-icons/image/brightness-1';   
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
import IconButton from 'material-ui/IconButton';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import MoreVertIcon from 'material-ui/svg-icons/navigation/more-vert';
import {grey400} from 'material-ui/styles/colors';
import Subheader from 'material-ui/Subheader';
import Snackbar from 'material-ui/Snackbar';
import {blue300, blue900, red300, red900, green300, green900, purple300, purple900, pink300, pink900, teal300, teal900, orange300, orange900, pink200} from 'material-ui/styles/colors';
import axios from 'axios';

var webserver = "http://jesselupica.com/"

axios.defaults.baseURL = webserver;


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

const list_padding = {
  padding: 0,
}

const cardContainerStyle = {
  display: 'flex',
  flexWrap: 'wrap',
  marginTop: '12px',
  justifyContent: 'center',
}

const cardsStyle = {
  flexGrow: 1,
  flexShrink: 1,
  margin: '0 10px 12px',
  width: '100wh',
  minWidth: '100px',
  maxWidth: '500px',
}

const cardContentStyle = {
    padding: '12px',
}

function handleRequestDelete() {
  alert('You clicked the delete button.');
}

function handleChipClick(color) {
  alert('You clicked the ' + color.toLowerCase() + ' chip.');
}

function ColorChip(props) {
    var fg_color_pallets = {"Blue" : blue300, "Red" : red300, "Green" : green300, "Purple" : purple300, "Pink" : pink300, "Teal" : teal300, "Orange" : orange300};
    var bg_color_pallets = {"Blue" : blue900, "Red" : red900, "Green" : green900, "Purple" : purple900, "Pink" : pink900, "Teal" : teal900, "Orange" : orange900};
    return(<Chip
          backgroundColor={fg_color_pallets[props.color]}
          onClick={() => props.onClick(props.color)}
          style={styles.chip}
        >
        <Avatar size={32} color={fg_color_pallets[props.color]} backgroundColor={bg_color_pallets[props.color]}>
            <ImageBrightness1 color={fg_color_pallets[props.color]}/> 
        </Avatar>  
          {props.color}
        </Chip>)
}

/**
 * Examples of Chips, using an image [Avatar](/#/components/font-icon), [Font Icon](/#/components/font-icon) Avatar,
 * [SVG Icon](/#/components/svg-icon) Avatar, "Letter" (string) Avatar, and with custom colors.
 *
 * Chips with the `onRequestDelete` property defined will display a delete icon.
 */
class ColorChipWrapper extends React.Component {

  render() {
    return (
      <div style={styles.chipWrapper}>
        {this.props.colors.map((color, index) => 
            <ColorChip key={index} color={color} onClick={this.props.onClick}/>)}        
      </div>
    );
  }
}

class ControlSlider extends Component {
  render() {
    return (
      <div>
        <h2 style={styles.headline}>{this.props.title} </h2>
        <Slider value={this.props.sliderValue} onChange={this.props.onChange} />
      </div>
    );
  }
}

function removeDevice(device_id, auth_token) {
  var url = webserver + "device/remove/" + device_id
    axios.post(url, {
      auth_token : auth_token
    }).then( (res) => {
      window.location.reload();
    });
}


const iconButtonElement = (
  <IconButton
    touch={true}
    tooltip="more"
    tooltipPosition="bottom-left"
  >
    <MoreVertIcon color={grey400}/>
  </IconButton>
);
 


function rightIconMenu(props) {
  return (
    <IconMenu iconButtonElement={<IconButton><MoreVertIcon /></IconButton>}
              onChange={this.handleChangeSingle}
              value={this.state.valueSingle}
    >      
      <MenuItem onClick={() => removeDevice(props.device_id)} primaryText={"Remove Device"}/>
    </IconMenu>
  );
};

class DeviceInfoHeader extends React.Component {

  state = {
    open: false,
    nickname: '',
    renamed: false,
    snackbar_open: false,
  };

  handlePermissionDeniedSnackbar = () => {
    this.setState({
      snackbar_open: true,
    });
  };

  handleSnackbarRequestClose = () => {
    this.setState({
      snackbar_open: false,
    });
  };

  handleOpenRename = () => {
    this.setState({open: true});
  };

  handleCloseRenameCancel = () => {
    console.log("cancel")
    this.setState({open: false});
  };

  handleCloseRenameSubmit = (device_id) => {
    var url = webserver + "device/rename/" + device_id
    axios.post(url, {
        nickname: this.state.nickname,
        auth_token: this.props.auth.auth_token
      }).then( res => {
        this.setState({renamed: true});
      }).catch( error => {
        this.handlePermissionDeniedSnackbar();
      });
    this.setState({open: false});
  };

  updateNickname = (event, newObject) => {
    this.setState({nickname: newObject});
  }


    render() {

      const actions = [
        <FlatButton
          label="Cancel"
          primary={false}
          onClick={this.handleCloseRenameCancel}
        />,
        <FlatButton
          label="Submit"
          primary={true}
          keyboardFocused={true}
          onClick={() => {this.handleCloseRenameSubmit(this.props.device_id)}}
        />,
      ];


      return (
            <div>

      <List>
      <ListItem
        leftAvatar={<Avatar backgroundColor='white' src='http://www.glassblower.info/blog/wp-content/uploads/2013/04/raspberry-pi-logo-300-pixels.png' />}
        rightIconButton={
          <IconMenu iconButtonElement={<IconButton><MoreVertIcon /></IconButton>}
            onChange={this.handleChangeSingle}
            value={this.state.valueSingle}
          >      
            <MenuItem onClick={() => removeDevice(this.props.device_id, this.props.auth.auth_token)} primaryText={"Remove Device"}/>
          </IconMenu>
        }
        primaryText={this.state.renamed ? this.state.nickname : this.props.nickname}
        secondaryText={this.props.deviceType}
        onClick={this.handleOpenRename}
      />
    </List>
    <Dialog
        title="Rename Device?"
        actions={actions}
        modal={false}
        open={this.state.open}
        onRequestClose={this.handleCloseRenameCancel}
        autoScrollBodyContent={true}
      >
      <TextField
        hintText="New Device Name"
        value={this.state.nickname}
        fullWidth={true}
        onChange={this.updateNickname}
      /><br />
    </Dialog>
    <Snackbar
          open={this.state.snackbar_open}
          message="Sorry, you don't have permission to rename the device"
          autoHideDuration={4000}
          onRequestClose={this.handleSnackbarRequestClose}
        />
    </div>)
    }
}

class LightModeTabs extends React.Component {


  constructor(props) {
    super(props);
    const modes = {'VISUALIZE_MUSIC' : "vis", 
                  'STATIC_COLOR' : "static", 
                  'FADE' : "fade", 
                  'ASLEEP' : "off", 
                  'OFF' : "off", 
                  'CUSTOM_STATIC_COLOR' : "static"}
    const colors = ["Blue", "Green", "Red", "Purple", "Pink", "Teal", "Orange"]

    this.state = {
      value: modes[props.device.state.mode],
      device: this.props.device,
      colors: colors,
    };

  }

  handleChange = (value) => {
    this.setState({
      value: value,
    });
  };

  handleActive = (tab) => {
    this.setState({
      value: tab.props.value,
    });
    var mode_args = {}
    console.log(tab.props.value)
    if (tab.props.value  == 'vis') {
      mode_args = {'brightness' : this.state.device.state.value, 'sat' : this.state.device.state.saturation,}
    } else if (tab.props.value  == 'fade') {
      mode_args = {'fade_speed' : this.state.device.state.fade_speed}
    } else if (tab.props.value == 'static') {
      mode_args = {'color' : this.state.colors[Math.floor(Math.random()*this.state.colors.length)]}
    }

    axios.post("device/" + this.state.device.id, {
        command: {function: 'mode', args: [tab.props.value, mode_args]},
        auth_token: this.props.auth.auth_token
      }).then( () => {
        if (tab.props.value == 'static') {
          axios.get("device/" + this.state.device.id).then(res => {
            const device = res.data
            this.setState({ device : device });
        });
      }
    });
  }
  

  handleBriChange = (event, value) => {
    this.state.device.state.value = value
    this.setState({
      device: this.state.device
    });
    axios.post("device/" + this.state.device.id, {
        command: {function: 'brightness', args: [this.state.device.state.value]},
        auth_token: this.props.auth.auth_token
      })
  }

  handleSatChange = (event, value) => {
    this.state.device.state.saturation = value
    this.setState({
      device: this.state.device
    });
    axios.post("device/" + this.state.device.id, {
        command: {function: 'sat', args: [this.state.device.state.saturation]},
        auth_token: this.props.auth.auth_token
      })  
  }
  handleHueChange = (event, value) => {
    this.state.device.state.hue = value
    this.setState({
      device: this.state.device
    });
    axios.post("device/" + this.state.device.id, {
        command: {function: 'hue', args: [this.state.device.state.hue]},
        auth_token: this.props.auth.auth_token
      })  
  }

  handleSetStaticColor = (color) => {
    axios.post("device/" + this.state.device.id, {
        command: {function: 'static color', args: [color]},
        auth_token: this.props.auth.auth_token
      }).then( () => {
          axios.get("device/" + this.state.device.id).then(res => {
            const device = res.data
            this.setState({ device : device });
        });
      
    });
  }

  handleFadeSpeedChange = (event, value) => {
    this.state.device.state.fade_speed = value
    this.setState({
      device: this.state.device
    });
    axios.post("device/" + this.state.device.id, {
        command: {function: 'fade_speed', args: [this.state.device.state.fade_speed]},
        auth_token: this.props.auth.auth_token
      })  
  }

  render() {
    return (
      <Tabs style={cardContentStyle} value={this.state.value} onChange={this.handleChange}>
        <Tab label="Visualize" value="vis" onActive={this.handleActive}>
          <div>
            <ControlSlider title="Brightness" sliderValue={this.state.device.state.value} onChange={this.handleBriChange}/>
            <ControlSlider title="Saturation" sliderValue={this.state.device.state.saturation} onChange={this.handleSatChange}/>
          </div>
        </Tab>
        <Tab label="Fade" value="fade" onActive={this.handleActive}>
          <div>
            <ControlSlider title="Fade Speed" sliderValue={this.state.device.state.fade_speed} onChange={this.handleFadeSpeedChange}/>
          </div>
        </Tab>
        <Tab
          label="Static"
          data-route="/home"
          value="static"
          onActive={this.handleActive}
        >
          <div>
            <h2 style={styles.headline}>Preset Colors</h2>
            <ColorChipWrapper key="chips" colors={this.state.colors} onClick={this.handleSetStaticColor}/>
            <Divider style={cardContainerStyle}/>
            <ControlSlider title="Hue" sliderValue={this.state.device.state.hue} onChange={this.handleHueChange}/>
            <ControlSlider title="Brightness" sliderValue={this.state.device.state.value} onChange={this.handleBriChange}/>
            <ControlSlider title="Saturation" sliderValue={this.state.device.state.saturation} onChange={this.handleSatChange}/>
          </div>
        </Tab>
        <Tab label="Off" value="off" onActive={this.handleActive}>
        </Tab>
      </Tabs>
    );
  }
}

function LightSettingsCard(props) {
    var displayed_name = props.device.nickname !== "" ? props.device.nickname : props.device.id
    return (
        <Card style={cardsStyle}>
            <DeviceInfoHeader nickname={displayed_name} device_id={props.device.id} auth={props.auth} deviceType="Light Visualizer"/>
            <Divider/>
            <LightModeTabs device={props.device} auth={props.auth} accessDenied={props.accessDenied}/>
            </Card>
        )
}

class AdminHeader extends React.Component {
    render() {
      return (
        <div>
          <List>

            <ListItem
              leftAvatar={<Avatar backgroundColor={red300}>A</Avatar>}
              primaryText="Admin Settings"
              secondaryText={this.props.deviceType}
              disabled={true}/>
          </List>
        </div>)
    }
}

class AdminPrivilidgeListItem extends React.Component {
  ios_logo = "https://png.icons8.com/color/500/000000/ios-logo.png"
  android_logo = "https://upload.wikimedia.org/wikipedia/commons/d/d7/Android_robot.svg"
  osx_logo = "https://upload.wikimedia.org/wikipedia/commons/b/bb/OS_X_El_Capitan_logo.svg"
  windows_logo = "https://upload.wikimedia.org/wikipedia/commons/5/5f/Windows_logo_-_2012.svg"
  linux_logo = "https://assets.ubuntu.com/v1/29985a98-ubuntu-logo32.png"

  render() {
    return(
      <ListItem key={this.props.index} primaryText={this.props.user} leftAvatar={<Avatar backgroundColor='white' src={this.linux_logo}/>}/>
    )
  } 
}

class AdminPrivilidgeList extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      users: []
    };
  }

  componentDidMount() {
    var url = webserver + "admin/users" 
    axios.get(url, {
      params: {
        auth_token: this.props.auth.auth_token
      }
    }).then(res => {
        const users = res.data
        this.setState({ users });
      });
  }

  render() {
    return (
      <List>
        <Subheader>Active Users</Subheader>
          {this.state.users.map((user, index) =>
            <AdminPrivilidgeListItem index={index} user={user} />
          )}
      </List>
    )
  }
}

function AdminCard(props) {
  if(props.is_admin) {
    return(
    <div style={cardContainerStyle}>
      <Card style={cardsStyle}>
          <AdminHeader deviceType="Light Visualizer"/>
          <Divider/>
          <AdminPrivilidgeList auth={props.auth}/>
          <div>
            <RaisedButton label="Pull from Git"
            primary={false}
            fullWidth={true}
            backgroundColor={red300}
            onClick={ (events, value) => {
                props.devices.map(device => (
                  axios.post("device/" + device.id, { 
                    command: {"function": "git pull", "args": []}, 
                    auth_token: props.auth.auth_token
                  }
                )
                  ))}}/> 
          </div> 
      </Card>
    </div>
    )
  }
  else {
    return (<div></div>)
  }
  
}

export default class CardStream extends Component {

  static propTypes = {
    editMode: PropTypes.bool,
    removeItem: PropTypes.func,
    moveUpItem: PropTypes.func,
    moveDownItem: PropTypes.func
  }

  constructor(props) {
    super(props);

    this.state = {
      devices: [],
      is_admin: false,
      snackbar_open: false
    };
  }

  handlePermissionDeniedSnackbar = () => {
    this.setState({
      snackbar_open: true,
    });
  };

  handleSnackbarRequestClose = () => {
    this.setState({
      snackbar_open: false,
    });
  };

  componentDidMount() {
    var url = webserver + "devices"
    axios.get(url)
      .then(res => {
        const devices = res.data
        this.setState({ devices });
      });

    var admin_check = webserver + 'is_admin'
    // for some reason get requests don't transmit the data. 
    // So im lazy and making this a post
    axios.post(admin_check, {
      auth_token: this.props.auth.auth_token,
    }).then(res => {
        this.setState({ is_admin : true });
      }).catch( error => {
        console.log("we tried to get is admin")
      });

  }

  render() {
    console.log(this.props.auth)
    return (
      <div>
        <AdminCard devices={this.state.devices} auth={this.props.auth} is_admin={this.state.is_admin}/>
        <ul style={list_padding}>
          {this.state.devices.map(device =>
            <li key={device.id} style={cardContainerStyle}>
              <LightSettingsCard device={device} auth={this.props.auth} accessDenied={this.handlePermissionDeniedSnackbar}/>
            </li>
          )}
        </ul>
        <Snackbar
          open={this.state.snackbar_open}
          message="Sorry, you don't have permission to perform this action"
          autoHideDuration={4000}
          onRequestClose={this.handleSnackbarRequestClose}
        />
      </div>
    );    
  }
}
