const fs = require('fs');
const format = require('pg-format');
const {Client} = require('pg')

const data = fs.readFileSync('db/dbdata.json', 'utf8')
const jsonData = JSON.parse(data)




for (const key in jsonData){
    const values = jsonData[key].map(x => Object.values(x))
    console.log(key, values[0], values[1], values[3])

}