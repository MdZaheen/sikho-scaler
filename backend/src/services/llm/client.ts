import OpenAI from "openai";
import config from "../../config";
import logger from "../../utils/logger";
import { LLMError } from "../../utils/errors";

class LLMClient {
  private client: OpenAI;
  private maxRetries: number = 3;
  private retryDelay: number = 1000;

  constructor() {
    if (!config.llm.apiKey) {
      throw new LLMError("LLM API key not configured");
    }

    // Check if using OpenRouter (starts with sk-or-)
    const isOpenRouter = config.llm.apiKey.startsWith("sk-or-");

    this.client = new OpenAI({
      apiKey: config.llm.apiKey,
      baseURL: isOpenRouter ? "https://openrouter.ai/api/v1" : undefined,
      defaultHeaders: isOpenRouter
        ? {
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "SIKHO Animation Backend",
          }
        : undefined,
    });
  }

  async generateCompletion(
    prompt: string,
    systemPrompt: string,
    temperature: number = 0.7
  ): Promise<string> {
    let lastError: Error | null = null;

    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        logger.info(`LLM request attempt ${attempt}/${this.maxRetries}`);

        // Use appropriate model based on API provider
        const isOpenRouter = config.llm.apiKey.startsWith("sk-or-");
        const model = isOpenRouter
          ? "openai/gpt-4-turbo-preview"
          : "gpt-4-turbo-preview";

        const response = await this.client.chat.completions.create({
          model,
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: prompt },
          ],
          temperature,
          response_format: { type: "json_object" },
        });

        const content = response.choices[0]?.message?.content;

        if (!content) {
          throw new LLMError("Empty response from LLM");
        }

        logger.info("LLM request successful");
        return content;
      } catch (error: any) {
        lastError = error;
        logger.error(`LLM request failed (attempt ${attempt}):`, error.message);

        if (attempt < this.maxRetries) {
          const delay = this.retryDelay * Math.pow(2, attempt - 1);
          logger.info(`Retrying in ${delay}ms...`);
          await this.sleep(delay);
        }
      }
    }

    throw new LLMError(
      `LLM request failed after ${this.maxRetries} attempts: ${lastError?.message}`
    );
  }

  async generateJSON<T>(
    prompt: string,
    systemPrompt: string,
    validator?: (data: any) => boolean
  ): Promise<T> {
    const response = await this.generateCompletion(prompt, systemPrompt);

    try {
      const parsed = JSON.parse(response);

      if (validator && !validator(parsed)) {
        throw new LLMError("LLM response validation failed");
      }

      return parsed as T;
    } catch (error: any) {
      logger.error("Failed to parse LLM response:", error.message);
      throw new LLMError("Invalid JSON response from LLM");
    }
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

export default new LLMClient();
