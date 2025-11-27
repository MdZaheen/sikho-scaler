// Simple test to verify OpenRouter API connection
import config from "./src/config/index.js";
import OpenAI from "openai";

console.log("🔍 Testing OpenRouter Configuration...\n");

// Check API key
console.log("API Key present:", config.llm.apiKey ? "✅ Yes" : "❌ No");
console.log(
  "API Key starts with sk-or-:",
  config.llm.apiKey.startsWith("sk-or-") ? "✅ Yes" : "❌ No"
);
console.log(
  "API Key (first 20 chars):",
  config.llm.apiKey.substring(0, 20) + "...\n"
);

// Test OpenRouter connection
const isOpenRouter = config.llm.apiKey.startsWith("sk-or-");
const client = new OpenAI({
  apiKey: config.llm.apiKey,
  baseURL: isOpenRouter ? "https://openrouter.ai/api/v1" : undefined,
  defaultHeaders: isOpenRouter
    ? {
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "SIKHO Animation Backend",
      }
    : undefined,
});

console.log("🚀 Making test request to OpenRouter...\n");

client.chat.completions
  .create({
    model: "openai/gpt-4-turbo-preview",
    messages: [
      {
        role: "system",
        content: "You are a helpful assistant. Respond in JSON format.",
      },
      {
        role: "user",
        content: 'Say hello in JSON format with a "message" field.',
      },
    ],
    response_format: { type: "json_object" },
  })
  .then((response) => {
    console.log("✅ SUCCESS! OpenRouter is working!\n");
    console.log("Response:", response.choices[0].message.content);
    console.log("\n✅ Backend is ready to generate animations!");
    process.exit(0);
  })
  .catch((error) => {
    console.error("❌ ERROR:", error.message);
    if (error.response) {
      console.error("Status:", error.response.status);
      console.error("Data:", JSON.stringify(error.response.data, null, 2));
    }
    process.exit(1);
  });
