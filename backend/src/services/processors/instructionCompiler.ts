import llmClient from '../llm/client';
import { INSTRUCTION_COMPILER_PROMPT } from '../llm/prompts';
import logger from '../../utils/logger';
import { SceneCollection } from './sceneGenerator';
import { Concept } from './conceptParser';

export interface TimelineInstruction {
  time: number;
  target: string;
  action: string;
  params: {
    from?: number;
    to?: number;
    duration: number;
    [key: string]: any;
  };
}

export interface AnimationObject {
  type: string;
  geometry: string;
  color: string;
  position?: { x: number; y: number; z: number };
  scale?: { x: number; y: number; z: number };
}

export interface AudioClip {
  time: number;
  clip: string;
}

export interface CompiledAnimation {
  timeline: TimelineInstruction[];
  objects: { [key: string]: AnimationObject };
  audio: AudioClip[];
  style: {
    background: string;
    themeColor: string;
  };
}

export class InstructionCompiler {
  async compile(
    concept: Concept,
    sceneCollection: SceneCollection
  ): Promise<CompiledAnimation> {
    logger.info('Starting instruction compilation');

    const prompt = this.buildPrompt(concept, sceneCollection);
    
    const compiled = await llmClient.generateJSON<CompiledAnimation>(
      prompt,
      INSTRUCTION_COMPILER_PROMPT,
      this.validateCompiled
    );

    // Sort timeline by time
    compiled.timeline.sort((a, b) => a.time - b.time);
    compiled.audio.sort((a, b) => a.time - b.time);

    logger.info(`Compiled ${compiled.timeline.length} timeline instructions`);
    return compiled;
  }

  private buildPrompt(concept: Concept, sceneCollection: SceneCollection): string {
    return `
Topic: ${concept.topic}
Style: ${concept.style.color} on ${concept.style.background}

Scenes:
${JSON.stringify(sceneCollection.scenes, null, 2)}

Compile these scenes into a flat GSAP timeline with absolute timestamps.
    `.trim();
  }

  private validateCompiled(data: any): boolean {
    if (!data || typeof data !== 'object') {
      return false;
    }

    const hasValidTimeline =
      Array.isArray(data.timeline) &&
      data.timeline.every(
        (inst: any) =>
          typeof inst.time === 'number' &&
          typeof inst.target === 'string' &&
          typeof inst.action === 'string' &&
          typeof inst.params === 'object' &&
          typeof inst.params.duration === 'number'
      );

    const hasValidObjects =
      typeof data.objects === 'object' &&
      Object.values(data.objects).every(
        (obj: any) =>
          typeof obj.type === 'string' &&
          typeof obj.geometry === 'string' &&
          typeof obj.color === 'string'
      );

    const hasValidAudio =
      Array.isArray(data.audio) &&
      data.audio.every(
        (clip: any) =>
          typeof clip.time === 'number' && typeof clip.clip === 'string'
      );

    const hasValidStyle =
      typeof data.style === 'object' &&
      typeof data.style.background === 'string' &&
      typeof data.style.themeColor === 'string';

    return hasValidTimeline && hasValidObjects && hasValidAudio && hasValidStyle;
  }
}

export default new InstructionCompiler();
