<script lang="ts">
  import ChatList from './ChatList.svelte';

  export let chats: Session[];
  export let currentChat: Session | null;
  export let isSidebarOpen = true;

  import { createEventDispatcher } from 'svelte';
  import type {Session} from "humangpt-client";
  const dispatch = createEventDispatcher();

  function createNewChat() {
    dispatch('newchat');
  }

  function handleSelectChat(event: CustomEvent<Session>) {
    dispatch('select', event.detail);
    // Auto-close sidebar on mobile after selecting a chat
    if (window.innerWidth <= 768) {
      dispatch('toggleSidebar');
    }
  }

  function toggleSidebar() {
    dispatch('toggleSidebar');
  }
</script>

<aside class="sidebar" class:open={isSidebarOpen}>
  <div class="sidebar-header">
    <h3>Chats</h3>
    <button class="new-chat-btn" on:click={createNewChat}>New Chat</button>
  </div>
  <button class="close-sidebar-btn" on:click={toggleSidebar}>×</button>
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
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    position: relative;
  }

  .close-sidebar-btn {
    display: none;
    position: absolute;
    top: 12px;
    right: 10px;
    background: transparent;
    border: none;
    color: white;
    font-size: 24px;
    padding: 0;
    cursor: pointer;
    z-index: 10;
  }

  .sidebar-header {
    padding: 15px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    height: 56px;
    box-sizing: border-box;
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

  /* Mobile styles */
  @media (max-width: 768px) {
    .sidebar {
      position: fixed;
      top: 0;
      left: -280px;
      height: 100%;
      z-index: 1000;
      transition: left 0.3s ease;
      box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
    }

    .sidebar.open {
      left: 0;
    }

    .close-sidebar-btn {
      display: block;
    }
  }
</style>
