import { Meteor } from 'meteor/meteor';
var PythonShell = require('python-shell');
var base = process.env.PWD;


Meteor.startup(() => {
  // code to run on server at startup

});


Meteor.methods({

    callPython: function(filepath, filename) {
        var options = {
            mode: 'text',
        //    pythonPath: 'path/to/python',
            pythonOptions: ['-u'],
            scriptPath: "" + base + '/server/python',
            args: ["../camera/" + filepath, "../processed/" + filename]
        };
        var pyshell = new PythonShell('matcher.py', options);

        pyshell.on('message', function (message) {
            // received a message sent from the Python script (a simple "print" statement)
            console.log(message);
        });

        pyshell.on('error', function (err) {
            console.log(err);
        });
    }
});
