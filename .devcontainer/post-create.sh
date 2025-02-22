#!/bin/bash
set -e

echo "Setting up development environment..."

# Create and activate Python virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install --no-cache-dir -r requirements.txt
else
    echo "Installing basic Python dependencies..."
    pip install flask requests pytest python-dotenv black pylint
fi

# Install NLTK data
echo "Installing NLTK data..."
python -m nltk.downloader punkt vader_lexicon

# Install Node.js dependencies
if [ -f "package.json" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "Initializing Node.js project..."
    npm init -y
    npm install react react-dom @testing-library/react
fi

# Setup database
if [ -f "./backend/init.sql" ]; then
    echo "Initializing database..."
    PGPASSWORD=postgres psql -h localhost -U postgres -d youtube_analyzer -f ./backend/init.sql
fi

# Create default environment configuration
if [ ! -f .env ]; then
    echo "Creating default environment configuration..."
    cat > .env << EOL
FLASK_ENV=development
FLASK_APP=backend/app.py
FLASK_DEBUG=1
YOUTUBE_API_KEY=your-youtube-api-key
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/youtube_analyzer
EOL
fi

echo "Setup complete! 🚀"
