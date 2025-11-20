import React from "react";

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  className = "",
  title,
}) => {
  return (
    <div
      className={`bg-ara-surface/40 backdrop-blur-md border border-white/10 rounded-xl p-6 shadow-xl ${className}`}
    >
      {title && (
        <h3 className="text-lg font-medium text-slate-200 mb-4 border-b border-white/5 pb-2">
          {title}
        </h3>
      )}
      {children}
    </div>
  );
};
