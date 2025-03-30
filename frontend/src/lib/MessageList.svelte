<script lang="ts">
  import type { Message } from './types';
  import MessageComponent from './Message.svelte';
  import InlineWaitingMessage from './InlineWaitingMessage.svelte';
  import { createEventDispatcher, onMount, afterUpdate } from 'svelte';
  import type {UserPublic} from "humangpt-client";

  export let user: UserPublic;

  export let messages: Message[];
  export let showWaitingMessage = false;
  export let skipWaitingAnimation = false;
  // We no longer need isAwaitingResponse in this component



  const dispatch = createEventDispatcher();
  let messagesContainer: HTMLElement;

  // Scroll to bottom of messages container with better visibility for waiting message
  function scrollToBottom() {
    if (messagesContainer) {
      // Delayed scroll to ensure waiting message is rendered
      setTimeout(() => {
        messagesContainer.scrollTo({
          top: messagesContainer.scrollHeight,
          behavior: 'smooth'
        });
      }, 10);
    }
  }

  // After any update, scroll to bottom
  afterUpdate(() => {
    scrollToBottom();
  });

  function handleCloseWaitingMessage() {
    dispatch('closeWaiting');
  }
</script>

<div class="messages-container" bind:this={messagesContainer}>
  <div class="messages-list">
    {#each messages as message}
      <MessageComponent {message} />
    {/each}
    <!-- Include waiting message as part of the scrollable content -->
    {#if showWaitingMessage}
      <div class="waiting-message-container">
        <InlineWaitingMessage
          visible={true}
          skipAnimation={skipWaitingAnimation}
          user={user}
          on:close={handleCloseWaitingMessage}
        />
      </div>
    {/if}
  </div>
</div>

<style>
  .messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    max-width: 100%;
    -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
  }
  
  /* iOS-specific adjustments */
  @supports (-webkit-touch-callout: none) {
    .messages-container {
      overflow-x: hidden;
      -webkit-box-sizing: border-box;
      box-sizing: border-box;
      /* Ensure smooth scrolling with momentum on iOS */
      -webkit-overflow-scrolling: touch;
      /* Prevent bouncing effects that cause whole page scrolling */
      overscroll-behavior: contain;
      /* Improve performance */
      -webkit-transform: translateZ(0);
    }
  }

  .messages-list {
    display: flex;
    flex-direction: column;
    gap: 24px;
    width: 100%;
  }

  /* Loading indicator is now included directly in messages-list */

  .waiting-message-container {
    display: flex;
    justify-content: center;
    width: 100%;
    margin: 16px 0;
    /* Fix iOS width issues */
    max-width: 100vw;
    overflow-x: hidden;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
  }
  
  /* iOS-specific adjustments */
  @supports (-webkit-touch-callout: none) {
    .waiting-message-container {
      width: 95vw; /* Slightly narrower on iOS */
      margin-left: auto;
      margin-right: auto;
    }
  }
</style>
