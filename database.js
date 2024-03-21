const fs = require('fs');
const format = require('pg-format');
const { Client } = require('pg');
const { execSync } = require('child_process');

// Seed the database synchronously:
const command = `./run-all.sh`;
execSync(command);

const client = new Client({
    user: 'mac',
    host: 'localhost',
    port: 5432,
    database: 'temp_staff'
});

// Read JSON data asynchronously
fs.readFile('db/2024-03-05 15-51-00.730403.json', 'utf8', async (err, data) => {
    if (err) {
        console.error('Error reading JSON file:', err);
        return;
    }

    const jsonData = JSON.parse(data);
    const queries = [];

    // Generate queries
    for (const key in jsonData) {
        const tableNames = Object.keys(jsonData[key][0]).join(', ');
        const values = jsonData[key].map(x => Object.values(x));
        const query = format(`INSERT INTO ${key} (${tableNames}) VALUES %L;`, values);
        queries.push(query);
    }

    try {
        await client.connect();
        for (const query of queries) {
            await client.query(query);
            console.log('Added!');
        }
    } catch (error) {
        console.error('Error executing queries:', error);
    } finally {
        await client.end();
    }
});