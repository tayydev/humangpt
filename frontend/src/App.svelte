<script lang="ts">
  import { onMount } from 'svelte';

  interface Message {
    id: string;
    content: string;
    role: 'user' | 'assistant';
    timestamp: Date;
  }

  interface Chat {
    id: string;
    title: string;
    messages: Message[];
    createdAt: Date;
  }

  let chats: Chat[] = [];
  let currentChat: Chat | null = null;
  let newMessage: string = '';

  // Create initial chat
  onMount(() => {
    createNewChat();
  });

  function createNewChat() {
    const newChat: Chat = {
      id: crypto.randomUUID(),
      title: 'New Chat',
      messages: [],
      createdAt: new Date()
    };
    chats = [newChat, ...chats];
    currentChat = newChat;
  }

  function formatDate(date: Date): string {
    return date.toLocaleDateString();
  }

  function selectChat(chat: Chat) {
    currentChat = chat;
  }

  function handleSubmit() {
    if (!newMessage.trim() || !currentChat) return;

    // Add user message
    const userMessage: Message = {
      id: crypto.randomUUID(),
      content: newMessage,
      role: 'user',
      timestamp: new Date()
    };

    // Add to current chat
    currentChat.messages = [...currentChat.messages, userMessage];
    chats = [...chats];

    // Reset input
    newMessage = '';

    // Simulate AI response after a short delay
    setTimeout(() => {
      if (!currentChat) return;

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        content: "I'm an AI assistant. How can I help you today?",
        role: 'assistant',
        timestamp: new Date()
      };

      currentChat.messages = [...currentChat.messages, assistantMessage];
      
      // Update chat title based on first message if this is the first exchange
      if (currentChat.messages.length === 2 && currentChat.title === 'New Chat') {
        currentChat.title = userMessage.content.substring(0, 30) + (userMessage.content.length > 30 ? '...' : '');
      }
      
      chats = [...chats];
    }, 1000);
  }
</script>

<div class="chat-container">
  <aside class="sidebar">
    <div class="sidebar-header">
      <h3>Chats</h3>
      <button class="new-chat-btn" on:click={createNewChat}>New Chat</button>
    </div>
    <div class="chat-list">
      {#each chats as chat}
        <div 
          class="chat-item" 
          class:active={currentChat && currentChat.id === chat.id}
          on:click={() => selectChat(chat)}
        >
          <div class="chat-title">{chat.title}</div>
          <div class="chat-date">{formatDate(chat.createdAt)}</div>
        </div>
      {/each}
    </div>
  </aside>

  <main class="chat-main">
    {#if currentChat}
      <div class="chat-header">
        <h2>{currentChat.title}</h2>
      </div>
      <div class="messages-container">
        {#each currentChat.messages as message}
          <div class="message {message.role}">
            <div class="message-role">{message.role === 'user' ? 'You' : 'AI'}</div>
            <div class="message-content">{message.content}</div>
          </div>
        {/each}
      </div>
      <div class="input-container">
        <form on:submit|preventDefault={handleSubmit}>
          <textarea 
            bind:value={newMessage} 
            placeholder="Type your message here..." 
            rows="2"
            on:keydown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit();
              }
            }}
          ></textarea>
          <button type="submit" disabled={!newMessage.trim()}>Send</button>
        </form>
      </div>
    {:else}
      <div class="empty-state">
        <p>Select a chat or create a new one</p>
      </div>
    {/if}
  </main>
</div>

<style>
  .chat-container {
    display: flex;
    height: 100vh;
    width: 100%;
    overflow: hidden;
  }

  .sidebar {
    width: 280px;
    background-color: #202123;
    color: white;
    display: flex;
    flex-direction: column;
    border-right: 1px solid #444654;
  }

  .sidebar-header {
    padding: 16px;
    border-bottom: 1px solid #444654;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .new-chat-btn {
    background-color: #10a37f;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
  }

  .chat-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px;
  }

  .chat-item {
    padding: 12px;
    margin-bottom: 8px;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .chat-item:hover {
    background-color: #2a2b32;
  }

  .chat-item.active {
    background-color: #343541;
  }

  .chat-title {
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .chat-date {
    font-size: 12px;
    color: #8e8ea0;
    margin-top: 4px;
  }

  .chat-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: #343541;
    color: white;
  }

  .chat-header {
    padding: 16px;
    border-bottom: 1px solid #444654;
    text-align: center;
  }

  .messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .message {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 16px;
    border-radius: 8px;
  }

  .message.user {
    background-color: #444654;
    align-self: flex-end;
    max-width: 80%;
  }

  .message.assistant {
    background-color: #343541;
    border: 1px solid #444654;
    align-self: flex-start;
    max-width: 80%;
  }

  .message-role {
    font-weight: bold;
    font-size: 14px;
  }

  .message-content {
    font-size: 15px;
    line-height: 1.5;
    white-space: pre-wrap;
  }

  .input-container {
    padding: 16px;
    border-top: 1px solid #444654;
  }

  form {
    display: flex;
    gap: 8px;
    align-items: center;
  }

  textarea {
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    background-color: #40414f;
    border: none;
    resize: none;
    color: white;
    font-family: inherit;
    min-height: 44px;
  }

  textarea:focus {
    outline: none;
    box-shadow: 0 0 0 2px #10a37f;
  }

  button[type="submit"] {
    background-color: #10a37f;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0 16px;
    cursor: pointer;
    height: 44px;
    flex-shrink: 0;
  }

  button[type="submit"]:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #8e8ea0;
  }

  h2, h3 {
    margin: 0;
  }
</style>
