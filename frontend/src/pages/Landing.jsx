import { Link } from "react-router-dom";
import {
  Database,
  Fingerprint,
  Gauge,
  GitBranch,
  Layers,
  ShieldCheck,
  Sparkles,
  ArrowRight,
  CircleCheck,
} from "lucide-react";

const WORKFLOW_STEPS = [
  { label: "Login", detail: "Authenticate into your workspace" },
  { label: "Organization", detail: "The top of your account hierarchy" },
  { label: "Project", detail: "A product or service you operate" },
  { label: "Environment", detail: "Development, staging, or production" },
  { label: "Database Connection", detail: "Point HypoQuery at real PostgreSQL" },
  { label: "Metadata Discovery", detail: "Schemas, tables, indexes, found automatically" },
  { label: "Analysis", detail: "Deterministic rules evaluate your workload" },
  { label: "Recommendations", detail: "Ranked, evidence-backed optimizations" },
  { label: "Knowledge", detail: "Findings explained in plain language" },
];

const FEATURES = [
  {
    icon: Gauge,
    title: "Deterministic optimization engine",
    body: "Execution plans, index usage, and query cost are evaluated by fixed rules — not a model guessing at performance.",
  },
  {
    icon: Fingerprint,
    title: "Automatic metadata discovery",
    body: "Connect a database once. HypoQuery discovers schemas, tables, views, indexes, and extensions on its own.",
  },
  {
    icon: ShieldCheck,
    title: "Validated recommendations",
    body: "Every suggested optimization carries a confidence score and a validation trail before it reaches you.",
  },
  {
    icon: GitBranch,
    title: "Organized like your infrastructure",
    body: "Organizations, projects, and environments mirror how engineering teams actually structure their systems.",
  },
  {
    icon: Layers,
    title: "A knowledge graph, not a chat log",
    body: "Findings persist as structured knowledge you can retrieve, not messages that scroll away.",
  },
  {
    icon: Sparkles,
    title: "AI that explains, never decides",
    body: "Language models narrate what the deterministic engine already found. They never invent a diagnosis.",
  },
];

const LAYERS = [
  "Frontend (React)",
  "REST API",
  "Platform Layer",
  "Execution Engine",
  "Optimization Engine",
  "Knowledge Platform",
  "AI Explanation Layer",
];

