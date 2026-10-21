import { useState, type FormEvent } from 'react';
import { api } from './api';

export default function App() {
  const [url, setUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [error, setError] = useState('');

  async function shorten(e: FormEvent) {
    e.preventDefault();
    setError('');
    try {
      const link = await api<{ short_url: string }>('/links', {
        method: 'POST',
        body: JSON.stringify({ url }),
      });
      setShortUrl(link.short_url);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div>
      <form onSubmit={shorten}>
        <input value={url} onChange={(e) => setUrl(e.target.value)} />
        <button>Shorten</button>
      </form>
      {error && <p>{error}</p>}
      {shortUrl && <p>{shortUrl}</p>}
    </div>
  );
}
