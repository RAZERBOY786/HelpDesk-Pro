import { Link } from 'react-router-dom'
import { Badge, Button, Card, EmptyState, Icon, IconBadge, SearchInput, SectionHeader } from '../components/ui.jsx'
import {
  assignedAssets,
  maintenanceNotices,
  myTickets,
  quickSearchChips,
  selfHelpRunbooks,
} from '../data/dashboard.js'
import { useSettings } from '../settings/context.js'

function RunbookCard({ runbook }) {
  return (
    <Card padding="lg" className="flex flex-col gap-space-sm">
      <div className="flex items-start justify-between gap-space-sm">
        <div className="flex items-center gap-space-xs">
          <span className="h-7 w-7 rounded-lg bg-primary-fixed text-on-primary-fixed-variant flex items-center justify-center text-sm font-bold">
            {runbook.step}
          </span>
          <div>
            <h3 className="font-headline-md text-headline-md text-on-surface font-semibold">{runbook.title}</h3>
            <span className="font-body-sm text-body-sm text-outline">{runbook.meta}</span>
          </div>
        </div>
        <Badge tone="success" pill className="shrink-0">
          {runbook.solved} Solved
        </Badge>
      </div>
      <div className="bg-surface-container-low rounded-lg p-space-sm font-body-sm text-body-sm space-y-1.5 text-on-surface-variant">
        {runbook.steps.map((step, i) => (
          <p className="flex items-center gap-2" key={i}>
            <Icon className="text-tertiary" name="check" size={16} />
            <span>{step}</span>
          </p>
        ))}
      </div>
      <div className="flex items-center justify-between pt-space-xs">
        <span className="font-body-sm text-body-sm text-outline">Did this solve your problem?</span>
        <div className="flex items-center gap-2">
          <Button icon="thumb_up" iconSize={15} size="sm" variant="soft">
            Yes
          </Button>
          <Button as={Link} icon="thumb_down" iconSize={15} size="sm" to="/submit" variant="soft">
            Still stuck
          </Button>
        </div>
      </div>
    </Card>
  )
}

