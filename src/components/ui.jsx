import { forwardRef } from 'react'

/* ------------------------------------------------------------------ */
/* Icon                                                                */
/* ------------------------------------------------------------------ */

export function Icon({ name, size = 18, filled = false, className = '', ...rest }) {
  return (
    <span
      aria-hidden="true"
      className={`material-symbols-outlined ${className}`}
      style={{
        fontSize: `${size}px`,
        ...(filled ? { fontVariationSettings: "'FILL' 1" } : null),
      }}
      {...rest}
    >
      {name}
    </span>
  )
}

/* ------------------------------------------------------------------ */
/* Button                                                              */
/* ------------------------------------------------------------------ */

const BUTTON_VARIANTS = {
  primary: 'bg-primary text-on-primary shadow-sm hover:bg-primary-container hover:text-on-primary-container',
  navy: 'bg-secondary text-on-secondary shadow-sm hover:bg-inverse-surface',
  secondary: 'bg-surface-container-low text-on-surface hover:bg-surface-container',
  soft: 'bg-surface-container text-on-surface hover:bg-surface-container-high',
  outline: 'bg-surface-container-lowest text-on-surface border border-outline-variant hover:bg-surface-container-low',
  ghost: 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface',
  destructive: 'bg-error-container text-on-error-container hover:bg-error hover:text-on-error',
  success: 'bg-tertiary-fixed text-on-tertiary-fixed hover:bg-tertiary hover:text-on-tertiary',
  link: 'text-primary hover:underline',
}

const BUTTON_SIZES = {
  sm: 'h-7 px-2.5 gap-1 font-label-sm text-label-sm rounded-lg',
  md: 'h-9 px-3.5 gap-1.5 font-label-md text-label-md rounded-lg',
  lg: 'h-11 px-4 gap-2 font-label-md text-label-md rounded-xl',
  icon: 'h-8 w-8 justify-center rounded-lg',
  'icon-sm': 'h-7 w-7 justify-center rounded-lg',
}

export const Button = forwardRef(function Button(
  {
    variant = 'secondary',
    size = 'md',
    as: Tag = 'button',
    icon,
    trailingIcon,
    iconSize,
    className = '',
    type = 'button',
    children,
    ...rest
  },
  ref,
) {
  const resolvedIconSize = iconSize ?? (size === 'sm' || size.startsWith('icon') ? 16 : 18)
  return (
    <Tag
      ref={ref}
      type={Tag === 'button' ? type : undefined}
      className={`inline-flex items-center whitespace-nowrap transition-colors disabled:opacity-40 disabled:pointer-events-none ${BUTTON_VARIANTS[variant]} ${BUTTON_SIZES[size]} ${className}`}
      {...rest}
    >
      {icon ? <Icon name={icon} size={resolvedIconSize} /> : null}
      {children}
      {trailingIcon ? <Icon name={trailingIcon} size={resolvedIconSize} /> : null}
    </Tag>
  )
})

/* ------------------------------------------------------------------ */
/* Badge                                                               */
/* ------------------------------------------------------------------ */

const BADGE_TONES = {
  neutral: 'bg-surface-container text-on-surface',
  muted: 'bg-surface-container-high text-on-surface-variant',
  primary: 'bg-primary-fixed text-on-primary-fixed-variant',
  info: 'bg-secondary-container text-on-secondary-container',
  success: 'bg-tertiary-fixed text-on-tertiary-fixed-variant',
  warning: 'bg-secondary-container text-on-secondary-container',
  danger: 'bg-error-container text-on-error-container',
  escalation: 'bg-error-container text-on-error-container',
}

const DOT_TONES = {
  neutral: 'bg-outline',
  muted: 'bg-outline',
  primary: 'bg-primary',
  info: 'bg-secondary',
  success: 'bg-tertiary',
  warning: 'bg-secondary',
  danger: 'bg-error',
  escalation: 'bg-error',
}

