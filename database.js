const fs = require('fs');
const format = require('pg-format');
const { Client } = require('pg');


// AWS Client Information:
// const client = new Client ({
//     user: 'postgres',
//     host: 'database-5761i.cfk2gikqsjhw.eu-west-2.rds.amazonaws.com',
//     database: 'database5761',
//     password: 'amberdog',
//     port: 5432
// })

// // Local Information:
const client = new Client(
    { user: 'mac',
     host: 'localhost',
     port: 5432,
     database: 'totesys'}
 )

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