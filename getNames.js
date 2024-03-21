"strict";
const axios = require("axios");
const {Client} = require('pg');
const format = require("pg-format");

const client = new Client(
   { user: 'mac',
    host: 'localhost',
    port: 5432,
    database: 'temp_staff'}
)

// client.connect().then(()=>{
//     console.log('Connected!')
//     client.query('SELECT * FROM staff_table;').then((res, err) => {
//        console.log(res.rows)
//     }).catch((err) => {
//         console.log(`Query Error!`)
//         console.log(err)
//     })
// }).catch((err) => {
//     console.log(err)
// })


// Returns a Promise (array of 150 Pokemon).
function getNames () {
    return axios.get('https://pokeapi.co/api/v2/pokemon?limit=150')
    .then(function (response){
    const arr = response.data.results;
    return arr
}).catch(function (error){
    console.log(error)
});
}

// Handle Promise and create random names.
function createFirstNames() {
    return getNames()
    .then(function (names) {
        const arr = []
        for(let i = 0; i < 10; i++){
            let num = Math.round(Math.random()*150)
            let name = names[num].name
            arr.push(name)
        }

        return arr;
    })
    .catch(function (error) {
        console.log(error); // Log any errors
    });
}

function createSecondNames() {
    return getNames()
    .then(function (names) {
        const arr = []

        for(let i = 0; i < 10; i++){
            let num = Math.round(Math.random()*150)
            arr.push(names[num].name)
        }

        return arr;
    })
    .catch(function (error) {
        console.log(error); // Log any errors
    });
}

function randomNumber () {
    return Math.ceil(Math.random()*5);
}

function randomEmail () {
    let emptyStr = ""
    const secondPart = "@mail.com"
    
    for(let i = 0; i < 5; i++){
        const randInt = Math.round(Math.random()*25)+65
        emptyStr += String.fromCharCode(randInt)
    }
    return `${emptyStr}${secondPart}`
}

function randomDate(){
    const current = new Date();
    const randomDays = Math.round(Math.random() * 1500);
    const pastDate = new Date(current.getTime() - randomDays * 24 * 60 * 60 * 1000)
    return pastDate
}


Promise.all([createFirstNames(), createSecondNames()]).then(function (results) {
    const arr = []

    for(let i = 0; i < results[0].length; i++){
        arr.push(String(`${results[0][i]} ${results[1][i]}`))
    }
    
    const values = arr.map((name)=>
    {
        tempArr = name.split(' ')
        return [tempArr[0], tempArr[1], randomNumber(), randomEmail(), new Date(), randomDate()]
    })

    console.log(values)

    const insertStr = format(
        `INSERT INTO staff_table
        (first_name, second_name, department_id, email_address, last_updated, created_at)
        VALUES
        %L
        RETURNING *
        `, values)
 
    client.connect().then(()=>{
    console.log('Connected!')
    client.query(insertStr).then((res, err) => {
       console.log(res.rows)
    }).catch((err) => {
        console.log(`Query Error!`)
        console.log(err)
    })
}).catch((err) => {
    console.log(err)
}) 
})

// client.connect().then(()=>{
//     console.log('Second Connection')
//     client.query('SELECT * FROM staff_table;').then((response, err) => {
//         console.log(response.rows)
//     })
// })





