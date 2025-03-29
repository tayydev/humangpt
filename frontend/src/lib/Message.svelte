<script lang="ts">
  import type { Message } from './types';

  export let message: Message;
</script>

<div class="message {message.role}">
  <div class="message-role">{message.role === 'user' ? 'You' : 'AI'}</div>
  <div class="message-content">{message.content}</div>
</div>

<style>
  .message {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 16px;
    border-radius: 8px;
  }

  .message.user {
    background-color: #444654;
    align-self: flex-end;
    max-width: 80%;
  }

  .message.assistant {
    background-color: #343541;
    border: 1px solid #444654;
    align-self: flex-start;
    max-width: 80%;
  }

  .message-role {
    font-weight: bold;
    font-size: 14px;
  }

  .message-content {
    font-size: 15px;
    line-height: 1.5;
    white-space: pre-wrap;
  }
</style>