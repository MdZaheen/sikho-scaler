import { Router, Request, Response } from "express";
import mongoose from "mongoose";

const router = Router();

router.get("/health", (_req: Request, res: Response) => {
  const dbStatus =
    mongoose.connection.readyState === 1 ? "connected" : "disconnected";

  res.status(200).json({
    success: true,
    status: "ok",
    database: dbStatus,
    timestamp: new Date().toISOString(),
  });
});

export default router;
