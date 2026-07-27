import React, { useState } from "react";
import {
  Leaf,
  AlertTriangle,
  ListOrdered,
  FlaskConical,
  ShieldCheck,
  CheckCircle2,
  Send,
  BadgeCheck,
  History,
} from "lucide-react";

/*
  DESIGN TOKENS
  Palette built around a working farm at dusk rather than a generic
  "agri-green" template: deep pine for trust/primary actions, a warm
  turned-soil brown for chemical/pesticide content (visually distinct
  from "safe" green), and a clay-ember accent reserved only for the
  urgency alert so it doesn't compete for attention anywhere else.
*/
const tokens = {
  page: "#F5F6F1",
  ink: "#1C2420",
  inkSoft: "#586058",
  card: "#FFFFFF",
  border: "#E7E7DF",
  primary: "#26543C",
  primarySoft: "#E3EFE6",
  soil: "#6B4A30",
  soilSoft: "#F1E6D9",
  amberSoft: "#FBEFDD",
  amberText: "#7A4A08",
  redSoft: "#FBE7E2",
  redText: "#9A3412",
  greenSoft: "#E7F3E1",
  greenText: "#2E5D2A",
  emberSoft: "#FDECE3",
  emberBorder: "#EFB699",
  emberText: "#9A3412",
};

const severityStyles = {
  Low: { bg: tokens.greenSoft, text: tokens.greenText },
  Moderate: { bg: tokens.amberSoft, text: tokens.amberText },
  High: { bg: tokens.emberSoft, text: tokens.emberText },
  Critical: { bg: tokens.redSoft, text: tokens.redText },
};

function ConfidenceRing({ value }) {
  const size = 56;
  const stroke = 5;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const offset = c - (value / 100) * c;
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: "rotate(-90deg)" }}>
        <circle cx={size / 2} cy={size / 2} r={r} stroke={tokens.border} strokeWidth={stroke} fill="none" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          stroke={tokens.primary}
          strokeWidth={stroke}
          fill="none"
          strokeDasharray={c}
          strokeDashoffset={offset}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-sm font-semibold" style={{ color: tokens.ink }}>
          {value}%
        </span>
      </div>
    </div>
  );
}

function Card({ children }) {
  return (
    <div
      className="rounded-2xl p-4 mb-3"
      style={{ background: tokens.card, border: `1px solid ${tokens.border}`, boxShadow: "0 1px 2px rgba(28,36,32,0.04)" }}
    >
      {children}
    </div>
  );
}

function CardLabel({ icon, children }) {
  return (
    <div className="flex items-center gap-2 mb-3">
      {icon}
      <span className="text-xs font-semibold tracking-wide uppercase" style={{ color: tokens.inkSoft }}>
        {children}
      </span>
    </div>
  );
}

function DiseaseOverviewCard({ disease, confidence, severity, status }) {
  const sev = severityStyles[severity] || severityStyles.Moderate;
  return (
    <Card>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <Leaf size={16} color={tokens.primary} />
            <span className="text-xs font-semibold uppercase tracking-wide" style={{ color: tokens.primary }}>
              {disease.crop}
            </span>
          </div>
          <h2 className="text-lg font-bold leading-snug truncate" style={{ color: tokens.ink }}>
            {disease.name}
          </h2>
          <p className="text-xs italic mt-0.5" style={{ color: tokens.inkSoft }}>
            {disease.scientific}
          </p>
        </div>
        {typeof confidence === "number" && <ConfidenceRing value={confidence} />}
      </div>

      <div className="flex flex-wrap items-center gap-2 mt-3">
        <span
          className="text-xs font-semibold px-3 py-1 rounded-full"
          style={{ background: sev.bg, color: sev.text }}
        >
          {severity} severity
        </span>
        <span
          className="text-xs font-medium px-3 py-1 rounded-full flex items-center gap-1"
          style={{
            background: status === "current" ? tokens.primarySoft : "#EFEFEA",
            color: status === "current" ? tokens.primary : tokens.inkSoft,
          }}
        >
          {status === "current" ? <BadgeCheck size={13} /> : <History size={13} />}
          {status === "current" ? "Current guidance" : "Outdated — for reference only"}
        </span>
      </div>
    </Card>
  );
}

function UrgencyAlertCard({ message }) {
  if (!message) return null;
  return (
    <div
      className="rounded-2xl p-4 mb-3 flex gap-3"
      style={{ background: tokens.emberSoft, border: `1px solid ${tokens.emberBorder}` }}
    >
      <AlertTriangle size={20} color={tokens.emberText} className="shrink-0 mt-0.5" />
      <div>
        <p className="text-sm font-semibold mb-0.5" style={{ color: tokens.emberText }}>
          Act now
        </p>
        <p className="text-sm leading-snug" style={{ color: tokens.emberText }}>
          {message}
        </p>
      </div>
    </div>
  );
}

