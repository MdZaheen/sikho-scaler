# SIKHO Animation Backend

> **Text-to-Animation Backend** - Converts natural language descriptions into structured animation instructions for Three.js + GSAP rendering.

## 🎯 Overview

This backend processes educational text descriptions through an LLM-powered pipeline to generate deterministic, structured animation plans. Perfect for creating educational videos without AI-generated hallucinations.

## 🏗️ Architecture

```
Text Input
    ↓
Concept Parser (LLM)
    ↓
Scene Generator (LLM)
    ↓
Instruction Compiler (LLM)
    ↓
JSON Animation Plan
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- MongoDB 6.0+
- OpenAI API key (or Google Gemini)

### Installation

```bash
# Clone and navigate to backend
cd backend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env and add your API keys
# MONGODB_URI=mongodb://localhost:27017/sikho-animation
# OPENAI_API_KEY=your_key_here
```

### Running the Server

```bash
# Development mode with auto-reload
npm run dev

# Production build
npm run build
npm start
```

Server will start on `http://localhost:3000`

## 📡 API Endpoints

### Generate Animation

```bash
POST /api/generate
Content-Type: application/json

{
  "text": "Animate the Pythagoras theorem with a growing square"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "objects": { ... },
    "timeline": [ ... ],
    "audio": [ ... ],
    "style": { ... }
  }
}
```

### Get Animation

```bash
GET /api/animation/:id
```

### List Animations

```bash
GET /api/animations?limit=20&skip=0
```

### Delete Animation

```bash
DELETE /api/animation/:id
```

### Health Check

```bash
GET /health
```

## 🔧 Configuration

All configuration is done via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `3000` |
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/sikho-animation` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `RATE_LIMIT_WINDOW_MS` | Rate limit window | `900000` (15 min) |
| `RATE_LIMIT_MAX_REQUESTS` | Max requests per window | `15` |
| `CORS_ORIGIN` | Allowed CORS origin | `http://localhost:3001` |

## 📁 Project Structure

```
backend/
├── src/
│   ├── config/           # Configuration and database setup
│   ├── models/           # MongoDB models
│   ├── services/         # Business logic
│   │   ├── llm/          # LLM client and prompts
│   │   ├── processors/   # Text→Concept→Scene→Instructions
│   │   └── pipeline/     # Orchestrator
│   ├── controllers/      # Request handlers
│   ├── routes/           # API routes
│   ├── middleware/       # Express middleware
│   ├── validators/       # Request validation
│   ├── utils/            # Utilities (logger, errors)
│   └── index.ts          # Server entry point
├── package.json
├── tsconfig.json
└── .env.example
```

## 🧪 Testing

```bash
# Run tests (when implemented)
npm test

# Run tests in watch mode
npm run test:watch
```

## 📝 Development

```bash
# Format code
npm run format

# Lint code
npm run lint
```

## 🔒 Security Features

- ✅ Helmet.js security headers
- ✅ CORS protection
- ✅ Rate limiting (15 requests per 15 minutes for generation)
- ✅ Request validation with Zod
- ✅ Error handling with proper status codes
- ✅ Request logging

## 📊 Logging

Logs are written to:
- Console (development)
- `logs/app.log` (all logs)
- `logs/error.log` (errors only)

## 🚢 Deployment

### Environment Setup

1. Set `NODE_ENV=production`
2. Configure production MongoDB URI
3. Set secure CORS origin
4. Add LLM API key

### Docker (Optional)

```bash
# Build image
docker build -t sikho-backend .

# Run container
docker run -p 3000:3000 --env-file .env sikho-backend
```

## 🤝 Contributing

1. Follow TypeScript strict mode
2. Use ESLint and Prettier
3. Write tests for new features
4. Update documentation

## 📄 License

MIT

## 🆘 Support

For issues or questions, please create an issue in the repository.
