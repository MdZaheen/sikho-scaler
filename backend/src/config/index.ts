import dotenv from "dotenv";
import path from "path";

// Load environment variables
dotenv.config();

interface Config {
  port: number;
  nodeEnv: string;
  mongodb: {
    uri: string;
  };
  llm: {
    provider: "openai" | "gemini";
    apiKey: string;
  };
  rateLimit: {
    windowMs: number;
    maxRequests: number;
  };
  logging: {
    level: string;
    filePath: string;
  };
  cors: {
    origin: string;
  };
}

const config: Config = {
  port: parseInt(process.env.PORT || "3000", 10),
  nodeEnv: process.env.NODE_ENV || "development",

  mongodb: {
    uri: process.env.MONGODB_URI || "mongodb://localhost:27017/sikho-animation",
  },

  llm: {
    provider: (process.env.LLM_PROVIDER as "openai" | "gemini") || "openai",
    apiKey:
      process.env.OPENROUTER_API_KEY ||
      process.env.OPENAI_API_KEY ||
      process.env.GEMINI_API_KEY ||
      "",
  },

  rateLimit: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || "900000", 10),
    maxRequests: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || "15", 10),
  },

  logging: {
    level: process.env.LOG_LEVEL || "info",
    filePath:
      process.env.LOG_FILE_PATH || path.join(__dirname, "../../logs/app.log"),
  },

  cors: {
    origin: process.env.CORS_ORIGIN || "http://localhost:3001",
  },
};

// Validate required configuration
if (!config.llm.apiKey) {
  console.warn(
    "⚠️  Warning: No LLM API key found. Please set OPENROUTER_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY in .env file"
  );
}

export default config;
