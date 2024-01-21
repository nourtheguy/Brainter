"use strict";
// Emotiv Cortex Service V2.x APIs
module.exports = {
  setFacialExpressionThreshold: function(
    node,
    action,
    value,
    sessionID,
    auth,
    profile
  ) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "facialExpressionThreshold",
        params : {
          cortexToken: auth,
          // Status: "set" or "get"
          status : "set",
          profile: profile,
          session: sessionID,
          action : action,
          value  : parseInt(value)
        },
        id: "setFacialExpressionThreshold"
      })
    );
  },

  getFacialExpressionThreshold: function(node, auth, session, profile, action) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "facialExpressionThreshold",
        params : {
          cortexToken: auth,
          status     : "get",     // "set" or "get"
          session    : session,
          profile    : profile,
          action     : action
        },
        id: "getFacialExpressionThreshold"
      })
    );
  },

  subscribe: function(node, auth, stream, session) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "subscribe",
        params : {
          cortexToken: auth,
          session    : session,
          streams    : stream
        },
        id: "subscribe"
      })
    );
  },

  unsubscribe: function(node, auth, stream) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "unsubscribe",
        params : {
          cortexToken: auth,
          streams    : [stream]
        },
        id: "unsubscribe"
      })
    );
  },

  subscribeWithSessionID: function(node, auth, sessionID, stream) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "subscribe",
        params : {
          cortexToken: auth,
          session    : sessionID,
          streams    : [stream]
        },
        id: "subscribe"
      })
    );
  },

  queryHeadsets: function(node) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "queryHeadsets",
        params : {},
        id     : "queryHeadsets"
      })
    );
  },

  querySession: function(node, auth) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "querySessions",
        params : {
          cortexToken: auth
        },
        id: "querySession"
      })
    );
  },

  getDetectionInfo: function(node, detection) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "getDetectionInfo",
        params : {
          detection: detection  // "facialExpression" or "mentalCommand"
        },
        id: "getDetectionInfo"
      })
    );
  },

  /* function loadProfile to using profile
  params: 
  - node
  - auth     : token based authorization
  - headsetID: headset ID, This field is required when load or save profile
  - profile  : profile's name
  - command: "load" load training data from profile
  */
  loadProfile: function(node, auth, headsetID, profile) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "setupProfile",
        params : {
          cortexToken: auth,
          headset    : headsetID,
          profile    : profile,
          status     : "load"
        },
        id: "loadProfile"
      })
    );
  },

  /* function createProfile
  params: 
  - node
  - auth   : token based authorization
  - profile: profile's name
  - command: create new profile
  */
  createProfile: function(node, auth, profile, headsetID) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "setupProfile",
        params : {
          cortexToken: auth,
          headset    : headsetID,
          profile    : profile,
          status     : "create"
        },
        id: "createProfile"
      })
    );
  },

  /* function saveProfile
  params: 
  - node
  - auth   : token based authorization
  - profile: profile's name
  - command: save profile
  */
  saveProfile: function(node, auth, profile, headsetID) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "setupProfile",
        params : {
          cortexToken: auth,
          headset    : headsetID,
          profile    : profile,
          status     : "save"
        },
        id: "saveProfile"
      })
    );
  },

  getCurrentProfile: function(node, auth, headsetID) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "getCurrentProfile",
        params : {
          cortexToken: auth,
          headset    : headsetID
        },
        id: "getCurrentProfile"
      })
    );
  },

  unloadProfile: function(node, auth, headsetID, profile) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "setupProfile",
        params : {
          cortexToken: auth,
          headset    : headsetID,
          profile    : profile,
          status     : "unload"
        },
        id: "unloadProfile"
      })
    );
  },

  /* function queryProfile
  Get all trainining profile of specific user on the local machine
  params: 
  - node
  - auth: token based authorization
  */
  queryProfile: function(node, auth) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "queryProfile",
        params : {
          cortexToken: auth
        },
        id: "queryProfile"
      })
    );
  },

  /* function createSession
  params: 
  - node
  - auth: token based authorization
  */
  createSession: function(node, auth, headsetID) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "createSession",
        params : {
          cortexToken : auth,
          headset     : headsetID,
          status      : "open"
        },
        id: "createSession"
      })
    );
  },

  closeSession: function(node, auth, session) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "updateSession",
        params : {
          cortexToken: auth,
          session    : session,
          status     : "close"
        },
        id: "closeSession"
      })
    );
  },

  connectHeadset: function(node, headsetID) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "controlDevice",
        params : {
          command: "connect",
          headset: headsetID
        },
        id: "connectHeadset"
      })
    );
  },

  activeSession: function(node, auth) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "updateSession",
        params : {
          cortexToken: auth,
          status     : "active"
        },
        id: "activeSession"
      })
    );
  },

  getUserLogin: function(node) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "getUserLogin",
        id     : "getUserLogin"
      })
    );
  },

  login: function(node, emotivID, password, clientID, clientSecret) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "login",
        params : {
          username    : emotivID,
          password    : password,
          clientId    : clientID,
          clientSecret: clientSecret
        },
        id: "login"
      })
    );
  },

  logout: function(node, emotivID) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "logout",
        params : {
          username: emotivID
        },
        id: "logout"
      })
    );
  },

  authorizeWithLicense: function(
    node,
    emotivID,
    clientId,
    clientSecret,
    licenseKey,
    debitNumber = 1
  ) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "authorize",
        params : {
          username    : emotivID,
          clientId    : clientId,
          clientSecret: clientSecret,
          license     : licenseKey,
          debit       : parseInt(debitNumber)
        },
        id: "authorizeWithLicense"
      })
    );
  },

  authorizeWithOutLicense: function(node, clientId, clientSecret) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "authorize",
        params : {
          clientId    : clientId,
          clientSecret: clientSecret,
          debit       : 1
        },
        id: "authorizeWithOutLicense"
      })
    );
  },

  hasAccessRight: function(node, clientId, clientSecret) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "hasAccessRight",
        params : {
          clientId    : clientId,
          clientSecret: clientSecret
        },
        id: "hasAccessRight"
      })
    );
  },

  requestAccess: function(node, clientId, clientSecret) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "requestAccess",
        params : {
          clientId    : clientId,
          clientSecret: clientSecret
        },
        id: "requestAccess"
      })
    );
  },

  getTrainedSignatureActions: function(
    node,
    profile,
    session,
    auth,
    detection
  ) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "getTrainedSignatureActions",
        params : {
          cortexToken: auth,
          detection  : detection,
          session    : session,
          profile    : profile
        },
        id: "getTrainedSignatureActions"
      })
    );
  },

  getTrainedSignatureActionsLocal: function(node, profile, auth, detection) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "getTrainedSignatureActions",
        params : {
          cortexToken: auth,
          detection  : detection,
          profile    : profile
        },
        id: "getTrainedSignatureActionsLocal"
      })
    );
  },

  /* Get/Set active MentalCommand actions with sessionID
    - actions: array of strings - List of action will active. Get from the field actions in response of request get detection info
    - status : get/set
  */
  getMentalCommandActiveAction: function(node, auth, session, profile) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "mentalCommandActiveAction",
        params : {
          cortexToken: auth,
          session    : session,
          profile    : profile,
          status     : "get"
          // action: actions
        },
        id: "getMentalCommandActiveAction"
      })
    );
  },

  /* Get/Set active MentalCommand actions without sessionID
    - actions: array of strings - List of action will active. Get from the field actions in response of request get detection info
    - status : get/set
  */
  getMentalCommandActiveActionLocal: function(node, auth, profile) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "mentalCommandActiveAction",
        params : {
          cortexToken: auth,
          profile    : profile,
          status     : "get"
        },
        id: "getMentalCommandActiveActionLocal"
      })
    );
  },

  /* Get Sensitivity MentalCommand with sessionID */
  getMentalCommandActionSensitivity: function(node, auth, session, profile) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "mentalCommandActionSensitivity",
        params : {
          cortexToken: auth,
          session    : session,
          profile    : profile,
          status     : "get"
        },
        id: "getMentalCommandActionSensitivity"
      })
    );
  },

  /* Set Sensitivity MentalCommand with sessionID 
    values: array of numbers with 4 elements
    Depend on the order of element will set senvitivity for activated action 1 - 4, range of value (min: 1, max: 10) 
  */
  setMentalCommandActionSensitivity: function(
    node,
    auth,
    session,
    profile,
    values
  ) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "mentalCommandActionSensitivity",
        params : {
          cortexToken: auth,
          session    : session,
          profile    : profile,
          status     : "set",
          values     : values
        },
        id: "setMentalCommandActionSensitivity"
      })
    );
  },

  /* Get Sensitivity MentalCommand without sessionID */
  getMentalCommandActionSensitivityLocal: function(node, auth, profile) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "mentalCommandActionSensitivity",
        params : {
          cortexToken: auth,
          profile    : profile,
          status     : "get"
        },
        id: "getMentalCommandActionSensitivityLocal"
      })
    );
  },

  /* Set Sensitivity MentalCommand without sessionID
    values: array of numbers with 4 elements
    Depend on the order of element will set senvitivity for activated action 1 - 4, range of value (min: 1, max: 10) 
  */
  setMentalCommandActionSensitivityLocal: function(
    node,
    auth,
    profile,
    values
  ) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "mentalCommandActionSensitivity",
        params : {
          cortexToken: auth,
          session    : session,
          profile    : profile,
          status     : "set",
          values     : values
        },
        id: "setMentalCommandActionSensitivityLocal"
      })
    );
  },

  loadGuestProfile: function(node, auth, headset) {
    node.socket.send(
      JSON.stringify({
        jsonrpc: "2.0",
        method : "loadGuestProfile",
        params : {
          cortexToken: auth,
          headset    : headset,
        },
        id: "loadGuestProfile"
      })
    );
  },
};
