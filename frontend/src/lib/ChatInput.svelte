<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';

  let message = '';
  const dispatch = createEventDispatcher();

  // New props to control input state
  export let isAwaitingResponse = false;
  export let canSendMessage = true;

  // Animation frames for waiting text
  const frames = [
    "Awaiting response   ",
    "Awaiting response.  ",
    "Awaiting response.. ",
    "Awaiting response..."
  ];

  let currentFrame = 0;
  let intervalId: number | null = null;
  let displayText = frames[0];

  // Start and stop animation for awaiting response
  function startAnimation() {
    if (intervalId) return;

    currentFrame = 0;
    displayText = frames[currentFrame];

    intervalId = window.setInterval(() => {
      currentFrame = (currentFrame + 1) % frames.length;
      displayText = frames[currentFrame];
    }, 400);
  }

  function stopAnimation() {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  }

  // Watch for changes in isAwaitingResponse
  $: if (isAwaitingResponse && !intervalId) {
    startAnimation();
  } else if (!isAwaitingResponse && intervalId) {
    stopAnimation();
  }

  function handleSubmit() {
    if (!message.trim() || !canSendMessage) return;
    dispatch('submit', message);
    message = '';
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey && canSendMessage) {
      e.preventDefault();
      handleSubmit();
    }
  }
</script>

<div class="input-container">
  <form on:submit|preventDefault={handleSubmit}>
{#if isAwaitingResponse}
      <!-- Show animated waiting text when awaiting response -->
      <div class="awaiting-response" in:fade={{ duration: 200 }}>
        <span class="waiting-text">{displayText}</span>
      </div>
    {:else}
      <!-- Normal textarea when not awaiting response -->
      <textarea
        bind:value={message}
        placeholder="Type your message here..."
        rows="2"
        on:keydown={handleKeydown}
        disabled={!canSendMessage}
      ></textarea>
      <button
        type="submit"
        disabled={!message.trim() || !canSendMessage}
        aria-label="Send message"
      >
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    {/if}
  </form>
</div>

<style>
  .input-container {
    padding: 16px;
    border-top: 1px solid #444654;
    background-color: #343541;
  }
  
  /* Safari-specific styles */
  @supports (-webkit-touch-callout: none) {
    .input-container {
      position: relative;
      z-index: 5;
    }
  }

  form {
    display: flex;
    gap: 8px;
    align-items: center;
  }

  textarea {
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    background-color: #40414f;
    border: none;
    resize: none;
    color: white;
    font-family: inherit;
    min-height: 44px;
  }

  textarea:focus {
    outline: none;
    box-shadow: 0 0 0 2px #10a37f;
  }

  button[type="submit"] {
    background-color: #10a37f;
    color: white;
    border: none;
    border-radius: 999px;
    width: 36px;
    height: 36px;
    cursor: pointer;
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;
    padding: 0;
    line-height: 1;
    overflow: hidden;
  }

  button[type="submit"]:hover {
    background-color: #0c8063;
  }

  button[type="submit"]:disabled {
    background-color: #2a2b32;
    cursor: not-allowed;
  }

  button svg {
    width: 16px;
    height: 16px;
    position: relative;
    top: 0;
    left: 0;
    transform: translate(0, 0); /* Adjust if needed for perfect centering */
  }

  /* Styles for awaiting response indicator */
  .awaiting-response {
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    background-color: #40414f;
    min-height: 44px;
    display: flex;
    align-items: center;
  }

  .waiting-text {
    font-family: inherit;
    font-style: italic;
    color: #8e8ea0;
    font-size: 15px;
    white-space: pre;
  }
</style>
