import rateLimit from 'express-rate-limit';
import config from '../config';

export const generateRateLimiter = rateLimit({
  windowMs: config.rateLimit.windowMs,
  max: config.rateLimit.maxRequests,
  message: {
    success: false,
    error: {
      message: 'Too many animation generation requests. Please try again later.',
      statusCode: 429,
    },
  },
  standardHeaders: true,
  legacyHeaders: false,
});

export const generalRateLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 100, // 100 requests per minute
  message: {
    success: false,
    error: {
      message: 'Too many requests. Please try again later.',
      statusCode: 429,
    },
  },
  standardHeaders: true,
  legacyHeaders: false,
});
