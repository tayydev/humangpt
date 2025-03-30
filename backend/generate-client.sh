#!/bin/bash

# Exit on error
set -e

# Configuration variables
API_URL="http://localhost:8000/openapi.json"  # Update with your FastAPI URL
OUTPUT_DIR="../client"
PACKAGE_NAME="humangpt-client"
PACKAGE_VERSION="0.1.0"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Install OpenAPI Generator if not already installed
if ! command -v openapi-generator &> /dev/null; then
    echo "Installing OpenAPI Generator CLI..."
    brew install openapi-generator
fi

# Fetch OpenAPI spec
echo "Fetching OpenAPI spec from $API_URL..."
curl -s "$API_URL" -o "$OUTPUT_DIR/openapi.json"

# Generate TypeScript client
echo "Generating TypeScript client..."
openapi-generator generate \
    -i "$OUTPUT_DIR/openapi.json" \
    -g typescript-axios \
    -o "$OUTPUT_DIR" \
    --additional-properties=npmName="$PACKAGE_NAME",npmVersion="$PACKAGE_VERSION",supportsES6=true,withInterfaces=true

echo "TypeScript client generated successfully in $OUTPUT_DIR"
