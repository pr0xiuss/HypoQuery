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
  source: z.string().min(1, "Source path/reference is required"),
});

export default function ApiDiscoveryDialog({
  organizationId,
  projectId,
  environmentId,
  apiId,
  onClose,
}) {
  const [syncResult, setSyncResult] = useState(null);
  const discoverApis = useDiscoverApis(organizationId, projectId, environmentId);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(discoverySchema),
    defaultValues: {
      source_type: "openapi_file",
      source: "",
    },
  });

  const sourceType = watch("source_type");
  const isUnsupported = sourceType === "openapi_url" || sourceType === "repository";

  const onSubmit = async (values) => {
    try {
      const result = await discoverApis.mutateAsync({
        apiId,
        payload: values,
      });
      setSyncResult(result);
    } catch {
      // Error is handled by the submitError display below
    }
  };

  if (syncResult) {
    return (
      <div className="dialog-overlay" onClick={onClose}>
        <div className="dialog-card max-w-2xl" onClick={(e) => e.stopPropagation()}>
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
              {...register("source_type")}
            >
              <option value="openapi_file">OpenAPI Specification (File Path)</option>
              <option value="openapi_url">OpenAPI Specification (URL) - Coming Soon</option>
              <option value="repository">Code Repository - Coming Soon</option>
            </select>
            {errors.source_type && (
              <p className="dialog-error-text">{errors.source_type.message}</p>
            )}
          </div>

          <div className="dialog-field">
            <label className="dialog-label" htmlFor="source">
              Source Reference
            </label>
            <input
              id="source"
              type="text"
              placeholder={
                sourceType === "openapi_file"
                  ? "e.g., /app/data/openapi.yaml (Server Path)"
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
              <p className="mt-1 text-xs text-fog">
                Note: Currently expects a path on the backend server. A dedicated file upload capability is not yet exposed by the API.
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
