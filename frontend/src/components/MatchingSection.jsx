import React, { useState } from 'react';
import { matchKundli } from '../api/kundliApi';

export default function MatchingSection({ defaultGroom }) {
  const [groom, setGroom] = useState(defaultGroom || {
    name: "Groom",
    date: "2001-08-15",
    time: "14:35:00",
    timezone: "Asia/Kolkata",
    latitude: 27.1767,
    longitude: 78.0081,
    ayanamsa: "Lahiri"
  });

  const [bride, setBride] = useState({
    name: "Bride",
    date: "2002-11-20",
    time: "10:15:00",
    timezone: "Asia/Kolkata",
    latitude: 28.6139,
    longitude: 77.2090,
    ayanamsa: "Lahiri"
  });

  const [matchResult, setMatchResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleMatch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await matchKundli(groom, bride);
      setMatchResult(res);
    } catch (err) {
      setError(err.message || 'Error calculating match');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card-vedic overflow-hidden">
      <div className="card-header-vedic px-4 py-3 flex items-center justify-between">
        <h3 className="font-bold text-amber-900 vedic-title flex items-center gap-2">
          <span>💍</span> Kundli Milan (36-Gun Marriage Compatibility)
        </h3>
        <span className="text-xs bg-amber-200/60 text-amber-950 font-bold px-2.5 py-1 rounded-full">
          Ashtakoota & Manglik Matching
        </span>
      </div>

      <div className="p-4 space-y-5">
        <form onSubmit={handleMatch} className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Groom Input */}
          <div className="p-3 bg-amber-50/50 rounded-xl border border-amber-200 space-y-2.5">
            <h4 className="text-xs font-bold text-amber-900 uppercase tracking-wider flex items-center gap-1.5">
              <span>🤵</span> Boy (Var) Details
            </h4>
            <div>
              <label className="text-[11px] font-semibold text-stone-600 block">Name</label>
              <input
                type="text"
                value={groom.name}
                onChange={e => setGroom({...groom, name: e.target.value})}
                className="w-full px-2.5 py-1.5 border border-amber-200 rounded text-xs bg-white"
                required
              />
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-[11px] font-semibold text-stone-600 block">Date of Birth</label>
                <input
                  type="date"
                  value={groom.date}
                  onChange={e => setGroom({...groom, date: e.target.value})}
                  className="w-full px-2.5 py-1.5 border border-amber-200 rounded text-xs bg-white"
                  required
                />
              </div>
              <div>
                <label className="text-[11px] font-semibold text-stone-600 block">Time of Birth</label>
                <input
                  type="time"
                  step="1"
                  value={groom.time}
                  onChange={e => setGroom({...groom, time: e.target.value})}
                  className="w-full px-2.5 py-1.5 border border-amber-200 rounded text-xs bg-white"
                  required
                />
              </div>
            </div>
          </div>

          {/* Bride Input */}
          <div className="p-3 bg-rose-50/40 rounded-xl border border-rose-200 space-y-2.5">
            <h4 className="text-xs font-bold text-rose-900 uppercase tracking-wider flex items-center gap-1.5">
              <span>👰</span> Girl (Kanya) Details
            </h4>
            <div>
              <label className="text-[11px] font-semibold text-stone-600 block">Name</label>
              <input
                type="text"
                value={bride.name}
                onChange={e => setBride({...bride, name: e.target.value})}
                className="w-full px-2.5 py-1.5 border border-rose-200 rounded text-xs bg-white"
                required
              />
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-[11px] font-semibold text-stone-600 block">Date of Birth</label>
                <input
                  type="date"
                  value={bride.date}
                  onChange={e => setBride({...bride, date: e.target.value})}
                  className="w-full px-2.5 py-1.5 border border-rose-200 rounded text-xs bg-white"
                  required
                />
              </div>
              <div>
                <label className="text-[11px] font-semibold text-stone-600 block">Time of Birth</label>
                <input
                  type="time"
                  step="1"
                  value={bride.time}
                  onChange={e => setBride({...bride, time: e.target.value})}
                  className="w-full px-2.5 py-1.5 border border-rose-200 rounded text-xs bg-white"
                  required
                />
              </div>
            </div>
          </div>

          <div className="md:col-span-2">
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-gradient-to-r from-amber-600 to-amber-700 text-white font-bold rounded-xl text-xs uppercase tracking-wider hover:from-amber-700 hover:to-amber-800 transition cursor-pointer shadow-sm"
            >
              {loading ? 'Matching Charts...' : 'Compare 36 Gun Milan & Manglik Compatibility'}
            </button>
          </div>
        </form>

        {error && (
          <div className="p-3 bg-red-50 text-red-700 text-xs rounded-lg border border-red-200">
            {error}
          </div>
        )}

        {/* Results */}
        {matchResult && (
          <div className="space-y-4 pt-3 border-t border-amber-100">
            {/* Score Banner */}
            <div className="p-4 bg-gradient-to-r from-amber-100 to-amber-200 rounded-xl border border-amber-300 flex flex-wrap items-center justify-between gap-3">
              <div>
                <span className="text-xs uppercase font-semibold text-amber-900 block">Milan Result</span>
                <span className="text-2xl font-black text-amber-950">
                  {matchResult.ashtakoota.total_score} / 36 Gun
                </span>
                <span className="text-xs text-amber-800 block mt-0.5 font-bold">
                  ({matchResult.ashtakoota.percentage}% Compatibility)
                </span>
              </div>
              <div className="text-right">
                <span className="text-sm font-bold text-amber-950 block">
                  {matchResult.ashtakoota.verdict}
                </span>
                <span className="text-xs font-semibold text-emerald-800 block">
                  {matchResult.overall_recommendation}
                </span>
              </div>
            </div>

            {/* Manglik Comparison */}
            <div className="p-3 bg-white rounded-xl border border-amber-200 text-xs">
              <span className="font-bold text-amber-900 block mb-1">Manglik Compatibility:</span>
              <p className="text-stone-700">{matchResult.manglik_matching.verdict}</p>
            </div>

            {/* 8 Kootas Table */}
            <div>
              <h4 className="text-xs font-bold text-amber-900 uppercase tracking-wider mb-2">
                Ashtakoota Breakdown (8 Classical Kootas)
              </h4>
              <div className="overflow-x-auto">
                <table className="vedic-table">
                  <thead>
                    <tr>
                      <th>Koota</th>
                      <th>Max</th>
                      <th>Obtained</th>
                      <th>Groom</th>
                      <th>Bride</th>
                      <th>Status / Notes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {matchResult.ashtakoota.koota_breakdown.map((k) => (
                      <tr key={k.name}>
                        <td className="font-bold text-amber-950 text-xs">{k.name}</td>
                        <td className="text-center font-mono">{k.max_score}</td>
                        <td className="text-center font-bold text-amber-800 font-mono">{k.obtained_score}</td>
                        <td className="text-xs text-stone-600">{k.groom_attribute}</td>
                        <td className="text-xs text-stone-600">{k.bride_attribute}</td>
                        <td className="text-xs">
                          {k.cancellation ? (
                            <span className="text-emerald-700 font-medium">{k.cancellation}</span>
                          ) : k.has_dosha ? (
                            <span className="text-rose-700 font-bold">Dosha</span>
                          ) : (
                            <span className="text-stone-500">Normal</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
