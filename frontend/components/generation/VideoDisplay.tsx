"use client";

import { Play, Download, Share2 } from "lucide-react";

interface VideoDisplayProps {
  videoUrl: string | null;
  isGenerating: boolean;
}

export default function VideoDisplay({ videoUrl, isGenerating }: VideoDisplayProps) {
  if (isGenerating) {
    return (
      <div className="w-full max-w-2xl mx-auto aspect-video bg-white/5 border border-white/10 rounded-xl flex flex-col items-center justify-center gap-4 animate-pulse">
        <div className="w-16 h-16 rounded-full bg-white/10 flex items-center justify-center">
          <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
        </div>
        <p className="text-white/50 text-sm">Creating your masterpiece...</p>
      </div>
    );
  }

  if (!videoUrl) {
    return (
      <div className="w-full max-w-2xl mx-auto aspect-video bg-white/5 border border-white/10 rounded-xl flex flex-col items-center justify-center gap-4">
        <div className="w-16 h-16 rounded-full bg-white/10 flex items-center justify-center text-white/20">
          <Play className="w-8 h-8 ml-1" />
        </div>
        <p className="text-white/30 text-sm">Your generated video will appear here</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-2xl mx-auto space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="relative aspect-video bg-black rounded-xl overflow-hidden border border-white/10 shadow-2xl shadow-purple-500/10 group">
        <video
          src={videoUrl}
          controls
          className="w-full h-full object-cover"
          poster="/placeholder-poster.jpg" // You might want to add a real placeholder
        />
      </div>
      
      <div className="flex items-center justify-between gap-4">
        <button className="flex-1 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-white/70 text-sm font-medium transition-colors flex items-center justify-center gap-2">
          <Download className="w-4 h-4" />
          Download
        </button>
        <button className="flex-1 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-white/70 text-sm font-medium transition-colors flex items-center justify-center gap-2">
          <Share2 className="w-4 h-4" />
          Share
        </button>
      </div>
    </div>
  );
}
