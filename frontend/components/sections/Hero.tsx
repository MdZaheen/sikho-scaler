"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight, Play, Terminal, Activity } from "lucide-react";

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center pt-32 pb-20 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-background">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]" />
        <div className="absolute left-0 right-0 top-0 -z-10 m-auto h-[310px] w-[310px] rounded-full bg-primary/20 opacity-20 blur-[100px]" />
        <div className="absolute right-0 top-0 -z-10 h-[310px] w-[310px] rounded-full bg-purple-500/20 opacity-20 blur-[100px]" />
      </div>

      <div className="container mx-auto px-4 relative z-10 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 mb-8 hover:bg-white/10 transition-colors cursor-pointer backdrop-blur-sm"
        >
          <span className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
          </span>
          <span className="text-sm font-medium text-muted-foreground">v2.0 is now live</span>
          <ArrowRight className="w-4 h-4 text-muted-foreground" />
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-5xl md:text-8xl font-bold tracking-tight mb-8 leading-tight"
        >
          Build <span className="text-gradient">Faster</span> than
          <br />
          ever before.
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-xl text-muted-foreground max-w-2xl mx-auto mb-12 leading-relaxed"
        >
          The complete toolkit for modern developers. Create stunning applications with our sophisticated components and powerful backend services.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-20"
        >
          <Link
            href="/signup"
            className="w-full sm:w-auto px-8 py-4 rounded-full bg-white text-black font-bold hover:bg-gray-200 transition-all flex items-center justify-center gap-2 group shadow-[0_0_20px_rgba(255,255,255,0.3)] hover:shadow-[0_0_30px_rgba(255,255,255,0.5)]"
          >
            Start Building
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
          <button className="w-full sm:w-auto px-8 py-4 rounded-full bg-white/5 border border-white/10 text-white font-bold hover:bg-white/10 transition-all flex items-center justify-center gap-2 group backdrop-blur-sm">
            <div className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center group-hover:scale-110 transition-transform">
              <Play className="w-3 h-3 fill-current" />
            </div>
            Watch Demo
          </button>
        </motion.div>

        {/* Dashboard Preview */}
        <motion.div
          initial={{ opacity: 0, y: 40, rotateX: 20 }}
          animate={{ opacity: 1, y: 0, rotateX: 0 }}
          transition={{ duration: 0.8, delay: 0.4, type: "spring" }}
          className="relative mx-auto max-w-6xl perspective-1000"
        >
          <div className="glass-panel rounded-xl overflow-hidden shadow-2xl bg-black/40 backdrop-blur-xl border border-white/10 transform-gpu">
            {/* Window Controls */}
            <div className="px-4 py-3 border-b border-white/10 flex items-center justify-between bg-white/5">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-[#ff5f56]" />
                <div className="w-3 h-3 rounded-full bg-[#ffbd2e]" />
                <div className="w-3 h-3 rounded-full bg-[#27c93f]" />
              </div>
              <div className="flex items-center gap-2 px-3 py-1 rounded-md bg-black/50 border border-white/5 text-xs text-muted-foreground font-mono">
                <Terminal className="w-3 h-3" />
                sikho-app — -zsh — 80x24
              </div>
              <div className="w-16" />
            </div>

            {/* Dashboard Content */}
            <div className="p-6 grid grid-cols-12 gap-6 h-[500px] overflow-hidden">
              {/* Sidebar */}
              <div className="col-span-2 hidden md:flex flex-col gap-4 border-r border-white/5 pr-6">
                <div className="h-8 w-8 rounded-lg bg-primary/20 mb-4" />
                {[1, 2, 3, 4, 5].map((i) => (
                  <div key={i} className="h-8 w-full rounded-md bg-white/5 animate-pulse" style={{ opacity: 1 - i * 0.15 }} />
                ))}
              </div>

              {/* Main Content */}
              <div className="col-span-12 md:col-span-10 flex flex-col gap-6">
                {/* Header */}
                <div className="flex items-center justify-between">
                  <div className="h-8 w-48 rounded-md bg-white/5 animate-pulse" />
                  <div className="flex gap-2">
                    <div className="h-8 w-8 rounded-full bg-white/5" />
                    <div className="h-8 w-8 rounded-full bg-white/5" />
                  </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-3 gap-4">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/5">
                      <div className="flex items-center justify-between mb-4">
                        <div className="h-8 w-8 rounded-lg bg-primary/10 flex items-center justify-center">
                          <Activity className="w-4 h-4 text-primary" />
                        </div>
                        <span className="text-xs text-green-400">+12.5%</span>
                      </div>
                      <div className="h-6 w-24 bg-white/10 rounded mb-2" />
                      <div className="h-4 w-16 bg-white/5 rounded" />
                    </div>
                  ))}
                </div>

                {/* Chart Area */}
                <div className="flex-1 rounded-xl bg-white/5 border border-white/5 p-4 relative overflow-hidden group">
                  <div className="absolute inset-0 bg-gradient-to-t from-primary/5 to-transparent opacity-50" />
                  <div className="flex items-end justify-between h-full gap-2 px-4 pb-4">
                    {[40, 60, 45, 70, 50, 80, 65, 85, 75, 90, 60, 70].map((h, i) => (
                      <div 
                        key={i} 
                        className="w-full bg-primary/20 rounded-t-sm hover:bg-primary/40 transition-colors relative group/bar"
                        style={{ height: `${h}%` }}
                      >
                         <div className="absolute -top-8 left-1/2 -translate-x-1/2 px-2 py-1 bg-black border border-white/10 rounded text-xs opacity-0 group-hover/bar:opacity-100 transition-opacity">
                            {h}%
                         </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Glow Effect */}
          <div className="absolute -inset-4 bg-gradient-to-r from-primary to-purple-600 rounded-xl blur-3xl opacity-10 -z-10 group-hover:opacity-20 transition-opacity duration-500" />
        </motion.div>
      </div>
    </section>
  );
}
