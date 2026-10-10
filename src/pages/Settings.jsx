import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Avatar,
  Badge,
  Button,
  Card,
  EmptyState,
  Icon,
  IconBadge,
  SegmentedControl,
  Select,
  SettingsRow,
  SettingsSection,
  TextField,
  Toggle,
} from '../components/ui.jsx'
import {
  activeSessions,
  apiTokens,
  densityOptions,
  escalationRules,
  integrationCatalog,
  landingOptions,
  languageOptions,
  notificationPrefs,
  responseTargetOptions,
  retentionOptions,
  settingsSections,
  sidebarOptions,
  teamMembers,
  themeOptions,
  timezoneOptions,
} from '../data/settings.js'
import { useSettings } from '../settings/context.js'
import { useTheme } from '../theme/context.js'

function Labeled({ label, hint, children }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="font-label-md text-label-md text-on-surface font-semibold">{label}</label>
      {children}
      {hint ? <p className="font-body-sm text-body-sm text-outline">{hint}</p> : null}
    </div>
  )
}

function SubHeading({ children, action }) {
  return (
    <div className="flex items-center justify-between pt-space-md">
      <h3 className="font-label-sm text-label-sm text-outline uppercase tracking-wider font-semibold">{children}</h3>
      {action}
    </div>
  )
}

