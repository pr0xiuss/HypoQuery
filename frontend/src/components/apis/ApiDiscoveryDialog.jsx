import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Loader2, Search } from "lucide-react";
import { useDiscoverApis } from "../../hooks/useApis";
import ApiDiscoveryResult from "./ApiDiscoveryResult";
import "../../styles/Organizations.css";

const discoverySchema = z.object({
  source_type: z.enum(["openapi_file", "openapi_url", "repository"], {
    errorMap: () => ({ message: "Select a valid source type" }),
  }),
  source: z.string().min(1, "Source path or reference is required"),
});

export default function ApiDiscoveryDialog({
  organizationId,
  projectId,
  environmentId,
  apiId,
  onClose,
}) {
  const [sourceType, setSourceType] = useState("openapi_file");
  const [syncResult, setSyncResult] = useState(null);
  const discoverApis = useDiscoverApis(organizationId, projectId, environmentId);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(discoverySchema),
    defaultValues: {
      source_type: "openapi_file",
      source: "",
    },
  });

  const isUnsupported = sourceType === "openapi_url" || sourceType === "repository";

  const handleSourceTypeChange = (e) => {
    const val = e.target.value;
    setSourceType(val);
    setValue("source_type", val);
  };

  const onSubmit = async (values) => {
    try {
      const result = await discoverApis.mutateAsync({
        apiId,
        payload: {
          source_type: values.source_type,
          source: values.source.trim(),
        },
      });
      setSyncResult(result);
    } catch {
      // Handled by discoverApis.error state
    }
  };

  if (syncResult) {
    return (
      <div className="dialog-overlay" onClick={onClose}>
        <div
          className="dialog-card max-w-2xl max-h-[85vh] flex flex-col"
          onClick={(e) => e.stopPropagation()}
        >
          <ApiDiscoveryResult result={syncResult} onClose={onClose} />
        </div>
      </div>
    );
  }

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-card" onClick={(e) => e.stopPropagation()}>
        <h2 className="font-display text-lg font-semibold text-paper">
          Discover Endpoints
        </h2>
        <p className="mt-1 text-sm text-fog">
          Automatically discover and synchronize API endpoints from a source specification.
        </p>

        {discoverApis.isError && (
          <div className="dialog-error">{discoverApis.error?.friendlyMessage}</div>
        )}

        <form className="mt-5" onSubmit={handleSubmit(onSubmit)} noValidate>
          <div className="dialog-field">
            <label className="dialog-label" htmlFor="source-type">
              Discovery Source
            </label>
            <select
              id="source-type"
              className={`dialog-input ${errors.source_type ? "dialog-input-error" : ""}`}
              value={sourceType}
              onChange={handleSourceTypeChange}
            >
              <option value="openapi_file">OpenAPI Specification (File Path)</option>
              <option value="openapi_url" disabled>
                OpenAPI Specification (URL) — Coming Soon
              </option>
              <option value="repository" disabled>
                Code Repository — Coming Soon
              </option>
            </select>
            {errors.source_type && (
              <p className="dialog-error-text">{errors.source_type.message}</p>
            )}
          </div>

          <div className="dialog-field">
            <label className="dialog-label" htmlFor="source">
              Specification File Path
            </label>
            <input
              id="source"
              type="text"
              placeholder={
                sourceType === "openapi_file"
                  ? "/path/to/openapi.yaml or spec.json (Server Path)"
                  : "Not yet available"
              }
              className={`dialog-input ${errors.source ? "dialog-input-error" : ""}`}
              disabled={isUnsupported}
              {...register("source")}
            />
            {errors.source && (
              <p className="dialog-error-text">{errors.source.message}</p>
            )}
            {sourceType === "openapi_file" && (
              <p className="mt-1.5 text-xs text-fog leading-relaxed">
                Provide the absolute or workspace path on the backend server where the OpenAPI JSON/YAML specification file is located.
              </p>
            )}
          </div>

          <div className="dialog-actions">
            <button
              type="button"
              className="orgs-secondary-btn"
              onClick={onClose}
              disabled={discoverApis.isPending}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="orgs-primary-btn"
              disabled={discoverApis.isPending || isUnsupported}
            >
              {discoverApis.isPending ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Discovering…
                </>
              ) : (
                <>
                  <Search className="h-4 w-4" />
                  Start Discovery
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
