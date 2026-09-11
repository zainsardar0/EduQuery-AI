import { lazy, Suspense, useEffect, useState } from 'react'

const DashboardPage = lazy(() => import('./dashboard/DashboardPage'))
const AppShell = lazy(() => import('./app/AppShell'))

const readRoute = () => {
  const h = window.location.hash
  if (h === '#/dashboard') return 'dashboard'
  return 'app'
}

export default function App() {
  const [route, setRoute] = useState(readRoute)

  useEffect(() => {
    const onHash = () => setRoute(readRoute())
    window.addEventListener('hashchange', onHash)
    return () => window.removeEventListener('hashchange', onHash)
  }, [])

  return (
    <Suspense
      fallback={
        <div className="flex h-dvh items-center justify-center bg-zinc-50 dark:bg-zinc-950 text-sm text-zinc-400 font-mono">
          Loading EduQuery AI Intelligence Suite...
        </div>
      }
    >
      {route === 'dashboard' ? (
        <DashboardPage onNavigate={(id) => (window.location.hash = id === 'dashboard' ? '#/dashboard' : '#/app')} />
      ) : (
        <AppShell onBack={() => (window.location.hash = '#/dashboard')} />
      )}
    </Suspense>
  )
}
