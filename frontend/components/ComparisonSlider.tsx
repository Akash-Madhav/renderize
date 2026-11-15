"use client";

import { useState, useRef, useCallback } from "react";
import Image from "next/image";
import { MoveHorizontal, ZoomIn, ZoomOut, RotateCcw } from "lucide-react";

interface ComparisonSliderProps {
  originalUrl: string;
  renderedUrl: string;
  originalLabel?: string;
  renderedLabel?: string;
}

export default function ComparisonSlider({
  originalUrl,
  renderedUrl,
  originalLabel = "Raw CAD Blueprint (Input)",
  renderedLabel = "Architectural Render (Output)"
}: ComparisonSliderProps) {
  const [sliderPosition, setSliderPosition] = useState<number>(50);
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [zoom, setZoom] = useState<number>(1);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleMove = useCallback((clientX: number) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = clientX - rect.left;
    const pos = Math.max(0, Math.min(100, (x / rect.width) * 100));
    setSliderPosition(pos);
  }, []);

  const handleTouchMove = (e: React.TouchEvent) => {
    if (isDragging) {
      handleMove(e.touches[0].clientX);
    }
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (isDragging) {
      handleMove(e.clientX);
    }
  };

  return (
    <div className="relative rounded-xl overflow-hidden border border-slate-800 bg-[#0A0D14] select-none shadow-2xl">
      {/* Zoom and Controls Header */}
      <div className="absolute top-4 right-4 z-30 flex items-center gap-1.5 bg-slate-900/80 backdrop-blur-md border border-slate-700/60 p-1 rounded-lg text-slate-300">
        <button
          onClick={() => setZoom(prev => Math.min(3, prev + 0.25))}
          className="p-1.5 hover:bg-slate-800 rounded hover:text-white transition-colors"
          title="Zoom In"
        >
          <ZoomIn className="w-4 h-4" />
        </button>
        <button
          onClick={() => setZoom(prev => Math.max(0.75, prev - 0.25))}
          className="p-1.5 hover:bg-slate-800 rounded hover:text-white transition-colors"
          title="Zoom Out"
        >
          <ZoomOut className="w-4 h-4" />
        </button>
        <button
          onClick={() => { setZoom(1); setSliderPosition(50); }}
          className="p-1.5 hover:bg-slate-800 rounded hover:text-white transition-colors"
          title="Reset View"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
      </div>

      {/* Floating Badges */}
      <div className="absolute top-4 left-4 z-20 pointer-events-none">
        <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-slate-950/80 backdrop-blur-md text-slate-300 border border-slate-700/60 shadow">
          {originalLabel}
        </span>
      </div>
      <div className="absolute top-4 right-28 z-20 pointer-events-none">
        <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-amber-500/20 backdrop-blur-md text-amber-300 border border-amber-500/40 shadow">
          {renderedLabel}
        </span>
      </div>

      {/* Slider Canvas Container */}
      <div
        ref={containerRef}
        className="relative w-full aspect-[4/3] md:aspect-[16/10] overflow-hidden cursor-ew-resize"
        onMouseDown={() => setIsDragging(true)}
        onMouseUp={() => setIsDragging(false)}
        onMouseLeave={() => setIsDragging(false)}
        onMouseMove={handleMouseMove}
        onTouchStart={() => setIsDragging(true)}
        onTouchEnd={() => setIsDragging(false)}
        onTouchMove={handleTouchMove}
      >
        {/* Layer 1: Rendered Presentation (Full Background Layer) */}
        <div
          className="absolute inset-0 w-full h-full flex items-center justify-center p-4 transition-transform duration-100"
          style={{ transform: `scale(${zoom})` }}
        >
          <img
            src={renderedUrl}
            alt="Architectural Render"
            className="max-w-full max-h-full object-contain pointer-events-none select-none drop-shadow-md"
          />
        </div>

        {/* Layer 2: Raw CAD (Clipped Layer based on slider position) */}
        <div
          className="absolute inset-0 w-full h-full overflow-hidden transition-transform duration-100"
          style={{
            clipPath: `polygon(0 0, ${sliderPosition}% 0, ${sliderPosition}% 100%, 0 100%)`,
            transform: `scale(${zoom})`
          }}
        >
          <div className="w-full h-full flex items-center justify-center p-4 bg-[#F7FBFE]">
            <img
              src={originalUrl}
              alt="Raw CAD Drawing"
              className="max-w-full max-h-full object-contain pointer-events-none select-none"
            />
          </div>
        </div>

        {/* Draggable Divider Line & Knob */}
        <div
          className="absolute top-0 bottom-0 z-20 w-0.5 bg-amber-400 shadow-[0_0_12px_rgba(251,191,36,0.8)]"
          style={{ left: `${sliderPosition}%` }}
        >
          <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-slate-950 border-2 border-amber-400 flex items-center justify-center text-amber-400 shadow-xl cursor-ew-resize hover:scale-110 active:scale-95 transition-transform">
            <MoveHorizontal className="w-4 h-4" />
          </div>
        </div>
      </div>

      {/* Footer Helper */}
      <div className="p-3 bg-slate-950/90 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
        <span>Drag the slider horizontally to compare wall alignments and material textures</span>
        <span className="font-mono text-amber-400/80">{Math.round(sliderPosition)}% split</span>
      </div>
    </div>
  );
}
