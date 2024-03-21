const fs = require('node:fs')
const format = require('pg-format')
const {Client} = require('pg');
const { execSync } = require('child_process');

// Seed the database synchronously:
const command = `./run-all.sh`;
execSync(command);

const client = new Client({user: 'mac',
host: 'localhost',
port: 5432,
database: 'temp_staff'})


// Scans JSON Database Backup 
// Uses synchronous version.
jsonData = JSON.parse(fs.readFileSync('db/2024-03-05 15-51-00.730403.json', 'utf8'))

strArr = []

for (const key in jsonData){
    // Get list of table names:
    const tableNames = Object.keys(jsonData[key][0]).join(', ')
    
    // Get values
    const values = jsonData[key].map((x)=>{
        return [...Object.values(x)]
    })

    // Create query String
    str = format(`INSERT INTO ${key}
    (${tableNames})
    VALUES
    %L;`, values)
    strArr.push(str)
}

async function addDatabase(){
    for (let i = 0; i < strArr.length; i++){
        await client.connect().then(()=>{
            client.query(strArr[i]).then((res, err)=>{
                console.log(`Added!`)
            }).catch((err) => {
                console.log('Error!', err)
            })
        })
    }
}
addDatabase()
client.end()




   


// Currency
// client.connect().then(()=>{
//     console.log('Connected!')
//     console.log('Adding to database...')
//     client.query(strArr[1]).then((res, err)=>{
//         console.log('Added!')
//         client.end()
//     }).catch((err)=>{
//         console.log(err)
//     })
// })


