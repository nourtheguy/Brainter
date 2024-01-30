module.exports = function (RED) {
  "use strict";
  let bciLib = require("./bci-lib");
  let config = require("./bci-config");

  function ProfileNameNode(n) {
    RED.nodes.createNode(this, n);
    let node = this;
    let profile = n.profileName;
    let auth = "";
    let globalContext = this.context().global;
    let loadedProfile = null;
    let headsetInfo = {};
    let headsetId = null;

    function startconn() {
      // Connect to remote endpoint
      node.tout = null;
      node.socket = globalContext.get("socket");
      handleConnection();
    }

    function handleConnection() {
      node.socket.on("open", function () {
        node.status({
          fill: "white",
          shape: "ring",
          text: "Connecting ..."
        });
      });

      node.socket.on("close", function () {
        node.status({
          fill: "red",
          shape: "ring",
          text:
            "Please ensure that you have Cortex installed and running in the background."
        });
        if (!node.closing) {
          clearTimeout(node.tout);
          node.tout = setTimeout(function () {
            startconn();
          }, 3000);
        }
      });

      node.socket.on("message", function (data) {
        let msg = JSON.parse(data);

        if (!!msg.error) {
          switch (msg.error.code) {
            case config.errorCode.ERR_PROFILE_CONFLICT:
              if (profile != null && loadedProfile != null) {
                if (profile === loadedProfile.name) {
                  node.status({
                    fill: "green",
                    shape: "dot",
                    text: profile.length > 0 ? `Profile ${profile} is not found. Loaded guest profile` : `Loaded ${profile}`
                  });
                } else {
                  bciLib.loadGuestProfile(node, auth, headsetId);
                }
              }
              break;

            default:
              break;
          }
        }

        switch (msg.id) {
          case "queryProfile":
            console.log(`[DEV-INFO] all profiles: `, msg.result)
            auth = node.context().global.get("auth");
            headsetInfo = node.context().global.get("headsetInfo");
            headsetId = headsetInfo.id

            if (msg?.result) {
              const availableProfiles = msg.result.map(profile => profile.name)
              const isProfileAvailable = availableProfiles.includes(profile)
              if (isProfileAvailable) {
                bciLib.getCurrentProfile(node, auth, headsetId)
              } else {
                bciLib.loadGuestProfile(node, auth, headsetId);
              }
              break;
            }

          case "getCurrentProfile":
            auth = node.context().global.get("auth");
            headsetInfo = node.context().global.get("headsetInfo");
            headsetId = headsetInfo.id

            if (profile === msg.result?.name) {
              if (msg.result.loadedByThisApp) {
                bciLib.loadProfile(node, auth, headsetId, profile);
              } else {
                bciLib.unloadProfile(node, auth, headsetId, profile);
              }
            }
            break;

          case "unloadProfile":
            auth = node.context().global.get("auth");
            headsetInfo = node.context().global.get("headsetInfo");
            headsetId = headsetInfo.id

            bciLib.loadProfile(node, auth, headsetId, profile);
            break;

          case "loadProfile":
            node.status({
              fill: "green",
              shape: "dot",
              text: "Loaded profile: " + profile
            });
            storeContextToFlow(auth, profile);
            break;

          case "loadGuestProfile":
            node.status({
              fill: "green",
              shape: "dot",
              text: `Profile ${profile} is not found. Loaded guest profile`
            });
            storeContextToFlow(auth, profile);
            break;
        }
      });
    }

    function storeContextToFlow(msg1, msg2) {
      // msg1: Auth token, msg2: Profile name
      node.send({ payload: [msg1, msg2] });
    }

    this.on("input", function (msg) {
      auth = msg.payload[0];
      headsetId = node.context().global.get("headsetId");
      bciLib.queryProfile(node, auth);
    });

    node.closing = false;
    startconn(); // start outbound connection

    node.on("close", function () {
      setTimeout(() => {
        node.closing = true;
        node.socket.close();
        if (node.tout) {
          clearTimeout(node.tout);
        }
      }, 3000);
    });
  }

  RED.nodes.registerType("Profile-Name", ProfileNameNode);
};
