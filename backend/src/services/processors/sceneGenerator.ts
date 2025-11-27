import llmClient from '../llm/client';
import { SCENE_GENERATOR_PROMPT } from '../llm/prompts';
import logger from '../../utils/logger';
import { Concept } from './conceptParser';

export interface Scene {
  id: string;
  duration: number;
  objects: string[];
  actions: Array<{
    target: string;
    action: string;
    duration: number;
  }>;
}

export interface SceneCollection {
  scenes: Scene[];
}

export class SceneGenerator {
  async generate(concept: Concept): Promise<SceneCollection> {
    logger.info('Starting scene generation');

    const prompt = this.buildPrompt(concept);
    
    const sceneCollection = await llmClient.generateJSON<SceneCollection>(
      prompt,
      SCENE_GENERATOR_PROMPT,
      this.validateScenes
    );

    logger.info(`Generated ${sceneCollection.scenes.length} scenes`);
    return sceneCollection;
  }

  private buildPrompt(concept: Concept): string {
    return `
Topic: ${concept.topic}
Objects: ${concept.objects.join(', ')}
Actions: ${concept.actions.join(', ')}
Style: ${concept.style.color} on ${concept.style.background}

Create a sequence of scenes that effectively teaches this concept through animation.
    `.trim();
  }

  private validateScenes(data: any): boolean {
    if (!data || !Array.isArray(data.scenes)) {
      return false;
    }

    return data.scenes.every(
      (scene: any) =>
        typeof scene.id === 'string' &&
        typeof scene.duration === 'number' &&
        Array.isArray(scene.objects) &&
        Array.isArray(scene.actions) &&
        scene.actions.every(
          (action: any) =>
            typeof action.target === 'string' &&
            typeof action.action === 'string' &&
            typeof action.duration === 'number'
        )
    );
  }
}

export default new SceneGenerator();
