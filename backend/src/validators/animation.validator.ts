import { z } from 'zod';

export const generateAnimationSchema = z.object({
  text: z
    .string()
    .min(10, 'Text must be at least 10 characters')
    .max(2000, 'Text must not exceed 2000 characters')
    .trim(),
});

export const animationIdSchema = z.object({
  id: z.string().regex(/^[0-9a-fA-F]{24}$/, 'Invalid animation ID'),
});

export const paginationSchema = z.object({
  limit: z
    .string()
    .optional()
    .transform((val) => (val ? parseInt(val, 10) : 20))
    .refine((val) => val > 0 && val <= 100, 'Limit must be between 1 and 100'),
  skip: z
    .string()
    .optional()
    .transform((val) => (val ? parseInt(val, 10) : 0))
    .refine((val) => val >= 0, 'Skip must be non-negative'),
});

export type GenerateAnimationInput = z.infer<typeof generateAnimationSchema>;
export type AnimationIdInput = z.infer<typeof animationIdSchema>;
export type PaginationInput = z.infer<typeof paginationSchema>;
