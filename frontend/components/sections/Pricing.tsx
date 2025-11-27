"use client";

import { motion } from "framer-motion";
import { Check, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

const plans = [
  {
    name: "Free Forever",
    price: 0,
    description: "Open source and free for everyone. No credit card required.",
    features: [
      "Unlimited projects",
      "Unlimited storage",
      "Community support",
      "Basic analytics",
      "SSO integration",
      "Audit logs",
      "API access",
    ],
    popular: true,
  },
];

export function Pricing() {
  return (
    <section id="pricing" className="py-32 relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/5 blur-[120px] rounded-full pointer-events-none" />

      <div className="container mx-auto px-4 relative z-10">
        <div className="text-center max-w-3xl mx-auto mb-20">
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl md:text-6xl font-bold mb-6 tracking-tight"
          >
            Simple, transparent <span className="text-gradient">pricing</span>
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-muted-foreground text-xl mb-10"
          >
            Everything is free. No hidden fees, no credit card required.
          </motion.p>
        </div>

        <div className="flex justify-center max-w-7xl mx-auto">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
              className={cn(
                "relative p-8 rounded-3xl border flex flex-col transition-all duration-300 group w-full max-w-md",
                "bg-white/5 border-primary/50 shadow-2xl shadow-primary/10 scale-105 z-10"
              )}
            >
              <div className="absolute -top-5 left-1/2 -translate-x-1/2 px-4 py-1.5 rounded-full bg-gradient-to-r from-primary to-purple-600 text-white text-sm font-bold shadow-lg flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 fill-white" />
                Everything Included
              </div>

              <div className="mb-8 text-center">
                <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                <p className="text-muted-foreground text-sm mb-6">{plan.description}</p>
                <div className="flex items-baseline justify-center gap-1">
                  <span className="text-5xl font-bold tracking-tight">
                    $0
                  </span>
                  <span className="text-muted-foreground">/forever</span>
                </div>
              </div>

              <ul className="space-y-4 mb-8 flex-1">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-3 text-sm text-muted-foreground group-hover:text-white transition-colors">
                    <div className="w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 transition-colors bg-primary/20 text-primary">
                      <Check className="w-3.5 h-3.5" />
                    </div>
                    {feature}
                  </li>
                ))}
              </ul>

              <button
                className="w-full py-4 rounded-xl font-bold transition-all duration-300 bg-primary text-white hover:bg-primary/90 shadow-lg hover:shadow-primary/25 hover:scale-[1.02]"
              >
                Get Started Now
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
