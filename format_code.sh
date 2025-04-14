#!/bin/bash
# Run Black formatter with project settings
cd "$(dirname "$0")"
black .
