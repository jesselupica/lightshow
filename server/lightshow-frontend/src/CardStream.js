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
import {blue300, blue900, red300, red900, green300, green900, purple300, purple900, pink300, pink900, teal300, teal900, orange300, orange900} from 'material-ui/styles/colors';
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

function removeDevice(device_id) {
  var url = webserver + "device/remove/" + device_id
    axios.post(url).then( (res) => {
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
        nickname: this.state.nickname
      });
    this.setState({open: false, renamed: true});
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
            <MenuItem onClick={() => removeDevice(this.props.device_id)} primaryText={"Remove Device"}/>
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
        command: {function: 'mode', args: [tab.props.value, mode_args]}
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
        command: {function: 'brightness', args: [this.state.device.state.value]}
      })
  }

  handleSatChange = (event, value) => {
    this.state.device.state.saturation = value
    this.setState({
      device: this.state.device
    });
    axios.post("device/" + this.state.device.id, {
        command: {function: 'sat', args: [this.state.device.state.saturation]}
      })  
  }

  handleHueChange = (event, value) => {
    this.state.device.state.hue = value
    this.setState({
      device: this.state.device
    });
    axios.post("device/" + this.state.device.id, {
        command: {function: 'hue', args: [this.state.device.state.hue]}
      })  
  }

  handleSetStaticColor = (color) => {
    axios.post("device/" + this.state.device.id, {
        command: {function: 'static color', args: [color]}
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
        command: {function: 'fade_speed', args: [this.state.device.state.fade_speed]}
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
            <DeviceInfoHeader nickname={displayed_name} device_id={props.device.id} deviceType="Light Visualizer"/>
            <Divider/>
            <LightModeTabs device={props.device}/>
            </Card>
        )
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
      devices: []
    };
  }

  componentDidMount() {
    var url = webserver + "devices"
    axios.get(url)
      .then(res => {
        const devices = res.data
        this.setState({ devices });
      });
  }

  render() {
    return (
      <div>
        <ul style={list_padding}>
          {this.state.devices.map(device =>
            <li key={device.id} style={cardContainerStyle}>
              <LightSettingsCard device={device}/>
            </li>
          )}
        </ul>
      </div>
    );    
  }
}
