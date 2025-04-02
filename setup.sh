#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .

# Run the tests
pytest app/tests/ 