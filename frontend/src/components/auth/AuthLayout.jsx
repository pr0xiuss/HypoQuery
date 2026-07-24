import { Database } from "lucide-react";

export default function AuthLayout({ heroTitle, heroSubtitle, children }) {
  return (
    <div className="auth-shell">
      <div className="auth-brand-panel">
        <div className="auth-grid-pattern" />
        <div className="auth-brand-glow" />

        <div className="relative flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-md bg-signal">
            <Database className="h-4 w-4 text-paper" strokeWidth={2.5} />
          </div>
          <span className="font-display text-lg font-semibold tracking-tight text-paper">
            HypoQuery
          </span>
        </div>

        <div className="relative max-w-sm">
          <p className="font-display text-2xl font-semibold leading-snug text-paper">
            {heroTitle}
          </p>
          <p className="mt-3 text-sm text-fog">{heroSubtitle}</p>
        </div>

        <p className="relative text-xs text-fog">
          © {new Date().getFullYear()} HypoQuery
        </p>
      </div>

      <div className="auth-form-panel">{children}</div>
    </div>
  );
}
