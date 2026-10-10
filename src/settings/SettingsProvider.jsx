import { useCallback, useEffect, useMemo, useState } from 'react'
import { DEFAULT_SETTINGS, SettingsContext, STORAGE_KEY } from './context.js'

const SECTIONS = ['profile', 'appearance', 'security', 'workspace', 'sla', 'data', 'notifications', 'integrations']

function loadSettings() {
  if (typeof window === 'undefined') return DEFAULT_SETTINGS
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    if (!raw) return DEFAULT_SETTINGS
    const parsed = JSON.parse(raw)
    return SECTIONS.reduce(
      (acc, section) => ({ ...acc, [section]: { ...DEFAULT_SETTINGS[section], ...(parsed[section] ?? {}) } }),
      { ...DEFAULT_SETTINGS },
    )
  } catch {
    // Corrupt or unavailable storage; fall back to defaults.
    return DEFAULT_SETTINGS
  }
}

export function SettingsProvider({ children }) {
  const [settings, setSettings] = useState(loadSettings)

  const update = useCallback((section, patch) => {
    setSettings((prev) => ({ ...prev, [section]: { ...prev[section], ...patch } }))
  }, [])

  const reset = useCallback(() => setSettings(DEFAULT_SETTINGS), [])

  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(settings))
    } catch {
      // Storage can be unavailable (private mode); settings still apply for the session.
    }
  }, [settings])

  useEffect(() => {
    const root = document.documentElement
    root.classList.toggle('density-compact', settings.appearance.density === 'compact')
    root.classList.toggle('reduce-motion', settings.appearance.reduceMotion)
  }, [settings.appearance.density, settings.appearance.reduceMotion])

  const value = useMemo(() => ({ settings, update, reset }), [settings, update, reset])

  return <SettingsContext.Provider value={value}>{children}</SettingsContext.Provider>
}
