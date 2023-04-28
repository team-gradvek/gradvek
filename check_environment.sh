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

# Check for Django
if ! python3 -c "import django" >/dev/null 2>&1; then
    echo >&2 "Django is required, but it's not installed. Installing Django using pip3...";
    pip3 install --user --upgrade django
fi

# Check for Node.js (npm)
command -v npm >/dev/null 2>&1 || {
    echo >&2 "npm is required, but it's not installed. Please install Node.js (npm) and try again.";
    exit 1;
}

# Check for Docker
command -v docker >/dev/null 2>&1 || {
    echo >&2 "Docker is required, but it's not installed. Please install Docker and try again.";
    exit 1;
}

# Check for required Python packages
required_python_packages=("wget" "neo4j" "pyarrow")
missing_python_packages=()

for package in "${required_python_packages[@]}"; do
    if ! pip3 show "$package" >/dev/null 2>&1; then
        missing_python_packages+=("$package")
    fi
done

if [ "${#missing_python_packages[@]}" -gt 0 ]; then
    echo "The following required Python packages are missing:"
    for package in "${missing_python_packages[@]}"; do
        echo "- $package"
    done

    echo "Installing and updating missing packages using pip3..."
    pip3 install --user --upgrade "${missing_python_packages[@]}"
else
    echo "All required Python packages are present. Updating packages..."
    pip3 install --user --upgrade "${required_python_packages[@]}"
fi

# Install and update Python dependencies
echo "Installing and Python dependencies..."
cd backend
pip3 install -r requirements.txt

# Install and update Node.js dependencies
echo "Installing and updating Node.js dependencies..."
cd ../frontend
npm install
npm update
