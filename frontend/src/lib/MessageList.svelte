<script lang="ts">
  import type { Message } from './types';
  import MessageComponent from './Message.svelte';
  import InlineWaitingMessage from './InlineWaitingMessage.svelte';
  import LoadingIndicator from './LoadingIndicator.svelte';
  import { createEventDispatcher } from 'svelte';

  export let messages: Message[];
  export let showWaitingMessage = false;
  export let skipWaitingAnimation = false;
  export let isAwaitingResponse = false;

  const dispatch = createEventDispatcher();

  function handleCloseWaitingMessage() {
    dispatch('closeWaiting');
  }
</script>

<div class="messages-container">
  <div class="messages-list">
    {#each messages as message}
      <MessageComponent {message} />
    {/each}
    
    <!-- Simple ASCII animation loading indicator -->
    <LoadingIndicator visible={isAwaitingResponse} />
  </div>

  <div class="waiting-message-container">
    <InlineWaitingMessage
      visible={showWaitingMessage}
      skipAnimation={skipWaitingAnimation}
      on:close={handleCloseWaitingMessage}
    />
  </div>
</div>

<style>
  .messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
  }

  .messages-list {
    display: flex;
    flex-direction: column;
    gap: 24px;
    margin-bottom: 16px;
  }

  /* Loading indicator is now included directly in messages-list */

  .waiting-message-container {
    margin-top: auto;
  }
</style>
