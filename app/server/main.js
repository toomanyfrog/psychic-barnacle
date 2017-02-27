import { Meteor } from 'meteor/meteor';
import { WebApp } from 'meteor/webapp';
var fs = Npm.require('fs');
var exec = Npm.require('child_process').exec;
var Fiber = Npm.require('fibers');
var Future = Npm.require('fibers/future');

Meteor.startup(() => {
  // code to run on server at startup

});



Meteor.methods({

  callPython: function() {
    var fut = new Future();
    exec('pythonScriptCommand with parameters', function (error, stdout, stderr) {

      // if you want to write to Mongo in this callback
      // you need to get yourself a Fiber
      new Fiber(function() {
        ...
        fut.return('Python was here');
      }).run();

    });
    return fut.wait();
  },

});
