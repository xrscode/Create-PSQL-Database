const fs = require('fs');
const format = require('pg-format');
const { Client } = require('pg');

// AWS Client Information:
const client = new Client ({
    user: 'postgres',
    host: 'database-5761i.cfk2gikqsjhw.eu-west-2.rds.amazonaws.com',
    database: 'database5761',
    password: 'amberdog',
    port: 5432,
    // Certificate of Authenticity(?):
    ssl: {
        rejectUnauthorized: false}
})

async function createTables() {
    try {
        // Connect to the database.
        await client.connect(); 
      
        // Reads SQL Queries in '02-create-tables.sql'
        const sqlQueries = fs.readFileSync('db/02-create_tables.sql', 'utf8').split(';')

        // Executes SQL Queries to create tables.
        for (let i = 0; i < sqlQueries.length; i++){
            await client.query(sqlQueries[i])
        }
        
        // Read from JSON file.
        const data = fs.readFileSync('db/2024-03-05 15-51-00.730403.json', 'utf8')
        // Convert into JSON useable object.
        const jsonData = JSON.parse(data);
        
        // Iterate and build queries.   
        for (const key in jsonData) {
            jsonData[key][0]
            // Each key represents individual tables.

            // rows are the names of the rows.
            const rows = Object.keys(jsonData[key][0]).join(', ');
           
            // Generate the values by mapping over data.
            const values = jsonData[key].map(x => Object.values(x));

            // Create query.
            const query = format(`INSERT INTO ${key} (${rows}) VALUES %L;`, values);

            await client.query(query);
            
        }
        console.log('Database successfully populated.')
    } catch (error) {
        console.error('Error:', error);
    } finally {
        await client.end(); // Close the client connection.
    }
}