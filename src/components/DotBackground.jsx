import { useTheme } from '../theme/context.js'
import DotGrid from './DotGrid.jsx'

const PALETTE = {
  light: { baseColor: '#d6d3ef', activeColor: '#1d4ed8' },
  dark: { baseColor: '#2a2a2c', activeColor: '#f5f5f6' },
}

function DotBackground() {
  const { resolved } = useTheme()
  const { baseColor, activeColor } = PALETTE[resolved] ?? PALETTE.light

  return (
    <div aria-hidden="true" className="fixed inset-0 z-0 pointer-events-none">
      <DotGrid
        activeColor={activeColor}
        baseColor={baseColor}
        dotSize={4}
        gap={14}
        proximity={130}
        resistance={750}
        returnDuration={1.4}
        shockRadius={220}
        shockStrength={4}
        speedTrigger={120}
      />
    </div>
  )
}

export default DotBackground
