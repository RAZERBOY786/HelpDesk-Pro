export const navGroups = [
  {
    label: 'Workspace',
    items: [
      { label: 'Dashboard', icon: 'dashboard', to: '/dashboard' },
      { label: 'Ticket Workspace', icon: 'confirmation_number', to: '/ticket-workspace' },
      { label: 'All Tickets Queue', icon: 'inbox', to: '/all-tickets' },
    ],
  },
  {
    label: 'Management',
    items: [
      { label: 'Analytics & SLAs', icon: 'monitoring', to: '/analytics' },
      { label: 'Asset Inventory', icon: 'devices', to: '/assets' },
      { label: 'User Directory', icon: 'badge', to: '/users' },
    ],
  },
  {
    label: 'Self-Service',
    items: [
      { label: 'Knowledge Base', icon: 'menu_book', to: '/knowledge-base' },
      { label: 'My Tickets', icon: 'assignment_ind', to: '/my-tickets' },
      { label: 'Submit Issue', icon: 'post_add', to: '/submit' },
    ],
  },
  {
    label: 'System',
    items: [
      { label: 'SLA Policies', icon: 'rule', to: '/sla-policies' },
      { label: 'Audit Logs', icon: 'history', to: '/audit-logs' },
      { label: 'Settings', icon: 'settings', to: '/settings' },
    ],
  },
]

export const workspaces = ['Tech', 'Admin', 'Employee']
