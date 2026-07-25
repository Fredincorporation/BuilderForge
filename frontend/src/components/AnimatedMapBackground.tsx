import React from "react";

export function AnimatedMapBackground() {
  // Global network node locations (x, y mapped to 1000x500 viewport)
  const nodes = [
    { id: "sf", label: "SAN FRANCISCO", x: 190, y: 190 },
    { id: "ny", label: "NEW YORK", x: 290, y: 180 },
    { id: "london", label: "LONDON", x: 475, y: 155 },
    { id: "dubai", label: "DUBAI", x: 600, y: 225 },
    { id: "sg", label: "SINGAPORE", x: 740, y: 285 },
    { id: "tokyo", label: "TOKYO", x: 825, y: 200 },
    { id: "sydney", label: "SYDNEY", x: 840, y: 360 },
  ];

  // Connection Arcs between Web3 hubs
  const connections = [
    { from: "sf", to: "ny" },
    { from: "ny", to: "london" },
    { from: "london", to: "dubai" },
    { from: "dubai", to: "sg" },
    { from: "sg", to: "tokyo" },
    { from: "tokyo", to: "sf" },
    { from: "london", to: "tokyo" },
    { from: "dubai", to: "sydney" },
    { from: "ny", to: "sf" },
  ];

  const getNode = (id: string) => nodes.find((n) => n.id === id);

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none select-none z-0">
      {/* 1. Black, White, & Orange Minimalist Map Asset */}
      <img
        src="/okx_black_white_orange_map.png"
        alt="OKX World Network Map"
        className="absolute inset-0 w-full h-full object-cover opacity-25 mix-blend-screen scale-105 filter contrast-150 grayscale-0 transition-opacity duration-1000"
      />

      {/* 2. Focused Subtle Orange Radial Glow Behind Node Center */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[400px] bg-primary/10 rounded-full blur-[160px]" />

      {/* 3. Minimalist Dotted Grid Matrix Layer */}
      <div 
        className="absolute inset-0 opacity-[0.08]"
        style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, #ffffff 1px, transparent 0)`,
          backgroundSize: "32px 32px",
        }}
      />

      {/* 4. High-Contrast Interactive Vector Arc & Node Layer */}
      <svg
        viewBox="0 0 1000 500"
        className="absolute inset-0 w-full h-full opacity-80"
        preserveAspectRatio="xMidYMid slice"
      >
        <defs>
          {/* Orange Connection Arc Gradient */}
          <linearGradient id="okxOrangeArc" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#ff5500" stopOpacity="0.05" />
            <stop offset="50%" stopColor="#ff5500" stopOpacity="0.9" />
            <stop offset="100%" stopColor="#ff5500" stopOpacity="0.05" />
          </linearGradient>

          {/* Clean Neon Filter */}
          <filter id="okxNeonGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Connection Arcs */}
        {connections.map((conn, idx) => {
          const start = getNode(conn.from);
          const end = getNode(conn.to);
          if (!start || !end) return null;

          const midX = (start.x + end.x) / 2;
          const midY = (start.y + end.y) / 2 - Math.abs(start.x - end.x) * 0.22;
          const pathD = `M ${start.x} ${start.y} Q ${midX} ${midY} ${end.x} ${end.y}`;

          return (
            <g key={`${conn.from}-${conn.to}`}>
              {/* Subtle Static Guide Arc */}
              <path
                d={pathD}
                fill="none"
                stroke="#ffffff"
                strokeOpacity="0.08"
                strokeWidth="1"
              />

              {/* Animated Orange Data Pulse Arc */}
              <path
                d={pathD}
                fill="none"
                stroke="url(#okxOrangeArc)"
                strokeWidth="2"
                className={idx % 2 === 0 ? "animate-dash" : "animate-dash-reverse"}
                filter="url(#okxNeonGlow)"
              />
            </g>
          );
        })}

        {/* Clean Node Markers */}
        {nodes.map((node, i) => (
          <g key={node.id} transform={`translate(${node.x}, ${node.y})`}>
            {/* Pulsing Signal Ring */}
            <circle
              r="12"
              fill="none"
              stroke="#ff5500"
              strokeWidth="1.2"
              className="animate-ping opacity-40"
              style={{ animationDuration: `${2.8 + (i % 3) * 0.4}s` }}
            />

            {/* Solid White Core with Orange Border */}
            <circle
              r="4"
              fill="#ffffff"
              stroke="#ff5500"
              strokeWidth="2"
              filter="url(#okxNeonGlow)"
            />

            {/* Subtly Floating White Badge */}
            <g transform="translate(0, -12)">
              <text
                x="0"
                y="0"
                textAnchor="middle"
                className="text-[8px] font-mono fill-white tracking-widest font-bold opacity-80"
                style={{ textShadow: "0 1px 4px rgba(0,0,0,0.9)" }}
              >
                {node.label}
              </text>
            </g>
          </g>
        ))}
      </svg>

      {/* 5. Central Backdrop Mask to Guarantee 100% Text Readability */}
      <div 
        className="absolute inset-0"
        style={{
          background: `radial-gradient(circle at 50% 40%, rgba(14, 16, 22, 0.45) 0%, rgba(14, 16, 22, 0.95) 75%)`,
        }}
      />

      {/* Vignette Edge Transitions */}
      <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-background opacity-95" />
    </div>
  );
}
