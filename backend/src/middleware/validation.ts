import { Request, Response, NextFunction } from "express";
import { AnyZodObject, ZodError } from "zod";
import { ValidationError } from "../utils/errors";
import logger from "../utils/logger";

export const validate =
  (schema: AnyZodObject, source: "body" | "params" | "query" = "body") =>
  async (req: Request, _res: Response, next: NextFunction) => {
    try {
      const data =
        source === "body"
          ? req.body
          : source === "params"
            ? req.params
            : req.query;

      const validated = await schema.parseAsync(data);

      if (source === "body") {
        req.body = validated;
      } else if (source === "params") {
        req.params = validated as any;
      } else {
        req.query = validated as any;
      }

      next();
    } catch (error) {
      if (error instanceof ZodError) {
        const messages = error.errors.map(
          (err) => `${err.path.join(".")}: ${err.message}`
        );
        logger.warn("Validation error:", messages);
        next(new ValidationError(messages.join(", ")));
      } else {
        next(error);
      }
    }
  };