export default function Landing() {
  return (
    <div className="min-h-screen bg-ink text-paper font-body">
      {/* Top navigation */}
      <header className="border-b border-line">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-md bg-signal">
              <Database className="h-4 w-4 text-paper" strokeWidth={2.5} />
            </div>
            <span className="font-display text-lg font-semibold tracking-tight">
              HypoQuery
            </span>
          </div>
          <nav className="flex items-center gap-3">
            <Link
              to="/login"
              className="rounded-md px-4 py-2 text-sm font-medium text-fog transition-colors hover:text-paper"
            >
              Login
            </Link>
            <Link
              to="/register"
              className="rounded-md bg-signal px-4 py-2 text-sm font-medium text-paper transition-colors hover:bg-signal/90"
            >
              Get Started
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="mx-auto max-w-6xl px-6 py-20 md:py-28">
        <div className="grid items-center gap-16 md:grid-cols-2">
          <div>
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-line bg-surface px-3 py-1 text-xs font-medium text-fog">
              <span className="h-1.5 w-1.5 rounded-full bg-ok" />
              Deterministic engine · AI only explains
            </div>
            <h1 className="font-display text-4xl font-semibold leading-[1.1] tracking-tight md:text-5xl">
              Know why your PostgreSQL database is slow.
              <span className="text-fog"> Not just that it is.</span>
            </h1>
            <p className="mt-6 max-w-lg text-base leading-relaxed text-fog">
              HypoQuery continuously analyzes your PostgreSQL workload, finds
              the queries and indexes costing you the most, and explains
              exactly why — backed by evidence, not intuition.
            </p>
            <div className="mt-9 flex flex-wrap items-center gap-4">
              <Link
                to="/register"
                className="inline-flex items-center gap-2 rounded-md bg-signal px-5 py-3 text-sm font-medium text-paper transition-colors hover:bg-signal/90"
              >
                Get Started
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                to="/login"
                className="inline-flex items-center gap-2 rounded-md border border-line px-5 py-3 text-sm font-medium text-paper transition-colors hover:border-fog"
              >
                Login
              </Link>
            </div>
          </div>

          {/* Signature element: a plan being turned into a recommendation */}
          <div className="rounded-xl border border-line bg-surface shadow-2xl shadow-black/40">
            <div className="flex items-center gap-2 border-b border-line px-4 py-3">
              <span className="h-2.5 w-2.5 rounded-full bg-danger/70" />
              <span className="h-2.5 w-2.5 rounded-full bg-warn/70" />
              <span className="h-2.5 w-2.5 rounded-full bg-ok/70" />
              <span className="ml-2 font-mono text-xs text-fog">
                orders_by_customer.sql
              </span>
            </div>
            <div className="px-5 py-5 font-mono text-[13px] leading-relaxed">
              <p className="text-fog">EXPLAIN ANALYZE</p>
              <p className="text-paper">SELECT * FROM orders</p>
              <p className="text-paper">WHERE customer_id = $1;</p>
              <p className="mt-3 text-danger">
                Seq Scan on orders (cost=0.00..8412.00)
              </p>
              <p className="text-fog">rows=1 actual_time=812.442ms</p>

              <div className="my-4 border-t border-dashed border-line" />

              <div className="flex items-start gap-2 rounded-md bg-signal-soft px-3 py-3">
                <CircleCheck className="mt-0.5 h-4 w-4 shrink-0 text-signal" />
                <div>
                  <p className="text-paper">
                    Missing index on{" "}
                    <span className="text-signal">orders.customer_id</span>
                  </p>
                  <p className="mt-1 text-xs text-fog">
                    Confidence 0.94 · Estimated gain 96% · Validated
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* What this is / is not */}
      <section className="border-t border-line bg-surface/40">
        <div className="mx-auto max-w-6xl px-6 py-20">
          <div className="grid gap-12 md:grid-cols-2">
            <div>
              <h2 className="font-display text-2xl font-semibold tracking-tight md:text-3xl">
                Not a chatbot. Not a dashboard.
                <br />
                Not another SQL linter.
              </h2>
              <p className="mt-4 max-w-md text-sm leading-relaxed text-fog">
                HypoQuery is an enterprise PostgreSQL workload intelligence
                platform. It discovers performance issues, explains why they
                occur, and recommends deterministic optimizations — then
                validates every one of them before it reaches you.
              </p>
            </div>
            <ul className="space-y-4 self-center">
              {[
                "The optimization engine is deterministic, not AI-guessed.",
                "AI exists only to explain what the engine already found.",
                "The backend is always the source of truth.",
              ].map((line) => (
                <li key={line} className="flex items-start gap-3 text-sm">
                  <CircleCheck className="mt-0.5 h-4 w-4 shrink-0 text-ok" />
                  <span className="text-paper/90">{line}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* Workflow — a genuine ordered sequence, numbered deliberately */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <div className="mb-12 max-w-lg">
          <h2 className="font-display text-2xl font-semibold tracking-tight md:text-3xl">
            One hierarchy. No guessing where you are.
          </h2>
          <p className="mt-4 text-sm leading-relaxed text-fog">
            Every action in HypoQuery happens inside this exact path, in this
            exact order.
          </p>
        </div>

        <div className="relative">
          <div className="absolute left-[15px] top-2 bottom-2 w-px bg-line md:left-[19px]" />
          <ol className="space-y-8">
            {WORKFLOW_STEPS.map((step, i) => (
              <li key={step.label} className="relative flex gap-5 pl-10 md:pl-12">
                <span className="absolute left-0 flex h-8 w-8 items-center justify-center rounded-full border border-line bg-surface font-mono text-xs text-fog md:h-10 md:w-10">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <div>
                  <p className="font-medium text-paper">{step.label}</p>
                  <p className="text-sm text-fog">{step.detail}</p>
                </div>
              </li>
            ))}
          </ol>
        </div>
      </section>

      {/* Feature grid — parallel capabilities, intentionally not numbered */}
      <section className="border-t border-line bg-surface/40">
        <div className="mx-auto max-w-6xl px-6 py-20">
          <h2 className="font-display text-2xl font-semibold tracking-tight md:text-3xl">
            Built for people who own the database, not just the query.
          </h2>
          <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {FEATURES.map(({ icon: Icon, title, body }) => (
              <div
                key={title}
                className="rounded-lg border border-line bg-surface p-6"
              >
                <div className="mb-4 flex h-9 w-9 items-center justify-center rounded-md bg-signal-soft">
                  <Icon className="h-4.5 w-4.5 text-signal" strokeWidth={2} />
                </div>
                <p className="font-medium text-paper">{title}</p>
                <p className="mt-2 text-sm leading-relaxed text-fog">{body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Architecture — the real system stack, top to bottom */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <div className="grid gap-16 md:grid-cols-2 md:items-center">
          <div>
            <h2 className="font-display text-2xl font-semibold tracking-tight md:text-3xl">
              The frontend never touches business logic.
            </h2>
            <p className="mt-4 max-w-md text-sm leading-relaxed text-fog">
              Every request passes through the same layered architecture. The
              interface only displays data, sends requests, and renders
              state — every optimization decision is made below it.
            </p>
          </div>
          <div className="rounded-xl border border-line bg-surface p-2">
            {LAYERS.map((layer, i) => (
              <div key={layer}>
                <div className="flex items-center gap-3 rounded-md px-4 py-3">
                  <span className="font-mono text-xs text-fog">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <span
                    className={
                      i === 0
                        ? "font-mono text-sm text-signal"
                        : "font-mono text-sm text-paper/90"
                    }
                  >
                    {layer}
                  </span>
                </div>
                {i < LAYERS.length - 1 && (
                  <div className="ml-8 h-4 w-px bg-line" />
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Closing CTA */}
      <section className="border-t border-line">
        <div className="mx-auto max-w-6xl px-6 py-20 text-center">
          <h2 className="font-display text-2xl font-semibold tracking-tight md:text-3xl">
            Connect your first database in minutes.
          </h2>
          <p className="mx-auto mt-4 max-w-md text-sm leading-relaxed text-fog">
            Metadata discovery, health checks, and structured findings start
            the moment you register a connection.
          </p>
          <Link
            to="/register"
            className="mt-8 inline-flex items-center gap-2 rounded-md bg-signal px-6 py-3 text-sm font-medium text-paper transition-colors hover:bg-signal/90"
          >
            Get Started
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-line">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 py-8 text-xs text-fog md:flex-row">
          <span>© {new Date().getFullYear()} HypoQuery. All rights reserved.</span>
          <span className="font-mono">PostgreSQL Workload Intelligence Platform</span>
        </div>
      </footer>
    </div>
  );
}
