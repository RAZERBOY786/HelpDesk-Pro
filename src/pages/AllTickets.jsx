import { useEffect, useRef, useState } from 'react'
import { Badge, Button, EmptyState, Icon, SearchInput } from '../components/ui.jsx'
import { ticketFilters, tickets } from '../data/tickets.js'

function Requester({ requester }) {
  const badge = requester.icon ? (
    <span className="w-6 h-6 shrink-0 rounded-full bg-surface-container-high flex items-center justify-center text-outline">
      <Icon name={requester.icon} size={14} />
    </span>
  ) : (
    <span className="w-6 h-6 shrink-0 rounded-full bg-primary-fixed text-on-primary-fixed-variant font-code-sm text-[10px] flex items-center justify-center font-bold">
      {requester.initials}
    </span>
  )
  return (
    <div className="flex items-center gap-2">
      {badge}
      <div className="flex flex-col leading-tight min-w-0">
        <span className="font-label-md text-label-md font-medium truncate text-on-surface">{requester.name}</span>
        <span className="font-body-sm text-body-sm text-on-surface-variant truncate">{requester.role}</span>
      </div>
    </div>
  )
}

function Technician({ technician }) {
  if (technician.action) {
    return (
      <Button
        className="font-semibold"
        icon="person_add"
        iconSize={14}
        size="sm"
        variant={technician.action === 'claim' ? 'destructive' : 'primary'}
      >
        {technician.action === 'claim' ? 'Claim Incident' : 'Assign'}
      </Button>
    )
  }
  return (
    <div className="flex items-center gap-2">
      <span className="w-6 h-6 shrink-0 rounded-full bg-secondary-fixed text-on-secondary-fixed-variant font-code-sm text-[10px] flex items-center justify-center font-bold">
        {technician.initials}
      </span>
      <span className="font-body-md text-body-md text-on-surface truncate">{technician.name}</span>
    </div>
  )
}

