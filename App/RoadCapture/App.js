import React, {useState} from 'react';
import {View, StyleSheet, Text, TouchableOpacity, PermissionsAndroid, TextInput, BackHandler, Switch} from 'react-native';
import { RNCamera } from 'react-native-camera';
import {useCamera} from 'react-native-camera-hooks'
import Icon from 'react-native-vector-icons/FontAwesome';
import Icon2 from 'react-native-vector-icons/Ionicons';

import RNFS from 'react-native-fs'
import Geolocation from '@react-native-community/geolocation';
import Slider from '@react-native-community/slider';
import NetInfo from "@react-native-community/netinfo";

const App = () => {
  const [{cameraRef},{takePicture}] = useCamera(null);
  const [locPermission, setLocPermission] = useState(false);
  const [playIndicator, setPlayIndicator] = useState("play-circle");
  const [connectionIndicator, setConnectionIndicator] = useState({color:"green", text:"Connected"});
  const [settinged, setSettinged] = useState(false);
  const [suggestedRoad, setSuggestedRoad] = useState("");
  const [captureFrequency, setCaptureFrequency] = useState(2);
  const [intervalStatus, setIntervalStatus] = useState({shooting:false, interval:null});
  const [testing, setTesting] = useState(false);
  const [location, setLocation] = useState({
    latitude: 0,
    longitude: 0
  });
  var flag = false, interval = null

  const captureHandle = async () => {
    console.log("Capturing");
    try{
      let posAllowed = locPermission
      posAllowed = await getPosition()
      if(!posAllowed){
        setLocPermission(posAllowed)
      }
      
      const data = await takePicture({quality: 0.5, maxWidth: 224, maxHeight: 124});
      await RNFS.readFile(data.uri, "base64")
      .then(async (res) => 
        await fetch('http://192.168.8.108:5000/predict',{
          method:'post',
          headers:{
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body:JSON.stringify({
            image:res.replace("data:image/jpg;base64,",""),
            longitude: location.longitude,
            latitude: location.latitude,
            testing:testing,
            action:"app"
          })
        }).then(response => response.json()).then(data=>console.log(data))
      )
    }
    catch(error){console.log(error)}
  }
  const doCapture = async () => {
    if(intervalStatus.shooting){
      clearInterval(intervalStatus.interval)
      setIntervalStatus({shooting:false, interval:null})
      setPlayIndicator("play-circle")
    }
    else{
      setIntervalStatus({shooting:true, interval:setInterval(()=>{captureHandle()},captureFrequency*1000)})
      setPlayIndicator("pause-circle")
    }
  }

  const getPosition = async () => {
    var allowed = await askPermissionForLocation()
    if(!allowed)return

    await Geolocation.getCurrentPosition(
      pos => {
        setLocation({
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude
        })
        return true
      },
      e => () => {return false}
    );
  };

  const askPermissionForLocation = async () => {
    try {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
        {
          title: 'Location Permission',
          message:
            'This App needs access to your location ' +
            'so you can find your current location.',
          buttonNeutral: 'Ask Me Later',
          buttonNegative: 'Cancel',
          buttonPositive: 'OK',
        },
      );
      if (granted === PermissionsAndroid.RESULTS.GRANTED) return true 
      else return false
    } 
    catch (err) {return false}
  };

  BackHandler.addEventListener(
    "hardwareBackPress",
    ()=>{
        if(settinged){
          setSettinged(false)
          return true
        }
        else return true
    }
  );
  NetInfo.addEventListener(networkState => {
    if((networkState.isConnected&&connectionIndicator.color==="red")||(!networkState.isConnected&&connectionIndicator.color==="green")){
      setConnectionIndicator({color:networkState.isConnected?"green":"red", text:networkState.isConnected?"Connected":"Disconnected"})
    }
  })

  askPermissionForLocation()

  const toggleSwitch = () => setTesting(!testing);

  if(!settinged)
    return (
      <View style={styles.container} >
        <View style={styles.indictorBarBg}></View>
        <View style={styles.indictorBar}>
          <Icon name="circle" size={20} color={connectionIndicator.color} />
          <Text>  {connectionIndicator.text}</Text>
        </View>
        <RNCamera
            ref={cameraRef}
            style={styles.preview}
            type={RNCamera.Constants.Type.back}
            autoFocus={RNCamera.Constants.AutoFocus.on}
            captureAudio={false}
            androidCameraPermissionOptions={{
              title: 'Permission to use camera',
              message: 'We need your permission to use your camera',
              buttonPositive: 'Ok',
              buttonNegative: 'Cancel',
            }}>
              <View style={styles.cameraBottom}>
                <View style={styles.bottomsChildBg} />
                <View style={styles.bottomsChildMain}>
                  <TouchableOpacity style={styles.bottomButtons} >
                    <Text><Icon2 name="refresh" size={30} color='white'  /></Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.bottomButtons} onPress={doCapture}>
                    <Text><Icon name={playIndicator} size={80} color='white' /></Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.bottomButtons} 
                    onPress={
                      async ()=>{
                        setSettinged(true)
                        if(intervalStatus.shooting)await doCapture()
                      }}>
                    <Text><Icon name="gear" size={33} color='white'/></Text>
                  </TouchableOpacity>
                </View>
              </View>
          </RNCamera>
      </View>
    );
  else
    return (
      <View style={settingStyles.container}>
        <Text style={{color:"black", fontSize:40, fontWeight:'bold'}} >Settings</Text>
        <View style={settingStyles.item}></View>
        <View style={settingStyles.item}>
          <Text style={{color:'black', fontSize:20, fontWeight:'bold'}} >Capture Frequency</Text>
          <Slider
              style={{width: '105%', height: 50, position:'relative', left:-10}}
              minimumValue={2}
              maximumValue={10}
              minimumTrackTintColor="blue"
              maximumTrackTintColor="gray"
              onValueChange={val=>setCaptureFrequency(Math.floor(val==0?2:val))}
            />
            <Text style={{color:'red'}} >{captureFrequency+" seconds"}</Text>
        </View>
        <View style={settingStyles.item}>
          <Text style={{color:'black', fontSize:20, fontWeight:'bold'}} >User suggested road</Text>
          <TextInput style={settingStyles.input} onChangeText={val=>setSuggestedRoad(val)} value={suggestedRoad} />
        </View>
        <View style={settingStyles.item}>
          <Text style={{color:'black', fontSize:20, fontWeight:'bold'}} >Demo mode</Text>
          <Switch
            trackColor={{ false: "#767577", true: "#81b0ff" }}
            thumbColor={testing ? "#f5dd4b" : "#f4f3f4"}
            ios_backgroundColor="#3e3e3e"
            onValueChange={toggleSwitch}
            value={testing}
            style={{
              left:5,
              width:'10%',
            }}
          />
        </View>
        {/* <View style={settingStyles.item}>
          <TouchableOpacity>
            <Text style={{color:'black', fontSize:20, fontWeight:'bold'}} >Flush Buffer</Text>
          </TouchableOpacity>
        </View> */}
        <View style={settingStyles.item}>
          <TouchableOpacity>
            <Text style={{color:'red', fontSize:20, fontWeight:'bold'}} >Logout</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
};

