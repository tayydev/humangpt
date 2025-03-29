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
    <button type="submit" disabled={!message.trim()}>Send</button>
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
    border-radius: 8px;
    padding: 0 16px;
    cursor: pointer;
    height: 44px;
    flex-shrink: 0;
  }

  button[type="submit"]:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
</style>