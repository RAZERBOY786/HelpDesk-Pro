import { useLocation } from 'react-router-dom'

function titleFromPath(pathname) {
  return pathname
    .replace(/^\//, '')
    .split('-')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ')
}

function Placeholder() {
  const { pathname } = useLocation()
  const title = titleFromPath(pathname) || 'Dashboard'

  return (
    <div className="flex flex-col items-center justify-center py-space-xl min-h-[60vh] text-center">
      <div className="w-14 h-14 rounded-xl bg-primary-fixed text-on-primary-fixed-variant flex items-center justify-center mb-space-md">
        <span className="material-symbols-outlined text-[28px]">construction</span>
      </div>
      <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight">{title}</h1>
      <p className="font-body-md text-body-md text-on-surface-variant mt-1 max-w-md">
        This workspace is part of the HelpDesk Pro navigation shell. The All Tickets Queue, Employee Self-Service Portal,
        Knowledge Base, and Submit New Ticket screens are fully built.
      </p>
    </div>
  )
}

export default Placeholder
