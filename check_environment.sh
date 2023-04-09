#!/bin/bash

# Check for Python
command -v python3 >/dev/null 2>&1 || {
    echo >&2 "Python3 is required, but it's not installed. Please install Python3 and try again.";
    exit 1;
}

# Check for pip3
command -v pip3 >/dev/null 2>&1 || {
    echo >&2 "pip3 is required, but it's not installed. Please install pip3 and try again.";
    exit 1;
}

# Check for required Python packages
required_packages=("wget" "neo4j" "pyarrow")
missing_packages=()

for package in "${required_packages[@]}"; do
    if ! pip3 show "$package" >/dev/null 2>&1; then
        missing_packages+=("$package")
    fi
done

if [ "${#missing_packages[@]}" -gt 0 ]; then
    echo "The following required Python packages are missing:"
    for package in "${missing_packages[@]}"; do
        echo "- $package"
    done

    echo "Installing missing packages using pip3..."
    pip3 install --user "${missing_packages[@]}"
else
    echo "All required tools and dependencies are present."
fi
