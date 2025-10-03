#!/bin/bash

# GeoMindIA - Setup Script

echo "🗺️  GeoMindIA - Setup"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found. You'll need to install it:"
    echo "   macOS: brew install postgresql postgis"
    echo "   Ubuntu: sudo apt-get install postgresql postgis"
    echo ""
fi

# Create virtual environment
echo ""
echo "📦 Creating Python virtual environment..."
cd backend
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r ../requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy env.example to .env and add your API keys:"
echo "   cp env.example .env"
echo ""
echo "2. Set up PostgreSQL database:"
echo "   createdb geospatial_ai"
echo "   psql geospatial_ai < database/init.sql"
echo ""
echo "3. Update frontend/index.html with your Google Maps API key"
echo ""
echo "4. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "5. In another terminal, serve the frontend:"
echo "   cd frontend"
echo "   python -m http.server 3000"
echo ""
echo "6. Open http://localhost:3000 in your browser"
echo ""

