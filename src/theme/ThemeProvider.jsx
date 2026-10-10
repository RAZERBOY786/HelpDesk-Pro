import { useCallback, useEffect, useMemo, useState } from 'react'
import { STORAGE_KEY, ThemeContext } from './context.js'

function getSystemTheme() {
  if (typeof window === 'undefined') return 'light'
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function getInitialTheme() {
  if (typeof window === 'undefined') return 'system'
  const stored = window.localStorage.getItem(STORAGE_KEY)
  return stored === 'light' || stored === 'dark' || stored === 'system' ? stored : 'system'
}

export function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState(getInitialTheme)
  const [systemTheme, setSystemTheme] = useState(getSystemTheme)

  useEffect(() => {
    const query = window.matchMedia('(prefers-color-scheme: dark)')
    const handler = (event) => setSystemTheme(event.matches ? 'dark' : 'light')
    query.addEventListener('change', handler)
    return () => query.removeEventListener('change', handler)
  }, [])

  const resolved = theme === 'system' ? systemTheme : theme

  useEffect(() => {
    const root = document.documentElement
    root.classList.toggle('dark', resolved === 'dark')
    root.style.colorScheme = resolved
  }, [resolved])

  const setTheme = useCallback((next) => {
    setThemeState(next)
    try {
      window.localStorage.setItem(STORAGE_KEY, next)
    } catch {
      // Storage can be unavailable (private mode); theme still applies for the session.
    }
  }, [])

  const value = useMemo(() => ({ theme, resolved, setTheme }), [theme, resolved, setTheme])

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}
