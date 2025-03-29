<script lang="ts">
  import type { Chat } from './types';
  import ChatList from './ChatList.svelte';

  export let chats: Chat[];
  export let currentChat: Chat | null;

  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function createNewChat() {
    dispatch('newchat');
  }

  function handleSelectChat(event: CustomEvent<Chat>) {
    dispatch('select', event.detail);
  }
</script>

<aside class="sidebar">
  <div class="sidebar-header">
    <h3>Chats</h3>
    <button class="new-chat-btn" on:click={createNewChat}>New Chat</button>
  </div>
  <ChatList 
    {chats} 
    {currentChat} 
    on:select={handleSelectChat}
  />
</aside>

<style>
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

  h3 {
    margin: 0;
  }
</style>