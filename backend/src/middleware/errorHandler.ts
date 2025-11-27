import { Request, Response, NextFunction } from "express";
import { AppError } from "../utils/errors";
import logger from "../utils/logger";

export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction
) => {
  if (err instanceof AppError) {
    logger.error(`${err.statusCode} - ${err.message}`, {
      path: req.path,
      method: req.method,
      stack: err.stack,
    });

    return res.status(err.statusCode).json({
      success: false,
      error: {
        message: err.message,
        statusCode: err.statusCode,
      },
    });
  }

  // Mongoose validation error
  if (err.name === "ValidationError") {
    logger.error("Mongoose validation error:", err);
    return res.status(400).json({
      success: false,
      error: {
        message: "Validation error",
        details: err.message,
        statusCode: 400,
      },
    });
  }

  // Mongoose cast error (invalid ObjectId)
  if (err.name === "CastError") {
    logger.error("Mongoose cast error:", err);
    return res.status(400).json({
      success: false,
      error: {
        message: "Invalid ID format",
        statusCode: 400,
      },
    });
  }

  // Unknown error
  logger.error("Unhandled error:", {
    message: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
  });

  return res.status(500).json({
    success: false,
    error: {
      message: "Internal server error",
      statusCode: 500,
    },
  });
};
