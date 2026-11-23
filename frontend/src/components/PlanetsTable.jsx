import React from 'react';

function formatDegree(deg) {
  if (deg == null) return '-';
  const d = Math.floor(deg);
  const m = Math.floor((deg - d) * 60);
  const s = Math.floor(((deg - d) * 60 - m) * 60);
  return `${d}° ${m}' ${s}"`;
}

function getDignityBadge(dignity) {
  if (!dignity) return null;
  const d = dignity.dignity || dignity;
  if (d === 'Exalted') return <span className="badge-exalted">Exalted</span>;
  if (d === 'Debilitated') return <span className="badge-debilitated">Debilitated</span>;
  if (d === 'Own Sign' || d === 'Moolatrikona') return <span className="badge-own">{d}</span>;
  if (d.includes('Friend')) return <span className="badge-friend">{d}</span>;
  return <span className="text-gray-500 font-medium text-xs">{d}</span>;
}

export default function PlanetsTable({ planets, dignities }) {
  if (!planets) return null;

  const planetList = [
    "Ascendant", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"
  ];

  return (
    <div className="card-vedic overflow-hidden">
      <div className="card-header-vedic px-4 py-3 flex items-center justify-between">
        <h3 className="font-bold text-amber-900 vedic-title flex items-center gap-2">
          <span>🪐</span> Graha Sthiti (Planetary Table)
        </h3>
        <span className="text-xs text-amber-800 font-semibold bg-amber-200/50 px-2.5 py-1 rounded-full">
          Sidereal Zodiac
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="vedic-table">
          <thead>
            <tr>
              <th>Planet</th>
              <th>Sign (Rashi)</th>
              <th>Degree</th>
              <th>Nakshatra (Pada)</th>
              <th>Star Lord</th>
              <th>House</th>
              <th>Chalit</th>
              <th>Speed</th>
              <th>Dignity</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {planetList.map((pName) => {
              const p = planets[pName];
              if (!p) return null;
              const dig = dignities?.[pName];
              return (
                <tr key={pName} className="font-medium text-stone-700">
                  <td className="font-bold text-amber-950 flex items-center gap-1.5">
                    {pName}
                  </td>
                  <td>
                    <span className="font-semibold text-stone-800">{p.sign}</span>
                    <span className="text-xs text-stone-600 block">Lord: {p.sign_lord}</span>
                  </td>
                  <td className="font-mono text-xs">{formatDegree(p.degree_in_sign)}</td>
                  <td>
                    <span className="font-semibold text-stone-800">{p.nakshatra}</span>
                    <span className="text-xs bg-amber-100 text-amber-800 px-1.5 py-0.5 rounded font-bold ml-1.5">
                      P{p.nakshatra_pada}
                    </span>
                  </td>
                  <td className="text-stone-600">{p.nakshatra_lord}</td>
                  <td className="font-bold text-amber-800 text-center">{p.house}</td>
                  <td className="font-bold text-blue-700 text-center">{p.bhava_chalit_house}</td>
                  <td className="font-mono text-xs">{p.speed ? p.speed.toFixed(3) : '0.000'}</td>
                  <td>{getDignityBadge(dig)}</td>
                  <td>
                    <div className="flex gap-1 items-center">
                      {p.retrograde && <span className="badge-retro">R</span>}
                      {p.is_combust && <span className="badge-combust">C</span>}
                      {!p.retrograde && !p.is_combust && <span className="text-xs text-gray-500">Direct</span>}
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
