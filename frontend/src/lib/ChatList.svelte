<script lang="ts">
  import type { Session } from './types';
  import ChatItem from './ChatItem.svelte';
  import { createEventDispatcher } from 'svelte';
  import type {SessionDTO} from "humangpt-client";

  export let chats: Session[];
  export let currentSession: SessionDTO | null;

  const dispatch = createEventDispatcher();

  function selectChat(chat: Session) {
    dispatch('select', chat);
  }

  // Sort function to order chats by creation date, newest first
  $: sortedChats = [...chats].sort((a, b) => {
    // Try to use created_timestamp first
    if (a.created_at && b.created_at) {
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    }

    // If no timestamps available, keep original order
    return 0;
  });
</script>

<div class="chat-list">
  {#each sortedChats as chat}
    <ChatItem
      {chat}
      isActive={(currentSession && currentSession.uuid === chat.uuid) ?? false}
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
