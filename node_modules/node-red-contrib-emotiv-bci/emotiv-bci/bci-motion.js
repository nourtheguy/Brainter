// Require authentication token from bci-login node
// connect to headset (via Emotiv Universal Dongle) then
// output motion data

module.exports = function(RED) {
  "use strict";
  let bciLib = require("./bci-lib");
  let config = require("./bci-config");

  function MotionNode(n) {
    RED.nodes.createNode(this, n);

    let node = this;
    let metric = parseInt(n.metric, 10);
    let auth = "";
    let stream = config.stream;

    let motionName = [
      "Quaternions 0",
      "Quaternions 1",
      "Quaternions 2",
      "Quaternions 3",
      "Acceleration, X axis",
      "Acceleration, Y axis",
      "Acceleration, Z axis",
      "Magnetometer, X axis",
      "Magnetometer, Y axis",
      "Magnetometer, Z axis",
      "Gyroscope, X axis",
      "Gyroscope, Y axis",
      "Gyroscope, Z axis"
    ];

    function startconn() {
      // Connect to remote endpoint
      node.tout = null;
      node.socket = node.context().global.get("socket");
      handleConnection();
    }

    function handleConnection() {
      node.socket.on("open", function() {
        // create a cortex session
        node.status({
          fill: "white",
          shape: "ring",
          text: "Connecting ..."
        });
      });

      node.socket.on("close", function() {
        node.status({
          fill: "red",
          shape: "ring",
          text:
            "Please ensure that you have Cortex installed and running in the background."
        });
        if (!node.closing) {
          clearTimeout(node.tout);
          node.tout = setTimeout(function() {
            startconn();
          }, 3000);
        }
      });

      node.socket.on("message", function(data) {
        let msg = JSON.parse(data);
        if (!!msg.id && !!msg.error) {
        } else {
          if (!!msg.mot) {
            const headsetInfo = node.context().global.get("headsetInfo")
            const isMN8 = headsetInfo.id.toLowerCase().includes('mn8')
            let outputMotionArr = new Array(9).fill(0);
            let cortexMotionArr = msg.mot.slice(2, msg.mot.length); // Remove "COUNTER_MEMS","INTERPOLATED_MEMS".
            const isNewTypeHeadset = msg.mot.length === 12
            node.context().global.set("isNewTypeHeadset", isNewTypeHeadset)


            // New headset
            // [
            //   "COUNTER_MEMS","INTERPOLATED_MEMS",
            //   "Q0","Q1","Q2","Q3",
            //   "ACCX","ACCY","ACCZ",
            //   "MAGX","MAGY","MAGZ"
            // ]

            // Old headset
            // [
            //   "COUNTER_MEMS","INTERPOLATED_MEMS",
            //   "GYROX","GYROY","GYROZ",
            //   "ACCX","ACCY","ACCZ",
            //   "MAGX","MAGY","MAGZ"
            // ]

            // MN8
            // [ 
            //   "COUNTER_MEMS","INTERPOLATED_MEMS",
            //   "Q0","Q1","Q2","Q3",
            // ]

            outputMotionArr = [...cortexMotionArr, ...outputMotionArr].slice(0, 9);
            const motionIndex = parseMotionIndex(isMN8, isNewTypeHeadset, metric)
            let motionChan = outputMotionArr[motionIndex];
            storeSocketToFlow(motionChan);
          }
          switch (msg.id) {
            case "subscribe":
              let outText = "";
              outText = parseNote(motionName[metric], metric);
              node.status({
                fill: "green",
                shape: "dot",
                text: outText
              });
              break;
          }
        }
      });
    }

    
    function parseMotionIndex(isMN8, isNewMotion, motionIndex) {
      if (isMN8 && (motionIndex > 3) || isNewMotion && [10, 11, 12].includes(motionIndex)) {
        return -1
      } else {
        if (motionIndex = 10) {
          return 0
        }
        if (motionIndex = 11) {
          return 1
        }
        if (motionIndex = 12) {
          return 2
        }
      }
      return motionIndex
    }

    function parseNote(text, metric) {
      const isNewTypeHeadset = !!node.context().global.get("isNewTypeHeadset")
      const headsetInfo = node.context().global.get("headsetInfo")
      const isMN8 = headsetInfo.id.toLowerCase().includes('mn8')

      if (metric > 3 && isMN8) {
        return 'Only quaternions metrics are available for MN8!'
      }

      if (metric > 9 && isNewTypeHeadset) {
        return 'Gyroscopes are only available for old headsets'
      }
      return text
    }

    function parseMsg(msg) {
      const headsetInfo = node.context().global.get("headsetInfo")
      const isMN8 = headsetInfo.id.toLowerCase().includes('mn8')
      if (isMN8 && metric > 3) {
        return 'Only quaternions metrics are available for MN8!'
      }

      if (!msg) {
        return 'Motion channel is not available on this headset!'
      }

      return msg
    }

    function storeSocketToFlow(msg) {
      node.send({ payload: parseMsg(msg) });
    }

    this.on("input", function(msg) {
      auth = msg.payload[0];
      let streamArr = node.context().global.get("streamArr") || [];
      let sessionID = node.context().global.get("sessionID");

      if (streamArr.indexOf(stream) < 0) {
        bciLib.subscribe(node, auth, stream, sessionID);
        streamArr.push(stream);
        node.context().global.set("streamArr", streamArr);
      }
    });

    node.closing = false;
    startconn(); // start outbound connection

    node.on("close", function() {
      node.closing = true;
      node.socket.close();
      if (node.tout) {
        clearTimeout(node.tout);
      }
    });
  }

  RED.nodes.registerType("Motion-Sensor", MotionNode);
};
