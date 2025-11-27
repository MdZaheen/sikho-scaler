import logger from '../../utils/logger';
import conceptParser, { Concept } from '../processors/conceptParser';
import sceneGenerator, { SceneCollection } from '../processors/sceneGenerator';
import instructionCompiler, { CompiledAnimation } from '../processors/instructionCompiler';
import Animation, { IAnimation } from '../../models/Animation.model';
import { DatabaseError } from '../../utils/errors';

export interface AnimationResult {
  id: string;
  inputText: string;
  concept: Concept;
  scenes: SceneCollection['scenes'];
  timeline: CompiledAnimation['timeline'];
  objects: CompiledAnimation['objects'];
  audio: CompiledAnimation['audio'];
  style: CompiledAnimation['style'];
  status: string;
  createdAt: Date;
  updatedAt: Date;
}

export class PipelineOrchestrator {
  async processText(inputText: string): Promise<AnimationResult> {
    logger.info('Starting animation pipeline');

    // Create initial animation record
    const animation = new Animation({
      inputText,
      status: 'processing',
    });

    try {
      await animation.save();
      logger.info(`Animation record created: ${animation._id}`);

      // Step 1: Parse text to concept
      logger.info('Step 1/3: Parsing concept');
      const concept = await conceptParser.parse(inputText);
      animation.concept = concept;
      await animation.save();

      // Step 2: Generate scenes
      logger.info('Step 2/3: Generating scenes');
      const sceneCollection = await sceneGenerator.generate(concept);
      animation.scenes = sceneCollection.scenes;
      await animation.save();

      // Step 3: Compile instructions
      logger.info('Step 3/3: Compiling instructions');
      const compiled = await instructionCompiler.compile(concept, sceneCollection);
      animation.timeline = compiled.timeline;
      animation.objects = compiled.objects;
      animation.audio = compiled.audio;
      animation.style = compiled.style;
      animation.status = 'completed';
      await animation.save();

      logger.info(`Animation pipeline completed: ${animation._id}`);

      return this.formatResult(animation);
      
    } catch (error: any) {
      logger.error('Animation pipeline failed:', error);
      animation.status = 'failed';
      animation.error = error.message;
      await animation.save();
      throw error;
    }
  }

  async getAnimation(id: string): Promise<AnimationResult | null> {
    try {
      const animation = await Animation.findById(id);
      if (!animation) {
        return null;
      }
      return this.formatResult(animation);
    } catch (error: any) {
      logger.error('Failed to retrieve animation:', error);
      throw new DatabaseError('Failed to retrieve animation');
    }
  }

  async listAnimations(limit: number = 20, skip: number = 0): Promise<AnimationResult[]> {
    try {
      const animations = await Animation.find()
        .sort({ createdAt: -1 })
        .limit(limit)
        .skip(skip);
      
      return animations.map(this.formatResult);
    } catch (error: any) {
      logger.error('Failed to list animations:', error);
      throw new DatabaseError('Failed to list animations');
    }
  }

  async deleteAnimation(id: string): Promise<boolean> {
    try {
      const result = await Animation.findByIdAndDelete(id);
      return result !== null;
    } catch (error: any) {
      logger.error('Failed to delete animation:', error);
      throw new DatabaseError('Failed to delete animation');
    }
  }

  private formatResult(animation: IAnimation): AnimationResult {
    return {
      id: animation._id.toString(),
      inputText: animation.inputText,
      concept: animation.concept,
      scenes: animation.scenes,
      timeline: animation.timeline,
      objects: animation.objects,
      audio: animation.audio,
      style: animation.style,
      status: animation.status,
      createdAt: animation.createdAt,
      updatedAt: animation.updatedAt,
    };
  }
}

export default new PipelineOrchestrator();
