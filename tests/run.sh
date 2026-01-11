#!/bin/bash

TEST_DIR="." 

echo "Running tests in $TEST_DIR using a find/loop approach..."

find "$TEST_DIR" -name "*.py" -print0 | while IFS= read -r -d '' test_file; do
    echo "Running tests in $test_file..."
    python -m unittest "$test_file"
done
