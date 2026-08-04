import { Link, useParams } from "react-router-dom";

export default function EnvironmentTabs({ active }) {
  const { organizationId, projectId, environmentId } = useParams();
  const basePath = `/organizations/${organizationId}/projects/${projectId}/environments/${environmentId}`;

  const tabs = [
    { key: "overview", label: "Overview", to: basePath },
    {
      key: "connections",
      label: "Database Connections",
      to: `${basePath}/database-connections`,
    },
    { key: "apis", label: "APIs", to: `${basePath}/apis` },
  ];

  return (
    <div className="environment-tabs">
      {tabs.map((tab) =>
        tab.disabled ? (
          <span
            key={tab.key}
            className="environment-tab environment-tab-disabled"
            title="Coming soon"
          >
            {tab.label}
            <span className="dashboard-soon-badge">Soon</span>
          </span>
        ) : (
          <Link
            key={tab.key}
            to={tab.to}
            className={`environment-tab ${active === tab.key ? "environment-tab-active" : ""}`}
          >
            {tab.label}
          </Link>
        )
      )}
    </div>
  );
}