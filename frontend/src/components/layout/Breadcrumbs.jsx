import { Link } from "react-router-dom";
import { ChevronRight } from "lucide-react";

/**
 * items: Array<{ label: string, to?: string, icon?: ComponentType }>
 * The last item always renders as the current page (plain text, no link),
 * regardless of whether it has a `to`.
 */
export default function Breadcrumbs({ items }) {
  return (
    <ol className="app-breadcrumb">
      {items.map((item, i) => {
        const isCurrent = i === items.length - 1;
        const Icon = item.icon;
        return (
          <li key={`${item.label}-${i}`} className="app-breadcrumb-item">
            {i > 0 && <ChevronRight className="h-3.5 w-3.5 text-fog" />}
            {Icon && <Icon className="h-3.5 w-3.5" />}
            {isCurrent || !item.to ? (
              <span className="text-paper">{item.label}</span>
            ) : (
              <Link to={item.to} className="app-breadcrumb-link">
                {item.label}
              </Link>
            )}
          </li>
        );
      })}
    </ol>
  );
}
