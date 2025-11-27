import mongoose, { Schema, Document } from "mongoose";

export interface IAnimation extends Document {
  inputText: string;
  concept: {
    topic: string;
    objects: string[];
    actions: string[];
    style: {
      color: string;
      background: string;
    };
  };
  scenes: Array<{
    id: string;
    duration: number;
    objects: string[];
    actions: Array<{
      target: string;
      action: string;
      duration: number;
    }>;
  }>;
  timeline: Array<{
    time: number;
    target: string;
    action: string;
    params: {
      from?: number;
      to?: number;
      duration: number;
      [key: string]: any;
    };
  }>;
  objects: {
    [key: string]: {
      type: string;
      geometry: string;
      color: string;
      position?: { x: number; y: number; z: number };
      scale?: { x: number; y: number; z: number };
    };
  };
  audio: Array<{
    time: number;
    clip: string;
  }>;
  style: {
    background: string;
    themeColor: string;
  };
  status: "pending" | "processing" | "completed" | "failed";
  error?: string;
  createdAt: Date;
  updatedAt: Date;
}

const AnimationSchema = new Schema<IAnimation>(
  {
    inputText: {
      type: String,
      required: true,
      trim: true,
      minlength: 10,
      maxlength: 2000,
    },
    concept: {
      topic: { type: String, required: false },
      objects: [{ type: String }],
      actions: [{ type: String }],
      style: {
        color: { type: String, default: "cyan" },
        background: { type: String, default: "dark" },
      },
    },
    scenes: [
      {
        id: { type: String, required: true },
        duration: { type: Number, required: true },
        objects: [{ type: String }],
        actions: [
          {
            target: { type: String, required: true },
            action: { type: String, required: true },
            duration: { type: Number, required: true },
          },
        ],
      },
    ],
    timeline: [
      {
        time: { type: Number, required: true },
        target: { type: String, required: true },
        action: { type: String, required: true },
        params: { type: Schema.Types.Mixed, required: true },
      },
    ],
    objects: {
      type: Schema.Types.Mixed,
      default: {},
    },
    audio: [
      {
        time: { type: Number, required: true },
        clip: { type: String, required: true },
      },
    ],
    style: {
      background: { type: String, default: "#0f0f0f" },
      themeColor: { type: String, default: "cyan" },
    },
    status: {
      type: String,
      enum: ["pending", "processing", "completed", "failed"],
      default: "pending",
    },
    error: {
      type: String,
    },
  },
  {
    timestamps: true,
  }
);

// Indexes for performance
AnimationSchema.index({ createdAt: -1 });
AnimationSchema.index({ status: 1 });
AnimationSchema.index({ "concept.topic": "text" });

export default mongoose.model<IAnimation>("Animation", AnimationSchema);
