<script lang="ts">
  import ChatList from './ChatList.svelte';

  export let chats: Session[];
  export let currentSession: SessionDTO | null;
  export let isSidebarOpen = true;

  import { createEventDispatcher } from 'svelte';
  import type {Session, SessionDTO} from "humangpt-client";
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
    {currentSession}
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
    color: #9ca3af;
    font-size: 20px;
    width: 28px;
    height: 28px;
    border-radius: 4px;
    cursor: pointer;
    z-index: 10;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s ease, color 0.2s ease;
    padding: 0;
  }

  .close-sidebar-btn:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
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

  @media (max-width: 768px) {
    .sidebar-header {
      padding-right: 60px; /* Increase padding to prevent overlap */
    }

    .new-chat-btn {
      margin-right: 12px; /* Add more margin to the new chat button */
      font-size: 0.95rem; /* Slightly reduce button text size */
      padding: 7px 10px; /* Slightly reduce button padding */
    }
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
      display: flex;
    }
  }
</style>
