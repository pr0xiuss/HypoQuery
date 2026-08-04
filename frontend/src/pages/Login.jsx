import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Link, useNavigate } from "react-router-dom";
import { Loader2 } from "lucide-react";
import AuthLayout from "../components/auth/AuthLayout";
import AuthCard from "../components/auth/AuthCard";
import AuthInput from "../components/auth/AuthInput";
import PasswordField from "../components/auth/PasswordField";
import { loginUser } from "../services/authService";
import { setTokens } from "../utils/auth";
import "../styles/Auth.css";

const loginSchema = z.object({
  identifier: z.string().min(1, "Enter your username or email"),
  password: z.string().min(1, "Password is required"),
});

export default function Login() {
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    setError,
    setFocus,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: zodResolver(loginSchema),
    defaultValues: { identifier: "", password: "" },
  });

  // Focus the first field on mount.
  useEffect(() => {
    setFocus("identifier");
  }, [setFocus]);

  const onSubmit = async (values) => {
    try {
      const data = await loginUser(values);
      setTokens(data);
      navigate("/organizations", { replace: true });
    } catch (err) {
      setError("root", {
        message: err.friendlyMessage || "Invalid username/email or password.",
      });
      // Send focus back to the identifier field so the user can retry immediately.
      setFocus("identifier");
    }
  };

  return (
    <AuthLayout
      heroTitle="Know why your database is slow, not just that it is."
      heroSubtitle="Deterministic PostgreSQL analysis, explained in plain language."
    >
      <AuthCard>
        <h1 className="font-display text-2xl font-semibold text-paper">
          Log in
        </h1>
        <p className="mt-2 text-sm text-fog">
          Welcome back. Enter your credentials to continue.
        </p>

        {errors.root && (
          <div className="auth-banner-error">{errors.root.message}</div>
        )}

        <form className="mt-8" onSubmit={handleSubmit(onSubmit)} noValidate>
          <AuthInput
            id="identifier"
            label="Username or Email"
            type="text"
            autoComplete="username"
            placeholder="you@company.com"
            error={errors.identifier?.message}
            {...register("identifier")}
          />

          <PasswordField
            id="password"
            label="Password"
            autoComplete="current-password"
            placeholder="••••••••"
            error={errors.password?.message}
            {...register("password")}
          />

          <button type="submit" className="auth-submit" disabled={isSubmitting}>
            {isSubmitting ? (
              <span className="flex items-center justify-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                Logging in…
              </span>
            ) : (
              "Log in"
            )}
          </button>
        </form>

        <div className="auth-divider">or</div>

        <p className="text-center text-sm text-fog">
          Don&apos;t have an account?{" "}
          <Link to="/register" className="text-signal hover:underline">
            Create Account
          </Link>
        </p>
      </AuthCard>
    </AuthLayout>
  );
}
