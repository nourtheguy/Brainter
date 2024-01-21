module.exports = function(RED) {
  "use strict";
  var bciLib = require("./bci-lib");
  var config = require("./bci-config");

  function PerformanceMetricNode(n) {
    RED.nodes.createNode(this, n);
    var node   = this;
    var auth   = null;
    var stream = config.stream;
    var pm     = n.pm;

    function startconn() {
      node.tout   = null;
      node.socket = node.context().global.get("socket");
      handleConnection();
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
        var msg = JSON.parse(data);
        var cons = 100;
        if (!!msg.met) {
          // Output rate: 0.1 Hz
          node.status({
            fill : "green",
            shape: "ring",
            text : "Getting " + pm + " data"
          });
          const output = msg.met.map(val => Math.ceil(val * cons));
          // https://emotiv.gitbook.io/cortex-api/data-subscription/data-sample-object#performance-metric
          switch (pm) {
            case "interest": 
              node.send({ payload: output[10]});
              break;
            case "stress": 
              node.send({ payload: output[6]});
              break;
            case "relaxation": 
              node.send({ payload: output[8]});
              break;
            case "excitement": 
              node.send({ payload: output[3]});
              break;
            case "engagement":
              node.send({ payload: output[1]});
              break;
            case "focus": 
              node.send({ payload: output[12]});
              break;
            case "longTermExcitement":
              node.send({ payload: output[4]});
              break;
            case "mn8-attention":
              node.send({ payload: output[2]});
              break;
            case "mn8-attention":
              node.send({ payload: output[4]});
              break;
            default:
              break;
          }
        }
      });
    }

    this.on("input", function(msg) {
      auth = msg.payload[0];

      var streamArr = node.context().global.get("streamArr") || [];
      var sessionID = node.context().global.get("sessionID");
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

  RED.nodes.registerType("Performance-Metric", PerformanceMetricNode);
};
