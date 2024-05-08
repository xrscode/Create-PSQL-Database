const fs = require('fs');
const format = require('pg-format');
const { Client } = require('pg');
require('dotenv').config();

let online = 0;
let client;

if (online === 0){
    // Local Client:
    client = new Client(
        { user: process.env.DB_USER,
         host: process.env.DB_HOST,
         port: process.env.DB_PORT,
         database: process.env.DB_NAME}
     )
} else if (online === 1){
    // AWS Client:
    client = new Client ({
        user: process.env.AWS_USER,
        host: process.env.AWS_HOST,
        database: process.env.AWS_DATABASE,
        password: process.env.AWS_PASSWORD,
        port: process.env.AWS_PORT
    })
}




async function createTables() {
    try {
        // Connect to the database.
        await client.connect(); 
        console.log('Database connection established.');
      
        // Reads SQL Queries in '02-create-tables.sql'
        const sqlQueries = fs.readFileSync('db/create_totesys.sql', 'utf8').split(';')

        // Executes SQL Queries to create tables.
        for (let i = 0; i < sqlQueries.length; i++){
        //    console.log(sqlQueries[i])
            await client.query(sqlQueries[i])
        }
        
        // Read from JSON file.
        const data = fs.readFileSync('db/dbdata.json', 'utf8')
        // Convert into JSON useable object.
        const jsonData = JSON.parse(data);
        
        // Iterate and build queries.   
        for (const key in jsonData) {
            // Each key represents individual tables.

            // rows are the names of the rows.
            const rows = Object.keys(jsonData[key][0]).join(', ');
            
            // Generate the values by mapping over data. Array of arrays.
            const values = jsonData[key].map(x => Object.values(x));


            // Create query.
            const query = format(`INSERT INTO ${key} (${rows}) VALUES %L;`, values);


            await client.query(query);
           
            if(key == 'staff'){
                await client.query(`SELECT setval ('staff_staff_id_seq', 20);`)
            }
        }
        console.log('Finished populating database.')
        
    } catch (error) {
        console.error('Error:', error);
    } finally {
        await client.end(); // Close the client connection.
    }
}

createTables(); // Call the async function to execute the queries.