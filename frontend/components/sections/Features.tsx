"use client";

import { motion } from "framer-motion";
import { Zap, Shield, Globe, Cpu, Layers, BarChart, ArrowUpRight } from "lucide-react";
import { cn } from "@/lib/utils";

const features = [
  {
    icon: Zap,
    title: "Lightning Fast",
    description: "Optimized for speed with edge computing and global CDN distribution.",
    className: "md:col-span-2",
  },
  {
    icon: Shield,
    title: "Enterprise Security",
    description: "Bank-grade encryption and SOC2 compliance out of the box.",
    className: "md:col-span-1",
  },
  {
    icon: Globe,
    title: "Global Scale",
    description: "Deploy to 35+ regions worldwide with a single click.",
    className: "md:col-span-1",
  },
  {
    icon: Cpu,
    title: "AI Powered",
    description: "Built-in AI capabilities to automate your workflow.",
    className: "md:col-span-2",
  },
  {
    icon: Layers,
    title: "Modern Stack",
    description: "Built on the latest technologies for maximum compatibility.",
    className: "md:col-span-1",
  },
  {
    icon: BarChart,
    title: "Real-time Analytics",
    description: "Deep insights into your application performance and usage.",
    className: "md:col-span-1",
  },
  {
    icon: Layers,
    title: "Seamless Integration",
    description: "Connect with your favorite tools in seconds.",
    className: "md:col-span-1",
  },
];

export function Features() {
  return (
    <section id="features" className="py-32 relative overflow-hidden bg-black/50">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-20">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="inline-block mb-4 px-4 py-1.5 rounded-full border border-primary/20 bg-primary/5 text-primary text-sm font-medium"
          >
            Features
          </motion.div>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-4xl md:text-6xl font-bold mb-6 tracking-tight"
          >
            Everything you need to <span className="text-gradient">scale</span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-muted-foreground text-xl leading-relaxed"
          >
            A complete suite of tools designed to help you build, deploy, and manage your applications with ease.
          </motion.p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
              className={cn(
                "glass-panel p-8 rounded-3xl hover:bg-white/5 transition-all group relative overflow-hidden",
                feature.className
              )}
            >
              <div className="absolute top-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity">
                <ArrowUpRight className="w-5 h-5 text-white/50" />
              </div>
              
              <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <feature.icon className="w-7 h-7 text-primary" />
              </div>
              
              <h3 className="text-2xl font-bold mb-3 group-hover:text-primary transition-colors">{feature.title}</h3>
              <p className="text-muted-foreground text-lg leading-relaxed">{feature.description}</p>
              
              {/* Hover Glow */}
              <div className="absolute -inset-px bg-gradient-to-r from-primary/20 to-purple-600/20 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
