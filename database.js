const fs = require('fs')
const format = require('pg-format')
const {Client} = require('pg');

const client = new Client(
    { user: 'mac',
     host: 'localhost',
     port: 5432,
     database: 'temp_staff'}
 )

// Scans JSON Database Backup 
const fullDatabase = fs.readFile('db/2024-03-05 15-51-00.730403.json', 'utf8', (err, data) => {
    if(!err){
        const jsonData = JSON.parse(data)

        for (const key in jsonData){
            console.log(`Currently adding data for ${key}.`)
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
            // Add to database.
            client.connect().then(()=>{
                client.query(str).then((res, err)=>{
                    console.log(`${key} insert complete.`)
                }).catch((err)=>{
                    console.log('Counterparty Error!')
                    console.log(err)
                })
            })
        }
    } else {
        console.log('Error!')
    }
})
