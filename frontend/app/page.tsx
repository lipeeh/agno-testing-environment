'use client'

import { useState } from 'react'
import { Settings, MessageCircle, Bot } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_AGENTOS_URL || 'https://agno.gohorse.srv.br'

export default function AgentUI() {
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [endpoint, setEndpoint] = useState(API_URL)
  const [showSettings, setShowSettings] = useState(false)

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const newMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, newMessage])
    setInput('')
    setLoading(true)

    try {
      // This would integrate with AgentOS API
      // For now, mock response
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Echo from ${endpoint}: ${newMessage.content}`
      }])
    } catch (error) {
      console.error('Failed to send message:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <div className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 p-4">
        <div className="flex items-center gap-2 mb-6">
          <Bot className="w-6 h-6 text-blue-600" />
          <h1 className="font-bold text-lg">Agno UI</h1>
        </div>
        
        <div className="space-y-2">
          <button 
            onClick={() => setShowSettings(!showSettings)}
            className="flex items-center gap-2 w-full p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <Settings className="w-4 h-4" />
            Settings
          </button>
          
          {showSettings && (
            <div className="pl-6 space-y-2">
              <div>
                <label className="text-sm text-gray-600 dark:text-gray-300">Endpoint:</label>
                <input 
                  value={endpoint}
                  onChange={(e) => setEndpoint(e.target.value)}
                  className="w-full mt-1 p-1 text-xs border rounded dark:bg-gray-700 dark:border-gray-600"
                />
              </div>
            </div>
          )}
          
          <div className="pt-4 border-t border-gray-200 dark:border-gray-600">
            <div className="text-xs text-gray-500 dark:text-gray-400 space-y-1">
              <div>Status: Connected</div>
              <div>Backend: {endpoint}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="border-b border-gray-200 dark:border-gray-700 p-4">
          <div className="flex items-center gap-2">
            <MessageCircle className="w-5 h-5" />
            <h2 className="font-semibold">Chat with Agents</h2>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 dark:text-gray-400 mt-8">
              <Bot className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>Start a conversation with your agents</p>
              <p className="text-sm mt-2">Connected to: {endpoint}</p>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message, i) => (
                <div key={i} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                    message.role === 'user' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600'
                  }`}>
                    {message.content}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg px-4 py-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Input */}
        <div className="border-t border-gray-200 dark:border-gray-700 p-4">
          <div className="flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Type your message..."
              className="flex-1 p-2 border border-gray-300 dark:border-gray-600 rounded-md dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
