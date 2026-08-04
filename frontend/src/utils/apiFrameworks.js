export const FRAMEWORK_OPTIONS = [
  { value: "FASTAPI", label: "FastAPI" },
  { value: "DJANGO", label: "Django" },
  { value: "FLASK", label: "Flask" },
  { value: "EXPRESS", label: "Express" },
  { value: "SPRING_BOOT", label: "Spring Boot" },
  { value: "ASP_NET", label: "ASP.NET" },
  { value: "GO", label: "Go" },
  { value: "LARAVEL", label: "Laravel" },
  { value: "OTHER", label: "Other" },
];

export const FRAMEWORK_VALUES = FRAMEWORK_OPTIONS.map((option) => option.value);

export function formatFrameworkLabel(framework) {
  return FRAMEWORK_OPTIONS.find((option) => option.value === framework)?.label || framework;
}