function TreatmentStepsCard({ steps }) {
  if (!steps?.length) return null;
  return (
    <Card>
      <CardLabel icon={<ListOrdered size={15} color={tokens.primary} />}>Treatment steps</CardLabel>
      <ol className="space-y-3">
        {steps.map((step, i) => (
          <li key={i} className="flex gap-3">
            <span
              className="shrink-0 flex items-center justify-center rounded-full text-xs font-bold"
              style={{ width: 22, height: 22, background: tokens.primarySoft, color: tokens.primary }}
            >
              {i + 1}
            </span>
            <span className="text-sm leading-snug pt-0.5" style={{ color: tokens.ink }}>
              {step}
            </span>
          </li>
        ))}
      </ol>
    </Card>
  );
}

function PesticideChipsCard({ items }) {
  if (!items?.length) return null;
  return (
    <Card>
      <CardLabel icon={<FlaskConical size={15} color={tokens.soil} />}>Recommended pesticides</CardLabel>
      <div className="flex flex-wrap gap-2">
        {items.map((name) => (
          <span
            key={name}
            className="text-sm font-medium px-3 py-1.5 rounded-full"
            style={{ background: tokens.soilSoft, color: tokens.soil }}
          >
            {name}
          </span>
        ))}
      </div>
      <p className="text-xs mt-3" style={{ color: tokens.inkSoft }}>
        Always follow the product label for dose, timing, and re-entry interval.
      </p>
    </Card>
  );
}

function PreventionChecklistCard({ items }) {
  if (!items?.length) return null;
  return (
    <Card>
      <CardLabel icon={<ShieldCheck size={15} color={tokens.primary} />}>Prevention checklist</CardLabel>
      <ul className="space-y-2">
        {items.map((item, i) => (
          <li key={i} className="flex items-start gap-2">
            <CheckCircle2 size={16} color={tokens.primary} className="shrink-0 mt-0.5" />
            <span className="text-sm leading-snug" style={{ color: tokens.ink }}>
              {item}
            </span>
          </li>
        ))}
      </ul>
    </Card>
  );
}

function FollowUpBar({ onAsk }) {
  const [value, setValue] = useState("");
  const submit = () => {
    if (!value.trim()) return;
    onAsk?.(value.trim());
    setValue("");
  };
  return (
    <div
      className="flex items-center gap-2 rounded-2xl p-2 mt-1"
      style={{ background: tokens.card, border: `1px solid ${tokens.border}` }}
    >
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && submit()}
        placeholder="Ask a follow-up, e.g. is this safe near harvest?"
        className="flex-1 text-sm bg-transparent outline-none px-2"
        style={{ color: tokens.ink }}
      />
      <button
        onClick={submit}
        aria-label="Send question"
        className="shrink-0 flex items-center justify-center rounded-full"
        style={{ width: 34, height: 34, background: tokens.primary, color: "white" }}
      >
        <Send size={15} />
      </button>
    </div>
  );
}

export default function RecommendationResult({
  disease = {
    crop: "Cucumber",
    name: "Downy Mildew",
    scientific: "Pseudoperonospora cubensis",
  },
  confidence = 87,
  severity = "Critical",
  status = "current",
  urgencyMessage = "Downy mildew can scorch a field within days under humid weather. Scout again tomorrow and start treatment today if new lesions appear.",
  steps = [
    "Remove and destroy the worst-affected leaves to slow spread.",
    "Switch to drip irrigation and stop overhead watering immediately.",
    "Apply a targeted oomycete fungicide, rotating modes of action.",
    "Re-scout the lower canopy every 2–3 days during humid weather.",
  ],
  pesticides = ["Fluopicolide", "Cyazofamid", "Propamocarb", "Mancozeb"],
  prevention = [
    "Choose downy-mildew-resistant cucumber varieties next season.",
    "Space rows for airflow and orient with prevailing wind.",
    "Avoid overhead irrigation, especially late in the day.",
  ],
  onAsk,
}) {
  return (
    <div className="w-full max-w-md mx-auto p-4" style={{ background: tokens.page }}>
      <DiseaseOverviewCard disease={disease} confidence={confidence} severity={severity} status={status} />
      <UrgencyAlertCard message={severity === "High" || severity === "Critical" ? urgencyMessage : null} />
      <TreatmentStepsCard steps={steps} />
      <PesticideChipsCard items={pesticides} />
      <PreventionChecklistCard items={prevention} />
      <FollowUpBar onAsk={onAsk} />
    </div>
  );
}