function Dashboard() {
  const { settings } = useSettings()
  const firstName = settings.profile.name.trim().split(/\s+/)[0]
  const greeting = firstName ? `Good morning, ${firstName}` : 'Good morning'

  return (
    <>
      {maintenanceNotices.length > 0 ? (
        <div className="mb-space-lg">
          {maintenanceNotices.map((notice, i) => (
            <div
              className="relative overflow-hidden rounded-xl bg-surface-container-high px-space-md py-space-sm shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-space-sm"
              key={i}
            >
              <div className="flex items-center gap-space-sm min-w-0">
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-surface-container-lowest text-primary shadow-sm">
                  <Icon name="info" size={20} />
                </span>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-space-xs flex-wrap">
                    <Badge tone="primary" className="uppercase">
                      {notice.label}
                    </Badge>
                    <span className="font-headline-sm text-headline-sm text-on-surface truncate">{notice.title}</span>
                  </div>
                  <p className="font-body-sm text-body-sm text-on-surface-variant truncate">{notice.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : null}

      <section className="grid grid-cols-1 lg:grid-cols-12 gap-space-md mb-space-xl">
        <div className="lg:col-span-7 flex flex-col justify-between rounded-xl bg-surface-container-lowest p-space-lg shadow-sm">
          <div>
            <div className="flex items-center justify-between mb-space-xs">
              <div className="flex items-center gap-2">
                <span className="font-code-sm text-code-sm uppercase tracking-wider text-outline">
                  Employee Self-Service Desk
                </span>
                <span className="h-1.5 w-1.5 rounded-full bg-tertiary"></span>
                <span className="font-label-sm text-label-sm text-tertiary">All Services Operational</span>
              </div>
              <Badge tone="neutral" pill>
                Tier-0 FastPath
              </Badge>
            </div>
            <h1 className="font-headline-xl text-headline-xl text-on-surface tracking-tight mb-1">{greeting}</h1>
            <p className="font-body-lg text-body-lg text-on-surface-variant mb-space-lg max-w-xl">
              Resolve workplace tech issues autonomously or request equipment approvals and IT service support.
            </p>
            <div className="relative w-full mb-space-md">
              <SearchInput placeholder="Search Wi-Fi config, VPN certificates, badge replacement, software licenses..." size="lg" />
              {quickSearchChips.length > 0 ? (
                <div className="flex items-center gap-1.5 mt-space-xs flex-wrap font-body-sm text-body-sm">
                  <span className="font-label-sm text-label-sm text-outline">Common:</span>
                  {quickSearchChips.map((chip) => (
                    <button
                      className="px-2 py-0.5 rounded bg-surface-container hover:bg-surface-container-high text-on-surface transition-colors"
                      key={chip}
                    >
                      {chip}
                    </button>
                  ))}
                </div>
              ) : null}
            </div>
          </div>
        </div>

        <div className="lg:col-span-5 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 gap-space-md">
          <Link
            className="relative overflow-hidden rounded-xl bg-primary-container text-on-primary-container p-space-lg shadow-md flex flex-col justify-between group hover:shadow-xl transition-all"
            to="/submit"
          >
            <div className="absolute -right-8 -top-8 w-36 h-36 rounded-full bg-white/10 blur-xl pointer-events-none group-hover:scale-125 transition-transform duration-500"></div>
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-space-md">
                <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/15 backdrop-blur-md shadow-sm">
                  <Icon className="text-on-primary" name="add_circle" size={26} />
                </span>
                <Badge tone="info" pill className="uppercase">
                  Avg 14m Triage
                </Badge>
              </div>
              <h2 className="font-headline-lg text-headline-lg text-on-primary font-semibold mb-1">Report an Incident</h2>
              <p className="font-body-sm text-body-sm text-on-primary/80 max-w-xs">
                Hardware failures, broken connectivity, system permissions, or urgent conference room bugs.
              </p>
            </div>
            <div className="relative z-10 pt-space-md flex items-center justify-between">
              <span className="font-label-md text-label-md font-semibold text-on-primary flex items-center gap-1">
                Open Guided Ticket Form
                <Icon className="group-hover:translate-x-1 transition-transform" name="arrow_forward" size={18} />
              </span>
              <span className="font-code-sm text-code-sm text-on-primary/70">⌘+N</span>
            </div>
          </Link>
          <Link
            className="rounded-xl bg-surface-container-lowest p-space-lg shadow-sm flex flex-col justify-between group hover:bg-surface-container-low transition-all"
            to="/knowledge-base"
          >
            <div>
              <div className="flex items-center justify-between mb-space-md">
                <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-surface-container text-primary">
                  <Icon name="menu_book" size={26} />
                </span>
                <Badge tone="muted" className="uppercase">
                  420+ Guides
                </Badge>
              </div>
              <h2 className="font-headline-lg text-headline-lg text-on-surface font-semibold mb-1">
                Knowledge Base &amp; Catalog
              </h2>
              <p className="font-body-sm text-body-sm text-on-surface-variant max-w-xs">
                Self-service onboarding wikis, automated software downloads, and IT peripherals requisitions.
              </p>
            </div>
            <div className="pt-space-md flex items-center justify-between text-primary">
              <span className="font-label-md text-label-md font-semibold flex items-center gap-1">
                Browse All Documentation
                <Icon className="group-hover:translate-x-1 transition-transform" name="arrow_forward" size={18} />
              </span>
              <Icon className="text-outline" name="library_books" size={20} />
            </div>
          </Link>
        </div>
      </section>

      <section className="mb-space-xl">
        <SectionHeader
          title="My Active Requests & Issues"
          subtitle="Real-time status updates and resolution progress for tickets created by you"
          actions={
            <>
              <Button icon="filter_list" variant="soft">
                Filter Status
              </Button>
              <Button icon="history" variant="softHigh">
                View All History
              </Button>
            </>
          }
        />
        <div className="stagger grid grid-cols-1 sm:grid-cols-3 gap-space-md mb-space-md">
          <Card className="flex items-center justify-between">
            <div className="flex items-center gap-space-sm">
              <IconBadge icon="pending_actions" tone="primary" />
              <div>
                <div className="font-headline-md text-headline-md text-on-surface">{myTickets.length} Active</div>
                <div className="font-body-sm text-body-sm text-on-surface-variant">Assigned &amp; In Progress</div>
              </div>
            </div>
          </Card>
          <Card className="flex items-center justify-between">
            <div className="flex items-center gap-space-sm">
              <IconBadge icon="how_to_reg" tone="info" />
              <div>
                <div className="font-headline-md text-headline-md text-on-surface">0 Pending</div>
                <div className="font-body-sm text-body-sm text-on-surface-variant">Manager Authorization</div>
              </div>
            </div>
          </Card>
          <Card className="flex items-center justify-between">
            <div className="flex items-center gap-space-sm">
              <IconBadge icon="task_alt" tone="success" />
              <div>
                <div className="font-headline-md text-headline-md text-on-surface">0 Resolved</div>
                <div className="font-body-sm text-body-sm text-on-surface-variant">Closed This Quarter</div>
              </div>
            </div>
          </Card>
        </div>
        <Card padding="none" className="overflow-hidden">
          {myTickets.length === 0 ? (
            <EmptyState
              icon="inbox"
              title="No active requests"
              description="You don't have any open tickets right now. Create one and it will appear here with live status."
              action={
                <Button as={Link} icon="add" to="/submit" variant="primary">
                  Report an Incident
                </Button>
              }
            />
          ) : (
            <div className="divide-y divide-surface-container">
              {myTickets.map((ticket) => (
                <div className="p-space-lg hover:bg-surface-container-low/40 transition-colors" key={ticket.id}>
                  <div className="flex items-start gap-space-sm">
                    <IconBadge icon={ticket.icon} tone={ticket.tone} radius="lg" />
                    <div>
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <Badge tone="muted">{ticket.id}</Badge>
                        <Badge dot tone={ticket.statusTone} pill>
                          {ticket.status}
                        </Badge>
                      </div>
                      <h3 className="font-headline-md text-headline-md text-on-surface font-semibold">{ticket.title}</h3>
                      <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">{ticket.description}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
        <div className="lg:col-span-5 flex flex-col gap-space-md stagger">
          <div className="flex items-center justify-between pb-space-xs">
            <div>
              <h2 className="font-headline-lg text-headline-lg text-on-surface">Assigned Assets</h2>
              <p className="font-body-sm text-body-sm text-on-surface-variant">Active corporate devices checked out to you</p>
            </div>
            <Badge tone="muted" pill>
              {assignedAssets.length} Items
            </Badge>
          </div>
          {assignedAssets.length === 0 ? (
            <Card padding="none">
              <EmptyState
                compact
                icon="devices"
                title="No assets assigned"
                description="Devices checked out to you will show up here with serial numbers and MDM status."
              />
            </Card>
          ) : (
            assignedAssets.map((asset) => (
              <Card className="flex items-center justify-between" key={asset.tag}>
                <div className="flex items-center gap-space-sm">
                  <IconBadge icon={asset.icon} tone="muted" size="lg" radius="lg" />
                  <div>
                    <h3 className="font-headline-sm text-headline-sm text-on-surface font-semibold">{asset.name}</h3>
                    <p className="font-code-sm text-code-sm text-outline">
                      Asset Tag: <span className="text-on-surface">{asset.tag}</span>
                    </p>
                  </div>
                </div>
                <Badge tone={asset.statusTone} pill>
                  {asset.status}
                </Badge>
              </Card>
            ))
          )}
        </div>

        <div className="lg:col-span-7 flex flex-col gap-space-md">
          <div className="flex items-center justify-between pb-space-xs">
            <div>
              <h2 className="font-headline-lg text-headline-lg text-on-surface">Top Self-Help Runbooks</h2>
              <p className="font-body-sm text-body-sm text-on-surface-variant">
                Instant troubleshooting guides verified by Network &amp; Security Engineering
              </p>
            </div>
            <Link className="font-label-md text-label-md text-primary hover:underline" to="/knowledge-base">
              View All Knowledge
            </Link>
          </div>
          {selfHelpRunbooks.length === 0 ? (
            <Card padding="none">
              <EmptyState
                icon="menu_book"
                title="No runbooks published yet"
                description="Self-help guides will appear here once Network & Security Engineering publishes them."
              />
            </Card>
          ) : (
            selfHelpRunbooks.map((runbook) => <RunbookCard key={runbook.step} runbook={runbook} />)
          )}
        </div>
      </section>

      <footer className="mt-space-xl p-space-md rounded-xl bg-surface-container-low flex flex-col md:flex-row items-center justify-between gap-space-md">
        <div className="flex items-center gap-space-sm">
          <div className="h-9 w-9 rounded-full bg-primary flex items-center justify-center text-on-primary">
            <Icon name="support_agent" size={20} />
          </div>
          <div>
            <p className="font-headline-sm text-headline-sm text-on-surface">Need Live Urgent Assistance?</p>
            <p className="font-body-sm text-body-sm text-on-surface-variant">
              IT Support Walk-Up Bar is open: Building B, 2nd Floor (Mon-Fri 08:00 - 18:00)
            </p>
          </div>
        </div>
        <div className="flex items-center gap-space-sm">
          <Button icon="chat" variant="outline" className="shadow-sm">
            Slack #it-helpdesk
          </Button>
          <Button icon="call" variant="primary" className="shadow-sm">
            Emergency NOC Line (Ext 4357)
          </Button>
        </div>
      </footer>
    </>
  )
}

export default Dashboard
