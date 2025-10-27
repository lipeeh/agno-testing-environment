import React from 'react'

const API_URL = process.env.NEXT_PUBLIC_AGENTOS_URL || ''

export default function Page() {
  return (
    <main style={{fontFamily:'ui-sans-serif, system-ui', padding: 24}}>
      <h1 style={{fontSize: 28, marginBottom: 8}}>Agno Agent UI</h1>
      <p style={{opacity: .8}}>Conectado ao backend AgentOS em:</p>
      <code style={{display:'inline-block', padding: 8, background:'#111', color:'#eee', borderRadius: 6}}>{API_URL}</code>

      <div style={{marginTop: 24}}>
        <a href={`${API_URL}/docs`} style={{marginRight:16}}>API Docs</a>
        <a href={`${API_URL}/health`}>Health</a>
      </div>

      <section style={{marginTop: 36}}>
        <h2 style={{fontSize: 20}}>Playground</h2>
        <p style={{opacity: .8}}>
          Esta é uma UI mínima. Para a UI completa (chat/teams/workflows), substituiremos por agno-agi/agent-ui.
        </p>
      </section>
    </main>
  )
}
