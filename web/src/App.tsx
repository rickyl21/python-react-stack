import { useEffect, useState, type FormEvent } from 'react';
import { api } from './api';

type Item = { id: number; name: string; created_at: number };

export default function App() {
  const [health, setHealth] = useState<string>('checking…');
  const [items, setItems] = useState<Item[]>([]);
  const [name, setName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api<{ ok: boolean; time: string }>('/health')
      .then((h) => setHealth(h.ok ? `API ok (${h.time})` : 'API not ok'))
      .catch((e) => setHealth(`API unreachable: ${e.message}`));

    api<Item[]>('/items')
      .then(setItems)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function addItem(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      const item = await api<Item>('/items', {
        method: 'POST',
        body: JSON.stringify({ name }),
      });
      setItems((prev) => [item, ...prev]);
      setName('');
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function removeItem(id: number) {
    setError(null);
    try {
      await api<void>(`/items/${id}`, { method: 'DELETE' });
      setItems((prev) => prev.filter((i) => i.id !== id));
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <main className="app">
      <h1>Interview template</h1>
      <p className="health">{health}</p>

      <form onSubmit={addItem} className="row">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="New item"
          aria-label="Item name"
        />
        <button type="submit">Add</button>
      </form>

      {error && <p className="error">{error}</p>}

      {loading ? (
        <p>Loading…</p>
      ) : items.length === 0 ? (
        <p className="muted">No items yet.</p>
      ) : (
        <ul className="list">
          {items.map((item) => (
            <li key={item.id}>
              <span>{item.name}</span>
              <button onClick={() => removeItem(item.id)} aria-label={`Delete ${item.name}`}>
                ×
              </button>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
