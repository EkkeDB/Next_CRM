#!/bin/bash

# NextCRM Frontend Local Development Script
# Use this to run the frontend locally while the backend runs in Docker

set -e

echo "🚀 Starting NextCRM Frontend Locally"
echo "===================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Set environment variables for local development
export NODE_ENV=development
export NEXT_PUBLIC_API_URL=http://localhost:8001
export NEXT_PUBLIC_APP_NAME=NextCRM

echo "✅ Environment configured:"
echo "   NODE_ENV: $NODE_ENV"
echo "   API URL: $NEXT_PUBLIC_API_URL"
echo "   App Name: $NEXT_PUBLIC_APP_NAME"
echo ""
echo "🌐 Frontend will be available at: http://localhost:3000"
echo "🔗 Backend is running at: http://localhost:8001"
echo ""
echo "📋 To test CORS fix:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Open browser console (F12)"
echo "   3. You should see no CORS errors in the console"
echo ""
echo "🛑 Press Ctrl+C to stop the development server"
echo ""

# Start the development server
npm run dev