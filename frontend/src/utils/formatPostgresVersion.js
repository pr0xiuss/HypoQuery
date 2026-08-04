// Backend returns the full server banner, e.g.
// "PostgreSQL 16.13 (Debian 16.13-1.pgdg13+1) on x86_64-pc-linux-gnu, ..."
// Users just want "PostgreSQL 16.13" — the full string is still available
// as a tooltip wherever this is used.
export function formatPostgresVersion(raw) {
  if (!raw) return "—";
  const match = raw.match(/^PostgreSQL\s+[\d.]+/i);
  return match ? match[0] : raw;
}
