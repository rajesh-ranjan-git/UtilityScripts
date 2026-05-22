const fs = require('fs');
const { exec } = require('child_process');
const path = require('path');

// Configurable constants
const MAX_CONCURRENT_CLONES = 3;
const MAX_RETRIES = 2;

// Get folder name from Git URL
function getRepoFolderName(url) {
  return url.trim().split('/').pop().replace(/\.git$/, '');
}

// Read the repo list from file
function readRepoList(filePath) {
  return new Promise((resolve, reject) => {
    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) reject(err);
      else {
        const repos = data
          .split('\n')
          .map(line => line.trim())
          .filter(Boolean);
        resolve(repos);
      }
    });
  });
}

// Clone a repository with retry and skip logic
function cloneRepo(url, retries = 0) {
  return new Promise((resolve) => {
    const folderName = getRepoFolderName(url);
    const folderPath = path.join(__dirname, folderName);

    // Skip if folder already exists
    if (fs.existsSync(folderPath)) {
      console.log(`⏩ Skipping (already exists): ${folderName}`);
      return resolve();
    }

    console.log(`📦 Cloning: ${url}`);
    exec(`git clone ${url}`, (error, stdout, stderr) => {
      if (error) {
        if (retries < MAX_RETRIES) {
          console.warn(`🔁 Retry ${retries + 1}/${MAX_RETRIES} for: ${url}`);
          return resolve(cloneRepo(url, retries + 1));
        } else {
          console.error(`❌ Failed after ${MAX_RETRIES} retries: ${url}`);
          return resolve();
        }
      }

      console.log(`✅ Cloned: ${url}`);
      resolve();
    });
  });
}

// Handle concurrency
async function cloneWithConcurrency(urls, maxConcurrent) {
  const queue = [...urls];
  const active = [];

  const runNext = async () => {
    if (queue.length === 0) return;

    const url = queue.shift();
    const task = cloneRepo(url).then(() => {
      active.splice(active.indexOf(task), 1);
    });

    active.push(task);

    if (active.length < maxConcurrent) {
      await runNext();
    }

    await Promise.race(active);
    return runNext();
  };

  await Promise.all(Array(Math.min(maxConcurrent, queue.length)).fill().map(runNext));
}

// Main
(async () => {
  try {
    const filePath = path.join(__dirname, 'repo_links.txt');
    const repos = await readRepoList(filePath);
    console.log(`🚀 Starting to clone ${repos.length} repositories...`);
    await cloneWithConcurrency(repos, MAX_CONCURRENT_CLONES);
    console.log('🏁 All done!');
  } catch (err) {
    console.error('Error:', err.message);
  }
})();
