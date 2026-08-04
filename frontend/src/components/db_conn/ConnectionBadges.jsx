export function ConnectionStatusBadge({ active }) {
  return (
    <span
      className="environment-type-badge"
      style={{
        color: active ? "var(--color-ok)" : "var(--color-fog)",
        backgroundColor: active ? "var(--color-ok-soft)" : "var(--color-line)",
      }}
    >
      {active ? "Active" : "Inactive"}
    </span>
  );
}

export function SslBadge({ enabled }) {
  return (
    <span
      className="environment-type-badge"
      style={{
        color: enabled ? "var(--color-signal)" : "var(--color-fog)",
        backgroundColor: enabled ? "var(--color-signal-soft)" : "var(--color-line)",
      }}
    >
      SSL {enabled ? "Enabled" : "Disabled"}
    </span>
  );
}
