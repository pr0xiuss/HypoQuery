const TYPE_STYLES = {
  DEVELOPMENT: { label: "Development", color: "var(--color-fog)", bg: "var(--color-line)" },
  TESTING: { label: "Testing", color: "var(--color-warn)", bg: "var(--color-warn-soft)" },
  STAGING: { label: "Staging", color: "var(--color-signal)", bg: "var(--color-signal-soft)" },
  PRODUCTION: { label: "Production", color: "var(--color-danger)", bg: "var(--color-danger-soft)" },
};

export default function EnvironmentTypeBadge({ type }) {
  const style =
    TYPE_STYLES[type] || {
      label: type || "Unknown",
      color: "var(--color-fog)",
      bg: "var(--color-line)",
    };

  return (
    <span
      className="environment-type-badge"
      style={{ color: style.color, backgroundColor: style.bg }}
    >
      {style.label}
    </span>
  );
}
