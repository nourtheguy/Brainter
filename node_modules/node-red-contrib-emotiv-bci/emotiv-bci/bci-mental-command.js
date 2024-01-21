module.exports = function(RED) {
  'use strict';
  var bciLib = require('./bci-lib');
  var config = require('./bci-config');

  function MentalCommandNode(n) {
    RED.nodes.createNode(this, n);
    var node        = this;
    var auth        = null;
    var sessionID   = null;
    var profileName = null;
    var actionName  = n.actionName;
    var stream      = 'com';
    var detection   = 'mentalCommand';
    var sen         = n.mcSen;

    function startconn() {
      node.tout   = null;
      node.socket = node.context().global.get('socket');

      handleConnection();
    }

    function checkSubscribedStream(auth, stream) {
      var streamArr = node.context().global.get('streamArr') || [];
      if (streamArr.indexOf(stream) < 0) {
        // MC stream isn't subscribed yet
        var stream = config.stream;
        bciLib.subscribe(node, auth, stream, sessionID);
        streamArr.push(stream);
        node.context().global.set('streamArr', streamArr);
      } else {
        // Subscribed, get data
        bciLib.getMentalCommandActiveAction(node, auth, sessionID, profileName);
      }
    }

    function handleConnection() {
      node.socket.on('open', function() {
        node.status({
          fill : 'white',
          shape: 'ring',
          text : 'Connecting ...'
        });
      });

      node.socket.on('close', function() {
        node.status({
          fill : 'red',
          shape: 'ring',
          text : 'Please ensure that you have Cortex installed and running in the background.'
        });
        if (!node.closing) {
          clearTimeout(node.tout);
          node.tout = setTimeout(function() {
            startconn();
          }, 3000);
        }
      });

      node.socket.on('message', function(data) {
        var msg = JSON.parse(data);

        if (!!msg.id && !!msg.error) {
          // Handle error
        } else if (!!msg.com && msg.com[0] == actionName) {
          node.send({payload: Math.ceil(msg.com[1] * 100)});
        } else {
          // node.send({payload: 0});
          switch (msg.id) {
            case 'getMentalCommandActiveAction': 
              const activatedActions = msg.result;
              if (activatedActions.indexOf(actionName) >= 0 || actionName == 'neutral') {
                // MC action was trained
                bciLib.getTrainedSignatureActions(node, profileName, sessionID, auth, detection);
                node.status({fill: 'green', shape: 'ring', text: 'Getting ' + actionName + ' data'});
              } else {
                // MC action wasn't trained
                node.status({
                  fill : 'red',
                  shape: 'ring',
                  text : 'Please train command ' + actionName + ' before using'
                });
              }
              break;

            case 'loadProfile': 
              // checkSubscribedStream(auth, stream);
              break;

            case 'getTrainedSignatureActions': 
              bciLib.setMentalCommandActionSensitivity(node, auth, sessionID, profileName, [sen, sen, sen, sen]);
              break;

            case 'subscribe': 
              bciLib.getMentalCommandActiveAction(node, auth, sessionID, profileName);
              break;
          }
        }
      });
    }

    this.on('input', function(msg) {
      auth        = msg.payload[0];
      profileName = msg.payload[1];
      sessionID   = node.context().global.get('sessionID');

      node.status({
        fill : 'white',
        shape: 'ring',
        text : 'Connecting ...'
      });

      checkSubscribedStream(auth, stream);
    });

    node.closing = false;
    startconn(); // start outbound connection

    node.on('close', function() {
      node.closing = true;
      node.socket.close();
      if (node.tout) {
        clearTimeout(node.tout);
      }
    });
  }

  RED.nodes.registerType('Mental-Command', MentalCommandNode);
};
