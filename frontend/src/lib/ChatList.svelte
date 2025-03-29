<script lang="ts">
  import type { Chat } from './types';
  import ChatItem from './ChatItem.svelte';

  export let chats: Chat[];
  export let currentChat: Chat | null;

  function selectChat(chat: Chat) {
    dispatch('select', chat);
  }

  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
</script>

<div class="chat-list">
  {#each chats as chat}
    <ChatItem 
      {chat} 
      isActive={currentChat && currentChat.id === chat.id}
      on:click={() => selectChat(chat)}
    />
  {/each}
</div>

<style>
  .chat-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px;
  }
</style>