// Require profile from "profile name" node.
// Output:
// Eye action
// Upper Face Action
// Lower Face Action

module.exports = function(RED) {
  "use strict";
  const bciLib = require("./bci-lib");
  const config = require("./bci-config");
  
  function FacialExpressionNode(n) {
    RED.nodes.createNode(this, n);

    let node      = this;
    let profile   = null;
    let auth      = null;
    let errorCode = config.errorCode;
    let sessionID = null;
    let detection = "facialExpression";

    let isActionTrained = false;

    const stream = config.stream;
    const action = n.action;
    const sens   = parseInt(n.sens);

    function startconn() {
      // Connect to remote endpoint
      node.tout   = null;
      node.socket = node.context().global.get("socket");

      handleConnection();
    }

    function checkSubscribedStream(auth, stream) {
      let streamArr = node.context().global.get("streamArr") || [];
      if (streamArr.indexOf(stream) < 0 || profile == undefined) {
        const stream = config.stream;
        bciLib.subscribe(node, auth, stream, sessionID);
        streamArr.push(stream);
        node.context().global.set("streamArr", streamArr);
      } else {
        if (!!profile && profile != "") {
          bciLib.getTrainedSignatureActions(
            node,
            profile,
            sessionID,
            auth,
            detection
          );
        }
      }
    }

    function filterAction(msg, action) {
      // [<eye_action>, <upper_face_action>, <upper_face_power>, <lower_face_action>, <lower_face_power>]
      const eyeAction = msg.fac[0] === 'neutral' ? 'eye-neutral' : msg.fac[0];
      const upperFace = msg.fac.slice(1, 3).map(element => element === 'neutral' ? 'uf-neutral' : element);
      const lowerFace = msg.fac.slice(3, 5).map(element => element === 'neutral' ? 'lf-neutral' : element);

      if (eyeAction === action) {
        return 1
      }

      if (upperFace[0] === action) {
        return action === 'uf-neutral' ? 1 : upperFace[1]
      }

      if (lowerFace[0] === action) {
        return action === 'lf-neutral' ? 1 : lowerFace[1]
      }

      return 0;
    }

    function handleConnection() {
      node.socket.on("open", function() {
        node.status({
          fill : "white",
          shape: "ring",
          text : "Connecting ..."
        });
      });

      node.socket.on("close", function() {
        node.status({
          fill : "red",
          shape: "ring",
          text : 
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
          if (msg.error.code == errorCode.ERR_INVALID_PROFILE) {
            node.status({
              fill : "green",
              shape: "ring",
              text : "Using default profile"
            });
          }
        } else {
          if (msg.fac != "undefined") {
            if (!!msg.fac) {
              // filter what to send (eye action, upper face action, lower face action)
              const result = filterAction(msg, action);
              storeSocketToFlow(Math.ceil(result * 100)); // Rescale power
            }

            switch (msg.id) {
              case "loadProfile": 
                checkSubscribedStream(auth, stream);
                break;

              case "getTrainedSignatureActions": 
                const trainedAction = msg.result.trainedActions;
                trainedAction.forEach((ele) => {
                  if (ele.action === action) {
                    isActionTrained = true;
                  }
                });

                if (isActionTrained) {
                  node.status({
                    fill : "green",
                    shape: "ring",
                    text : `Getting ${action} data.`
                  });
                  bciLib.setFacialExpressionThreshold(
                    node,
                    action,
                    sens,
                    sessionID,
                    auth,
                    profile
                  );
                } else {
                  node.status({
                    fill : "yellow",
                    shape: "ring",
                    text : `${action} is not trained! Using universal profile.`
                  });
                }
                break;

              case "subscribe": 
                if (profile == undefined) {
                  node.status({
                    fill : "yellow",
                    shape: "ring",
                    text : `${action} is not trained! Using universal profile.`
                  });
                }
                break;
            }
          }
        }
      });
    }

    function storeSocketToFlow(msg) {
      node.send({ payload: msg });
    }

    node.on("input", function(msg) {
      auth      = msg.payload[0];
      profile   = msg.payload[1];
      sessionID = node.context().global.get("sessionID");
      checkSubscribedStream(auth, stream);
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

  RED.nodes.registerType("Facial-Expression", FacialExpressionNode);
};
