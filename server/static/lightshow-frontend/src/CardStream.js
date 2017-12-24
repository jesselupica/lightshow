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
import MoreVertIcon from 'material-ui/svg-icons/navigation/more-vert';
import {grey400} from 'material-ui/styles/colors';
import {blue300, blue900, red300, red900, green300, green900, purple300, purple900, pink300, pink900, teal300, teal900, orange300, orange900} from 'material-ui/styles/colors';

var websocket = new WebSocket("ws://localhost:5001");

websocket.onopen = function(evt) { 
    console.log("we have opened");
}; //on open event
websocket.onmessage = function(str) {
  console.log("Someone sent: ", str);
};


function sendAMessage() {
    // Tell the server this is client 1 (swap for client 2 of course)
    websocket.send(JSON.stringify({
      id: "client1"
    }));
    // Tell the server we want to send something to the other client
    websocket.send(JSON.stringify({
      to: "client2",
      data: "foo"
    }));
}




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

function handleClick() {
  alert('You clicked the Chip.');
}

function ColorChip(props) {
    var fg_color_pallets = {"Blue" : blue300, "Red" : red300, "Green" : green300, "Purple" : purple300, "Pink" : pink300, "Teal" : teal300, "Orange" : orange300};
    var bg_color_pallets = {"Blue" : blue900, "Red" : red900, "Green" : green900, "Purple" : purple900, "Pink" : pink900, "Teal" : teal900, "Orange" : orange900};
    return(<Chip
          backgroundColor={fg_color_pallets[props.color]}
          onClick={sendAMessage}
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
            <ColorChip key={index} color={color}/>)}        
      </div>
    );
  }
}

class ControlSlider extends Component {
  state = {
    sliderValue: 0.5,
  };

  handleSliderChange = (event, value) => {
    this.setState({firstSlider: value});
  };

  render() {
    return (
      <div>
        <h2 style={styles.headline}>{this.props.title} </h2>
        <Slider value={this.state.sliderValue} onChange={this.handleSliderChange} />
      </div>
    );
  }
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


const rightIconMenu2 = (
  <IconMenu iconButtonElement={iconButtonElement}>
    <MenuItem>Rename Device</MenuItem>
  </IconMenu>
);

function DeviceInfoHeader(props) {
    return (<List>
      <ListItem
        leftAvatar={<Avatar backgroundColor='white' src='http://www.glassblower.info/blog/wp-content/uploads/2013/04/raspberry-pi-logo-300-pixels.png' />}
        rightIconButton={rightIconMenu2}
        primaryText={props.nickname}
        secondaryText={props.deviceType}
      />
    </List>)
}

const LightModeTabs = () => (
  <Tabs style={cardContentStyle}>
    <Tab label="Visualize" >
      <div>
        <ControlSlider title="Brightness" />
        <ControlSlider title="Saturation" />
      </div>
    </Tab>
    <Tab label="Fade" >
      <div>
        <ControlSlider title="Fade Speed" />
      </div>
    </Tab>
    <Tab
      label="Static"
      data-route="/home"
    >
      <div>
        <h2 style={styles.headline}>Preset Colors</h2>
        <ColorChipWrapper colors={["Blue", "Green", "Red", "Purple", "Pink", "Teal", "Orange"]}/>
      </div>
    </Tab>
    <Tab label="Off">
    </Tab>
  </Tabs>
);

function LightSettingsCard(props) {
    return (
        <Card style={cardsStyle}>
            <DeviceInfoHeader nickname="Jesse's Bedroom Pi" deviceType="Light Visualizer"/>
            <Divider/>
            <LightModeTabs/>
            </Card>
        )
}

export default class CardStream extends Component {
  static propTypes = {
    items: PropTypes.arrayOf(PropTypes.node).isRequired,
    editMode: PropTypes.bool,
    removeItem: PropTypes.func,
    moveUpItem: PropTypes.func,
    moveDownItem: PropTypes.func
  }

  render() {
    return (
      <div style={cardContainerStyle}>
          <LightSettingsCard items={this.props.items}/>
      </div>
    )
  }
}
