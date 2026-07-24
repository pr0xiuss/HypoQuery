import { forwardRef } from "react";

const AuthInput = forwardRef(function AuthInput(
  { label, id, error, trailingSlot, ...inputProps },
  ref
) {
  return (
    <div className="auth-field">
      <div className="flex items-center justify-between">
        <label className="auth-label" htmlFor={id}>
          {label}
        </label>
        {trailingSlot}
      </div>
      <input
        id={id}
        ref={ref}
        className={`auth-input ${error ? "auth-input-error" : ""}`}
        aria-invalid={Boolean(error)}
        {...inputProps}
      />
      {error && <p className="auth-error-text">{error}</p>}
    </div>
  );
});

export default AuthInput;
