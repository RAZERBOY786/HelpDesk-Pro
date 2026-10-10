import { useState } from 'react'
import { Badge, Button, Card, EmptyState, Icon, IconBadge, ProgressBar, SearchInput } from '../components/ui.jsx'
import {
  deflectionMetrics,
  knowledgeArticles,
  knowledgeDomains,
  knowledgeStats,
  maintenanceNotice,
  popularSearches,
  selfHealingScripts,
} from '../data/knowledge.js'

function KnowledgeBase() {
  const [query, setQuery] = useState('')
  const [generating, setGenerating] = useState(false)

  const generate = () => {
    setGenerating(true)
    setTimeout(() => setGenerating(false), 1200)
  }

  return (
    <>
      {maintenanceNotice ? (
        <div className="w-full flex items-center justify-between px-space-md py-1.5 rounded-xl bg-surface-container-low text-on-surface mb-space-md">
          <div className="flex items-center gap-space-sm min-w-0">
            <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-tertiary-container text-on-tertiary-container">
              <Icon name="verified" size={14} />
            </span>
            <span className="font-label-sm text-label-sm text-on-surface font-semibold truncate">
              {maintenanceNotice.label}
            </span>
            <span className="font-body-sm text-body-sm text-on-surface-variant truncate">
              {maintenanceNotice.description}
            </span>
          </div>
        </div>
      ) : null}

      <section className="relative w-full rounded-2xl bg-surface-container-lowest shadow-sm p-space-xl mb-space-xl overflow-hidden">
        <div className="absolute -right-16 -top-24 w-96 h-96 rounded-full bg-primary-fixed/30 blur-3xl pointer-events-none"></div>
        <div className="absolute right-48 -bottom-20 w-80 h-80 rounded-full bg-secondary-fixed/40 blur-3xl pointer-events-none"></div>
        <div className="relative z-10 max-w-4xl mx-auto flex flex-col items-center text-center">
          <Badge tone="primary" pill className="uppercase tracking-wider mb-space-sm gap-1.5">
            <Icon name="terminal" size={15} />
            Self-Service Engine &amp; Runbooks
          </Badge>
          <h1 className="font-headline-xl text-headline-xl text-on-surface mb-space-xs font-semibold tracking-tight">
            Enterprise Knowledge Base &amp; Self-Help Hub
          </h1>
          <p className="font-body-lg text-body-lg text-on-surface-variant max-w-2xl mb-space-lg">
            Instant, verified operational runbooks, resolution workflows, and auto-remediation scripts maintained by IT
            Operations.
          </p>
          <div className="w-full relative shadow-md rounded-2xl bg-surface-container-low focus-within:bg-surface-container-lowest focus-within:shadow-lg transition-all">
            <div className="flex items-center px-space-lg py-3 gap-space-sm">
              <Icon className="text-primary" name="search" size={24} />
              <input
                className="w-full bg-transparent font-body-lg text-body-lg text-on-surface placeholder:text-outline focus:outline-none"
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search verified guides, runbooks, error codes, or ask the ITSM AI Assistant..."
                type="text"
                value={query}
              />
              <div className="flex items-center gap-space-xs shrink-0">
                {query ? (
                  <Button icon="close" iconSize={18} onClick={() => setQuery('')} size="icon" variant="ghost" />
                ) : null}
                <span className="hidden sm:inline-block font-code-sm text-code-sm px-2 py-1 rounded bg-surface-container-high text-on-surface font-semibold select-none">
                  ⌘K
                </span>
                <Button iconSize={16} trailingIcon="arrow_forward" variant="primary">
                  Query
                </Button>
              </div>
            </div>
          </div>
          {popularSearches.length > 0 ? (
            <div className="flex flex-wrap items-center justify-center gap-space-xs mt-space-md">
              <span className="font-label-sm text-label-sm text-outline mr-1 font-semibold uppercase">
                Popular Searches:
              </span>
              {popularSearches.map((chip) => (
                <button
                  className="px-space-sm py-1 rounded-full bg-surface-container text-on-surface font-label-sm text-label-sm hover:bg-secondary-container hover:text-on-secondary-container transition-all"
                  key={chip}
                  onClick={() => setQuery(chip)}
                  type="button"
                >
                  {chip}
                </button>
              ))}
            </div>
          ) : null}
        </div>
      </section>

      {knowledgeStats.length > 0 ? (
        <section className="stagger grid grid-cols-1 md:grid-cols-4 gap-space-md mb-space-xl">
          {knowledgeStats.map((stat) => (
            <Card className="flex items-center justify-between" key={stat.label}>
              <div>
                <div className="font-label-sm text-label-sm text-outline uppercase font-semibold">{stat.label}</div>
                <div className="font-headline-lg text-headline-lg text-on-surface font-semibold mt-0.5">{stat.value}</div>
                <div className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">{stat.footer}</div>
              </div>
              <IconBadge icon={stat.icon} tone={stat.tone} />
            </Card>
          ))}
        </section>
      ) : null}

      <section className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg mb-space-xl">
        <Card padding="lg" radius="2xl" className="lg:col-span-8 flex flex-col relative overflow-hidden">
          <div className="absolute -right-10 -bottom-10 w-64 h-64 rounded-full bg-primary-fixed/20 blur-2xl pointer-events-none"></div>
          <div>
            <div className="flex items-center justify-between pb-space-sm mb-space-md">
              <div className="flex items-center gap-space-sm">
                <span className="w-8 h-8 rounded-lg bg-primary text-on-primary flex items-center justify-center shadow-sm">
                  <Icon name="psychology" size={18} />
                </span>
                <div>
                  <div className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-1.5">
                    <span>ITSM AI Runbook Assistant</span>
                    <Badge tone="success" className="uppercase">Live</Badge>
                  </div>
                  <div className="font-body-sm text-body-sm text-on-surface-variant">
                    Instant enterprise diagnostic &amp; auto-generated remediation scripts
                  </div>
                </div>
              </div>
            </div>
            <p className="font-body-md text-body-md text-on-surface-variant mb-space-md">
              Describe your issue in plain English to get an instant verified diagnosis and automated self-healing
              script.
            </p>
            <div className="rounded-xl bg-surface-container-low mb-space-md">
              <EmptyState
                compact
                icon="forum"
                title="No conversation yet"
                description="Ask a question below and the assistant will return a validated diagnosis and remediation script."
              />
            </div>
          </div>
          <div className="flex items-center gap-space-xs pt-space-xs">
            <SearchInput className="flex-1" placeholder="E.g., Docker container can't reach internal Artifactory repo..." size="toolbar" />
            <Button
              className="shrink-0"
              icon={generating ? 'refresh' : 'auto_fix_high'}
              iconSize={16}
              onClick={generate}
              variant="primary"
            >
              {generating ? 'Synthesizing...' : 'Generate Runbook'}
            </Button>
          </div>
        </Card>

        <div className="lg:col-span-4 flex flex-col gap-space-md">
          <Card padding="lg" radius="2xl" className="flex-1 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-space-sm">
                <span className="font-headline-sm text-headline-sm text-on-surface font-semibold">Self-Healing Toolkit</span>
                <Badge tone="muted">Mac &amp; Windows</Badge>
              </div>
              <p className="font-body-sm text-body-sm text-on-surface-variant mb-space-md">
                Execute one-click IT-certified remediation scripts directly on your enrolled workstation without
                submitting a ticket.
              </p>
              {selfHealingScripts.length === 0 ? (
                <EmptyState
                  compact
                  icon="terminal"
                  title="No scripts available"
                  description="Remediation scripts appear here once the IT agent publishes them."
                />
              ) : (
                <div className="space-y-space-xs">
                  {selfHealingScripts.map((script) => (
                    <div
                      className="flex items-center justify-between p-space-sm rounded-xl bg-surface-container-low hover:bg-surface-container transition-colors cursor-pointer group"
                      key={script.title}
                    >
                      <div className="flex items-center gap-space-sm">
                        <Icon className="text-primary" name={script.icon} size={20} />
                        <div>
                          <div className="font-label-md text-label-md text-on-surface font-semibold group-hover:text-primary">
                            {script.title}
                          </div>
                          <div className="font-body-sm text-body-sm text-outline">{script.description}</div>
                        </div>
                      </div>
                      <Button size="sm" variant="outline">
                        Run
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </Card>
          <Card className="bg-secondary-container text-on-secondary-container flex items-center gap-space-md">
            <IconBadge icon="support_agent" tone="neutral" radius="lg" />
            <div className="min-w-0 flex-1">
              <div className="font-label-md text-label-md font-semibold text-on-secondary-fixed">
                Major Incident or P1 Outage?
              </div>
              <div className="font-body-sm text-body-sm text-on-secondary-container">
                NOC Incident Bridge is live at ext. 4400.
              </div>
            </div>
            <Button className="shrink-0" size="sm" variant="outline">
              Join Bridge
            </Button>
          </Card>
        </div>
      </section>

      <section className="mb-space-xl">
        <div className="flex items-end justify-between mb-space-md">
          <div>
            <div className="font-label-sm text-label-sm text-outline uppercase font-semibold">Knowledge Architecture</div>
            <h2 className="font-headline-lg text-headline-lg text-on-surface font-semibold tracking-tight">
              Browse by Enterprise Technology Domain
            </h2>
          </div>
          <span className="font-label-sm text-label-sm text-on-surface-variant">
            {knowledgeDomains.length} Categories
          </span>
        </div>
        {knowledgeDomains.length === 0 ? (
          <Card padding="none">
            <EmptyState
              icon="category"
              title="No knowledge domains yet"
              description="Technology domains will appear here once articles are published."
            />
          </Card>
        ) : (
          <div className="stagger grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-space-md">
            {knowledgeDomains.map((domain) => (
              <Card padding="lg" radius="2xl" className="hover:shadow-md transition-all flex flex-col justify-between group cursor-pointer" key={domain.title}>
                <div>
                  <div className="flex items-center justify-between mb-space-sm">
                    <IconBadge icon={domain.icon} tone={domain.tone} size="lg" radius="lg" />
                    <Badge tone="neutral" pill>
                      {domain.count}
                    </Badge>
                  </div>
                  <h3 className="font-headline-sm text-headline-sm text-on-surface group-hover:text-primary transition-colors font-semibold mb-1">
                    {domain.title}
                  </h3>
                  <p className="font-body-sm text-body-sm text-on-surface-variant mb-space-md">{domain.description}</p>
                </div>
              </Card>
            ))}
          </div>
        )}
      </section>

      <section className="mb-space-xl" id="quick-runbooks">
        <div className="flex items-center justify-between mb-space-md">
          <div>
            <div className="font-label-sm text-label-sm text-outline uppercase font-semibold">Validated Operations</div>
            <h2 className="font-headline-lg text-headline-lg text-on-surface font-semibold tracking-tight">
              Featured &amp; High-Impact Guides
            </h2>
          </div>
          <div className="flex items-center gap-space-xs">
            <Button size="sm" variant="soft">
              Sort by Helpfulness
            </Button>
            <Button size="sm" variant="ghost">
              Most Viewed
            </Button>
          </div>
        </div>
        {knowledgeArticles.length === 0 ? (
          <Card padding="none">
            <EmptyState
              icon="article"
              title="No guides published yet"
              description="Featured and high-impact guides will be listed here once they are validated."
            />
          </Card>
        ) : (
          <div className="stagger grid grid-cols-1 md:grid-cols-2 gap-space-md">
            {knowledgeArticles.map((article) => (
              <Card padding="lg" radius="2xl" className="hover:shadow-md transition-all flex flex-col justify-between" key={article.code}>
                <div>
                  <div className="flex items-center justify-between mb-space-xs">
                    <div className="flex items-center gap-space-xs">
                      <Badge tone="primary">{article.code}</Badge>
                      <span className="font-label-sm text-label-sm text-outline">{article.category}</span>
                    </div>
                    <div className="flex items-center gap-1 text-tertiary font-label-sm text-label-sm font-semibold">
                      <Icon name="thumb_up" size={15} />
                      <span>{article.helpful}</span>
                    </div>
                  </div>
                  <h3 className="font-headline-md text-headline-md text-on-surface font-semibold mb-space-xs hover:text-primary transition-colors cursor-pointer">
                    {article.title}
                  </h3>
                  <p className="font-body-md text-body-md text-on-surface-variant mb-space-md">{article.description}</p>
                </div>
                <div className="pt-space-sm flex items-center justify-between">
                  <div className="flex items-center gap-space-sm">
                    <span className="w-7 h-7 rounded-full bg-secondary-fixed text-on-secondary-fixed flex items-center justify-center font-label-sm text-label-sm font-bold">
                      {article.initials}
                    </span>
                    <div className="text-left">
                      <div className="font-label-sm text-label-sm text-on-surface font-semibold flex items-center gap-1">
                        <span>Verified by {article.author}</span>
                        <Icon className="text-tertiary" name="verified" size={13} />
                      </div>
                      <div className="font-body-sm text-body-sm text-outline">{article.role}</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-space-md text-outline font-code-sm text-code-sm">
                    <span className="flex items-center gap-1">
                      <Icon name="visibility" size={14} />
                      {article.views}
                    </span>
                    <span className="flex items-center gap-1">
                      <Icon name="update" size={14} />
                      {article.updated}
                    </span>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </section>

      {deflectionMetrics.length > 0 ? (
        <Card padding="lg" radius="2xl" className="mb-space-xl">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-md pb-space-md mb-space-md">
            <div>
              <div className="font-label-sm text-label-sm text-outline uppercase font-semibold">
                Incident Prevention Visualizer
              </div>
              <h3 className="font-headline-md text-headline-md text-on-surface font-semibold">
                Real-Time Knowledge Deflection Telemetry
              </h3>
            </div>
            <div className="flex items-center gap-space-sm">
              <Badge tone="neutral">Live Event Bus</Badge>
              <Button size="sm" variant="soft">
                Export Telemetry
              </Button>
            </div>
          </div>
          <div className="stagger grid grid-cols-1 md:grid-cols-3 gap-space-md items-center">
            {deflectionMetrics.map((metric) => (
              <div className="p-space-md rounded-xl bg-surface-container-low" key={metric.label}>
                <div className="flex items-center justify-between mb-1">
                  <span className="font-label-md text-label-md text-on-surface font-semibold">{metric.label}</span>
                  <span className="font-code-sm text-code-sm text-primary font-bold">{metric.value}</span>
                </div>
                <ProgressBar className="mb-2" value={metric.progress} />
                <p className="font-body-sm text-body-sm text-outline">{metric.description}</p>
              </div>
            ))}
          </div>
        </Card>
      ) : null}

      <Card padding="lg" radius="2xl" className="bg-surface-container-low flex flex-col md:flex-row items-center justify-between gap-space-lg">
        <div className="flex items-center gap-space-md">
          <span className="w-12 h-12 rounded-xl bg-surface-container-lowest text-primary shadow-xs flex items-center justify-center shrink-0">
            <Icon name="shield_person" size={26} />
          </span>
          <div>
            <div className="font-headline-sm text-headline-sm text-on-surface font-semibold flex items-center gap-2">
              <span>Are you an authorized technician?</span>
              <Badge tone="primary" pill>Tier 2+ Required</Badge>
            </div>
            <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">
              Contribute new remediation runbooks, update deprecations, or peer-review pending community documentation.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-space-sm shrink-0 w-full md:w-auto justify-end">
          <Button className="flex-1 md:flex-none justify-center" icon="rate_review" variant="outline">
            Review Drafts
          </Button>
          <Button className="flex-1 md:flex-none justify-center" icon="add_circle" variant="primary">
            Create New KB Article
          </Button>
        </div>
      </Card>
    </>
  )
}

export default KnowledgeBase
