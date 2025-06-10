// pages/dms.tsx
import { useEffect, useState } from 'react'

type DirectMessage = {
  id: number
  sender: number
  receiver: number
  message: string
  timestamp: string
  is_read: boolean
}

export default function DirectMessagesPage() {
  const [messages, setMessages] = useState<DirectMessage[]>([])
  const [newMessage, setNewMessage] = useState('')
  const [receiverId, setReceiverId] = useState<number | ''>('')
  const [error, setError] = useState('')
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null

  useEffect(() => {
    if (!token) return

    const fetchMessages = async () => {
      try {
        const res = await fetch(
          'https://world-beats-backend.onrender.com/api/dms/direct-messages/',
          { headers: { Authorization: `Bearer ${token}` } }
        )
        if (!res.ok) throw new Error()
        const data = await res.json()
        setMessages(data)
      } catch {
        setError('📩 メッセージ取得に失敗しました')
      }
    }

    fetchMessages()
  }, [token])

  const handleSend = async () => {
    setError('')

    if (!receiverId || !newMessage.trim()) {
      setError('宛先ユーザーIDとメッセージを入力してください')
      return
    }

    try {
      const res = await fetch(
        'https://world-beats-backend.onrender.com/api/dms/direct-messages/',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ receiver: receiverId, message: newMessage }),
        }
      )

      if (!res.ok) throw new Error()
      const sent = await res.json()
      setMessages(prev => [sent, ...prev])
      setNewMessage('')
      setReceiverId('')
    } catch {
      setError('📤 メッセージ送信に失敗しました')
    }
  }

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">📨 ダイレクトメッセージ</h1>

      {error && <p className="text-red-600 mb-2">{error}</p>}

      <div className="space-y-2 mb-6">
        <input
          type="number"
          placeholder="宛先ユーザーID"
          value={receiverId}
          onChange={e => setReceiverId(Number(e.target.value))}
          className="w-full border p-2 rounded"
        />
        <textarea
          placeholder="メッセージ内容"
          value={newMessage}
          onChange={e => setNewMessage(e.target.value)}
          rows={3}
          className="w-full border p-2 rounded"
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          送信
        </button>
      </div>

      <h2 className="text-xl font-semibold mb-2">📥 受信メッセージ</h2>
      <ul className="space-y-4">
        {messages.map(msg => (
          <li key={msg.id} className="border p-3 rounded bg-white">
            <p><strong>From:</strong> ユーザーID {msg.sender}</p>
            <p>{msg.message}</p>
            <p className="text-sm text-gray-500">
              {new Date(msg.timestamp).toLocaleString()}
            </p>
          </li>
        ))}
      </ul>
    </div>
  )
}
