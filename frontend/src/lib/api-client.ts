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

// WebSocket client using Svelte runes
export function createWebSocketClient(sessionId: string, clientId: string) {
  let ws: WebSocket | null = null;
  let connected = false;
  let reconnTimer: number | null = null;
  let messages: Message[] = [];
  
  // This will need to be called from a component with $effect
  function connect(baseUrl = window.location.origin.replace('http', 'ws')) {
    if (ws) ws.close();
    if (reconnTimer) clearTimeout(reconnTimer);
    
    const url = `${baseUrl}/ws/session?session_id=${sessionId}&client_id=${clientId}`;
    ws = new WebSocket(url);
    
    ws.onopen = () => {
      connected = true;
    };
    
    ws.onmessage = (e) => {
      try {
        const msg = JSON.parse(e.data);
        messages = [...messages, msg];
      } catch (err) {
        console.error('WS parse error:', err);
      }
    };
    
    ws.onclose = () => {
      connected = false;
      reconnTimer = window.setTimeout(() => connect(baseUrl), 3000);
    };
    
    ws.onerror = () => ws?.close();
  }
  
  function disconnect() {
    if (reconnTimer) clearTimeout(reconnTimer);
    if (ws) {
      ws.close();
      ws = null;
    }
  }
  
  function send(msg: Message) {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      console.error('Cannot send: WS not connected');
      return;
    }
    ws.send(JSON.stringify(msg));
  }
  
  return {
    get connected() { return connected; },
    get messages() { return messages; },
    connect,
    disconnect,
    send
  };
}

export const apiClient = new DefaultApi(config);
