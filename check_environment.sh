#!/bin/bash

# Check for Python
command -v python3 >/dev/null 2>&1 || {
    echo >&2 "Python3 is required, but it's not installed. Please install Python3 and try again.";
    exit 1;
}

# Check for Python version and ensure it is version 3.11 or higher
python_version=$(python3 -c 'import platform; major, minor, _ = platform.python_version_tuple(); print(f"{major}.{minor}")')
if [[ "$python_version" < "3.11" ]]; then
    echo >&2 "Python version 3.11 or higher is required, but you have version $python_version. Please install Python 3.11 or higher and try again."
    exit 1
fi

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

# Check for Django version and ensure it is version 4.2 or higher
django_version=$(python3 -c "import django; print(django.get_version())")
if [[ "$django_version" < "4.2" ]]; then
    echo >&2 "Django version 4.2 or higher is required, but you have version $django_version. Please install Django 4.2 or higher and try again."
    exit 1
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

# Install and update Python dependencies
echo "Installing and Python dependencies..."
cd backend
pip3 install -r requirements.txt

# Install and update Node.js dependencies
echo "Installing and updating Node.js dependencies..."
cd ../frontend
npm install
npm update
