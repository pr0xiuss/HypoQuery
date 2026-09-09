import { useState, useRef, useEffect } from "react";
import { Bell, Check, CheckCircle2, AlertCircle, RefreshCw } from "lucide-react";
import {
  useNotifications,
  useMarkNotificationRead,
  useMarkAllNotificationsRead,
} from "../../hooks/useNotifications";
import "../../styles/AppLayout.css"; // Ensure standard tokens are available

export default function NotificationBell() {
  const [isOpen, setIsOpen] = useState(false);
  const popoverRef = useRef(null);
  
  const { data: notificationsData, isLoading } = useNotifications(20, 0, false);
  const { mutate: markRead } = useMarkNotificationRead();
  const { mutate: markAllRead } = useMarkAllNotificationsRead();

  const notifications = notificationsData?.items || [];
  const unreadCount = notificationsData?.unread_count || 0;

  // Close popover when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (popoverRef.current && !popoverRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const getIconForType = (type) => {
    switch (type) {
      case "job_completed":
        return <CheckCircle2 className="h-5 w-5 text-ok" />;
      case "job_failed":
        return <AlertCircle className="h-5 w-5 text-danger" />;
      case "job_retrying":
        return <RefreshCw className="h-5 w-5 text-warn" />;
      default:
        return <Bell className="h-5 w-5 text-fog" />;
    }
  };

  const handleNotificationClick = (notification) => {
    if (!notification.is_read) {
      markRead(notification.id);
    }
    // Could navigate to job details here if we had a route for it
  };

  return (
    <div className="relative" ref={popoverRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative flex h-9 w-9 items-center justify-center rounded-md hover:bg-surface-raised transition-colors"
      >
        <Bell className="h-5 w-5 text-fog hover:text-paper transition-colors" />
        {unreadCount > 0 && (
          <span className="absolute top-1.5 right-1.5 flex h-2 w-2 rounded-full bg-danger ring-2 ring-ink"></span>
        )}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 rounded-lg border border-line bg-surface shadow-lg ring-1 ring-black ring-opacity-5 z-50 overflow-hidden">
          <div className="flex items-center justify-between border-b border-line bg-surface-raised px-4 py-3">
            <h3 className="text-sm font-semibold text-paper">Notifications</h3>
            {unreadCount > 0 && (
              <button
                onClick={() => markAllRead()}
                className="flex items-center text-xs font-medium text-fog hover:text-paper transition-colors"
              >
                <Check className="mr-1 h-3 w-3" />
                Mark all read
              </button>
            )}
          </div>

          <div className="max-h-96 overflow-y-auto">
            {isLoading ? (
              <div className="flex items-center justify-center py-8">
                <span className="text-sm text-fog">Loading...</span>
              </div>
            ) : notifications.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-8 px-4 text-center">
                <Bell className="mb-2 h-8 w-8 text-fog/50" />
                <p className="text-sm text-fog">No notifications yet.</p>
              </div>
            ) : (
              <div className="divide-y divide-line">
                {notifications.map((notification) => (
                  <div
                    key={notification.id}
                    onClick={() => handleNotificationClick(notification)}
                    className={`flex items-start gap-3 p-4 cursor-pointer hover:bg-surface-raised transition-colors ${
                      !notification.is_read ? "bg-surface-raised/50" : ""
                    }`}
                  >
                    <div className="mt-0.5 shrink-0">
                      {getIconForType(notification.notification_type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm ${!notification.is_read ? 'font-semibold text-paper' : 'font-medium text-paper'}`}>
                        {notification.title}
                      </p>
                      <p className="mt-1 text-xs text-fog leading-relaxed break-words">
                        {notification.message}
                      </p>
                      <p className="mt-2 text-[10px] font-medium text-fog/70">
                        {new Date(notification.created_at).toLocaleString()}
                      </p>
                    </div>
                    {!notification.is_read && (
                      <div className="mt-1.5 shrink-0 h-2 w-2 rounded-full bg-signal"></div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
