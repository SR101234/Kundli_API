import React from 'react';

export default function PanchangCard({ panchang, metadata }) {
  if (!panchang) return null;

  const items = [
    { label: "Tithi", value: `${panchang.tithi_name} (${panchang.paksha})`, sub: `${panchang.tithi_percentage_left}% remaining` },
    { label: "Vara (Day)", value: `${panchang.vara}`, sub: `Lord: ${panchang.vara_lord}` },
    { label: "Nakshatra", value: `${panchang.nakshatra}`, sub: `Pada: ${panchang.nakshatra_pada}` },
    { label: "Yoga", value: `${panchang.yoga}`, sub: `Yoga #${panchang.yoga_number}` },
    { label: "Karana", value: `${panchang.karana}`, sub: `Karana #${panchang.karana_number}` },
    { label: "Sun Timings", value: `🌅 Rise: ${panchang.sunrise_time}`, sub: `🌇 Set: ${panchang.sunset_time}` }
  ];

  return (
    <div className="card-vedic overflow-hidden">
      <div className="card-header-vedic px-4 py-3 flex items-center justify-between">
        <h3 className="font-bold text-amber-900 vedic-title flex items-center gap-2">
          <span>☀️</span> Janma Panchang (Birth Limbs)
        </h3>
        <span className="text-xs text-amber-800 font-mono">
          Ayanamsa: {metadata?.ayanamsa} ({metadata?.ayanamsa_value?.toFixed(4)}°)
        </span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 p-4">
        {items.map((it, idx) => (
          <div key={idx} className="bg-amber-50/50 p-2.5 rounded-lg border border-amber-100/70">
            <span className="text-xs uppercase tracking-wider font-semibold text-amber-800 block">
              {it.label}
            </span>
            <span className="font-bold text-sm text-stone-800 block mt-0.5">
              {it.value}
            </span>
            <span className="text-xs text-stone-600 block mt-0.5">
              {it.sub}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
