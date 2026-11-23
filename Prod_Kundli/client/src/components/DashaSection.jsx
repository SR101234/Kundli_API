import React, { useState } from 'react';

export default function DashaSection({ dashaData }) {
  const [expandedMaha, setExpandedMaha] = useState(null);
  const [dashaSystem, setDashaSystem] = useState('vimshottari'); // 'vimshottari' or 'yogini'

  if (!dashaData) return null;
  const { vimshottari, yogini } = dashaData;

  const toggleMaha = (lord) => {
    setExpandedMaha(expandedMaha === lord ? null : lord);
  };

  return (
    <div className="card-vedic overflow-hidden">
      <div className="card-header-vedic px-4 py-3 flex flex-wrap items-center justify-between gap-2">
        <h3 className="font-bold text-amber-900 vedic-title flex items-center gap-2">
          <span>⏳</span> Dasha Systems (Vimshottari & Yogini)
        </h3>

        <div className="flex bg-amber-200/50 p-1 rounded-lg text-xs font-semibold">
          <button
            onClick={() => setDashaSystem('vimshottari')}
            className={`px-3 py-1 rounded-md transition ${dashaSystem === 'vimshottari' ? 'bg-amber-800 text-white shadow' : 'text-amber-950 hover:bg-amber-200'}`}
          >
            Vimshottari (120Y)
          </button>
          <button
            onClick={() => setDashaSystem('yogini')}
            className={`px-3 py-1 rounded-md transition ${dashaSystem === 'yogini' ? 'bg-amber-800 text-white shadow' : 'text-amber-950 hover:bg-amber-200'}`}
          >
            Yogini (36Y)
          </button>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* Current Running Dasha Badge */}
        {vimshottari?.current_running && (
          <div className="p-3 bg-gradient-to-r from-amber-500 to-amber-600 rounded-xl text-white shadow-sm flex flex-wrap items-center justify-between gap-2">
            <div>
              <span className="text-xs uppercase tracking-wider font-semibold block text-amber-100">
                Current Running Vimshottari Period
              </span>
              <span className="text-lg font-black tracking-wide">
                {vimshottari.current_running.summary || 'Active Dasha'}
              </span>
            </div>
            <div className="text-right text-xs text-amber-100">
              <div>Balance at Birth: <strong>{vimshottari.balance_years} years</strong></div>
              <div>Starting Lord: <strong>{vimshottari.first_lord}</strong></div>
            </div>
          </div>
        )}

        {/* Vimshottari View */}
        {dashaSystem === 'vimshottari' && (
          <div className="space-y-2">
            <h4 className="text-sm font-bold text-amber-900 mb-2">9 Mahadashas (Click to expand Antardashas)</h4>
            <div className="divide-y divide-amber-100 border border-amber-200 rounded-xl overflow-hidden bg-white">
              {vimshottari?.mahadashas?.map((md) => {
                const isExpanded = expandedMaha === md.lord;
                return (
                  <div key={md.lord}>
                    <button
                      onClick={() => toggleMaha(md.lord)}
                      className="w-full px-4 py-3 flex items-center justify-between hover:bg-amber-50/60 transition text-left cursor-pointer"
                    >
                      <div className="flex items-center gap-3">
                        <span className="w-8 h-8 rounded-full bg-amber-100 text-amber-900 flex items-center justify-center font-bold text-xs">
                          {md.lord.slice(0, 2)}
                        </span>
                        <div>
                          <span className="font-bold text-stone-800 text-sm">{md.lord} Mahadasha</span>
                          <span className="text-xs text-stone-500 block font-mono">
                            {md.start_date} to {md.end_date}
                          </span>
                        </div>
                      </div>
                      <span className="text-amber-800 font-bold text-sm">
                        {isExpanded ? '▲' : '▼'}
                      </span>
                    </button>

                    {/* Antardashas dropdown */}
                    {isExpanded && (
                      <div className="bg-amber-50/40 px-4 py-2 border-t border-amber-100">
                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 py-1">
                          {md.antardashas?.map((ad) => (
                            <div key={ad.lord} className="p-2 bg-white rounded border border-amber-100 text-xs">
                              <span className="font-bold text-amber-900 block">{md.lord} - {ad.lord}</span>
                              <span className="text-[11px] text-stone-500 font-mono">
                                {ad.start_date} to {ad.end_date}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Yogini View */}
        {dashaSystem === 'yogini' && (
          <div>
            <div className="flex justify-between items-center mb-2">
              <h4 className="text-sm font-bold text-amber-900">Yogini Dasha (36-Year Cycle)</h4>
              <span className="text-xs text-stone-600">
                Starting: <strong>{yogini?.starting_yogini} ({yogini?.starting_lord})</strong> | Balance: {yogini?.balance_years}y
              </span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2">
              {yogini?.periods?.map((yp, idx) => (
                <div key={idx} className="p-3 bg-amber-50/60 rounded-xl border border-amber-200">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-amber-950 text-sm">{yp.yogini}</span>
                    <span className="text-xs bg-amber-200/70 text-amber-900 px-1.5 py-0.5 rounded font-semibold">
                      {yp.lord}
                    </span>
                  </div>
                  <span className="text-xs text-stone-600 block mt-1 font-mono">
                    {yp.start_date} → {yp.end_date}
                  </span>
                  <span className="text-[11px] text-stone-500 block">Span: {yp.years} years</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