const settingStyles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'flex-start',
    padding:10,
    paddingTop: 50,
  },
  item:{
    paddingTop:20,
    paddingBottom:20,
    borderBottomWidth:1,
    borderBottomColor:'#c2c0c0',
    width:'100%',
  },
  input:{
    width:'100%', 
    height:50, 
    borderColor:'gray', 
    color:'black',
    borderWidth:1, 
    borderRadius:7, 
    padding:10,
    marginTop:10
  }
});


const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: 'black',
  },
  indictorBarBg:{
    padding:10,
    backgroundColor:'cyan',
    opacity:0.15,
    height:40,
  },
  indictorBar:{
    position:'absolute',
    padding:10,
    height:40,
    flexDirection:'row',
  },
  preview: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
  },
  cameraBottom:{
    flex: 0.30,
    justifyContent:'center',
    alignItems:'center',
    width: '100%',
  },
  bottomsChildBg:{
    width:100,
    height:100, 
    backgroundColor:'cyan',
    justifyContent:'center',
    alignItems:'center',
    width: '70%',
    borderRadius:50,
    opacity:0.15,
  },
  bottomsChildMain:{
    position:'absolute',
    flex:1,
    flexDirection:'row',
    justifyContent:'space-between',
    alignItems:'center',    
  },
  bottomButtons:{
    elevation:5, // Android
    borderRadius:50,
    shadowColor: 'black',
    shadowRadius: 10,
    margin:20,
  },
  img:{
    width:100,
    height:100,
  }
});

export default App;