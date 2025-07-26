#!/bin/bash
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🚀 Starting Flask application..."
cd app
python main.py
