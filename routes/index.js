const express = require('express');
const router = express.Router();
const csv = require("csv-parser");
const fs = require("fs")

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
  var spawn = require("child_process").spawn;
  var process = spawn('python', ["../Final_Python_File.py"]); // py file => Final_Python_File.py
  var positions0=[];
  var positions1 = []
  process.on("close", (err)=>{
    fs.createReadStream("../file_no_io_positions0.csv")
    .pipe(csv())
    .on('data', (row)=>{
      var temp = []
      temp.push(parseFloat(row['0']))
      temp.push(parseFloat(row['1']))
      temp.push(parseFloat(row['2']))
      positions0.push(temp)
    })
    fs.createReadStream("../file_no_io_positions1.csv")
    .pipe(csv())
    .on('data', (row)=>{
      var temp = []
      temp.push(parseFloat(row['0']))
      temp.push(parseFloat(row['1']))
      temp.push(parseFloat(row['2']))
      positions1.push(temp)
    })
  })
  /**
   * Code to visualize the plot using the csv files
   */
});

router.post('/', (req, res)=>{
  var spawn = require("child_process").spawn;
  var process = spawn('python', "../python_final_file.py"); // py file => python_final_file.py
  var positions0=[];
  var positions1 = []
  process.on("close", (err)=>{
    fs.createReadStream("../file_no_io_positions0.csv")
    .pipe(csv())
    .on('data', (row)=>{
      var temp = []
      temp.push(parseFloat(row['0']))
      temp.push(parseFloat(row['1']))
      temp.push(parseFloat(row['2']))
      positions0.push(temp)
    })
    fs.createReadStream("../file_no_io_positions1.csv")
    .pipe(csv())
    .on('data', (row)=>{
      var temp = []
      temp.push(parseFloat(row['0']))
      temp.push(parseFloat(row['1']))
      temp.push(parseFloat(row['2']))
      positions1.push(temp)
    })
  })
})


module.exports = router;