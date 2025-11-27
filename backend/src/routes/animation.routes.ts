import { Router } from 'express';
import animationController from '../controllers/animation.controller';
import { validate } from '../middleware/validation';
import { generateRateLimiter } from '../middleware/rateLimiter';
import {
  generateAnimationSchema,
  animationIdSchema,
  paginationSchema,
} from '../validators/animation.validator';

const router = Router();

// POST /api/generate - Generate animation from text
router.post(
  '/generate',
  generateRateLimiter,
  validate(generateAnimationSchema, 'body'),
  animationController.generateAnimation
);

// GET /api/animation/:id - Get animation by ID
router.get(
  '/animation/:id',
  validate(animationIdSchema, 'params'),
  animationController.getAnimation
);

// GET /api/animations - List all animations
router.get(
  '/animations',
  validate(paginationSchema, 'query'),
  animationController.listAnimations
);

// DELETE /api/animation/:id - Delete animation
router.delete(
  '/animation/:id',
  validate(animationIdSchema, 'params'),
  animationController.deleteAnimation
);

export default router;
