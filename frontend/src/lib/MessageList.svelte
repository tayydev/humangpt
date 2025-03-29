<script lang="ts">
  import type { Message } from './types';
  import MessageComponent from './Message.svelte';

  export let messages: Message[];
</script>

<div class="messages-container">
  {#each messages as message}
    <MessageComponent {message} />
  {/each}
</div>

<style>
  .messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
</style>