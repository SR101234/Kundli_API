import React, { useState } from 'react';

const DIVISIONAL_TITLES = {
  "D1": "Rashi (Overall Life)",
  "D2": "Hora (Wealth & Resources)",
  "D3": "Drekkana (Siblings & Vitality)",
  "D4": "Chaturthamsha (Assets & Luck)",
  "D7": "Saptamsha (Children & Progeny)",
  "D9": "Navamsha (Dharma & Marriage)",
  "D10": "Dashamsha (Career & Status)",
  "D12": "Dwadashamsha (Parents & Lineage)",
  "D16": "Shodashamsha (Vehicles & Pleasures)",
  "D20": "Vimshamsha (Spiritual Progress)",
  "D24": "Chaturvimshamsha (Learning & Intellect)",
  "D27": "Bhamsa (Strengths & Physical Prowess)",
  "D30": "Trimshamsha (Misfortunes & Obstacles)",
  "D40": "Khavedamsha (Subtle Auspiciousness)",
  "D45": "Akshavedamsha (General Character)",
  "D60": "Shashtiamsha (Past Karma & Fine Destiny)"
};

export default function DivisionalSection({ divisionalCharts }) {
  const [selectedDiv, setSelectedDiv] = useState('D9');

  if (!divisionalCharts) return null;
  const chart = divisionalCharts[selectedDiv];

  return (
    <div className="card-vedic overflow-hidden">
      <div className="card-header-vedic px-4 py-3 flex flex-wrap items-center justify-between gap-2">
        <h3 className="font-bold text-amber-900 vedic-title flex items-center gap-2">
          <span>☸️</span> Shodashavargas (D1 to D60 Divisional Charts)
        </h3>
        <select
          value={selectedDiv}
          onChange={(e) => setSelectedDiv(e.target.value)}
          className="px-3 py-1.5 border border-amber-300 rounded-lg text-xs font-bold text-amber-900 bg-white shadow-xs focus:ring-2 focus:ring-amber-500"
        >
          {Object.keys(DIVISIONAL_TITLES).map((dKey) => (
            <option key={dKey} value={dKey}>
              {dKey}: {DIVISIONAL_TITLES[dKey]}
            </option>
          ))}
        </select>
      </div>

      <div className="p-4 space-y-4">
        {chart && (
          <div>
            <div className="flex flex-wrap items-center justify-between gap-2 mb-3 bg-amber-50/70 p-3 rounded-xl border border-amber-200">
              <div>
                <span className="font-bold text-amber-950 text-base">{chart.name} ({chart.division})</span>
                <span className="text-xs text-stone-600 block">{chart.traditional_use}</span>
              </div>
              <div className="text-right">
                <span className="text-xs text-stone-500 block uppercase font-semibold">Ascendant Sign</span>
                <span className="font-bold text-sm text-amber-900">{chart.ascendant_sign}</span>
              </div>
            </div>

            {/* Divisional Chart Placements Table */}
            <div className="overflow-x-auto">
              <table className="vedic-table">
                <thead>
                  <tr>
                    <th>Planet</th>
                    <th>Placed Sign</th>
                    <th>Sign Lord</th>
                    <th>House in {chart.division}</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.values(chart.placements || {}).map((p) => (
                    <tr key={p.planet}>
                      <td className="font-bold text-amber-950">{p.planet}</td>
                      <td>{p.sign}</td>
                      <td className="text-stone-600">{p.sign_lord}</td>
                      <td className="font-bold text-amber-800 text-center">{p.house}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
