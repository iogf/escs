#!/bin/bash

TEST_DIR="." 

echo "Tests in $TEST_DIR"

find "$TEST_DIR" -name "*.py" -print0 | 
while IFS= read -r -d '' test_file; 
do
    echo "Running tests in $test_file..."
    python -m unittest "$test_file"
done