function Settings() {
  const { theme, setTheme } = useTheme()
  const { settings, update, reset: resetSettings } = useSettings()
  const [active, setActive] = useState('profile')
  const [saved, setSaved] = useState(false)

  const { profile, appearance, security, workspace, sla, data, notifications, integrations } = settings

  const save = () => {
    setSaved(true)
    setTimeout(() => setSaved(false), 2200)
  }

  const reset = () => {
    setTheme('system')
    resetSettings()
  }

  const connectedCount = Object.values(integrations).filter(Boolean).length
  const currentSection = settingsSections.find((section) => section.key === active)

  return (
    <>
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-space-sm pt-4 pb-space-md">
        <div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight">Settings</h1>
          <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">
            Changes apply across HelpDesk Pro instantly and are saved to this device.
          </p>
        </div>
        <div className="flex items-center gap-space-sm">
          {saved ? (
            <Badge dot tone="success">
              Saved
            </Badge>
          ) : null}
          <Button onClick={reset} variant="soft">
            Reset
          </Button>
          <Button icon="save" onClick={save} variant="primary">
            Save changes
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <nav className="lg:col-span-3 flex flex-col gap-0.5 lg:sticky lg:top-20 stagger">
          {settingsSections.map((section) => {
            const isActive = section.key === active
            return (
              <button
                className={`flex items-start gap-space-sm px-space-sm py-2 rounded-xl text-left transition-colors ${
                  isActive
                    ? 'bg-primary-container text-on-primary-container'
                    : 'text-on-surface-variant hover:bg-surface-container'
                }`}
                key={section.key}
                onClick={() => setActive(section.key)}
                type="button"
              >
                <Icon name={section.icon} size={18} />
                <span className="flex flex-col">
                  <span className="font-label-md text-label-md font-semibold">{section.label}</span>
                  <span className={`font-body-sm text-body-sm ${isActive ? 'text-on-primary-container/80' : 'text-on-surface-variant'}`}>
                    {section.description}
                  </span>
                </span>
              </button>
            )
          })}
        </nav>

        <div className="lg:col-span-9 flex flex-col gap-8">
          {active === 'profile' ? (
            <SettingsSection
              description="Shown to technicians and colleagues across the workspace."
              icon="person"
              title="Profile"
            >
              <SettingsRow description="Upload a photo or let us generate an avatar from your initials." title="Avatar">
                <div className="flex items-center gap-space-sm">
                  <Avatar name={profile.name} size="lg" />
                  <Button size="sm" variant="soft">
                    Upload
                  </Button>
                  <Button size="sm" variant="ghost">
                    Remove
                  </Button>
                </div>
              </SettingsRow>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-space-md py-space-md">
                <Labeled label="Full name">
                  <TextField onChange={(e) => update('profile', { name: e.target.value })} placeholder="Your full name" value={profile.name} />
                </Labeled>
                <Labeled label="Email address">
                  <TextField onChange={(e) => update('profile', { email: e.target.value })} placeholder="you@company.com" type="email" value={profile.email} />
                </Labeled>
                <Labeled label="Job title">
                  <TextField onChange={(e) => update('profile', { title: e.target.value })} placeholder="e.g. Marketing Director" value={profile.title} />
                </Labeled>
                <Labeled label="Department">
                  <TextField onChange={(e) => update('profile', { department: e.target.value })} placeholder="e.g. Marketing" value={profile.department} />
                </Labeled>
                <Labeled label="Time zone">
                  <Select onChange={(e) => update('profile', { timezone: e.target.value })} options={timezoneOptions} value={profile.timezone} />
                </Labeled>
                <Labeled label="Language">
                  <Select onChange={(e) => update('profile', { language: e.target.value })} options={languageOptions} value={profile.language} />
                </Labeled>
              </div>
            </SettingsSection>
          ) : null}

          {active === 'appearance' ? (
            <SettingsSection description="Customize how HelpDesk Pro looks and feels on this device." icon="palette" title="Appearance">
              <SettingsRow description="Choose a light, dark, or system-matched theme." title="Theme">
                <SegmentedControl onChange={setTheme} options={themeOptions} value={theme} />
              </SettingsRow>
              <SettingsRow description="Adjust the spacing of tables, lists, and cards." title="Density">
                <SegmentedControl onChange={(density) => update('appearance', { density })} options={densityOptions} value={appearance.density} />
              </SettingsRow>
              <SettingsRow description="How much room the main navigation rail takes up." title="Navigation rail">
                <SegmentedControl onChange={(sidebar) => update('appearance', { sidebar })} options={sidebarOptions} value={appearance.sidebar} />
              </SettingsRow>
              <SettingsRow description="Reduce animations and transitions across the interface." title="Reduce motion">
                <Toggle checked={appearance.reduceMotion} onChange={(v) => update('appearance', { reduceMotion: v })} />
              </SettingsRow>
              <SettingsRow description="Show keyboard shortcut hints in the header and search fields." title="Keyboard hint labels">
                <Toggle checked={appearance.tips} onChange={(v) => update('appearance', { tips: v })} />
              </SettingsRow>
            </SettingsSection>
          ) : null}

          {active === 'notifications' ? (
            <SettingsSection description="Decide what you get notified about and where." icon="notifications" title="Notifications">
              {notificationPrefs.map((pref) => (
                <SettingsRow description={pref.description} key={pref.key} title={pref.label}>
                  <Toggle
                    checked={notifications[pref.key]}
                    onChange={(v) => update('notifications', { [pref.key]: v })}
                  />
                </SettingsRow>
              ))}
            </SettingsSection>
          ) : null}

          {active === 'security' ? (
            <SettingsSection description="Keep your account and workspace secure." icon="shield" title="Security">
              <SettingsRow description="Use at least 12 characters with a mix of letters, numbers, and symbols." title="Password">
                <Button icon="key" variant="soft">
                  Change password
                </Button>
              </SettingsRow>
              <SettingsRow description="Add a hardware key or authenticator app for extra protection." title="Two-factor authentication">
                <div className="flex items-center gap-space-sm">
                  <Badge dot tone="warning">
                    Not enabled
                  </Badge>
                  <Button size="sm" variant="primary">
                    Enable
                  </Button>
                </div>
              </SettingsRow>
              <SettingsRow description="Email me whenever a new device signs in to my account." title="Login alerts">
                <Toggle checked={security.loginAlerts} onChange={(v) => update('security', { loginAlerts: v })} />
              </SettingsRow>

              <SubHeading>Active sessions</SubHeading>
              {activeSessions.length === 0 ? (
                <EmptyState
                  compact
                  description="Devices currently signed in to your account will appear here."
                  icon="devices"
                  title="No other active sessions"
                />
              ) : null}

              <SubHeading
                action={
                  <Button icon="add" size="sm" variant="soft">
                    Generate token
                  </Button>
                }
              >
                API tokens
              </SubHeading>
              {apiTokens.length === 0 ? (
                <EmptyState
                  compact
                  description="Create a personal token to authenticate the HelpDesk Pro API."
                  icon="vpn_key"
                  title="No API tokens"
                />
              ) : null}
            </SettingsSection>
          ) : null}

          {active === 'workspace' ? (
            <SettingsSection description="Configure your shared workspace and team defaults." icon="workspaces" title="Workspace">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-space-md py-space-md">
                <Labeled label="Workspace name">
                  <TextField onChange={(e) => update('workspace', { name: e.target.value })} value={workspace.name} />
                </Labeled>
                <Labeled hint="Used in URLs and API references." label="Workspace URL">
                  <TextField onChange={(e) => update('workspace', { slug: e.target.value })} value={workspace.slug} />
                </Labeled>
                <Labeled label="Default landing page">
                  <Select onChange={(e) => update('workspace', { landing: e.target.value })} options={landingOptions} value={workspace.landing} />
                </Labeled>
                <Labeled label="Business hours">
                  <div className="flex items-center gap-space-sm">
                    <TextField onChange={(e) => update('workspace', { hoursStart: e.target.value })} type="time" value={workspace.hoursStart} />
                    <span className="text-outline">to</span>
                    <TextField onChange={(e) => update('workspace', { hoursEnd: e.target.value })} type="time" value={workspace.hoursEnd} />
                  </div>
                </Labeled>
              </div>

              <SubHeading
                action={
                  <Button icon="person_add" size="sm" variant="soft">
                    Invite member
                  </Button>
                }
              >
                Team members ({teamMembers.length})
              </SubHeading>
              {teamMembers.length === 0 ? (
                <EmptyState
                  compact
                  description="Invite colleagues to collaborate on the ticket queue."
                  icon="group"
                  title="No teammates yet"
                />
              ) : null}
            </SettingsSection>
          ) : null}

          {active === 'sla' ? (
            <SettingsSection description="Set service-level targets and how tickets get routed." icon="rule" title="SLA & Routing">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-space-md py-space-md">
                <Labeled hint="Target time to first human response. Used on the ticket intake form." label="Default first response">
                  <Select onChange={(e) => update('sla', { firstResponse: e.target.value })} options={responseTargetOptions} value={sla.firstResponse} />
                </Labeled>
                <Labeled hint="Target time to full resolution." label="Default resolution">
                  <Select onChange={(e) => update('sla', { resolution: e.target.value })} options={responseTargetOptions} value={sla.resolution} />
                </Labeled>
              </div>
              <SettingsRow description="Automatically assign new tickets to the best-matched technician." title="Auto-assignment">
                <Toggle checked={sla.autoAssign} onChange={(v) => update('sla', { autoAssign: v })} />
              </SettingsRow>
              <SettingsRow description="Distribute unassigned tickets evenly across the on-duty team." title="Round-robin distribution">
                <Toggle checked={sla.roundRobin} onChange={(v) => update('sla', { roundRobin: v })} />
              </SettingsRow>

              <SubHeading
                action={
                  <Button icon="add" size="sm" variant="soft">
                    Add rule
                  </Button>
                }
              >
                Escalation rules
              </SubHeading>
              {escalationRules.length === 0 ? (
                <EmptyState
                  compact
                  description="Create rules to escalate at-risk tickets to leads automatically."
                  icon="crisis_alert"
                  title="No escalation rules"
                />
              ) : null}
            </SettingsSection>
          ) : null}

          {active === 'integrations' ? (
            <SettingsSection
              actions={<Badge tone="neutral">{connectedCount} connected</Badge>}
              description="Connect HelpDesk Pro to the tools your team already uses."
              icon="extension"
              title="Integrations"
            >
              <div className="stagger grid grid-cols-1 md:grid-cols-2 gap-space-md py-space-md">
                {integrationCatalog.map((item) => {
                  const connected = integrations[item.key]
                  return (
                    <Card className="flex flex-col gap-space-sm" key={item.key} padding="md" radius="lg">
                      <div className="flex items-start justify-between gap-space-sm">
                        <div className="flex items-center gap-space-sm">
                          <IconBadge icon={item.icon} radius="lg" size="sm" tone="muted" />
                          <div>
                            <div className="font-label-md text-label-md text-on-surface font-semibold">{item.name}</div>
                            {connected ? (
                              <Badge dot tone="success" className="mt-0.5">
                                Connected
                              </Badge>
                            ) : null}
                          </div>
                        </div>
                        <Toggle checked={connected} onChange={(v) => update('integrations', { [item.key]: v })} />
                      </div>
                      <p className="font-body-sm text-body-sm text-on-surface-variant">{item.description}</p>
                    </Card>
                  )
                })}
              </div>
            </SettingsSection>
          ) : null}

          {active === 'data' ? (
            <>
              <SettingsSection description="Control your data, exports, and retention." icon="database" title="Data & Privacy">
                <SettingsRow description="Download a full archive of tickets, users, and knowledge articles." title="Export workspace data">
                  <Button icon="download" variant="soft">
                    Export
                  </Button>
                </SettingsRow>
                <SettingsRow description="How long closed tickets are kept before permanent deletion." title="Data retention">
                  <Select className="w-48" onChange={(e) => update('data', { retention: e.target.value })} options={retentionOptions} value={data.retention} />
                </SettingsRow>
                <SettingsRow description="Review every administrative action taken in this workspace." title="Audit log">
                  <Button as={Link} icon="history" to="/audit-logs" variant="soft">
                    View audit log
                  </Button>
                </SettingsRow>
              </SettingsSection>

              <Card className="border border-error-container" padding="lg">
                <div className="flex items-start gap-space-sm pb-space-sm mb-space-sm border-b border-error-container/60">
                  <IconBadge icon="warning" radius="lg" size="sm" tone="danger" />
                  <div>
                    <h2 className="font-headline-md text-headline-md text-error">Danger zone</h2>
                    <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">
                      These actions are irreversible. Please proceed with caution.
                    </p>
                  </div>
                </div>
                <SettingsRow
                  description="Permanently delete this workspace along with all tickets, assets, and knowledge articles."
                  title="Delete workspace"
                >
                  <Button icon="delete_forever" variant="destructive">
                    Delete workspace
                  </Button>
                </SettingsRow>
              </Card>
            </>
          ) : null}

          <p className="font-body-sm text-body-sm text-outline text-center">
            {currentSection ? `Editing: ${currentSection.label}` : null}
          </p>
        </div>
      </div>
    </>
  )
}

export default Settings
