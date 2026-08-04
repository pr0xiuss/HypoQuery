import { forwardRef, useState } from "react";
import { Eye, EyeOff } from "lucide-react";

const PasswordField = forwardRef(function PasswordField(
  { label, id, error, ...inputProps },
  ref
) {
  const [visible, setVisible] = useState(false);

  return (
    <div className="auth-field">
      <label className="auth-label" htmlFor={id}>
        {label}
      </label>
      <div className="auth-password-wrap">
        <input
          id={id}
          ref={ref}
          type={visible ? "text" : "password"}
          className={`auth-input ${error ? "auth-input-error" : ""}`}
          aria-invalid={Boolean(error)}
          {...inputProps}
        />
        <button
          type="button"
          className="auth-password-toggle"
          onClick={() => setVisible((v) => !v)}
          tabIndex={-1}
          aria-label={visible ? "Hide password" : "Show password"}
        >
          {visible ? (
            <EyeOff className="h-4 w-4" />
          ) : (
            <Eye className="h-4 w-4" />
          )}
        </button>
      </div>
      {error && <p className="auth-error-text">{error}</p>}
    </div>
  );
});

export default PasswordField;
