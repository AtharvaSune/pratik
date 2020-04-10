const express = require('express');
const router = express.Router();
const csv = require("csv-parser");
const fs = require("fs");

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', {title: 'Home Page'})
})

router.get('/first', function(req, res, next) {
  var spawn = require("child_process").spawn;
  var process = spawn('python', ["./Final_Python_File.py"]); // py file => Final_Python_File.py
  var positions0 = []; // variable to plot
  var positions1 = [];

  var positions0x = []; // variable to plot
  var positions0y = [];
  var positions0z = [];
  var positions1x = []; // variable to plot
  var positions1y = [];
  var positions1z = [];

  process.on("close", (err)=>{
    fs.createReadStream("./file_no_io_positions0.csv")
    .pipe(csv())
    .on('data', (row)=>{
      var temp = [];
      temp.push(parseFloat(row['0']));
      temp.push(parseFloat(row['1']));
      temp.push(parseFloat(row['2']));
      positions0x.push(parseFloat(row['0']));
      positions0y.push(parseFloat(row['1']));
      positions0z.push(parseFloat(row['2']));

      positions0.push(temp);
    })
    .on('end', (err)=>{
      if(err){
        console.log(err);
        return;
      }
      fs.createReadStream("./file_no_io_positions1.csv")
      .pipe(csv())
      .on('data', (row)=>{
        var temp = [];
        temp.push(parseFloat(row['0']));
        temp.push(parseFloat(row['1']));
        temp.push(parseFloat(row['2']));
        positions1x.push(parseFloat(row['0']));
        positions1y.push(parseFloat(row['1']));
        positions1z.push(parseFloat(row['2']));

        positions1.push(temp);
      })
      .on('end', (err)=>{
        if(err){
          console.log(err);
          return;
        }
        res.render('first', { title: 'Brillouin Flow Model', x0: positions0x, y0: positions0y, z0: positions0z, x1: positions1x, y1: positions1y, z1: positions1z });
      })
    })
  });
})

router.get('/second', function(req, res, next) {
  res.render('form', { title: 'Charged Particle Model' })
})

router.post('/second', (req, res)=>{
  var spawn = require("child_process").spawn;
  var process = spawn('python', 
                  [ "./python_final_file.py",
                    req.query.x, 
                    req.query.y,
                    req.query.z,
                    req.query.vx,
                    req.query.vy,
                    req.query.vz,
                    req.query.bx,
                    req.query.by,
                    req.query.bz,
                    req.query.ex,
                    req.query.ey,
                    req.query.ez,
                    req.query.q
                  ]); // py file => python_final_file.py which requires inputs 13 inputs for info on inputs view the file
  var positions=[];
  let x = [], y = [], z = [];
  process.on("close", (err)=>{
    fs.createReadStream("./file_io_positions0.csv")
    .pipe(csv())
    .on('data', (row)=>{
      var temp = []
      temp.push(parseFloat(row['0']));
      temp.push(parseFloat(row['1']));
      temp.push(parseFloat(row['2']));
      x.push(parseFloat(row['0']));
      y.push(parseFloat(row['1']));
      z.push(parseFloat(row['2']));
      // console.log(x.length)
      positions.push(temp);
    })
  .on('end', (err)=>{
      if(err){
      console.log(err);
      return;
    }
    
    res.render('next', {title: 'Charged Particle Model', x: x, y: y, z: z})
  })
  })
})


module.exports = router;


