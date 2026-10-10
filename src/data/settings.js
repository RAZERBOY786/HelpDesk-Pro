export const settingsSections = [
  { key: 'profile', label: 'Profile', icon: 'person', description: 'Personal information and preferences' },
  { key: 'appearance', label: 'Appearance', icon: 'palette', description: 'Theme, layout and density' },
  { key: 'notifications', label: 'Notifications', icon: 'notifications', description: 'Email, desktop and alert rules' },
  { key: 'security', label: 'Security', icon: 'shield', description: 'Password, MFA and active sessions' },
  { key: 'workspace', label: 'Workspace', icon: 'workspaces', description: 'Team, business hours and defaults' },
  { key: 'sla', label: 'SLA & Routing', icon: 'rule', description: 'Response targets and auto-assignment' },
  { key: 'integrations', label: 'Integrations', icon: 'extension', description: 'Connect external tools' },
  { key: 'data', label: 'Data & Privacy', icon: 'database', description: 'Export, retention and danger zone' },
]

export const themeOptions = [
  { value: 'light', label: 'Light', icon: 'light_mode' },
  { value: 'dark', label: 'Dark', icon: 'dark_mode' },
  { value: 'system', label: 'System', icon: 'contrast' },
]

export const densityOptions = [
  { value: 'comfortable', label: 'Comfortable' },
  { value: 'compact', label: 'Compact' },
]

export const sidebarOptions = [
  { value: 'expanded', label: 'Expanded' },
  { value: 'compact', label: 'Compact' },
]

export const landingOptions = [
  { value: 'dashboard', label: 'Dashboard' },
  { value: 'all-tickets', label: 'All Tickets Queue' },
  { value: 'knowledge-base', label: 'Knowledge Base' },
  { value: 'my-tickets', label: 'My Tickets' },
]

export const timezoneOptions = [
  { value: 'utc', label: 'UTC (Coordinated Universal Time)' },
  { value: 'america_new_york', label: 'America/New York (EST/EDT)' },
  { value: 'america_los_angeles', label: 'America/Los Angeles (PST/PDT)' },
  { value: 'europe_london', label: 'Europe/London (GMT/BST)' },
  { value: 'asia_tokyo', label: 'Asia/Tokyo (JST)' },
  { value: 'asia_dhaka', label: 'Asia/Dhaka (BST)' },
]

export const languageOptions = [
  { value: 'en', label: 'English (US)' },
  { value: 'en_gb', label: 'English (UK)' },
  { value: 'fr', label: 'Francais' },
  { value: 'de', label: 'Deutsch' },
  { value: 'es', label: 'Espanol' },
]

export const responseTargetOptions = [
  { value: '15m', label: '15 minutes' },
  { value: '30m', label: '30 minutes' },
  { value: '1h', label: '1 hour' },
  { value: '4h', label: '4 hours' },
  { value: '1d', label: '1 business day' },
]

export const retentionOptions = [
  { value: '90d', label: '90 days' },
  { value: '6m', label: '6 months' },
  { value: '1y', label: '1 year' },
  { value: '3y', label: '3 years' },
  { value: 'forever', label: 'Keep indefinitely' },
]

export const notificationPrefs = [
  { key: 'email', label: 'Email notifications', description: 'Receive a copy of every ticket update by email.', default: true },
  { key: 'desktop', label: 'Desktop push', description: 'Show in-browser push notifications while you work.', default: true },
  { key: 'assigned', label: 'Ticket assigned to me', description: 'Alert me the moment a ticket is assigned to me.', default: true },
  { key: 'mentions', label: 'Mentions and comments', description: 'Notify me when I am mentioned in a ticket thread.', default: true },
  { key: 'sla', label: 'SLA breach warnings', description: 'Warn me before a ticket breaches its SLA target.', default: true },
  { key: 'digest', label: 'Weekly digest', description: 'A Monday summary of queue volume and resolution rates.', default: false },
  { key: 'product', label: 'Product announcements', description: 'Occasional emails about new HelpDesk Pro features.', default: false },
]

export const integrationCatalog = [
  { key: 'slack', name: 'Slack', icon: 'chat', description: 'Post ticket updates and alerts into channels.' },
  { key: 'okta', name: 'Okta', icon: 'passkey', description: 'Sync user directory and single sign-on.' },
  { key: 'jamf', name: 'Jamf Pro', icon: 'laptop_mac', description: 'Pull managed device inventory and MDM status.' },
  { key: 'pagerduty', name: 'PagerDuty', icon: 'crisis_alert', description: 'Escalate P1 incidents to on-call rotations.' },
  { key: 'teams', name: 'Microsoft Teams', icon: 'groups', description: 'Route approvals and notifications to Teams.' },
  { key: 'jira', name: 'Jira', icon: 'apps', description: 'Two-way sync of engineering escalations.' },
]

// Populated from your backend.
export const teamMembers = []
export const activeSessions = []
export const apiTokens = []
export const escalationRules = []
export const connectedIntegrations = []
