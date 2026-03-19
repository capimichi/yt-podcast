# yt-podcast

API FastAPI per convertire contenuti YouTube in feed podcast RSS e file audio scaricabili.

## Avvio rapido

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export YT_API_KEY=la_tua_chiave
python -m ytpodcast.api
```

Server di default: `http://0.0.0.0:8459`

Documentazione Swagger: `GET /docs`

## Endpoint API

### 1) Redirect docs

- **Metodo**: `GET`
- **Path**: `/`
- **Descrizione**: reindirizza alla documentazione Swagger (`/docs`).

Esempio:
```bash
curl -i http://localhost:8459/
```

### 2) Health check

- **Metodo**: `GET`
- **Path**: `/health`
- **Descrizione**: verifica rapida stato servizio.

Risposta 200:
```json
{
  "status": "ok"
}
```

Esempio:
```bash
curl http://localhost:8459/health
```

### 3) Dettagli canale

- **Metodo**: `GET`
- **Path**: `/channels/{identifier}`
- **Descrizione**: recupera i metadati di un canale YouTube.
- **Path param**:
  - `identifier`: ID canale (es. `UC...`) o handle supportato dalla logica del servizio.

Risposta 200 (JSON):
```json
{
  "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
  "title": "Google for Developers",
  "description": "Canale ufficiale...",
  "url": "https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw"
}
```

Esempio:
```bash
curl "http://localhost:8459/channels/UC_x5XG1OV2P6uZZ5FSM9Ttw"
```

### 4) Feed RSS XML del canale

- **Metodo**: `GET`
- **Path**: `/feeds/{channel_id}/xml`
- **Descrizione**: genera un feed RSS 2.0 con enclosure audio (`/videos/{video_id}/download`).
- **Content-Type**: `application/rss+xml`

Query params opzionali:
- `limit` (int, `>=1`): numero massimo di item.
- `offset` (int, `>=0`): offset sugli item.
- `fromDate` (datetime ISO 8601): include video pubblicati da questa data in poi.
- `toDate` (datetime ISO 8601): include video fino a questa data.
- `includeShorts` (bool, default `false`): include anche YouTube Shorts.

Esempio:
```bash
curl "http://localhost:8459/feeds/UC_x5XG1OV2P6uZZ5FSM9Ttw/xml?limit=20&includeShorts=false"
```

### 5) Dettagli video

- **Metodo**: `GET`
- **Path**: `/videos/{video_id}`
- **Descrizione**: recupera metadati video e informazioni audio selezionate.

Risposta 200 (JSON):
```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Titolo video",
  "description": "Descrizione video",
  "duration_seconds": 213,
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "channel_id": "UC...",
  "audio_format": "mp3",
  "audio_bitrate_kbps": 128
}
```

Esempio:
```bash
curl "http://localhost:8459/videos/dQw4w9WgXcQ"
```

### 6) Download audio video

- **Metodo**: `GET`
- **Path**: `/videos/{video_id}/download`
- **Descrizione**: restituisce il file audio se e' gia' pronto; in caso contrario crea o mantiene un placeholder a 0 byte e risponde che il download e' ancora in coda.
- **Risposta 200**: file binario (`FileResponse`) con `Content-Disposition: attachment; filename=...`.
- **Risposta 409**: JSON con `code=download_not_ready` e header `Retry-After: 60`.

Esempio:
```bash
curl -L "http://localhost:8459/videos/dQw4w9WgXcQ/download" -o audio.mp3
```

Esempio risposta non pronta:
```json
{
  "detail": {
    "code": "download_not_ready",
    "message": "Audio not ready yet.",
    "video_id": "dQw4w9WgXcQ"
  }
}
```

## Comando batch download pending

- Elabora tutti i placeholder audio a 0 byte presenti in `DOWNLOAD_DIR`.
- Usa lock su filesystem per evitare download concorrenti dello stesso video.

```bash
python -m ytpodcast.commands.process_pending_downloads
```

Il worker scarica ogni file pending in una directory temporanea e sostituisce il placeholder solo a download completato.

## Docker e aggiornamento yt-dlp

- L'immagine avvia `cron` insieme all'API.
- `yt-dlp` viene aggiornato automaticamente ogni ora tramite job schedulato nel container.

## Note

- L'API usa CORS permissivo (`*`).
- Le risposte del feed XML sono cache-ate lato server (TTL: 3 ore).
- Per test di integrazione esistono i test sotto `tests/integration/` (richiedono configurazione variabili ambiente, in particolare `YT_API_KEY`).
