#!/bin/bash

# File containing GitHub URLs (one per line)
URL_FILE="repos.txt"

# Check if the file exists
if [[ ! -f "$URL_FILE" ]]; then
  echo "File $URL_FILE not found!"
  exit 1
fi

# Read each line and clone the repo
while IFS= read -r repo_url; do
  if [[ -n "$repo_url" ]]; then
    echo "Cloning $repo_url..."
    git clone "$repo_url"
    echo
  fi
done < "$URL_FILE"
