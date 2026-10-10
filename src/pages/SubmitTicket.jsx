import { useMemo, useState } from 'react'
import { Avatar, Badge, Button, Card, EmptyState, Icon, IconBadge } from '../components/ui.jsx'
import { responseTargetOptions } from '../data/settings.js'
import { assetOptions, categoryOptions, impactLevels, urgencyOptions } from '../data/submit.js'
import { useSettings } from '../settings/context.js'

const MAX_SUBJECT = 120

function Field({ label, required, hint, children }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="font-headline-sm text-headline-sm text-on-surface flex items-center justify-between">
        <span>
          {label} {required ? <span className="text-error">*</span> : null}
        </span>
        {hint}
      </label>
      {children}
    </div>
  )
}

function Select({ options, placeholder, ...rest }) {
  return (
    <div className="relative">
      <select
        className="w-full h-10 px-3.5 pr-8 rounded-lg bg-surface-container-low text-on-surface font-body-md text-body-md appearance-none focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all cursor-pointer"
        {...rest}
      >
        <option value="">{placeholder}</option>
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      <Icon className="absolute right-3 top-2.5 pointer-events-none text-outline" name="expand_more" size={18} />
    </div>
  )
}

function SectionShell({ step, title, subtitle, aside, children }) {
  return (
    <Card padding="lg" className="flex flex-col gap-6">
      <div className="flex items-center justify-between pb-3">
        <div className="flex items-center gap-3">
          <span className="w-7 h-7 rounded-lg bg-primary text-on-primary font-headline-sm text-headline-sm flex items-center justify-center font-bold">
            {step}
          </span>
          <div>
            <h2 className="font-headline-md text-headline-md text-on-surface">{title}</h2>
            <p className="font-body-sm text-body-sm text-on-surface-variant">{subtitle}</p>
          </div>
        </div>
        {aside}
      </div>
      {children}
    </Card>
  )
}

