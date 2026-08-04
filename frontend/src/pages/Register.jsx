import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Link, useNavigate } from "react-router-dom";
import { Loader2 } from "lucide-react";
import AuthLayout from "../components/auth/AuthLayout";
import AuthCard from "../components/auth/AuthCard";
import AuthInput from "../components/auth/AuthInput";
import PasswordField from "../components/auth/PasswordField";
import { registerUser } from "../services/authService";
import { useToast } from "../components/toast/ToastProvider";
import "../styles/Auth.css";

const signupSchema = z
  .object({
    username: z
      .string()
      .min(3, "Username must be at least 3 characters")
      .regex(/^[a-zA-Z0-9_]+$/, "Only letters, numbers, and underscores"),
    email: z
      .string()
      .min(1, "Email is required")
      .email("Enter a valid email address"),
    password: z.string().min(8, "Password must be at least 8 characters"),
    confirmPassword: z.string().min(1, "Confirm your password"),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
  });

function getPasswordStrength(password) {
  if (!password) return { score: 0, label: "", color: "var(--color-line)" };
  let score = 0;
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
  if (/\d/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;

  const levels = [
    { label: "Very weak", color: "var(--color-danger)" },
    { label: "Weak", color: "var(--color-danger)" },
    { label: "Fair", color: "var(--color-warn)" },
    { label: "Good", color: "var(--color-signal)" },
    { label: "Strong", color: "var(--color-ok)" },
  ];
  return { score, ...levels[Math.min(score, levels.length - 1)] };
}

export default function Register() {
  const navigate = useNavigate();
  const { showToast } = useToast();

  const {
    register,
    handleSubmit,
    watch,
    setError,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: zodResolver(signupSchema),
    defaultValues: { username: "", email: "", password: "", confirmPassword: "" },
  });

  const password = watch("password");
  const strength = getPasswordStrength(password);

  const onSubmit = async (values) => {
    try {
      const { confirmPassword: _confirmPassword, ...payload } = values;
      await registerUser(payload);
      showToast("Account created. Please log in.", { type: "success" });
      navigate("/login", { replace: true });
    } catch (err) {
      setError("root", {
        message:
          err.friendlyMessage ||
          "Unable to create your account. Please try again.",
      });
    }
  };

  return (
    <AuthLayout
      heroTitle="Connect your first database in minutes."
      heroSubtitle="Automatic metadata discovery and health checks start the moment you register a connection."
    >
      <AuthCard>
        <h1 className="font-display text-2xl font-semibold text-paper">
          Create your account
        </h1>
        <p className="mt-2 text-sm text-fog">
          Start analyzing your PostgreSQL workload today.
        </p>

        {errors.root && (
          <div className="auth-banner-error">{errors.root.message}</div>
        )}

        <form className="mt-8" onSubmit={handleSubmit(onSubmit)} noValidate>
          <AuthInput
            id="username"
            label="Username"
            type="text"
            autoComplete="username"
            placeholder="mannan"
            error={errors.username?.message}
            {...register("username")}
          />

          <AuthInput
            id="email"
            label="Email"
            type="email"
            autoComplete="email"
            placeholder="you@company.com"
            error={errors.email?.message}
            {...register("email")}
          />

          <PasswordField
            id="password"
            label="Password"
            autoComplete="new-password"
            placeholder="At least 8 characters"
            error={errors.password?.message}
            {...register("password")}
          />

          {password && (
            <div className="auth-strength">
              <div className="auth-strength-track">
                {[0, 1, 2, 3, 4].map((i) => (
                  <span
                    key={i}
                    className="auth-strength-segment"
                    style={{
                      backgroundColor:
                        i < strength.score ? strength.color : "var(--color-line)",
                    }}
                  />
                ))}
              </div>
              <span
                className="auth-strength-label"
                style={{ color: strength.color }}
              >
                {strength.label}
              </span>
            </div>
          )}

          <PasswordField
            id="confirmPassword"
            label="Confirm password"
            autoComplete="new-password"
            placeholder="Re-enter your password"
            error={errors.confirmPassword?.message}
            {...register("confirmPassword")}
          />

          <button type="submit" className="auth-submit" disabled={isSubmitting}>
            {isSubmitting ? (
              <span className="flex items-center justify-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                Creating account…
              </span>
            ) : (
              "Create account"
            )}
          </button>
        </form>

        <div className="auth-divider">or</div>

        <p className="text-center text-sm text-fog">
          Already have an account?{" "}
          <Link to="/login" className="text-signal hover:underline">
            Sign In
          </Link>
        </p>
      </AuthCard>
    </AuthLayout>
  );
}
