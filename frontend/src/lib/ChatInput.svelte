<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  
  let message = '';
  const dispatch = createEventDispatcher();

  function handleSubmit() {
    if (!message.trim()) return;
    dispatch('submit', message);
    message = '';
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }
</script>

<div class="input-container">
  <form on:submit|preventDefault={handleSubmit}>
    <textarea 
      bind:value={message} 
      placeholder="Type your message here..." 
      rows="2"
      on:keydown={handleKeydown}
    ></textarea>
    <button type="submit" disabled={!message.trim()} aria-label="Send message">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </form>
</div>

<style>
  .input-container {
    padding: 16px;
    border-top: 1px solid #444654;
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
</style>