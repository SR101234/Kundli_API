import React, { useState, useEffect } from 'react';
import BirthForm from './components/BirthForm';
import ChartRenderer from './components/ChartRenderer';
import PlanetsTable from './components/PlanetsTable';
import PanchangCard from './components/PanchangCard';
import KPSection from './components/KPSection';
import AshtakavargaSection from './components/AshtakavargaSection';
import DashaSection from './components/DashaSection';
import YogasDoshasSection from './components/YogasDoshasSection';
import MatchingSection from './components/MatchingSection';
import TransitsSection from './components/TransitsSection';
import DivisionalSection from './components/DivisionalSection';
import AdminPanel from './components/AdminPanel';
import ContactModal from './components/ContactModal';
import { generateKundli } from './api/kundliApi';
import { fetchUserQuota } from './api/adminApi';

export default function App() {
  const [formData, setFormData] = useState({
    user_name: localStorage.getItem('kundli_user_name') || "",
    user_email: localStorage.getItem('kundli_user_email') || "",
    user_mobile: localStorage.getItem('kundli_user_mobile') || "",
    name: "Example User",
    date: "2001-08-15",
    time: "14:35:00",
    timezone: "Asia/Kolkata",
    latitude: 27.1767,
    longitude: 78.0081,
    ayanamsa: "Lahiri",
    house_system: "P",
    node_type: "mean",
    chart_type: "vedic"
  });

  const [kundliData, setKundliData] = useState(null);
  const [userQuota, setUserQuota] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [showAdmin, setShowAdmin] = useState(false);
  const [showContactModal, setShowContactModal] = useState(false);

  const checkQuota = async (email, mobile, name) => {
    if (!email) return;
    try {
      const q = await fetchUserQuota(email, mobile, name);
      setUserQuota(q);
    } catch {
      // ignore
    }
  };

  const fetchKundli = async (inputData) => {
    setLoading(true);
    setError(null);
    try {
      const data = await generateKundli(inputData);
      setKundliData(data);
      if (data.user_quota) {
        setUserQuota(data.user_quota);
      }
    } catch (err) {
      setError(err.message || "Failed to calculate birth chart");
      if (inputData.user_email) {
        checkQuota(inputData.user_email, inputData.user_mobile, inputData.user_name);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (formData.user_email) {
      checkQuota(formData.user_email, formData.user_mobile, formData.user_name);
    }
    fetchKundli(formData);
  }, []);

  const handleContactConfirm = (contactDetails) => {
    const updated = {
      ...formData,
      ...contactDetails
    };
    setFormData(updated);
    setShowContactModal(false);
    fetchKundli(updated);
  };

  return (
    <div className="min-h-screen bg-stone-50 pb-16">
      {/* Header */}
      <header className="bg-gradient-to-r from-amber-800 via-amber-700 to-amber-900 text-white py-6 shadow-md border-b-2 border-amber-600">
        <div className="max-w-7xl mx-auto px-4 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="text-3xl">☸️</span>
            <div>
              <h1 className="text-2xl sm:text-3xl font-extrabold vedic-title tracking-wider">
                Vedic & KP Kundli Engine
              </h1>
              <p className="text-xs sm:text-sm text-amber-200 font-medium">
                10 Free Kundli Checks per User • Swiss Ephemeris • KP 249 Sub-Lords • Ashtakavarga 337
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2.5">
            {userQuota && (
              <div className="bg-amber-950/70 border border-amber-500/50 px-3 py-1.5 rounded-lg text-xs">
                <span className="text-amber-300 block text-[10px] uppercase font-bold">Checks Remaining</span>
                <span className="font-extrabold text-amber-100">{userQuota.remaining_checks} / {userQuota.max_limit}</span>
              </div>
            )}
            <button
              onClick={() => setShowAdmin(true)}
              className="text-xs bg-amber-500 hover:bg-amber-400 text-amber-950 font-extrabold px-3.5 py-2 rounded-lg shadow-sm transition flex items-center gap-1.5 cursor-pointer"
            >
              <span>🛡️</span> Admin Panel
            </button>
            <a
              href="http://127.0.0.1:8000/docs"
              target="_blank"
              rel="noreferrer"
              className="text-xs bg-amber-950/60 hover:bg-amber-950 px-3 py-2 rounded-lg border border-amber-500/50 text-amber-100 font-semibold transition"
            >
              📖 API Docs
            </a>
          </div>
        </div>
      </header>

      {/* Contact Info Pop-up Modal */}
      <ContactModal
        isOpen={showContactModal}
        onClose={() => setShowContactModal(false)}
        onConfirm={handleContactConfirm}
        seekerName={formData.name}
        birthDate={formData.date}
        birthTime={formData.time}
        userQuota={userQuota}
        initialUser={{
          user_name: formData.user_name,
          user_email: formData.user_email,
          user_mobile: formData.user_mobile
        }}
        loading={loading}
      />

      {/* Admin Panel Modal / View */}
      {showAdmin && (
        <AdminPanel onClose={() => setShowAdmin(false)} />
      )}

      {/* Main Content Container */}
      <main className="max-w-7xl mx-auto px-4 mt-6 space-y-6">
        {/* Top Grid: Form and Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left Form (5 cols) */}
          <div className="lg:col-span-5 space-y-4">
            <BirthForm
              formData={formData}
              setFormData={setFormData}
              onOpenContactModal={() => setShowContactModal(true)}
              loading={loading}
              userQuota={userQuota}
            />

            {/* Quick Native Summary Badge */}
            {kundliData && (
              <div className="p-4 bg-gradient-to-br from-amber-100 to-amber-200/70 border border-amber-300 rounded-xl shadow-xs text-xs space-y-1">
                <div className="flex justify-between items-center">
                  <span className="font-bold text-amber-950 block text-sm">
                    {kundliData.metadata.name}
                  </span>
                  <span className="text-stone-500 text-[11px]">
                    {formData.user_email ? `Account: ${formData.user_email}` : 'Guest Session'}
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-1 text-stone-700 pt-1 border-t border-amber-200/60">
                  <div>Lagna: <strong>{kundliData.ascendant.sign} ({kundliData.ascendant.degree_in_sign.toFixed(2)}°)</strong></div>
                  <div>Moon: <strong>{kundliData.planets.Moon.sign}</strong></div>
                  <div>Nakshatra: <strong>{kundliData.planets.Moon.nakshatra} (P{kundliData.planets.Moon.nakshatra_pada})</strong></div>
                  <div>Day Lord: <strong>{kundliData.panchang.vara_lord}</strong></div>
                </div>
              </div>
            )}
          </div>

          {/* Right Visual Chart (7 cols) */}
          <div className="lg:col-span-7">
            {error && (
              <div className="p-4 mb-4 bg-rose-100 border border-rose-300 text-rose-900 rounded-xl text-sm font-semibold flex items-center gap-2">
                <span>⚠️</span> {error}
              </div>
            )}

            {kundliData && (
              <div className="space-y-4">
                <ChartRenderer
                  d1Chart={kundliData.charts.d1_rashi}
                  svgNorth={kundliData.charts.svg_north_indian}
                  svgSouth={kundliData.charts.svg_south_indian}
                  title="Janma Kundli (D1 Rashi Chart)"
                />
                <PanchangCard
                  panchang={kundliData.panchang}
                  metadata={kundliData.metadata}
                />
              </div>
            )}
          </div>
        </div>

        {/* Multi-Module Navigation Tabs */}
        {kundliData && (
          <div className="space-y-4">
            <div className="flex overflow-x-auto gap-1.5 p-1 bg-amber-100/60 rounded-xl border border-amber-200">
              {[
                { id: 'overview', label: 'Planetary Table', icon: '🪐' },
                { id: 'kp', label: 'KP Astrology (249)', icon: '📐' },
                { id: 'ashtakavarga', label: 'Ashtakavarga (337)', icon: '📊' },
                { id: 'divisional', label: 'Divisional (D1-D60)', icon: '☸️' },
                { id: 'dasha', label: 'Dasha Timeline', icon: '⏳' },
                { id: 'yogas', label: 'Yogas & Doshas', icon: '🔮' },
                { id: 'transits', label: 'Transits & Sade Sati', icon: '🌌' },
                { id: 'matching', label: 'Kundli Milan (36 Gun)', icon: '💍' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-4 py-2.5 rounded-lg text-xs font-bold whitespace-nowrap transition cursor-pointer flex items-center gap-1.5 ${
                    activeTab === tab.id
                      ? 'bg-amber-800 text-white shadow-md'
                      : 'text-amber-950 hover:bg-amber-200/80'
                  }`}
                >
                  <span>{tab.icon}</span>
                  <span>{tab.label}</span>
                </button>
              ))}
            </div>

            {/* Active Tab Contents */}
            <div>
              {activeTab === 'overview' && (
                <PlanetsTable
                  planets={kundliData.planets}
                  dignities={kundliData.dignities}
                />
              )}

              {activeTab === 'kp' && (
                <KPSection kpData={kundliData.kp_astrology} />
              )}

              {activeTab === 'ashtakavarga' && (
                <AshtakavargaSection ashtakavarga={kundliData.ashtakavarga} />
              )}

              {activeTab === 'divisional' && (
                <DivisionalSection divisionalCharts={kundliData.charts.divisional} />
              )}

              {activeTab === 'dasha' && (
                <DashaSection dashaData={kundliData.dasha} />
              )}

              {activeTab === 'yogas' && (
                <YogasDoshasSection
                  yogas={kundliData.yogas}
                  doshas={kundliData.doshas}
                />
              )}

              {activeTab === 'transits' && (
                <TransitsSection
                  transitsData={kundliData.transits}
                  sadeSatiData={kundliData.sade_sati}
                />
              )}

              {activeTab === 'matching' && (
                <MatchingSection defaultGroom={formData} />
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
