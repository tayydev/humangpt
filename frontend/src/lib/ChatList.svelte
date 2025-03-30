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

  // Sort function to order chats by creation date, newest first
  $: sortedChats = [...chats].sort((a, b) => {
    // Try to use created_timestamp first
    if (a.updated_timestamp && b.updated_timestamp) {
      return new Date(b.updated_timestamp).getTime() - new Date(a.updated_timestamp).getTime();
    }

    // If no timestamps available, keep original order
    return 0;
  });
</script>

<div class="chat-list">
  {#each sortedChats as chat}
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
