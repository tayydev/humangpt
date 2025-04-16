// API Client setup

// Direct imports from client source files since the client package isn't built
import {DefaultApi, type Message} from "humangpt-client";
import { Configuration } from "humangpt-client";

// Default API base path with environment variable override
const API_BASE_PATH = import.meta.env.VITE_API_BASE_PATH || 'https://api.humangpt.dev';

// Create a singleton instance of the API client
const config = new Configuration({
  basePath: API_BASE_PATH
});

//claude garbage:
export class WSClient {
  private ws: WebSocket | null = null;
  private msgListeners: ((msg: Message) => void)[] = [];
  private connListeners: ((status: boolean) => void)[] = [];
  private connected = false;
  private reconnTimer: number | null = null;

  constructor(private sessionId: string, private clientId: string) {}

  connect(baseUrl = window.location.origin.replace('http', 'ws')): void {
    if (this.ws) this.ws.close();
    if (this.reconnTimer) clearTimeout(this.reconnTimer);

    const url = `${baseUrl}/ws/session?session_id=${this.sessionId}&client_id=${this.clientId}`;
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      this.connected = true;
      this.notifyConn(true);
    };

    this.ws.onmessage = (e) => {
      try {
        this.notifyMsg(JSON.parse(e.data));
      } catch (err) {
        console.error('WS parse error:', err);
      }
    };

    this.ws.onclose = () => {
      this.connected = false;
      this.notifyConn(false);
      this.reconnTimer = window.setTimeout(() => this.connect(baseUrl), 3000);
    };

    this.ws.onerror = () => this.ws?.close();
  }

  disconnect(): void {
    if (this.reconnTimer) clearTimeout(this.reconnTimer);
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  send(msg: Message): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.error('Cannot send: WS not connected');
      return;
    }
    this.ws.send(JSON.stringify(msg));
  }

  onMessage(cb: (msg: Message) => void): () => void {
    this.msgListeners.push(cb);
    return () => {
      this.msgListeners = this.msgListeners.filter(l => l !== cb);
    };
  }

  onConnection(cb: (status: boolean) => void): () => void {
    this.connListeners.push(cb);
    cb(this.connected);
    return () => {
      this.connListeners = this.connListeners.filter(l => l !== cb);
    };
  }

  isConnected(): boolean {
    return this.connected;
  }

  private notifyMsg(msg: Message): void {
    this.msgListeners.forEach(cb => cb(msg));
  }

  private notifyConn(status: boolean): void {
    this.connListeners.forEach(cb => cb(status));
  }
}


export const apiClient = new DefaultApi(config);
