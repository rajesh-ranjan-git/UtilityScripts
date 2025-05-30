const fs = require('fs');
const readline = require('readline');
const path = require('path');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

let folderPaths = [];

console.log("=== Folder Deletion Utility ===");
console.log("Enter full folder paths to delete, one per line.");
console.log("Type DONE when you are finished.\n");

function askFolder() {
  rl.question(`Enter folder path [${folderPaths.length}]: `, (input) => {
    if (input.trim().toUpperCase() === 'DONE') {
      if (folderPaths.length === 0) {
        console.log("No folder paths entered. Exiting.");
        rl.close();
        return;
      }
      confirmDeletion();
    } else {
      if (fs.existsSync(input) && fs.lstatSync(input).isDirectory()) {
        folderPaths.push(input.trim());
      } else {
        console.log(`❌ Folder not found: ${input}`);
      }
      askFolder();
    }
  });
}

function confirmDeletion() {
  console.log("\n=== Confirm Deletion ===");
  folderPaths.forEach((folder, index) => {
    console.log(`[${index + 1}] ${folder}`);
  });

  rl.question("\nAre you sure you want to delete these folders? (Y/N): ", (confirm) => {
    if (confirm.trim().toUpperCase() === 'Y') {
      deleteFolders();
    } else {
      console.log("Deletion cancelled.");
      rl.close();
    }
  });
}

function deleteFolders() {
  console.log("\n=== Deleting Folders ===");
  folderPaths.forEach((folder) => {
    try {
      fs.rmSync(folder, { recursive: true, force: true });
      console.log(`✅ Deleted: ${folder}`);
    } catch (err) {
      console.error(`❌ Failed to delete: ${folder}`, err.message);
    }
  });
  rl.close();
}

askFolder();
