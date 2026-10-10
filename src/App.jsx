import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import AppShell from './components/AppShell.jsx'
import AllTickets from './pages/AllTickets.jsx'
import Dashboard from './pages/Dashboard.jsx'
import KnowledgeBase from './pages/KnowledgeBase.jsx'
import Placeholder from './pages/Placeholder.jsx'
import Settings from './pages/Settings.jsx'
import SubmitTicket from './pages/SubmitTicket.jsx'
import { useSettings } from './settings/context.js'

const LANDING_PATHS = {
  dashboard: '/dashboard',
  'all-tickets': '/all-tickets',
  'knowledge-base': '/knowledge-base',
  'my-tickets': '/my-tickets',
}

function Home() {
  const { settings } = useSettings()
  return <Navigate replace to={LANDING_PATHS[settings.workspace.landing] ?? '/dashboard'} />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route index element={<Home />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="all-tickets" element={<AllTickets />} />
          <Route path="knowledge-base" element={<KnowledgeBase />} />
          <Route path="submit" element={<SubmitTicket />} />
          <Route path="settings" element={<Settings />} />
          <Route path="*" element={<Placeholder />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
