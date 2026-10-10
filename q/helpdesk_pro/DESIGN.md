---
name: HelpDesk Pro
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#424754'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#727785'
  outline-variant: '#c2c6d6'
  surface-tint: '#005ac2'
  primary: '#0058be'
  on-primary: '#ffffff'
  primary-container: '#2170e4'
  on-primary-container: '#fefcff'
  inverse-primary: '#adc6ff'
  secondary: '#565e74'
  on-secondary: '#ffffff'
  secondary-container: '#dae2fd'
  on-secondary-container: '#5c647a'
  tertiary: '#006947'
  on-tertiary: '#ffffff'
  tertiary-container: '#00855b'
  on-tertiary-container: '#f5fff6'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#dae2fd'
  secondary-fixed-dim: '#bec6e0'
  on-secondary-fixed: '#131b2e'
  on-secondary-fixed-variant: '#3f465c'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 34px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
  body-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-compact: 0.5rem
  margin: 1.5rem
  margin-sm: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1.25rem
  space-xl: 2rem
---

## Brand & Style

This design system targets enterprise IT operations, site reliability engineers, tier 1–3 service desk analysts, and IT leadership. The visual identity projects operational control, instant triage capability, low cognitive fatigue, and high throughput. It balances the high-density technical utility of Datadog and Linear with the enterprise governance standards of modern ServiceNow and Jira Service Management.

The aesthetic philosophy centers on **Corporate Modern Precision**:
- High-density data presentation without visual clutter.
- Low-contrast hairline dividers paired with crisp surface elevations.
- Precise functional chromatic signals against a calm slate base.
- Fast visual scanning enabled by rigid vertical alignment, monospaced metadata identifiers, and tight typographical scale intervals.

## Colors

The color palette is built for rapid status comprehension under enterprise triage conditions. Structural surfaces rely on cool slate neutrals, reserving saturated hues strictly for functional meaning and operational states.

### Core Semantic Roles
- **Primary (`#3B82F6` - Electric Indigo / Core Blue):** Active actions, selected rows, link text, and `In Progress` / `New` workflow states.
- **Secondary (`#0F172A` - Deep Slate Navy):** High-contrast text headers, primary container framing, structural telemetry sidebars, and critical action buttons.
- **Tertiary (`#10B981` - Emerald Green):** `Resolved`, `Closed`, SLA met, healthy telemetry indicators, and operational uptime.
- **Neutral (`#64748B` - Slate Grey):** Subdued metadata, secondary labels, borders, icon fills, and table grid structures.

### Functional Status Scale
- **Urgent / Breached (`#E11D48` Rose-600 / `#FFF1F2` Rose-50):** SLA violations, P1 incidents, error toasts, and critical blocking alerts.
- **Warning / Approaching SLA (`#D97706` Amber-600 / `#FFFBEB` Amber-50):** Imminent breach within 60 minutes, pending user approval, and degraded infrastructure.
- **Escalated (`#8B5CF6` Purple-600 / `#F5F3FF` Purple-50):** Tier reassignment, management oversight required, and cross-team dependencies.
- **Surface Neutral Layering (Light Mode):** Canvas background `#F8FAFC`, panel surface `#FFFFFF`, table hover `#F1F5F9`, border hairline `#E2E8F0`, dark borders `#CBD5E1`.

## Typography

Typography prioritizes high density, legibility, and vertical rhythm. Inter provides uniform stroke geometry and accessible legibility at compact sizes (11px to 13px), standard in incident management grids.

- **Monospaced Identifiers:** All ticket keys (`INC-8041`, `PRB-204`), IP addresses, and SLA countdowns use a monospaced font family for immediate character distinction and tabular alignment.
- **Label Tracking:** Small labels (11px) use uppercase casing with positive tracking (`0.04em`) to maintain legibility inside badge containers and table column headers.
- **Header Compactness:** Headlines use negative letter spacing (`-0.01em` to `-0.02em`) to retain visual solidity without consuming valuable vertical workspace.

## Layout & Spacing

This design system uses an adjustable fluid layout tailored for high-density widescreen workspaces (1440px to 2560px), multi-monitor NOC setups, and compact laptop screens.

### Grid & Structure
- **Navigation Shell:** Collapsible 64px icon rail expandable to a 240px tree-navigation drawer.
- **Main Incident View:** Split-pane fluid layout. Left table view expands flexibly; right contextual inspector maintains a fixed 420px or 480px side sheet.
- **Data Table Density:** Row heights standardize strictly to 36px (compact), 44px (default), and 56px (expanded/preview mode).
- **Responsive Adaptations:**
  - **Desktop (>=1280px):** Multi-column ticket layout with visible telemetry sidebar, full inline filtering toolbar, and sticky table headers.
  - **Tablet (768px - 1279px):** Inspector transitions from an inline split view to an overlay drawer; non-critical table columns collapse into a child chevron row.
  - **Mobile (<768px):** Navigation transitions to bottom bar or hamburger panel; ticket lists render as grouped linear cards.

## Elevation & Depth

