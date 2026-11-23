import React from 'react';

const ZODIAC_SIGNS = [
  "Aries", "Taurus", "Gemini", "Cancer",
  "Leo", "Virgo", "Libra", "Scorpio",
  "Sagittarius", "Capricorn", "Aquarius", "Pisces"
];

const PLANETS_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"];

export default function AshtakavargaSection({ ashtakavarga }) {
  if (!ashtakavarga) return null;
  const { bav, sav, sample_shodhya_pinda_moon } = ashtakavarga;

  return (
    <div className="card-vedic overflow-hidden">
      <div className="card-header-vedic px-4 py-3 flex items-center justify-between">
        <h3 className="font-bold text-amber-900 vedic-title flex items-center gap-2">
          <span>📊</span> Ashtakavarga Matrix (BAV & SAV 337 Points)
        </h3>
        <span className="text-xs bg-amber-800 text-white px-2.5 py-1 rounded-full font-bold">
          Total Bindus: {sav?.grand_total} / 337
        </span>
      </div>

      <div className="p-4 space-y-5 overflow-x-auto">
        {/* Sarvashtakavarga (SAV) Grid */}
        <div>
          <h4 className="text-sm font-bold text-amber-900 mb-2">Sarvashtakavarga (Combined Bindu Strengths per Sign)</h4>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
            {sav?.sign_analysis?.map((s) => {
              const isStrong = s.status === 'Strong';
              return (
                <div
                  key={s.sign}
                  className={`p-3 rounded-xl border text-center transition ${
                    isStrong
                      ? 'bg-emerald-50/60 border-emerald-200'
                      : 'bg-rose-50/60 border-rose-200'
                  }`}
                >
                  <span className="text-xs font-semibold text-stone-600 block">{s.sign}</span>
                  <span className={`text-xl font-black mt-0.5 block ${isStrong ? 'text-emerald-700' : 'text-rose-700'}`}>
                    {s.total_bindus}
                  </span>
                  <span className={`text-[10px] font-bold uppercase px-1.5 py-0.5 rounded ${
                    isStrong ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                  }`}>
                    {s.status} (Avg: 28)
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Bhinnashtakavarga (BAV) Table */}
        <div>
          <h4 className="text-sm font-bold text-amber-900 mb-2">Bhinnashtakavarga (7 Traditional Planets x 12 Signs)</h4>
          <table className="vedic-table text-center">
            <thead>
              <tr>
                <th className="text-left">Planet</th>
                {ZODIAC_SIGNS.map((sign) => (
                  <th key={sign} className="text-center font-mono text-xs">{sign.slice(0, 3)}</th>
                ))}
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {PLANETS_7.map((pName) => {
                const row = bav?.[pName] || [];
                const pTotal = row.reduce((a, b) => a + b, 0);
                return (
                  <tr key={pName}>
                    <td className="text-left font-bold text-amber-950">{pName}</td>
                    {row.map((val, idx) => (
                      <td key={idx} className="font-mono text-xs font-semibold text-stone-700">
                        {val}
                      </td>
                    ))}
                    <td className="font-bold text-amber-900 bg-amber-50">{pTotal}</td>
                  </tr>
                );
              })}
              {/* SAV Row */}
              <tr className="bg-amber-100/60 font-black">
                <td className="text-left text-amber-950">SAV Total</td>
                {sav?.sav_totals?.map((val, idx) => (
                  <td key={idx} className="font-mono text-xs text-amber-950">{val}</td>
                ))}
                <td className="text-amber-950">{sav?.grand_total}</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Reductions / Shodhya Pinda */}
        {sample_shodhya_pinda_moon && (
          <div className="bg-amber-50/70 p-3.5 rounded-xl border border-amber-200">
            <h5 className="text-xs font-bold uppercase tracking-wider text-amber-900 mb-2">
              Advanced Shodhana & Shodhya Pinda (Chandra Kundli Reference)
            </h5>
            <div className="flex flex-wrap gap-4 text-xs">
              <div>Rashi Pinda: <strong className="text-amber-950 font-mono text-sm">{sample_shodhya_pinda_moon.rashi_pinda}</strong></div>
              <div>Graha Pinda: <strong className="text-amber-950 font-mono text-sm">{sample_shodhya_pinda_moon.graha_pinda}</strong></div>
              <div>Shodhya Pinda Total: <strong className="text-amber-950 font-mono text-sm">{sample_shodhya_pinda_moon.shodhya_pinda}</strong></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
