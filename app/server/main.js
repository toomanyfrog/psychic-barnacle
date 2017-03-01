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
            args: [filepath, filename]
        };

        PythonShell.run('matcher.py', options, function (err, results) {
            if (err) throw err;
            // results is an array consisting of messages collected during execution
            console.log('results: %j', results);
        });
    }
});
