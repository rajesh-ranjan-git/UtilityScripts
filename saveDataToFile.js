const fs = require('fs');
const path = require('path');

/**
 * Appends an object to a JSON file containing an array of objects.
 * If the file doesn't exist, it creates one.
 * @param {string} filename - The name of the JSON file.
 * @param {Object} data - The JavaScript object to append.
 */
function appendObjectToFile(filename, data) {
  const filepath = path.resolve(__dirname, filename);
  let fileData = [];

  if (fs.existsSync(filepath)) {
    const existing = fs.readFileSync(filepath, 'utf8');
    try {
      fileData = JSON.parse(existing);
      if (!Array.isArray(fileData)) {
        console.error('File does not contain a JSON array.');
        return;
      }
    } catch (e) {
      console.error('Error parsing existing JSON file:', e);
      return;
    }
  }

  fileData.push(data);
  fs.writeFileSync(filepath, JSON.stringify(fileData, null, 2), 'utf8');
  console.log(`Object appended to ${filepath}`);
}

// Example usage:
// const newEntry = { name: 'Bob', age: 25 };
// appendObjectToFile('data.json', newEntry);
