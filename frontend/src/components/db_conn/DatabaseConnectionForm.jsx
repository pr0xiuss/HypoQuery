import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Link } from "react-router-dom";
import { Loader2 } from "lucide-react";

const connectionSchema = z.object({
  name: z
    .string()
    .min(2, "Connection name must be at least 2 characters")
    .max(100, "Connection name must be at most 100 characters"),
  host: z.string().min(1, "Host is required"),
  port: z.coerce
    .number({ invalid_type_error: "Port must be a number" })
    .int("Port must be a whole number")
    .min(1, "Port must be between 1 and 65535")
    .max(65535, "Port must be between 1 and 65535"),
  database_name: z.string().min(1, "Database name is required"),
  username: z.string().min(1, "Username is required"),
  password: z.string().min(1, "Password is required"),
  ssl_enabled: z.boolean().optional(),
});

/**
 * defaultValues: { name, host, port, database_name, username, password, ssl_enabled }
 * Password is never prefilled (the API never returns it) — re-entering it
 * is required on both create and edit, per spec.
 */
export default function DatabaseConnectionForm({
  defaultValues,
  onSubmit,
  isSubmitting,
  submitError,
  submitLabel,
  savingLabel,
  cancelTo,
}) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(connectionSchema),
    defaultValues: defaultValues || {
      name: "",
      host: "",
      port: 5432,
      database_name: "",
      username: "",
      password: "",
      ssl_enabled: false,
    },
  });

  return (
    <>
      {submitError && <div className="dialog-error">{submitError}</div>}

      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <div className="dialog-field">
          <label className="dialog-label" htmlFor="conn-name">
            Connection Name
          </label>
          <input
            id="conn-name"
            type="text"
            autoFocus
            placeholder="Production"
            className={`dialog-input ${errors.name ? "dialog-input-error" : ""}`}
            {...register("name")}
          />
          {errors.name && <p className="dialog-error-text">{errors.name.message}</p>}
        </div>

        <div className="dialog-field-row">
          <div className="dialog-field dialog-field-grow">
            <label className="dialog-label" htmlFor="conn-host">
              Host
            </label>
            <input
              id="conn-host"
              type="text"
              placeholder="localhost"
              className={`dialog-input ${errors.host ? "dialog-input-error" : ""}`}
              {...register("host")}
            />
            {errors.host && <p className="dialog-error-text">{errors.host.message}</p>}
          </div>

          <div className="dialog-field dialog-field-narrow">
            <label className="dialog-label" htmlFor="conn-port">
              Port
            </label>
            <input
              id="conn-port"
              type="number"
              placeholder="5432"
              className={`dialog-input ${errors.port ? "dialog-input-error" : ""}`}
              {...register("port")}
            />
            {errors.port && <p className="dialog-error-text">{errors.port.message}</p>}
          </div>
        </div>

        <div className="dialog-field">
          <label className="dialog-label" htmlFor="conn-database">
            Database Name
          </label>
          <input
            id="conn-database"
            type="text"
            placeholder="postgres"
            className={`dialog-input ${errors.database_name ? "dialog-input-error" : ""}`}
            {...register("database_name")}
          />
          {errors.database_name && (
            <p className="dialog-error-text">{errors.database_name.message}</p>
          )}
        </div>

        <div className="dialog-field">
          <label className="dialog-label" htmlFor="conn-username">
            Username
          </label>
          <input
            id="conn-username"
            type="text"
            placeholder="postgres"
            className={`dialog-input ${errors.username ? "dialog-input-error" : ""}`}
            {...register("username")}
          />
          {errors.username && (
            <p className="dialog-error-text">{errors.username.message}</p>
          )}
        </div>

        <div className="dialog-field">
          <label className="dialog-label" htmlFor="conn-password">
            Password
          </label>
          <input
            id="conn-password"
            type="password"
            placeholder="••••••••"
            autoComplete="new-password"
            className={`dialog-input ${errors.password ? "dialog-input-error" : ""}`}
            {...register("password")}
          />
          {errors.password && (
            <p className="dialog-error-text">{errors.password.message}</p>
          )}
        </div>

        <div className="dialog-field dialog-checkbox-field">
          <label className="dialog-checkbox-label" htmlFor="conn-ssl">
            <input id="conn-ssl" type="checkbox" {...register("ssl_enabled")} />
            SSL Enabled
          </label>
        </div>

        <div className="dialog-actions create-project-actions">
          <button type="submit" className="orgs-primary-btn" disabled={isSubmitting}>
            {isSubmitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                {savingLabel}
              </>
            ) : (
              submitLabel
            )}
          </button>
          <Link to={cancelTo} className="orgs-secondary-btn">
            Cancel
          </Link>
        </div>
      </form>
    </>
  );
}
