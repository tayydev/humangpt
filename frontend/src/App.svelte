<script lang="ts">
  import type { Chat, Message } from './lib/types';
  import Sidebar from './lib/Sidebar.svelte';
  import ChatHeader from './lib/ChatHeader.svelte';
  import MessageList from './lib/MessageList.svelte';
  import ChatInput from './lib/ChatInput.svelte';
  import AnimatedNames from './lib/AnimatedNames.svelte';

  let chats: Chat[] = [];
  let currentChat: Chat | null = null;

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

  function selectChat(event: CustomEvent<Chat>) {
    currentChat = event.detail;
  }

  function handleMessageSubmit(event: CustomEvent<string>) {
    const messageContent = event.detail;
    
    if (!currentChat) {
      // Create a new chat if none exists
      createNewChat();
    }
    
    // Add user message
    const userMessage: Message = {
      id: crypto.randomUUID(),
      content: messageContent,
      role: 'user',
      timestamp: new Date()
    };

    // Add to current chat
    currentChat.messages = [...currentChat.messages, userMessage];
    chats = [...chats];

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
  <Sidebar 
    {chats} 
    {currentChat} 
    on:newchat={createNewChat} 
    on:select={selectChat}
  />

  <main class="chat-main">
    {#if currentChat}
      <ChatHeader title={currentChat.title} />
      <MessageList messages={currentChat.messages} />
      <ChatInput on:submit={handleMessageSubmit} />
    {:else}
      <div class="empty-state">
        <div class="welcome-container">
          <h1>HumanGPT</h1>
          <p class="welcome-text">How can <AnimatedNames /> help you today?</p>
          <div class="centered-input">
            <ChatInput on:submit={handleMessageSubmit} />
          </div>
        </div>
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

  .chat-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: #343541;
    color: white;
  }

  .empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #8e8ea0;
  }

  .welcome-container {
    max-width: 600px;
    text-align: center;
  }

  .welcome-container h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: #10a37f;
  }

  .welcome-text {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    color: #c5c5d2;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.2em;
  }

  .centered-input {
    width: 100%;
  }
</style>