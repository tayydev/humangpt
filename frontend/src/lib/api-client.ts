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

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private connected: boolean = false;
  private reconnTimer: number | null = null;
  private messages: Message[] = [];
  private readonly sessionId: string;
  private baseUrl: string;
  private messageQueue: Message[] = [];

  constructor(sessionId: string, baseUrl?: string) {
    this.sessionId = sessionId;
    this.baseUrl = baseUrl || API_BASE_PATH.replace("http", "ws");
  }

  public connect(): void {
    this.cleanup();

    const url = `${this.baseUrl}/ws/session?session_id=${this.sessionId}`;

    console.log("connecting websocket to url:", url)

    this.ws = new WebSocket(url);

    this.ws.onopen = this.handleOpen.bind(this);
    this.ws.onmessage = this.handleMessage.bind(this);
    this.ws.onclose = this.handleClose.bind(this);
    this.ws.onerror = this.handleError.bind(this);
  }

  public disconnect(): void {
    this.cleanup();
    this.ws = null;
  }

  /**
   * Sends a message through the WebSocket.
   * If the socket is not connected, the message is automatically queued.
   * @param msg The message to send
   * @returns Whether the message was sent immediately (true) or queued (false)
   */
  public send(msg: Message): boolean {
    if (!this.isConnected()) {
      this.messageQueue.push(msg);
      console.log(`Message queued. Queue length: ${this.messageQueue.length}`);
      return false;
    }

    try {
      this.ws!.send(JSON.stringify(msg));
      return true;
    } catch (error) {
      console.error("Failed to send message:", error);
      this.messageQueue.push(msg);
      return false;
    }
  }

  /**
   * Clears all queued messages without sending them.
   * @returns The number of messages cleared
   */
  public clearQueue(): number {
    const count = this.messageQueue.length;
    this.messageQueue = [];
    return count;
  }

  /**
   * Gets the current number of queued messages.
   */
  public getQueueLength(): number {
    return this.messageQueue.length;
  }

  public isConnected(): boolean {
    return this.connected && this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }

  public getMessages(): Message[] {
    return [...this.messages]; // Return a copy to prevent external modification
  }

  public clearMessages(): void {
    this.messages = [];
  }

  private handleOpen(): void {
    this.connected = true;
    this.flushQueue();
  }

  private handleMessage(event: MessageEvent): void {
    try {
      const msg = JSON.parse(event.data);
      this.messages.push(msg);
    } catch (err) {
      console.error("WS parse error:", err);
    }
  }

  private handleClose(): void {
    this.connected = false;
    this.scheduleReconnect();
  }

  private handleError(): void {
    this.ws?.close();
  }

  private scheduleReconnect(): void {
    if (this.reconnTimer) {
      clearTimeout(this.reconnTimer);
    }
    this.reconnTimer = window.setTimeout(() => this.connect(), 3000);
  }

  private cleanup(): void {
    if (this.reconnTimer) {
      clearTimeout(this.reconnTimer);
      this.reconnTimer = null;
    }

    if (this.ws) {
      this.ws.onopen = null;
      this.ws.onmessage = null;
      this.ws.onclose = null;
      this.ws.onerror = null;
      this.ws.close();
    }
  }

  /**
   * Attempts to send all queued messages.
   * @returns The number of messages successfully sent
   */
  private flushQueue(): number {
    console.log("attempting to flush queue")
    if (!this.isConnected()) {
      return 0;
    }

    let sentCount = 0;
    while (this.messageQueue.length > 0) {
      const msg = this.messageQueue.shift()!;

      try {
        this.ws!.send(JSON.stringify(msg));
        sentCount++;
      } catch (error) {
        console.error("Failed to send queued message:", error);
        // Put the message back at the front of the queue
        this.messageQueue.unshift(msg);
        break;
      }
    }

    if (sentCount > 0) {
      console.log(`Flushed ${sentCount} queued messages.`);
    }

    return sentCount;
  }
}




export const apiClient = new DefaultApi(config);
