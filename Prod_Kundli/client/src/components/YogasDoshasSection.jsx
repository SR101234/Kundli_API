import React, { useState } from 'react';

export default function YogasDoshasSection({ yogas, doshas }) {
  const [filter, setFilter] = useState('all'); // 'all', 'yogas', 'doshas'

  const activeYogas = yogas?.filter(y => y.detected) || [];
  const activeDoshas = doshas?.filter(d => d.detected) || [];

  return (
    <div className="card-vedic overflow-hidden">
      <div className="card-header-vedic px-4 py-3 flex flex-wrap items-center justify-between gap-2">
        <h3 className="font-bold text-amber-900 vedic-title flex items-center gap-2">
          <span>🔮</span> Yogas & Doshas Analysis
        </h3>

        <div className="flex bg-amber-200/50 p-1 rounded-lg text-xs font-semibold">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 rounded-md transition ${filter === 'all' ? 'bg-amber-800 text-white shadow' : 'text-amber-950 hover:bg-amber-200'}`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('yogas')}
            className={`px-3 py-1 rounded-md transition ${filter === 'yogas' ? 'bg-amber-800 text-white shadow' : 'text-amber-950 hover:bg-amber-200'}`}
          >
            Yogas ({activeYogas.length})
          </button>
          <button
            onClick={() => setFilter('doshas')}
            className={`px-3 py-1 rounded-md transition ${filter === 'doshas' ? 'bg-amber-800 text-white shadow' : 'text-amber-950 hover:bg-amber-200'}`}
          >
            Doshas ({activeDoshas.length})
          </button>
        </div>
      </div>

      <div className="p-4 space-y-6">
        {/* Yogas Section */}
        {(filter === 'all' || filter === 'yogas') && (
          <div>
            <h4 className="text-sm font-bold text-emerald-900 mb-3 flex items-center gap-1.5">
              <span>🌟</span> Auspicious Yogas Detected ({activeYogas.length})
            </h4>

            {activeYogas.length === 0 ? (
              <p className="text-xs text-stone-500 italic">No major classical yogas detected under primary criteria.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {activeYogas.map((y, idx) => (
                  <div key={idx} className="p-3.5 bg-emerald-50/40 rounded-xl border border-emerald-200 shadow-xs">
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <span className="font-bold text-sm text-emerald-950">{y.name}</span>
                      <span className="text-[11px] bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded-full">
                        {y.category}
                      </span>
                    </div>
                    <p className="text-xs text-stone-600 mb-2">{y.description}</p>
                    <div className="bg-white/80 p-2 rounded border border-emerald-100">
                      <span className="text-[11px] font-bold text-emerald-900 block mb-1">Rule Evidence:</span>
                      <ul className="list-disc list-inside text-xs text-stone-700 space-y-0.5">
                        {y.conditions_met?.map((c, i) => (
                          <li key={i}>{c}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Doshas Section */}
        {(filter === 'all' || filter === 'doshas') && (
          <div>
            <h4 className="text-sm font-bold text-rose-900 mb-3 flex items-center gap-1.5">
              <span>⚠️</span> Inauspicious Doshas & Cancellations
            </h4>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {doshas?.map((d, idx) => {
                const isDetected = d.detected;
                const isCancelled = d.is_cancelled;
                return (
                  <div
                    key={idx}
                    className={`p-3.5 rounded-xl border shadow-xs ${
                      !isDetected
                        ? 'bg-stone-50/60 border-stone-200 opacity-70'
                        : isCancelled
                        ? 'bg-amber-50/50 border-amber-300'
                        : 'bg-rose-50/50 border-rose-200'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <span className="font-bold text-sm text-stone-900">{d.name}</span>
                      <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${
                        !isDetected
                          ? 'bg-stone-200 text-stone-700'
                          : isCancelled
                          ? 'bg-amber-200 text-amber-900'
                          : 'bg-rose-100 text-rose-800'
                      }`}>
                        {!isDetected ? 'Not Detected' : isCancelled ? 'Cancelled' : `Severity: ${d.severity}`}
                      </span>
                    </div>

                    <p className="text-xs text-stone-600 mb-2">{d.description}</p>

                    {isDetected && (
                      <div className="space-y-1.5">
                        {d.conditions_met?.length > 0 && (
                          <div className="bg-white/90 p-2 rounded border border-stone-200">
                            <span className="text-[11px] font-bold text-stone-800 block mb-0.5">Conditions:</span>
                            <ul className="list-disc list-inside text-xs text-stone-700">
                              {d.conditions_met.map((c, i) => (
                                <li key={i}>{c}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {isCancelled && d.cancellation_reasons?.length > 0 && (
                          <div className="bg-emerald-50 p-2 rounded border border-emerald-200 text-xs text-emerald-900">
                            <strong>Cancellation Factor:</strong> {d.cancellation_reasons.join(', ')}
                          </div>
                        )}

                        {!isCancelled && d.remedies?.length > 0 && (
                          <div className="bg-white/80 p-2 rounded border border-rose-100 text-xs text-stone-700">
                            <strong className="text-rose-900 block mb-0.5">Classical Remedies:</strong>
                            <ul className="list-disc list-inside">
                              {d.remedies.map((r, i) => (
                                <li key={i}>{r}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
