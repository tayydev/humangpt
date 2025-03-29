<script lang="ts">
  import type { Session } from './types';
  import ChatItem from './ChatItem.svelte';
  import { createEventDispatcher } from 'svelte';
  
  export let chats: Session[];
  export let currentChat: Session | null;
  
  const dispatch = createEventDispatcher();

  function selectChat(chat: Session) {
    dispatch('select', chat);
  }
</script>

<div class="chat-list">
  {#each chats as chat}
    <ChatItem 
      {chat} 
      isActive={currentChat && currentChat.uuid === chat.uuid}
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