Visual separation relies on structural hair-line borders (`1px solid #E2E8F0`) reinforced by subtle, low-opacity ambient drop shadows. Heavy blurs and exaggerated drops are avoided to preserve interface sharpness.

- **Level 0 (Base / Canvas):** Neutral `#F8FAFC`, flat, zero elevation. Hosts workspace panels and table containers.
- **Level 1 (Cards, Modules & Table Rows):** Surface `#FFFFFF`, border `1px solid #E2E8F0`, shadow `0 1px 2px 0 rgba(15, 23, 42, 0.04)`.
- **Level 2 (Dropdowns, Popovers & Context Menus):** Surface `#FFFFFF`, border `1px solid #CBD5E1`, shadow `0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -2px rgba(15, 23, 42, 0.04)`.
- **Level 3 (Modals, Command Palettes & Quick Search):** Backdrop `#0F172A` with 40% opacity, surface `#FFFFFF`, border `1px solid #94A3B8`, shadow `0 20px 25px -5px rgba(15, 23, 42, 0.12), 0 8px 10px -6px rgba(15, 23, 42, 0.06)`.
- **Level 4 (Toasts & Global Incident Banners):** Floating elevated state, shadow `0 10px 15px -3px rgba(15, 23, 42, 0.1)`.

## Shapes

The design system employs a disciplined, soft corner radius (4px to 6px) across interactive and structural elements, preventing childish bubbly forms while avoiding harsh brutalist points.

- **Containers & Cards:** Corner radius set to 6px (`rounded-md`).
- **Inputs & Standard Buttons:** Corner radius set to 6px (`rounded-md`).
- **Status Badges, SLA Pills & Avatars:** Fully rounded pill radius (`9999px`) to create clear shape differentiation between interactive control triggers and informational metadata tokens.
- **Checkboxes & Segmented Controls:** Corner radius set to 4px (`rounded-sm`).

## Components

### Buttons
- **Primary:** Background `#0F172A` (Navy/Slate) with white text, or `#3B82F6` for explicit primary workflow progression (e.g., "Assign to Me", "Resolve Ticket"). 6px radius, font weight 500, padding `8px 14px`.
- **Secondary / Outline:** Background `#FFFFFF`, border `1px solid #E2E8F0`, text `#0F172A`. Hover: background `#F8FAFC`, border `#CBD5E1`.
- **Destructive:** Background `#FFF1F2`, text `#E11D48`, border `1px solid #FECDD3`. Hover: background `#FFE4E6`.
- **Icon / Ghost:** Transparent background, text `#64748B`. Hover: background `#F1F5F9`, text `#0F172A`.

### Badges & Status Pills
- **Construction:** 20px height, pill-shaped (`9999px`), inline-flex, centered text, padding `2px 8px`, 11px uppercase bold font with leading 6px colored dot indicator.
- **Healthy / Resolved:** Background `#ECFDF5`, text `#065F46`, dot `#10B981`.
- **In Progress / New:** Background `#EFF6FF`, text `#1E40AF`, dot `#3B82F6`.
- **Approaching SLA:** Background `#FFFBEB`, text `#92400E`, dot `#F59E0B`.
- **Breached / Critical:** Background `#FFF1F2`, text `#9F1239`, dot `#E11D48`.
- **Escalated:** Background `#F5F3FF`, text `#5B21B6`, dot `#8B5CF6`.

### Data Tables (Incident & Asset Lists)
- **Header:** Background `#F8FAFC`, border-bottom `1px solid #E2E8F0`, text `#64748B`, font-size 11px, uppercase, font-weight 600.
- **Rows:** Background `#FFFFFF`, border-bottom `1px solid #F1F5F9`, hover background `#F8FAFC`, selected row background `#EFF6FF` with `2px solid #3B82F6` left indicator.
- **Cells:** Vertical padding `8px 12px`, numeric and ID values right-aligned or monospaced.

### Form Inputs & Search Fields
- **Text Inputs:** Height 34px (compact) or 40px (default). Background `#FFFFFF`, border `1px solid #CBD5E1`, text `#0F172A`, placeholder `#94A3B8`. Focus state: border `#3B82F6` with `0 0 0 2px rgba(59, 130, 246, 0.15)`.
- **Global Command Search (Cmd+K):** Centered floating input, 48px height, 14px font, inset leading magnifying glass, trailing keybinding pill indicator (`⌘K`).

### Cards & Telemetry Panels
- **Container:** Background `#FFFFFF`, border `1px solid #E2E8F0`, border-radius 6px, padding `16px`.
- **Metric Header:** 12px neutral label (`#64748B`), followed by a 24px bold numeric counter (`#0F172A`), accompanied by a mini trend sparkline or badge delta.

### Checkboxes & Radio Controls
- **Checkbox:** 16x16px square, 4px corner radius, border `1.5px solid #94A3B8`. Checked state: background `#3B82F6`, border `#3B82F6`, white checkmark glyph.
- **Radio Button:** 16x16px circle, border `1.5px solid #94A3B8`. Selected state: border `#3B82F6`, 6px solid `#3B82F6` inner circle.