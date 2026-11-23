import React, { useState } from 'react';

export default function KPSection({ kpData }) {
  const [activeTab, setActiveTab] = useState('cusps'); // 'cusps', 'planets', 'significators', 'rp'
  if (!kpData) return null;

  const { cusps, planets, significators, ruling_planets } = kpData;

  return (
    <div className="card-vedic overflow-hidden">
      <div className="card-header-vedic px-4 py-3 flex flex-wrap items-center justify-between gap-2">
        <h3 className="font-bold text-amber-900 vedic-title flex items-center gap-2">
          <span>📐</span> KP Astrology (Krishnamurti Paddhati)
        </h3>

        <div className="flex bg-amber-200/50 p-1 rounded-lg text-xs font-semibold">
          {['cusps', 'planets', 'significators', 'rp'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-3 py-1 rounded-md transition capitalize ${
                activeTab === tab ? 'bg-amber-800 text-white shadow' : 'text-amber-950 hover:bg-amber-200'
              }`}
            >
              {tab === 'rp' ? 'Ruling Planets' : tab}
            </button>
          ))}
        </div>
      </div>

      <div className="p-4 overflow-x-auto">
        {/* 1. KP Cusp Table */}
        {activeTab === 'cusps' && (
          <div>
            <h4 className="text-sm font-bold text-amber-900 mb-2">12 Placidus House Cusps (KP 4-Fold Lordship)</h4>
            <table className="vedic-table">
              <thead>
                <tr>
                  <th>Cusp</th>
                  <th>Sign</th>
                  <th>Degree</th>
                  <th>Sign Lord</th>
                  <th>Star (Nakshatra)</th>
                  <th>Star Lord</th>
                  <th>Sub Lord</th>
                  <th>Sub-Sub Lord</th>
                </tr>
              </thead>
              <tbody>
                {cusps?.map((c) => (
                  <tr key={c.house}>
                    <td className="font-bold text-amber-900">House {c.house}</td>
                    <td>{c.sign}</td>
                    <td className="font-mono text-xs">{c.degree_in_sign.toFixed(2)}°</td>
                    <td className="font-medium text-stone-700">{c.sign_lord}</td>
                    <td>{c.star}</td>
                    <td className="font-medium text-stone-700">{c.star_lord}</td>
                    <td>
                      <span className="bg-amber-100 text-amber-900 px-2 py-0.5 rounded font-bold text-xs">
                        {c.sub_lord}
                      </span>
                    </td>
                    <td className="text-stone-600 text-xs">{c.sub_sub_lord}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* 2. KP Planets Table */}
        {activeTab === 'planets' && (
          <div>
            <h4 className="text-sm font-bold text-amber-900 mb-2">Planetary Sub-Lords Table</h4>
            <table className="vedic-table">
              <thead>
                <tr>
                  <th>Planet</th>
                  <th>Sign</th>
                  <th>Degree</th>
                  <th>Sign Lord</th>
                  <th>Star</th>
                  <th>Star Lord</th>
                  <th>Sub Lord</th>
                  <th>Sub-Sub Lord</th>
                  <th>House</th>
                </tr>
              </thead>
              <tbody>
                {planets?.map((p) => (
                  <tr key={p.planet}>
                    <td className="font-bold text-amber-950">{p.planet}</td>
                    <td>{p.sign}</td>
                    <td className="font-mono text-xs">{p.degree_in_sign.toFixed(2)}°</td>
                    <td>{p.sign_lord}</td>
                    <td>{p.star}</td>
                    <td>{p.star_lord}</td>
                    <td>
                      <span className="bg-amber-100 text-amber-900 px-2 py-0.5 rounded font-bold text-xs">
                        {p.sub_lord}
                      </span>
                    </td>
                    <td className="text-stone-600 text-xs">{p.sub_sub_lord}</td>
                    <td className="font-bold text-blue-700">{p.house}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* 3. KP 4-Step Significators */}
        {activeTab === 'significators' && (
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-bold text-amber-900 mb-1">Planet-Centric Significators (4 Levels)</h4>
              <p className="text-xs text-stone-600 mb-2">
                Level 1: House occupied by Star Lord | Level 2: House occupied by Planet | Level 3: Houses owned by Star Lord | Level 4: Houses owned by Planet
              </p>
              <table className="vedic-table">
                <thead>
                  <tr>
                    <th>Planet</th>
                    <th>Level 1</th>
                    <th>Level 2</th>
                    <th>Level 3</th>
                    <th>Level 4</th>
                    <th>All Houses Signified</th>
                  </tr>
                </thead>
                <tbody>
                  {significators?.planet_significators?.map((ps) => (
                    <tr key={ps.planet}>
                      <td className="font-bold text-amber-950">{ps.planet}</td>
                      <td className="font-mono text-xs text-amber-800">{ps.level_1.join(', ') || '-'}</td>
                      <td className="font-mono text-xs text-blue-700">{ps.level_2.join(', ') || '-'}</td>
                      <td className="font-mono text-xs text-emerald-700">{ps.level_3.join(', ') || '-'}</td>
                      <td className="font-mono text-xs text-purple-700">{ps.level_4.join(', ') || '-'}</td>
                      <td>
                        <span className="font-bold text-xs bg-amber-100 text-amber-900 px-2 py-0.5 rounded">
                          {ps.all_signified_houses.join(', ')}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* 4. Ruling Planets */}
        {activeTab === 'rp' && (
          <div className="space-y-4">
            <h4 className="text-sm font-bold text-amber-900 mb-2">Primary Ruling Planets (RP) at Chart Moment</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
              {ruling_planets?.primary_ruling_planets?.map((rp, idx) => (
                <div key={idx} className="p-3 bg-amber-50 rounded-lg border border-amber-200">
                  <span className="text-xs uppercase tracking-wider font-semibold text-amber-800 block">
                    {rp.role}
                  </span>
                  <span className="text-base font-bold text-amber-950 mt-1 block">
                    {rp.planet}
                  </span>
                </div>
              ))}
            </div>

            <div className="p-3 bg-stone-50 rounded-lg border border-stone-200 text-xs">
              <span className="font-bold text-stone-700 block mb-1">Nodal Affiliations:</span>
              <div>Rahu represents: <strong>{ruling_planets?.node_affiliations?.Rahu_represents?.join(', ')}</strong></div>
              <div>Ketu represents: <strong>{ruling_planets?.node_affiliations?.Ketu_represents?.join(', ')}</strong></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
