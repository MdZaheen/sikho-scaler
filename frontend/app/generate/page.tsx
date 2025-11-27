"use client";

import { useState } from "react";
import { ArrowRight, Loader2, Play, Sparkles, Download, RefreshCw, Check, Clock } from "lucide-react";

interface GeneratedVideo {
  id: string;
  topic: string;
  url: string;
  timestamp: number;
}

export default function GeneratePage() {
  const [topic, setTopic] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [isDownloading, setIsDownloading] = useState(false);
  const [previousGenerations, setPreviousGenerations] = useState<GeneratedVideo[]>([]);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setIsGenerating(true);
    setVideoUrl(null);

    // Simulate API call
    setTimeout(() => {
      setIsGenerating(false);
      const newVideoUrl = "https://www.w3schools.com/html/mov_bbb.mp4";
      setVideoUrl(newVideoUrl);
      
      // Add current video to previous generations
      const newGeneration: GeneratedVideo = {
        id: Date.now().toString(),
        topic: topic,
        url: newVideoUrl,
        timestamp: Date.now(),
      };
      setPreviousGenerations((prev) => [newGeneration, ...prev]);
    }, 3000);
  };

  const handleDownload = () => {
    if (!videoUrl) return;

    setIsDownloading(true);
    try {
      // Use our proxy API route to force download
      const filename = `generated-video-${Date.now()}.mp4`;
      const downloadUrl = `/api/download?url=${encodeURIComponent(videoUrl)}&filename=${filename}`;
      
      // Create a temporary link to trigger the download
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = downloadUrl;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } catch (error) {
      console.error("Download failed:", error);
      // Fallback
      window.open(videoUrl, "_blank");
    } finally {
      setIsDownloading(false);
    }
  };

  const handleRegenerate = () => {
    setVideoUrl(null);
    setTopic("");
  };

  return (
    <main className="min-h-screen pt-24 pb-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-background to-background -z-10" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl -z-10 animate-pulse-slow" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl -z-10 animate-pulse-slow" style={{ animationDelay: "1s" }} />

      <div className="max-w-4xl mx-auto space-y-12">
        {/* Header */}
        <div className="text-center space-y-4 animate-fade-in">
          <div className="inline-flex items-center px-3 py-1 rounded-full border border-blue-500/20 bg-blue-500/10 text-blue-400 text-sm font-medium mb-4">
            <Sparkles className="w-4 h-4 mr-2" />
            AI Video Generation
          </div>
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
            Turn your ideas into <span className="text-gradient-blue">Videos</span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Describe your topic and let our AI create a professional video for you in seconds.
          </p>
        </div>

        {/* Input Section */}
        {!videoUrl ? (
          <div className="glass-panel p-8 rounded-2xl animate-fade-in-up" style={{ animationDelay: "0.1s" }}>
            <form onSubmit={handleGenerate} className="space-y-6">
              <div className="space-y-2">
                <label htmlFor="topic" className="text-sm font-medium text-gray-200">
                  What's your video about?
                </label>
                <div className="relative">
                  <input
                    id="topic"
                    type="text"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="e.g., The history of artificial intelligence..."
                    className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-4 text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
                    disabled={isGenerating}
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={!topic.trim() || isGenerating}
                className="w-full group relative flex items-center justify-center px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white rounded-xl font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden shadow-lg shadow-blue-500/20"
              >
                <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
                {isGenerating ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Generating Magic...
                  </>
                ) : (
                  <>
                    Generate Video
                    <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </button>
            </form>
          </div>
        ) : (
          /* Video Result Section */
          <div className="glass-panel p-2 rounded-2xl animate-fade-in-up overflow-hidden ring-1 ring-white/10 shadow-2xl" style={{ animationDelay: "0.2s" }}>
            <div className="relative aspect-video bg-black rounded-xl overflow-hidden group">
              <video
                src={videoUrl}
                controls
                className="w-full h-full object-cover"
                poster="/placeholder-video-thumb.jpg"
              >
                Your browser does not support the video tag.
              </video>
            </div>
            <div className="p-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h3 className="text-xl font-semibold text-white mb-1 flex items-center gap-2">
                  {topic}
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-500/10 text-green-400 border border-green-500/20">
                    <Check className="w-3 h-3 mr-1" />
                    Ready
                  </span>
                </h3>
                <p className="text-sm text-gray-400">Generated successfully in 3.2s</p>
              </div>
              <div className="flex items-center gap-3 w-full sm:w-auto">
                <button
                  onClick={handleRegenerate}
                  className="flex-1 sm:flex-none inline-flex items-center justify-center px-4 py-2 bg-white/5 hover:bg-white/10 text-gray-300 rounded-lg text-sm font-medium transition-colors border border-white/5"
                >
                  <RefreshCw className="w-4 h-4 mr-2" />
                  New Video
                </button>
                <button
                  onClick={handleDownload}
                  disabled={isDownloading}
                  className="flex-1 sm:flex-none inline-flex items-center justify-center px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-medium transition-colors shadow-lg shadow-blue-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isDownloading ? (
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  ) : (
                    <Download className="w-4 h-4 mr-2" />
                  )}
                  Download
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Previous Generations Section */}
        {previousGenerations.length > 0 && (
          <div className="mt-16 animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
            <div className="flex items-center gap-2 mb-6">
              <Clock className="w-5 h-5 text-blue-400" />
              <h2 className="text-2xl font-semibold text-white">Previous Generations</h2>
              <span className="text-sm text-gray-400">({previousGenerations.length})</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {previousGenerations.map((video) => (
                <div
                  key={video.id}
                  className="glass-panel p-4 rounded-xl hover:ring-2 hover:ring-blue-500/30 transition-all group"
                >
                  <div className="relative aspect-video bg-black rounded-lg overflow-hidden mb-3">
                    <video
                      src={video.url}
                      className="w-full h-full object-cover"
                      poster="/placeholder-video-thumb.jpg"
                    >
                      Your browser does not support the video tag.
                    </video>
                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                      <Play className="w-12 h-12 text-white" />
                    </div>
                  </div>
                  <h3 className="text-sm font-medium text-white mb-1 truncate">{video.topic}</h3>
                  <p className="text-xs text-gray-400 mb-3">
                    {new Date(video.timestamp).toLocaleString()}
                  </p>
                  <button
                    onClick={() => {
                      const filename = `${video.topic.replace(/\s+/g, '-').toLowerCase()}-${video.id}.mp4`;
                      const downloadUrl = `/api/download?url=${encodeURIComponent(video.url)}&filename=${filename}`;
                      const a = document.createElement("a");
                      a.style.display = "none";
                      a.href = downloadUrl;
                      document.body.appendChild(a);
                      a.click();
                      document.body.removeChild(a);
                    }}
                    className="w-full inline-flex items-center justify-center px-3 py-2 bg-blue-600/20 hover:bg-blue-600 text-blue-400 hover:text-white rounded-lg text-xs font-medium transition-colors border border-blue-500/20"
                  >
                    <Download className="w-3 h-3 mr-2" />
                    Download
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
