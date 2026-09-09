
import { useNotificationPreferences, useUpdateNotificationPreference } from "../hooks/useNotifications";

export default function Settings() {
  const { data: preferences, isLoading } = useNotificationPreferences();
  const { mutate: updatePreference, isPending } = useUpdateNotificationPreference();

  const handleToggle = (notificationType, currentEnabled) => {
    updatePreference({ notificationType, isEnabled: !currentEnabled });
  };

  if (isLoading) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-semibold text-paper mb-6">Settings</h1>
        <p className="text-fog">Loading settings...</p>
      </div>
    );
  }

  // Ensure all types are shown even if they have no explicit db preference yet
  const prefMap = (preferences || []).reduce((acc, pref) => {
    acc[pref.notification_type] = pref.is_enabled;
    return acc;
  }, {});

  const notificationTypes = [
    { type: "job_completed", label: "Job Completed", description: "Receive a notification when a background job finishes successfully." },
    { type: "job_failed", label: "Job Failed", description: "Receive a notification when a background job fails completely after all retries." },
    { type: "job_retrying", label: "Job Retrying", description: "Receive a notification when a background job encounters an error but is scheduled to retry." }
  ];

  return (
    <div className="max-w-4xl">
      <h1 className="text-2xl font-display font-semibold text-paper mb-6">Settings</h1>

      <div className="bg-surface rounded-lg border border-line">
        <div className="px-6 py-5 border-b border-line">
          <h2 className="text-lg font-medium text-paper">Notification Preferences</h2>
          <p className="mt-1 text-sm text-fog">Manage how you want to be notified about background jobs and activities.</p>
        </div>
        <ul className="divide-y divide-line">
          {notificationTypes.map(({ type, label, description }) => {
            const isEnabled = prefMap[type] !== undefined ? prefMap[type] : true; // Default to true if no preference exists
            return (
              <li key={type} className="px-6 py-5 flex items-center justify-between hover:bg-surface-raised transition-colors">
                <div className="pr-4">
                  <h3 className="text-sm font-medium text-paper">{label}</h3>
                  <p className="text-sm text-fog mt-1">{description}</p>
                </div>
                <div>
                  <button
                    type="button"
                    onClick={() => handleToggle(type, isEnabled)}
                    disabled={isPending}
                    className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-signal focus:ring-offset-2 focus:ring-offset-ink ${
                      isEnabled ? 'bg-signal' : 'bg-surface-raised'
                    } ${isPending ? 'opacity-50 cursor-not-allowed' : ''}`}
                    role="switch"
                    aria-checked={isEnabled}
                  >
                    <span className="sr-only">Toggle {label}</span>
                    <span
                      aria-hidden="true"
                      className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-paper shadow ring-0 transition duration-200 ease-in-out ${
                        isEnabled ? 'translate-x-5' : 'translate-x-0'
                      }`}
                    />
                  </button>
                </div>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}
