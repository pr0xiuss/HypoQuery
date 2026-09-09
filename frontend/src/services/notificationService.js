import api from "./api";

export const getNotifications = async (limit = 50, offset = 0, unreadOnly = false) => {
  const params = new URLSearchParams({ limit, offset });
  if (unreadOnly) {
    params.append("unread_only", "true");
  }
  const { data } = await api.get(`/api/v1/notifications?${params.toString()}`);
  return data;
};

export const markNotificationRead = async (notificationId) => {
  const { data } = await api.patch(`/api/v1/notifications/${notificationId}/read`);
  return data;
};

export const markAllNotificationsRead = async () => {
  // Not implemented on backend, throwing error or ignoring
  return [];
};

export const getNotificationPreferences = async () => {
  const { data } = await api.get(`/api/v1/notifications/preferences`);
  return data;
};

export const updateNotificationPreference = async (notificationType, isEnabled) => {
  const { data } = await api.put(`/api/v1/notifications/preferences`, {
    notification_type: notificationType,
    is_enabled: isEnabled,
  });
  return data;
};
