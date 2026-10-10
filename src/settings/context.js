import { createContext, useContext } from 'react'
import { integrationCatalog, notificationPrefs } from '../data/settings.js'

export const STORAGE_KEY = 'helpdesk-settings'

export const DEFAULT_SETTINGS = {
  profile: { name: '', email: '', title: '', department: '', timezone: 'utc', language: 'en' },
  appearance: { density: 'comfortable', sidebar: 'expanded', reduceMotion: false, tips: true },
  security: { loginAlerts: true },
  workspace: { name: 'HelpDesk Pro', slug: 'helpdesk-pro', landing: 'dashboard', hoursStart: '08:00', hoursEnd: '18:00' },
  sla: { firstResponse: '30m', resolution: '4h', autoAssign: true, roundRobin: true },
  data: { retention: '1y' },
  notifications: Object.fromEntries(notificationPrefs.map((pref) => [pref.key, pref.default])),
  integrations: Object.fromEntries(integrationCatalog.map((item) => [item.key, false])),
}

export const SettingsContext = createContext(null)

export function useSettings() {
  const context = useContext(SettingsContext)
  if (!context) throw new Error('useSettings must be used within a SettingsProvider')
  return context
}
