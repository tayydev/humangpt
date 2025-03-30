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

  // Scroll to bottom of messages container
  function scrollToBottom() {
    if (messagesContainer) {
      messagesContainer.scrollTo({
        top: messagesContainer.scrollHeight,
        behavior: 'smooth'
      });
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
    <!-- No longer using LoadingIndicator in the message list -->
  </div>

  <div class="waiting-message-container">
    <InlineWaitingMessage
      visible={showWaitingMessage}
      skipAnimation={skipWaitingAnimation}
      user={user}
      on:close={handleCloseWaitingMessage}
    />
  </div>
</div>

<style>
  .messages-container {
    position: absolute;
    top: 56px; /* Height of the header */
    bottom: 77px; /* Height of the input container */
    left: 0;
    right: 0;
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
      /* Fix iOS scrolling */
      -webkit-overflow-scrolling: touch;
    }
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
    display: flex;
    justify-content: center;
    width: 100%;
    position: relative;
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
