var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
  var spawn = require("child_process").spawn;
  var process = spawn('python', "../Final_Python_File.py");
  var csv_files = new Array(3);
  process.on("close", (err)=>{
    csv_files[0] = "" //path to csv file 1
    csv_files[1] = "" //path to csv file 2
    csv_files[2] = "" //path to csv file 3 .... 
  })
  /**
   * Code to visualize the plot using the csv files
   */
});

module.exports = router;