function AllTickets() {
  const [selected, setSelected] = useState([])
  const [activeTab, setActiveTab] = useState(ticketFilters.tabs[0].key)
  const [query, setQuery] = useState('')
  const headerRef = useRef(null)
  const allChecked = tickets.length > 0 && selected.length === tickets.length

  useEffect(() => {
    if (headerRef.current) {
      headerRef.current.indeterminate = selected.length > 0 && selected.length < tickets.length
    }
  }, [selected])

  const toggleRow = (id) => {
    setSelected((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]))
  }

  const stats = [
    { label: 'Total Queue', value: tickets.length, className: 'bg-surface-container-lowest', valueClass: 'text-on-surface' },
    { label: 'Unassigned', value: tickets.length, className: 'bg-secondary-container/50', valueClass: 'text-primary' },
    { label: 'At Risk / Breached', value: 0, className: 'bg-error-container/60', valueClass: 'text-error', danger: true },
  ]

  return (
    <>
      <div className="flex flex-col gap-space-md mb-space-lg">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-space-md">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight">All Tickets Queue</h1>
              <Badge tone="neutral" pill className="font-code-sm">
                <span className="w-1.5 h-1.5 rounded-full bg-tertiary"></span>
                Live Sync
              </Badge>
            </div>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">
              Central service desk dispatch, incident triage, and automated SLA compliance tracker
            </p>
          </div>
          <div className="stagger flex items-center gap-2 flex-wrap">
            {stats.map((stat) => (
              <div className={`flex items-center gap-2 px-space-md py-1.5 rounded-xl shadow-sm ${stat.className}`} key={stat.label}>
                {stat.danger ? (
                  <span className="flex h-2 w-2 relative">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-error opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-error"></span>
                  </span>
                ) : null}
                <span className="font-label-sm text-label-sm uppercase text-on-surface-variant">{stat.label}</span>
                <span className={`font-code-sm text-headline-sm font-semibold ${stat.valueClass}`}>{stat.value}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="flex items-center justify-between bg-surface-container-low p-1 rounded-xl">
          <div className="flex items-center gap-1 overflow-x-auto">
            {ticketFilters.tabs.map((tab) => {
              const active = activeTab === tab.key
              return (
                <button
                  className={
                    'px-space-md py-1.5 rounded-lg font-label-md text-label-md transition-all flex items-center gap-1.5 ' +
                    (active
                      ? 'bg-surface-container-lowest text-on-surface shadow-sm'
                      : tab.danger
                        ? 'text-error hover:bg-error-container/40'
                        : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-container-lowest/50')
                  }
                  key={tab.key}
                  onClick={() => setActiveTab(tab.key)}
                >
                  {tab.icon ? <Icon name={tab.icon} size={16} /> : null}
                  <span>{tab.label}</span>
                </button>
              )
            })}
          </div>
          <div className="hidden md:flex items-center gap-1 pr-1">
            <Button icon="view_column" size="icon-sm" title="Table View Settings" variant="ghost" />
            <Button icon="refresh" size="icon-sm" title="Refresh Feed" variant="ghost" />
          </div>
        </div>
      </div>

      <div className="bg-surface-container-lowest rounded-xl p-space-md shadow-sm mb-space-md flex flex-col gap-space-sm">
        <div className="flex flex-col xl:flex-row items-stretch xl:items-center justify-between gap-space-sm">
          <SearchInput
            className="flex-1 max-w-2xl"
            onChange={(e) => setQuery(e.target.value)}
            onClear={() => setQuery('')}
            placeholder="Filter by Ticket ID (HD-...), Requester, Hostname, Asset Tag, or Issue Summary..."
            size="toolbar"
            value={query}
          />
          <div className="flex items-center gap-2 flex-wrap">
            <Button icon="rule_settings" trailingIcon="expand_more" variant="softHigh">
              Bulk Actions
            </Button>
            <Button icon="file_download" variant="soft">
              Export CSV
            </Button>
            <Button icon="add_circle" variant="primary" className="shadow-sm">
              New Incident
            </Button>
          </div>
        </div>
        <div className="flex items-center gap-2 flex-wrap pt-2">
          {ticketFilters.dropdowns.map((filter) => (
            <button
              className="flex items-center gap-1 bg-surface-container-low px-2.5 py-1 rounded-lg text-on-surface-variant hover:text-on-surface cursor-pointer"
              key={filter.key}
            >
              <span className="font-label-sm text-label-sm uppercase text-outline">{filter.label}:</span>
              <span className="font-label-md text-label-md text-on-surface font-medium">{filter.value}</span>
              <Icon className="text-outline" name="expand_more" size={16} />
            </button>
          ))}
          <button className="flex items-center gap-1 bg-surface-container-low px-2.5 py-1 rounded-lg text-on-surface-variant hover:text-on-surface cursor-pointer">
            <Icon className="text-outline" name="calendar_today" size={16} />
            <span className="font-label-md text-label-md text-on-surface font-medium">{ticketFilters.dateRange}</span>
            <Icon className="text-outline" name="expand_more" size={16} />
          </button>
          <Button className="ml-auto" icon="filter_alt_off" iconSize={14} size="sm" variant="link">
            Reset Filters
          </Button>
        </div>
      </div>

      <div className="bg-surface-container-lowest rounded-xl shadow-sm overflow-hidden flex flex-col">
        {selected.length > 0 ? (
          <div className="bg-primary-fixed text-on-primary-fixed-variant px-space-lg py-2 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Icon name="check_circle" size={18} />
              <span className="font-label-md text-label-md font-semibold">
                {selected.length} tickets selected across view
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Button size="sm" variant="outline">
                Assign Technician
              </Button>
              <Button size="sm" variant="outline">
                Change Priority
              </Button>
              <Button size="sm" variant="outline" className="text-error">
                Resolve / Close
              </Button>
              <Button onClick={() => setSelected([])} size="sm" variant="link" className="text-on-primary-fixed-variant">
                Clear
              </Button>
            </div>
          </div>
        ) : null}

        <div className="overflow-x-auto w-full">
          <table className="w-full text-left border-collapse select-none">
            <thead>
              <tr className="bg-surface-container-low text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider h-10">
                <th className="w-10 px-3 text-center">
                  <input
                    checked={allChecked}
                    className="rounded w-4 h-4 accent-primary cursor-pointer"
                    disabled={tickets.length === 0}
                    onChange={(e) => setSelected(e.target.checked ? tickets.map((t) => t.id) : [])}
                    ref={headerRef}
                    type="checkbox"
                  />
                </th>
                <th className="px-3 min-w-[130px]">Ticket ID &amp; Priority</th>
                <th className="px-3 min-w-[340px]">Subject &amp; Details</th>
                <th className="px-3 min-w-[170px]">Requester</th>
                <th className="px-3 min-w-[160px]">Technician</th>
                <th className="px-3 min-w-[120px]">Category</th>
                <th className="px-3 min-w-[110px]">Status</th>
                <th className="px-3 min-w-[130px]">SLA Remaining</th>
                <th className="px-3 min-w-[110px] text-right pr-4">Updated</th>
              </tr>
            </thead>
            <tbody className="stagger-fade divide-y divide-surface-container text-on-surface">
              {tickets.length === 0 ? (
                <tr>
                  <td colSpan={9}>
                    <EmptyState
                      icon="inbox"
                      title="No tickets in this view"
                      description="There are no tickets matching the current filters. New incidents will appear here in real time."
                      action={
                        <Button icon="add_circle" variant="primary">
                          New Incident
                        </Button>
                      }
                    />
                  </td>
                </tr>
              ) : (
                tickets.map((ticket) => (
                  <tr className="hover:bg-surface-container-low/60 transition-colors cursor-pointer" key={ticket.id}>
                    <td className="w-10 px-3 py-2.5 text-center">
                      <input
                        checked={selected.includes(ticket.id)}
                        className="rounded w-4 h-4 accent-primary cursor-pointer"
                        onChange={() => toggleRow(ticket.id)}
                        type="checkbox"
                      />
                    </td>
                    <td className="px-3 py-2.5">
                      <div className="flex items-center gap-1.5">
                        <span className="font-code-sm text-code-sm font-semibold text-primary">{ticket.id}</span>
                        <Badge tone={ticket.priorityTone}>{ticket.priority}</Badge>
                      </div>
                    </td>
                    <td className="px-3 py-2.5">
                      <span className="font-body-md font-semibold transition-colors truncate max-w-lg flex items-center gap-1.5 text-on-surface hover:text-primary">
                        <Icon name={ticket.subjectIcon} size={16} />
                        {ticket.subject}
                      </span>
                      <div className="flex items-center gap-2 text-on-surface-variant font-body-sm text-body-sm mt-0.5">
                        <span className="flex items-center gap-0.5">
                          <Icon name={ticket.subjectIcon} size={13} /> {ticket.metaA}
                        </span>
                        <span>-</span>
                        <span>{ticket.metaB}</span>
                      </div>
                    </td>
                    <td className="px-3 py-2.5">
                      <Requester requester={ticket.requester} />
                    </td>
                    <td className="px-3 py-2.5">
                      <Technician technician={ticket.technician} />
                    </td>
                    <td className="px-3 py-2.5">
                      <Badge tone="neutral">{ticket.category}</Badge>
                    </td>
                    <td className="px-3 py-2.5">
                      <Badge dot pill tone={ticket.status.tone}>
                        {ticket.status.label}
                      </Badge>
                    </td>
                    <td className="px-3 py-2.5">
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded font-code-sm text-code-sm text-on-surface-variant">
                        <Icon name={ticket.sla.icon} size={14} />
                        {ticket.sla.label}
                      </span>
                    </td>
                    <td className="px-3 py-2.5 text-right pr-4 font-code-sm text-code-sm text-on-surface-variant">
                      {ticket.updated}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        <div className="bg-surface-container-low px-space-md py-3 flex flex-col sm:flex-row items-center justify-between gap-space-sm select-none">
          <div className="flex items-center gap-4 text-on-surface-variant font-body-sm text-body-sm">
            <span>
              Showing <strong className="text-on-surface font-semibold font-code-sm">0</strong> of{' '}
              <strong className="text-on-surface font-semibold font-code-sm">{tickets.length}</strong> incidents
            </span>
            <div className="flex items-center gap-1.5">
              <span className="font-label-sm text-label-sm uppercase">Rows per page:</span>
              <select className="bg-surface-container-lowest text-on-surface font-code-sm text-code-sm rounded px-2 py-1 focus:outline-none cursor-pointer">
                <option>10</option>
                <option>25</option>
                <option>50</option>
                <option>100</option>
              </select>
            </div>
          </div>
          <div className="flex items-center gap-1">
            <Button disabled icon="first_page" size="icon-sm" variant="ghost" />
            <Button disabled icon="chevron_left" size="icon-sm" variant="ghost" />
            <button className="w-7 h-7 rounded-lg bg-primary text-on-primary font-code-sm text-code-sm font-bold flex items-center justify-center shadow-sm">
              1
            </button>
            <Button disabled icon="chevron_right" size="icon-sm" variant="ghost" />
            <Button disabled icon="last_page" size="icon-sm" variant="ghost" />
          </div>
        </div>
      </div>
    </>
  )
}

export default AllTickets
