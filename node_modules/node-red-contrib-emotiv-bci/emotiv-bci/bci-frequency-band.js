// Output rate: 8 Hz

module.exports = function(RED) {
  'use strict';
  var bciLib = require('./bci-lib');
  var config = require('./bci-config');
  var arrMetric = ['Theta', 'Alpha', 'Beta-Low', 'Beta-High', 'Gamma'];
  function FrequencyBandPowerNode(n) {
    RED.nodes.createNode(this, n);

    var node = this;
    var freq = n.freq;
    var sensor = parseInt(n.sensor, 10);
    var stream = config.stream;

    function startconn() {
      // Connect to remote endpoint
      node.tout = null;
      node.socket = node.context().global.get('socket');
      handleConnection();
    }

    function handleConnection() {
      node.socket.on('open', function() {
        node.status({
          fill: 'white',
          shape: 'ring',
          text: 'Connecting ...',
        });
      });

      node.socket.on('close', function() {
        node.status({
          fill: 'red',
          shape: 'ring',
          text: 'Please ensure that you have Cortex installed and running in the background.',
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

        if (!!msg.pow) {
          var powArr = msg.pow || [];
          var frequencyArr = [];
          let numberOfBand = 5;
          for (let i = parseInt(freq); i < powArr.length; i += numberOfBand) {
            frequencyArr.push(powArr[i]);
          }
          if (sensor === 0) {
            // output all sensors
            storeSocketToFlow(frequencyArr);
          } else {
            // output a specific sensor
            storeSocketToFlow(frequencyArr[sensor - 1]);
          }
        }

        switch (msg.id) {
          case 'subscribe':
            var nameMetric = arrMetric[parseInt(n.freq)];
            node.status({ fill: 'green', shape: 'dot', text: 'Getting ' + nameMetric + ' data' });
            break;
        }
      });
    }

    function storeSocketToFlow(msg) {
      node.send({ payload: msg });
    }

    this.on('input', function(msg) {
      var auth = msg.payload[0];
      var streamArr = node.context().global.get('streamArr') || [];
      var sessionID = node.context().global.get('sessionID');
      if (streamArr.indexOf(stream) < 0) {
        bciLib.subscribe(node, auth, stream, sessionID);
        streamArr.push(stream);
        node.context().global.set('streamArr', streamArr);
      }
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

  RED.nodes.registerType('Frequency-Band-Power', FrequencyBandPowerNode);
};
