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

<div class="welcome-input-container">
  <form on:submit|preventDefault={handleSubmit}>
    <textarea 
      bind:value={message} 
      placeholder="Type your message here..." 
      rows="1"
      on:keydown={handleKeydown}
    ></textarea>
    <button type="submit" disabled={!message.trim()} aria-label="Send message">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </form>
</div>

<style>
  .welcome-input-container {
    width: 100%;
    padding: 0;
    border-radius: 24px;
    background-color: #40414f;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  }

  form {
    display: flex;
    gap: 8px;
    align-items: center;
    padding: 6px 16px;
  }

  textarea {
    width: 100%;
    padding: 10px 0;
    background-color: transparent;
    border: none;
    resize: none;
    color: white;
    font-family: inherit;
    min-height: 24px;
    font-size: 1rem;
    line-height: 1.5;
  }

  textarea:focus {
    outline: none;
  }

  button[type="submit"] {
    background-color: #10a37f;
    color: white;
    border: none;
    border-radius: 999px;
    width: 32px;
    height: 32px;
    cursor: pointer;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;
    padding: 0;
  }

  button[type="submit"]:hover {
    background-color: #0c8063;
  }

  button[type="submit"]:disabled {
    background-color: #1e1e2b;
    cursor: not-allowed;
  }

  button svg {
    width: 16px;
    height: 16px;
  }
</style>