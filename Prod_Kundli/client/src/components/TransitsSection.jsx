import React from 'react';

export default function TransitsSection({ transitsData, sadeSatiData }) {
  if (!transitsData) return null;

  return (
    <div className="card-vedic overflow-hidden">
      <div className="card-header-vedic px-4 py-3 flex items-center justify-between">
        <h3 className="font-bold text-amber-900 vedic-title flex items-center gap-2">
          <span>🌌</span> Gochar (Transits) & Shani Sade Sati
        </h3>
        <span className="text-xs text-amber-800 font-mono">
          As of: {transitsData.transit_date}
        </span>
      </div>

      <div className="p-4 space-y-5">
        {/* Sade Sati Card */}
        {sadeSatiData && (
          <div className={`p-4 rounded-xl border ${
            sadeSatiData.is_in_sade_sati
              ? 'bg-rose-50/60 border-rose-200'
              : sadeSatiData.is_in_dhaiya
              ? 'bg-amber-50/60 border-amber-200'
              : 'bg-emerald-50/60 border-emerald-200'
          }`}>
            <div className="flex items-center justify-between gap-2 mb-1">
              <span className="font-bold text-sm text-stone-900">Saturn's Current Influence: {sadeSatiData.phase}</span>
              <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                sadeSatiData.is_in_sade_sati ? 'bg-rose-100 text-rose-800' : 'bg-emerald-100 text-emerald-800'
              }`}>
                {sadeSatiData.is_in_sade_sati ? 'Active Sade Sati' : 'No Direct Sade Sati'}
              </span>
            </div>
            <p className="text-xs text-stone-600 mb-2">{sadeSatiData.description}</p>
            {sadeSatiData.remedies && (
              <div className="bg-white/80 p-2.5 rounded-lg border border-amber-100 text-xs">
                <strong className="text-amber-900 block mb-1">Traditional Saturn Remedies:</strong>
                <ul className="list-disc list-inside text-stone-700 space-y-0.5">
                  {sadeSatiData.remedies.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Gochar Table */}
        <div>
          <h4 className="text-sm font-bold text-amber-900 mb-2">Current Planetary Transits vs Natal Positions</h4>
          <div className="overflow-x-auto">
            <table className="vedic-table">
              <thead>
                <tr>
                  <th>Planet</th>
                  <th>Current Sign</th>
                  <th>Degree</th>
                  <th>House from Moon</th>
                  <th>House from Ascendant</th>
                  <th>Transit Effect</th>
                </tr>
              </thead>
              <tbody>
                {transitsData.transits?.map((t) => (
                  <tr key={t.planet}>
                    <td className="font-bold text-amber-950 flex items-center gap-1.5">
                      {t.planet}
                      {t.retrograde && <span className="badge-retro">R</span>}
                    </td>
                    <td>{t.current_sign}</td>
                    <td className="font-mono text-xs">{t.current_degree.toFixed(2)}°</td>
                    <td className="font-bold text-center">{t.house_from_moon}th</td>
                    <td className="font-bold text-center text-stone-600">{t.house_from_ascendant}th</td>
                    <td>
                      <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                        t.is_favorable ? 'bg-emerald-100 text-emerald-800' : 'bg-stone-100 text-stone-600'
                      }`}>
                        {t.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
