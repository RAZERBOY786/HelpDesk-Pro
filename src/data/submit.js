// Configuration for the new-ticket intake flow. No requester or prefilled values.

export const impactLevels = [
  {
    value: 'single',
    icon: 'person',
    title: 'Only Me',
    description: 'Single user workstation or local peripheral issue.',
    slaLabel: 'Default SLA:',
    slaValue: '4h',
    accent: 'primary',
  },
  {
    value: 'department',
    icon: 'groups',
    title: 'Department / Team',
    description: 'Multiple colleagues or conference room floor impacted.',
    slaLabel: 'Default SLA:',
    slaValue: '1h 30m',
    accent: 'primary',
    default: true,
  },
  {
    value: 'outage',
    icon: 'bolt',
    title: 'Production Outage',
    description: 'Total service outage, revenue block, or P1 system crash.',
    slaLabel: 'P1 Incident SLA:',
    slaValue: '< 15 min',
    accent: 'error',
  },
]

export const urgencyOptions = [
  { value: 'critical', label: 'High - Blocks work completely with no alternative' },
  { value: 'moderate', label: 'Medium - Degraded functionality; workaround exists' },
  { value: 'low', label: 'Low - Minor nuisance, aesthetic flaw, or future inquiry' },
]

export const categoryOptions = [
  { value: 'network', label: 'Network & Connectivity (Wi-Fi, VPN, DNS, Switch)' },
  { value: 'hardware', label: 'Hardware & Laptop (MacBook, Peripherals, Battery)' },
  { value: 'software', label: 'Software / SaaS (Slack, Office 365, Figma, Jira)' },
  { value: 'identity', label: 'Identity & Access (Okta, Duo MFA, Vault Permissions)' },
  { value: 'facilities', label: 'Facilities (Monitors, Docking Stations, Conference AV)' },
]

// Populated from the requester's assigned assets / inventory.
export const assetOptions = []
