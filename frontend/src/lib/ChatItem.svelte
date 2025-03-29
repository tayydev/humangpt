<script lang="ts">
  import type { Chat } from './types';

  export let chat: Chat;
  export let isActive: boolean;

  function formatDate(date: Date): string {
    return date.toLocaleDateString();
  }
</script>

<div 
  class="chat-item" 
  class:active={isActive}
  on:click
>
  <div class="chat-title">{chat.title}</div>
  <div class="chat-date">{formatDate(chat.createdAt)}</div>
</div>

<style>
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
</style>