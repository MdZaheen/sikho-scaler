import llmClient from '../llm/client';
import { CONCEPT_PARSER_PROMPT } from '../llm/prompts';
import logger from '../../utils/logger';
import { ValidationError } from '../../utils/errors';

export interface Concept {
  topic: string;
  objects: string[];
  actions: string[];
  style: {
    color: string;
    background: string;
  };
}

export class ConceptParser {
  async parse(inputText: string): Promise<Concept> {
    logger.info('Starting concept parsing');

    if (!inputText || inputText.trim().length < 10) {
      throw new ValidationError('Input text must be at least 10 characters');
    }

    if (inputText.length > 2000) {
      throw new ValidationError('Input text must not exceed 2000 characters');
    }

    const concept = await llmClient.generateJSON<Concept>(
      inputText,
      CONCEPT_PARSER_PROMPT,
      this.validateConcept
    );

    logger.info(`Concept parsed successfully: ${concept.topic}`);
    return concept;
  }

  private validateConcept(data: any): boolean {
    return (
      typeof data === 'object' &&
      typeof data.topic === 'string' &&
      Array.isArray(data.objects) &&
      Array.isArray(data.actions) &&
      typeof data.style === 'object' &&
      typeof data.style.color === 'string' &&
      typeof data.style.background === 'string'
    );
  }
}

export default new ConceptParser();
