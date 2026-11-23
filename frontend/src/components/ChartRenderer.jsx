import React, { useState } from 'react';

export default function ChartRenderer({ d1Chart, svgNorth, svgSouth, title = "Janma Kundli (D1)" }) {
  const [style, setStyle] = useState('north'); // 'north' or 'south'

  return (
    <div className="card-vedic p-4">
      <div className="flex items-center justify-between mb-3 border-b border-amber-100 pb-2">
        <h3 className="text-lg font-bold text-amber-900 vedic-title flex items-center gap-2">
          <span>☸️</span> {title}
        </h3>
        <div className="flex bg-amber-100/60 p-1 rounded-lg text-xs font-semibold">
          <button
            onClick={() => setStyle('north')}
            className={`px-3 py-1 rounded-md transition ${style === 'north' ? 'bg-amber-700 text-white shadow' : 'text-amber-900 hover:bg-amber-200'}`}
          >
            North Indian
          </button>
          <button
            onClick={() => setStyle('south')}
            className={`px-3 py-1 rounded-md transition ${style === 'south' ? 'bg-amber-700 text-white shadow' : 'text-amber-900 hover:bg-amber-200'}`}
          >
            South Indian
          </button>
        </div>
      </div>

      <div className="flex justify-center items-center p-3 bg-amber-50/30 rounded-xl border border-amber-100 overflow-hidden">
        {style === 'north' ? (
          <div
            className="chart-container-box flex items-center justify-center drop-shadow-xs"
            dangerouslySetInnerHTML={{ __html: svgNorth }}
          />
        ) : (
          <div
            className="chart-container-box flex items-center justify-center drop-shadow-xs"
            dangerouslySetInnerHTML={{ __html: svgSouth }}
          />
        )}
      </div>

      <div className="mt-3 flex items-center justify-center gap-4 text-xs text-amber-800 font-medium">
        <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-amber-600 inline-block"></span> (R) Retrograde</span>
        <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-red-500 inline-block"></span> (C) Combust</span>
        <span className="flex items-center gap-1">Asc: <strong>{d1Chart?.ascendant_sign || ''} ({d1Chart?.ascendant_degree?.toFixed(2)}°)</strong></span>
      </div>
    </div>
  );
}
