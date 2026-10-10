import { useState } from 'react'
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom'
import { navGroups, workspaces } from '../data/nav.js'
import { useSettings } from '../settings/context.js'
import DotBackground from './DotBackground.jsx'
import { Avatar, Badge, Button, Icon } from './ui.jsx'

function AmbientBackdrop() {
  return (
    <div aria-hidden="true" className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
      <span className="ambient-orb ambient-orb--a" />
      <span className="ambient-orb ambient-orb--b" />
      <span className="ambient-orb ambient-orb--c" />
    </div>
  )
}

function NavItem({ item, active, compact }) {
  return (
    <NavLink
      className={
        'flex items-center rounded-lg transition-colors ' +
        (compact ? 'justify-center py-2' : 'justify-between px-space-sm py-1.5 ') +
        (active
          ? 'bg-primary-container text-on-primary-container font-semibold'
          : 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface')
      }
      title={compact ? item.label : undefined}
      to={item.to}
    >
      <span className={'flex items-center ' + (compact ? 'justify-center' : 'gap-space-sm')}>
        <Icon name={item.icon} size={compact ? 22 : 18} />
        {compact ? null : <span className="font-body-md text-body-md">{item.label}</span>}
      </span>
    </NavLink>
  )
}

function WorkspaceToggle() {
  const [active, setActive] = useState(workspaces[0])
  return (
    <div className="bg-surface-container-low p-0.5 rounded-xl flex items-center justify-between">
      {workspaces.map((w) => (
        <button
          className={
            'flex-1 py-1 text-center font-label-sm text-label-sm rounded-lg transition-colors ' +
            (active === w
              ? 'bg-surface-container-lowest text-on-surface shadow-[0_1px_4px_rgba(0,0,0,0.05)]'
              : 'text-on-surface-variant hover:text-on-surface')
          }
          key={w}
          onClick={() => setActive(w)}
          type="button"
        >
          {w}
        </button>
      ))}
    </div>
  )
}

function AppShell() {
  const { pathname } = useLocation()
  const { settings, update } = useSettings()
  const compact = settings.appearance.sidebar === 'compact'
  const tips = settings.appearance.tips
  const profile = settings.profile

  const toggleRail = () => update('appearance', { sidebar: compact ? 'expanded' : 'compact' })

  return (
    <>
      <AmbientBackdrop />
      <DotBackground />
      <aside
        className={`fixed left-0 top-0 h-screen ${
          compact ? 'w-[72px]' : 'w-64'
        } glass-panel bg-surface-container-lowest/80 backdrop-blur-xl z-50 flex flex-col justify-between select-none transition-[width] duration-200`}
      >
        <div className="flex flex-col flex-1 min-h-0">
          <div className={`pt-space-md pb-space-sm flex items-center ${compact ? 'justify-center px-space-xs' : 'justify-between px-space-md'}`}>
            <div className="flex items-center gap-space-sm">
              <span className="h-8 w-8 rounded-lg bg-primary text-on-primary flex items-center justify-center shrink-0">
                <Icon name="support_agent" size={20} />
              </span>
              {compact ? null : (
                <span className="font-headline-sm text-headline-sm text-on-surface tracking-tight truncate">
                  {settings.workspace.name}
                </span>
              )}
            </div>
            {compact ? null : (
              <Badge tone="muted" className="uppercase">
                v4.2
              </Badge>
            )}
          </div>
          {compact ? null : (
            <div className="px-space-md py-space-xs">
              <WorkspaceToggle />
            </div>
          )}
          <div className="flex-1 overflow-y-auto px-space-sm py-space-xs">
            {navGroups.map((group) => (
              <div className={compact ? 'mb-space-sm' : 'mb-space-md'} key={group.label}>
                {compact ? null : (
                  <div className="px-space-sm py-1 font-label-sm text-label-sm text-outline uppercase tracking-wider">
                    {group.label}
                  </div>
                )}
                <nav className="flex flex-col gap-0.5 mt-0.5">
                  {group.items.map((item) => (
                    <NavItem active={pathname === item.to} compact={compact} item={item} key={item.to} />
                  ))}
                </nav>
              </div>
            ))}
          </div>
        </div>

        <div className="p-space-sm">
          {compact ? (
            <div className="flex flex-col items-center gap-2 py-space-xs">
              <span className="relative flex h-2 w-2" title="Operational">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-tertiary-container opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-tertiary"></span>
              </span>
              <button
                className="text-on-surface-variant hover:text-on-surface transition-colors p-1"
                onClick={toggleRail}
                title="Expand navigation rail"
                type="button"
              >
                <Icon name="keyboard_double_arrow_right" size={18} />
              </button>
            </div>
          ) : (
            <div className="p-space-xs rounded-xl bg-surface-container-lowest shadow-[0_1px_4px_rgba(0,0,0,0.03)] flex flex-col gap-1.5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-1.5">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-tertiary-container opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-tertiary"></span>
                  </span>
                  <span className="font-label-sm text-label-sm text-on-surface font-semibold">Operational</span>
                </div>
              </div>
              <div className="flex items-center justify-between pt-1 border-t border-surface-container">
                <button className="flex items-center gap-1 font-body-sm text-body-sm text-on-surface-variant hover:text-on-surface transition-colors" type="button">
                  <Icon name="keyboard" size={15} />
                  <span>Shortcuts</span>
                </button>
                <button
                  className="text-on-surface-variant hover:text-on-surface transition-colors p-0.5"
                  onClick={toggleRail}
                  title="Collapse navigation rail"
                  type="button"
                >
                  <Icon name="keyboard_double_arrow_left" size={16} />
                </button>
              </div>
            </div>
          )}
        </div>
      </aside>

      <div className={'relative z-10 ' + (compact ? 'pl-[72px]' : 'pl-64')}>
        <header
          className={`fixed top-0 ${
            compact ? 'left-[72px]' : 'left-64'
          } right-0 h-16 glass-panel bg-surface-container-lowest/80 backdrop-blur-xl z-40 flex items-center justify-between px-space-lg transition-[left] duration-200`}
        >
          <div className="flex items-center flex-1 max-w-xl mr-space-md">
            <div className="w-full flex items-center gap-space-sm px-space-md py-1.5 rounded-xl bg-surface-container-low text-on-surface-variant focus-within:bg-surface-container-lowest focus-within:ring-2 focus-within:ring-primary/20 transition-all">
              <Icon className="text-outline" name="search" size={18} />
              <input
                className="w-full bg-transparent font-body-md text-body-md text-on-surface placeholder:text-outline focus:outline-none"
                placeholder="Search tickets, assets, KB articles..."
                type="text"
              />
              {tips ? (
                <span className="font-code-sm text-code-sm px-1.5 py-0.5 rounded bg-surface-container-high text-on-surface font-medium select-none">
                  ⌘K
                </span>
              ) : null}
            </div>
          </div>
          <div className="flex items-center gap-space-md">
            <Button as={Link} icon="add" to="/submit" variant="primary">
              New Ticket
            </Button>
            <div className="flex items-center gap-1">
              <button className="p-2 rounded-xl text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors" title="Alerts" type="button">
                <Icon name="warning" size={20} />
              </button>
              <button className="p-2 rounded-xl text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-colors" title="Notifications" type="button">
                <Icon name="notifications" size={20} />
              </button>
            </div>
            <div className="h-6 w-px bg-surface-container-high mx-space-xs"></div>
            <button className="flex items-center gap-space-sm p-1 rounded-xl hover:bg-surface-container-low transition-colors" type="button">
              <Avatar name={profile.name} size="md" />
              <span className="hidden lg:block font-body-sm text-body-sm text-on-surface-variant max-w-32 truncate">
                {profile.name || 'Account'}
              </span>
              <Icon className="hidden sm:block text-outline" name="expand_more" size={18} />
            </button>
          </div>
        </header>
        <main className="relative pt-16 w-full px-space-lg min-h-screen bg-transparent">
          <div key={pathname} className="page-anim flex flex-col w-full pb-12">
            <Outlet />
          </div>
        </main>
      </div>
    </>
  )
}

export default AppShell
