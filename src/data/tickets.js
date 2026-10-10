// Ticket collection. Populate from your API to render the queue.
// Each ticket: { id, priority, priorityTone, subject, subjectIcon, metaA, metaB,
//   requester: { name, role, initials, tone }, technician: { name, initials, tone } | { action },
//   category, status: { label, tone }, sla: { icon, label, tone }, updated }
export const tickets = []

export const ticketFilters = {
  tabs: [
    { key: 'all', label: 'All Tickets' },
    { key: 'unassigned', label: 'Unassigned Queue' },
    { key: 'breached', label: 'Breached / At Risk', icon: 'crisis_alert', danger: true },
    { key: 'team', label: 'My Team' },
    { key: 'resolved', label: 'Recently Resolved' },
  ],
  dropdowns: [
    { key: 'status', label: 'Status', value: 'All Statuses' },
    { key: 'priority', label: 'Priority', value: 'Any Priority' },
    { key: 'department', label: 'Dept', value: 'All Depts' },
    { key: 'assignee', label: 'Assignee', value: 'Everyone' },
  ],
  dateRange: 'Last 7 Days',
}
