const fs = require('fs');
const { MongoClient } = require('mongodb');

const TXT_PATH = './output.txt';
const MONGO_URI = 'mongodb://localhost:27017';
const DB_NAME = 'ocrDB';
const COLLECTION = 'results';

// Call this function to append OCR result to TXT
function appendResultToTxt(result) {
    fs.appendFileSync(TXT_PATH, result + '\n');
}

// Call this function when video stops
async function sendTxtToMongo() {
    const content = fs.readFileSync(TXT_PATH, 'utf-8');
    const client = new MongoClient(MONGO_URI);
    try {
        await client.connect();
        const db = client.db(DB_NAME);
        const collection = db.collection(COLLECTION);
        await collection.insertOne({ content, timestamp: new Date() });
        console.log('Result sent to MongoDB');
    } finally {
        await client.close();
    }
}

// Example usage:
// appendResultToTxt('Sample OCR result'); // Call this per frame
// sendTxtToMongo(); // Call this when video stops