export function Badge({ children, tone = 'neutral', dot = false, pill = false, className = '' }) {
  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 font-label-sm text-label-sm font-semibold ${
        pill ? 'rounded-full' : 'rounded'
      } ${BADGE_TONES[tone]} ${className}`}
    >
      {dot ? <span className={`w-1.5 h-1.5 rounded-full ${DOT_TONES[tone]}`} /> : null}
      {children}
    </span>
  )
}

/* ------------------------------------------------------------------ */
/* Card                                                                */
/* ------------------------------------------------------------------ */

const CARD_PADDING = { none: '', sm: 'p-space-sm', md: 'p-space-md', lg: 'p-space-lg', xl: 'p-space-xl' }
const CARD_RADIUS = { lg: 'rounded-lg', xl: 'rounded-xl', '2xl': 'rounded-2xl' }

export function Card({ as: Tag = 'div', padding = 'md', radius = 'xl', className = '', children, ...rest }) {
  return (
    <Tag
      className={`glass-card bg-surface-container-lowest ${CARD_RADIUS[radius]} ${CARD_PADDING[padding]} ${className}`}
      {...rest}
    >
      {children}
    </Tag>
  )
}

/* ------------------------------------------------------------------ */
/* IconBadge                                                           */
/* ------------------------------------------------------------------ */

const ICON_BADGE_TONES = {
  primary: 'bg-primary-fixed text-on-primary-fixed-variant',
  info: 'bg-secondary-fixed text-on-secondary-fixed',
  success: 'bg-tertiary-fixed text-on-tertiary-fixed',
  danger: 'bg-error-container text-on-error-container',
  neutral: 'bg-surface-container text-on-surface',
  muted: 'bg-surface-container-low text-primary',
}

const ICON_BADGE_RADIUS = { md: 'rounded-md', lg: 'rounded-lg', xl: 'rounded-xl', full: 'rounded-full' }

export function IconBadge({ icon, tone = 'primary', size = 'md', radius = 'lg', iconSize, className = '' }) {
  const box = { sm: 'h-8 w-8', md: 'h-10 w-10', lg: 'h-12 w-12', xl: 'h-14 w-14' }[size]
  const fallbackIcon = { sm: 16, md: 20, lg: 24, xl: 32 }[size]
  return (
    <span
      className={`inline-flex shrink-0 items-center justify-center ${box} ${ICON_BADGE_RADIUS[radius]} ${ICON_BADGE_TONES[tone]} ${className}`}
    >
      <Icon name={icon} size={iconSize ?? fallbackIcon} />
    </span>
  )
}

/* ------------------------------------------------------------------ */
/* Avatar                                                              */
/* ------------------------------------------------------------------ */

const AVATAR_SIZES = { sm: 'w-6 h-6 text-[10px]', md: 'w-8 h-8 text-body-sm', lg: 'w-11 h-11 text-label-md' }

function initialsFromName(name) {
  if (!name) return ''
  return name
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .join('')
}

export function Avatar({ name, src, size = 'md', tone = 'primary', className = '' }) {
  const initials = initialsFromName(name)
  const dims = AVATAR_SIZES[size]
  if (src) {
    return <img alt={name ?? 'Avatar'} className={`${dims} rounded-full object-cover shrink-0 ${className}`} src={src} />
  }
  return (
    <span
      className={`inline-flex items-center justify-center rounded-full shrink-0 font-code-sm font-bold ${dims} ${
        ICON_BADGE_TONES[tone]
      } ${className}`}
    >
      {initials || <Icon name="person" size={size === 'sm' ? 14 : 18} />}
    </span>
  )
}

/* ------------------------------------------------------------------ */
/* ProgressBar                                                         */
/* ------------------------------------------------------------------ */

const PROGRESS_TONES = { primary: 'bg-primary', success: 'bg-tertiary', info: 'bg-secondary', danger: 'bg-error' }

export function ProgressBar({ value = 0, tone = 'primary', className = '' }) {
  const width = `${Math.max(0, Math.min(100, value))}%`
  return (
    <div className={`w-full bg-surface-container rounded-full overflow-hidden ${className}`}>
      <div className={`h-full rounded-full ${PROGRESS_TONES[tone]}`} style={{ width }} />
    </div>
  )
}

/* ------------------------------------------------------------------ */
/* SectionHeader                                                       */
/* ------------------------------------------------------------------ */

export function SectionHeader({ eyebrow, title, subtitle, badge, actions, className = '' }) {
  return (
    <div className={`flex flex-col sm:flex-row sm:items-end justify-between gap-3 pb-space-sm mb-space-md ${className}`}>
      <div>
        {eyebrow ? (
          <div className="font-label-sm text-label-sm text-outline uppercase font-semibold">{eyebrow}</div>
        ) : null}
        <div className="flex items-center gap-2">
          <h2 className="font-headline-lg text-headline-lg text-on-surface tracking-tight">{title}</h2>
          {badge}
        </div>
        {subtitle ? <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">{subtitle}</p> : null}
      </div>
      {actions ? <div className="flex items-center gap-space-xs">{actions}</div> : null}
    </div>
  )
}

/* ------------------------------------------------------------------ */
/* EmptyState                                                          */
/* ------------------------------------------------------------------ */

export function EmptyState({ icon = 'inbox', title, description, action, compact = false, className = '' }) {
  return (
    <div
      className={`flex flex-col items-center justify-center text-center ${
        compact ? 'py-space-lg' : 'py-space-xl'
      } px-space-md ${className}`}
    >
      <span className="w-12 h-12 rounded-xl bg-surface-container text-outline flex items-center justify-center mb-space-sm">
        <Icon name={icon} size={26} />
      </span>
      <p className="font-headline-sm text-headline-sm text-on-surface">{title}</p>
      {description ? (
        <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5 max-w-sm">{description}</p>
      ) : null}
      {action ? <div className="mt-space-md">{action}</div> : null}
    </div>
  )
}

/* ------------------------------------------------------------------ */
/* SearchInput                                                         */
/* ------------------------------------------------------------------ */

export function SearchInput({
  value,
  onChange,
  placeholder,
  onClear,
  icon = 'search',
  size = 'md',
  className = '',
  inputClassName = '',
  ...rest
}) {
  const wrapper =
    size === 'lg'
      ? 'px-space-lg py-3 rounded-2xl'
      : size === 'toolbar'
        ? 'px-space-md py-1.5 rounded-xl'
        : 'px-3 py-2 rounded-lg'
  const iconSize = size === 'lg' ? 24 : 18
  return (
    <div
      className={`flex items-center gap-space-sm bg-surface-container-low text-on-surface-variant transition-colors focus-within:bg-surface-container-lowest ${wrapper} ${className}`}
    >
      <Icon className="text-outline" name={icon} size={iconSize} />
      <input
        className={`w-full bg-transparent font-body-md text-body-md text-on-surface placeholder:text-outline focus:outline-none ${inputClassName}`}
        onChange={onChange}
        placeholder={placeholder}
        type="text"
        value={value}
        {...rest}
      />
      {onClear && value ? (
        <button className="text-outline hover:text-on-surface transition-colors p-0.5" onClick={onClear} type="button">
          <Icon name="close" size={16} />
        </button>
      ) : null}
    </div>
  )
}

/* ------------------------------------------------------------------ */
/* StatCard                                                            */
/* ------------------------------------------------------------------ */

const TREND_TONES = { up: 'text-tertiary', down: 'text-tertiary', flat: 'text-on-surface-variant', danger: 'text-error' }

export function StatCard({
  label,
  value,
  icon,
  iconTone = 'primary',
  trend,
  trendIcon,
  trendTone = 'up',
  progress,
  progressTone = 'primary',
  footer,
  className = '',
}) {
  return (
    <Card className={`flex items-center gap-space-md ${className}`}>
      {icon ? <IconBadge icon={icon} tone={iconTone} /> : null}
      <div className="flex-1 min-w-0">
        <div className="font-label-sm text-label-sm uppercase text-outline">{label}</div>
        <div className="flex items-center gap-2 mt-0.5">
          <span className="font-headline-md text-headline-md text-on-surface font-bold">{value}</span>
          {trend ? (
            <span className={`font-label-sm text-label-sm flex items-center gap-0.5 ${TREND_TONES[trendTone]}`}>
              {trendIcon ? <Icon name={trendIcon} size={13} /> : null}
              {trend}
            </span>
          ) : null}
        </div>
        {typeof progress === 'number' ? <ProgressBar className="mt-1.5" tone={progressTone} value={progress} /> : null}
        {footer ? <div className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">{footer}</div> : null}
      </div>
    </Card>
  )
}

/* ------------------------------------------------------------------ */
/* Toggle                                                              */
/* ------------------------------------------------------------------ */

export function Toggle({ checked = false, onChange, disabled = false, className = '' }) {
  return (
    <button
      aria-checked={checked}
      className={`relative inline-flex h-6 w-11 shrink-0 items-center rounded-full transition-colors disabled:opacity-40 disabled:pointer-events-none ${
        checked ? 'bg-primary' : 'bg-surface-container-highest'
      } ${className}`}
      disabled={disabled}
      onClick={() => onChange?.(!checked)}
      role="switch"
      type="button"
    >
      <span
        className={`inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform ${
          checked ? 'translate-x-6' : 'translate-x-1'
        }`}
      />
    </button>
  )
}

/* ------------------------------------------------------------------ */
/* SegmentedControl                                                    */
/* ------------------------------------------------------------------ */

export function SegmentedControl({ options, value, onChange, className = '' }) {
  return (
    <div className={`inline-flex items-center gap-0.5 bg-surface-container-low p-0.5 rounded-lg ${className}`}>
      {options.map((option) => {
        const active = option.value === value
        return (
          <button
            className={`inline-flex items-center gap-1 px-3 py-1.5 rounded-md font-label-md text-label-md transition-colors ${
              active
                ? 'bg-surface-container-lowest text-on-surface shadow-sm'
                : 'text-on-surface-variant hover:text-on-surface'
            }`}
            key={option.value}
            onClick={() => onChange?.(option.value)}
            type="button"
          >
            {option.icon ? <Icon name={option.icon} size={16} /> : null}
            {option.label}
          </button>
        )
      })}
    </div>
  )
}

/* ------------------------------------------------------------------ */
/* Select                                                              */
/* ------------------------------------------------------------------ */

export function Select({ options = [], placeholder, className = '', selectClassName = '', ...rest }) {
  return (
    <div className={`relative ${className}`}>
      <select
        className={`w-full h-10 px-3.5 pr-8 rounded-lg bg-surface-container-low text-on-surface font-body-md text-body-md appearance-none focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all cursor-pointer ${selectClassName}`}
        {...rest}
      >
        {placeholder ? <option value="">{placeholder}</option> : null}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      <Icon className="absolute right-3 top-2.5 pointer-events-none text-outline" name="expand_more" size={18} />
    </div>
  )
}

/* ------------------------------------------------------------------ */
/* TextField / TextArea                                                */
/* ------------------------------------------------------------------ */

export function TextField({ className = '', ...rest }) {
  return (
    <input
      className={`w-full h-10 px-3.5 rounded-lg bg-surface-container-low text-on-surface font-body-md text-body-md placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all ${className}`}
      {...rest}
    />
  )
}

export function TextArea({ className = '', ...rest }) {
  return (
    <textarea
      className={`w-full p-3.5 rounded-lg bg-surface-container-low text-on-surface font-body-md text-body-md placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all resize-y ${className}`}
      {...rest}
    />
  )
}

/* ------------------------------------------------------------------ */
/* SettingsRow / SettingsSection                                       */
/* ------------------------------------------------------------------ */

export function SettingsRow({ title, description, children, className = '' }) {
  return (
    <div className={`flex flex-col sm:flex-row sm:items-center justify-between gap-space-sm py-space-md ${className}`}>
      <div className="min-w-0">
        <div className="font-label-md text-label-md text-on-surface font-semibold">{title}</div>
        {description ? (
          <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5 max-w-md">{description}</p>
        ) : null}
      </div>
      <div className="shrink-0">{children}</div>
    </div>
  )
}

export function SettingsSection({ id, icon, title, description, actions, children, className = '' }) {
  return (
    <Card as="section" id={id} padding="lg" className={className}>
      <div className="flex items-start justify-between gap-space-sm pb-space-sm mb-space-sm border-b border-surface-container">
        <div className="flex items-start gap-space-sm">
          {icon ? <IconBadge icon={icon} tone="primary" radius="lg" size="sm" /> : null}
          <div>
            <h2 className="font-headline-md text-headline-md text-on-surface">{title}</h2>
            {description ? <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">{description}</p> : null}
          </div>
        </div>
        {actions ? <div className="flex items-center gap-space-xs">{actions}</div> : null}
      </div>
      <div>{children}</div>
    </Card>
  )
}
