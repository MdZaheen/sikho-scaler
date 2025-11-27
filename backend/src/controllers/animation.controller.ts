import { Request, Response, NextFunction } from 'express';
import pipelineOrchestrator from '../services/pipeline/orchestrator';
import { NotFoundError } from '../utils/errors';
import logger from '../utils/logger';

export class AnimationController {
  async generateAnimation(req: Request, res: Response, next: NextFunction) {
    try {
      const { text } = req.body;
      
      logger.info('Received animation generation request');
      
      const result = await pipelineOrchestrator.processText(text);
      
      res.status(201).json({
        success: true,
        data: result,
      });
    } catch (error) {
      next(error);
    }
  }

  async getAnimation(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      
      const animation = await pipelineOrchestrator.getAnimation(id);
      
      if (!animation) {
        throw new NotFoundError('Animation not found');
      }
      
      res.status(200).json({
        success: true,
        data: animation,
      });
    } catch (error) {
      next(error);
    }
  }

  async listAnimations(req: Request, res: Response, next: NextFunction) {
    try {
      const { limit, skip } = req.query;
      
      const animations = await pipelineOrchestrator.listAnimations(
        Number(limit) || 20,
        Number(skip) || 0
      );
      
      res.status(200).json({
        success: true,
        data: animations,
        pagination: {
          limit: Number(limit) || 20,
          skip: Number(skip) || 0,
          count: animations.length,
        },
      });
    } catch (error) {
      next(error);
    }
  }

  async deleteAnimation(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      
      const deleted = await pipelineOrchestrator.deleteAnimation(id);
      
      if (!deleted) {
        throw new NotFoundError('Animation not found');
      }
      
      res.status(200).json({
        success: true,
        message: 'Animation deleted successfully',
      });
    } catch (error) {
      next(error);
    }
  }
}

export default new AnimationController();