function SubmitTicket() {
  const { settings } = useSettings()
  const profile = settings.profile
  const hasRequester = Boolean(profile.name)
  const requesterDetail = [profile.title, profile.department, profile.email].filter(Boolean).join(' · ')
  const defaultResponse =
    responseTargetOptions.find((option) => option.value === settings.sla.firstResponse)?.label ?? '30 minutes'

  const [impact, setImpact] = useState('')
  const [urgency, setUrgency] = useState('')
  const [category, setCategory] = useState('')
  const [asset, setAsset] = useState('')
  const [subject, setSubject] = useState('')
  const [description, setDescription] = useState('')

  const canSubmit = Boolean(impact && category && subject.trim() && description.trim())

  const selectedImpact = useMemo(() => impactLevels.find((l) => l.value === impact), [impact])

  return (
    <>
      <div className="flex flex-wrap items-center justify-between gap-space-sm pt-4 pb-2">
        <nav className="flex items-center gap-2">
          <span className="font-label-sm text-label-sm text-outline tracking-wider uppercase">HelpDesk Pro</span>
          <Icon className="text-outline" name="chevron_right" size={14} />
          <span className="font-label-sm text-label-sm text-outline tracking-wider uppercase">Self-Service</span>
          <Icon className="text-outline" name="chevron_right" size={14} />
          <span className="font-label-sm text-label-sm text-primary font-semibold tracking-wider uppercase">
            Submit New Ticket
          </span>
        </nav>
        <Badge tone="info" pill>
          <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
          Interactive Ticket Intake Flow
        </Badge>
      </div>

      <div className="relative mt-2 mb-8 p-6 rounded-xl bg-linear-to-r from-surface-container-lowest via-surface-container-low to-surface-container-lowest shadow-sm overflow-hidden">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="max-w-3xl">
            <h1 className="font-headline-xl text-headline-xl text-on-surface tracking-tight">
              Submit an IT Support Request
            </h1>
            <p className="font-body-lg text-body-lg text-on-surface-variant mt-1.5">
              Provide accurate telemetry and environmental details so our automated triage system can route your incident
              to the right engineers.
            </p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-primary-container text-on-primary-container flex items-center justify-center shadow-md self-start md:self-auto">
            <Icon name="forward_to_inbox" size={26} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <div className="lg:col-span-8 flex flex-col gap-8 stagger">
          <SectionShell
            step="1"
            title="Requester &amp; Impact Context"
            subtitle="Verify profile credentials and quantify operational blast radius."
            aside={
              hasRequester ? (
                <Badge tone="success" className="uppercase tracking-wider">
                  Verified Identity
                </Badge>
              ) : null
            }
          >
            {hasRequester ? (
              <div className="p-4 rounded-xl bg-surface-container-low flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div className="flex items-center gap-3.5">
                  <Avatar name={profile.name} size="lg" />
                  <div>
                    <span className="font-headline-sm text-headline-sm text-on-surface">{profile.name}</span>
                    {requesterDetail ? (
                      <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">{requesterDetail}</p>
                    ) : null}
                  </div>
                </div>
                <Badge tone="neutral" pill>
                  <Icon name="verified_user" size={14} />
                  Set in Settings
                </Badge>
              </div>
            ) : (
              <div className="p-4 rounded-xl border border-dashed border-outline-variant bg-surface-container-low">
                <EmptyState
                  compact
                  icon="person_off"
                  title="No requester selected"
                  description="Add your name in Settings → Profile and it will appear here automatically."
                />
              </div>
            )}

            <div className="flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <label className="font-headline-sm text-headline-sm text-on-surface">
                  Operational Impact Radius <span className="text-error">*</span>
                </label>
                <span className="font-body-sm text-body-sm text-outline">Determines blast-radius priority vector</span>
              </div>
              <div className="stagger grid grid-cols-1 md:grid-cols-3 gap-3">
                {impactLevels.map((level) => {
                  const active = impact === level.value
                  const isError = level.accent === 'error'
                  return (
                    <label
                      className={`cursor-pointer relative p-4 rounded-xl transition-all flex flex-col justify-between group ${
                        active
                          ? isError
                            ? 'bg-error-container/10 shadow-sm'
                            : 'bg-primary-container/10 shadow-sm'
                          : 'bg-surface hover:bg-surface-container'
                      }`}
                      key={level.value}
                    >
                      <input
                        checked={active}
                        className="sr-only"
                        name="impact_level"
                        onChange={() => setImpact(level.value)}
                        type="radio"
                        value={level.value}
                      />
                      <div className="flex items-start justify-between">
                        <IconBadge icon={level.icon} tone={isError ? 'danger' : 'primary'} radius="lg" size="sm" />
                        <span
                          className={`w-4 h-4 rounded-full flex items-center justify-center transition-all ${
                            active
                              ? isError
                                ? 'bg-error ring-4 ring-error/20'
                                : 'bg-primary ring-4 ring-primary/20'
                              : 'bg-surface-container-highest'
                          }`}
                        >
                          {active ? (
                            <span className={`w-1.5 h-1.5 rounded-full ${isError ? 'bg-on-error' : 'bg-on-primary'}`}></span>
                          ) : null}
                        </span>
                      </div>
                      <div className="mt-3">
                        <p className={`font-headline-sm text-headline-sm ${active ? (isError ? 'text-error' : 'text-primary') : 'text-on-surface'}`}>
                          {level.title}
                        </p>
                        <p className="font-body-sm text-body-sm text-on-surface-variant mt-1 leading-normal">
                          {level.description}
                        </p>
                      </div>
                      <div className="mt-3 pt-2 flex items-center gap-1 font-code-sm text-code-sm text-outline">
                        <span>{level.slaLabel}</span>
                        <span className="font-semibold text-on-surface">{level.slaValue}</span>
                      </div>
                    </label>
                  )
                })}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
              <Field label="Perceived Urgency">
                <Select onChange={(e) => setUrgency(e.target.value)} options={urgencyOptions} placeholder="Select perceived urgency" value={urgency} />
              </Field>
              <div className="p-3 rounded-lg bg-surface-container-low flex items-center gap-3">
                <IconBadge icon="speed" tone="info" radius="lg" size="sm" />
                <div>
                  <p className="font-label-md text-label-md text-on-surface font-semibold">
                    {selectedImpact ? `SLA: ${selectedImpact.slaValue}` : 'SLA Matrix'}
                  </p>
                  <p className="font-body-sm text-body-sm text-on-surface-variant">
                    {selectedImpact
                      ? 'First response target based on the selected impact radius.'
                      : `Workspace default first response: ${defaultResponse}.`}
                  </p>
                </div>
              </div>
            </div>
          </SectionShell>

          <SectionShell
            step="2"
            title="Issue Categorization &amp; Details"
            subtitle="Classify hardware assets and supply descriptive reproduction steps."
            aside={<Badge tone="muted" className="font-code-sm">AUTO-TAGGER: ON</Badge>}
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Field label="Primary Category" required>
                <Select onChange={(e) => setCategory(e.target.value)} options={categoryOptions} placeholder="Select a category" value={category} />
              </Field>
              <Field label="Assigned Asset / Device">
                <Select onChange={(e) => setAsset(e.target.value)} options={assetOptions} placeholder="Select an asset" value={asset} />
              </Field>
            </div>

            <Field
              label="Subject Line"
              required
              hint={
                <span className="font-code-sm text-code-sm text-outline">
                  {subject.length} / {MAX_SUBJECT} chars
                </span>
              }
            >
              <input
                className="w-full h-11 px-3.5 rounded-lg bg-surface-container-low text-on-surface font-body-lg text-body-lg focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
                maxLength={MAX_SUBJECT}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="e.g. Office Wi-Fi keeps disconnecting every 5 minutes in Conference Room 4B"
                type="text"
                value={subject}
              />
            </Field>

            <Field
              label="Detailed Incident Description"
              required
              hint={
                <button className="font-label-sm text-label-sm text-primary hover:underline flex items-center gap-1" type="button">
                  <Icon name="auto_fix_high" size={14} />
                  Summarize with AI
                </button>
              }
            >
              <div className="rounded-xl bg-surface-container-low overflow-hidden">
                <div className="px-3 py-2 bg-surface-container flex items-center justify-between gap-2 flex-wrap">
                  <div className="flex items-center gap-1">
                    {['format_bold', 'format_italic', 'code', 'format_list_bulleted', 'link', 'format_quote'].map((tool) => (
                      <button
                        className="p-1.5 rounded hover:bg-surface-container-high text-on-surface-variant hover:text-on-surface transition-colors"
                        key={tool}
                        type="button"
                      >
                        <Icon name={tool} size={18} />
                      </button>
                    ))}
                  </div>
                  <span className="font-code-sm text-code-sm text-outline">Markdown Supported</span>
                </div>
                <textarea
                  className="w-full p-4 bg-surface-container-low text-on-surface font-body-md text-body-md focus:outline-none resize-y placeholder:text-outline"
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Describe what happened, error messages received, and exact steps to reproduce..."
                  rows="6"
                  value={description}
                ></textarea>
              </div>
            </Field>
          </SectionShell>
        </div>

        <div className="lg:col-span-4 flex flex-col gap-4 lg:sticky lg:top-20 stagger">
          <Card padding="lg" className="flex flex-col gap-space-md">
            <h3 className="font-headline-md text-headline-md text-on-surface">Submission Summary</h3>
            <dl className="flex flex-col gap-2 font-body-sm text-body-sm">
              <div className="flex items-center justify-between">
                <dt className="text-on-surface-variant">Impact</dt>
                <dd className="text-on-surface font-medium">{selectedImpact?.title ?? 'Not set'}</dd>
              </div>
              <div className="flex items-center justify-between">
                <dt className="text-on-surface-variant">Category</dt>
                <dd className="text-on-surface font-medium">
                  {categoryOptions.find((c) => c.value === category)?.label.split(' (')[0] ?? 'Not set'}
                </dd>
              </div>
              <div className="flex items-center justify-between">
                <dt className="text-on-surface-variant">Priority</dt>
                <dd className="text-on-surface font-medium">{urgency ? 'Set' : 'Not set'}</dd>
              </div>
            </dl>
            <Button className="w-full justify-center" disabled={!canSubmit} icon="send" variant="primary" size="lg">
              Submit Ticket
            </Button>
            <p className="font-body-sm text-body-sm text-outline text-center">
              {canSubmit ? 'Required fields complete.' : 'Complete all required fields to submit.'}
            </p>
          </Card>

          <Card className="flex items-start gap-space-sm">
            <IconBadge icon="lightbulb" tone="info" radius="lg" size="sm" />
            <div>
              <div className="font-label-md text-label-md text-on-surface font-semibold">Faster Resolution</div>
              <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">
                Include exact error messages and reproduction steps. Attach logs or screenshots where possible.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </>
  )
}

export default SubmitTicket
