import express, { Application } from "express";
import cors from "cors";
import helmet from "helmet";
import config from "./config";
import { connectDB, disconnectDB } from "./config/database";
import logger from "./utils/logger";
import { requestLogger } from "./middleware/requestLogger";
import { errorHandler } from "./middleware/errorHandler";
import { generalRateLimiter } from "./middleware/rateLimiter";
import animationRoutes from "./routes/animation.routes";
import healthRoutes from "./routes/health.routes";

const app: Application = express();

// Middleware
app.use(helmet()); // Security headers
app.use(cors({ origin: config.cors.origin })); // CORS
app.use(express.json({ limit: "10mb" })); // JSON parser
app.use(express.urlencoded({ extended: true, limit: "10mb" })); // URL-encoded parser
app.use(requestLogger); // Request logging
app.use(generalRateLimiter); // General rate limiting

// Routes
app.use("/", healthRoutes);
app.use("/api", animationRoutes);

// 404 handler
app.use("*", (_req, res) => {
  res.status(404).json({
    success: false,
    error: {
      message: "Route not found",
      statusCode: 404,
    },
  });
});

// Error handler (must be last)
app.use(errorHandler);

// Server startup
const startServer = async () => {
  try {
    // Connect to database
    await connectDB();

    // Start server
    const server = app.listen(config.port, () => {
      logger.info(`🚀 Server running on port ${config.port}`);
      logger.info(`📝 Environment: ${config.nodeEnv}`);
      logger.info(`🔗 CORS origin: ${config.cors.origin}`);
    });

    // Graceful shutdown
    const gracefulShutdown = async (signal: string) => {
      logger.info(`${signal} received. Starting graceful shutdown...`);

      server.close(async () => {
        logger.info("HTTP server closed");
        await disconnectDB();
        logger.info("Graceful shutdown completed");
        process.exit(0);
      });

      // Force shutdown after 10 seconds
      setTimeout(() => {
        logger.error("Forced shutdown after timeout");
        process.exit(1);
      }, 10000);
    };

    process.on("SIGTERM", () => gracefulShutdown("SIGTERM"));
    process.on("SIGINT", () => gracefulShutdown("SIGINT"));
  } catch (error) {
    logger.error("Failed to start server:", error);
    process.exit(1);
  }
};

startServer();

export default app;
