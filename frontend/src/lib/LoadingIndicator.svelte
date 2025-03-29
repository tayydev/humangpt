<script lang="ts">
  import { fade } from 'svelte/transition';
  export let visible = false;
</script>

{#if visible}
<div class="loading-indicator" in:fade={{ duration: 150, delay: 0 }} out:fade={{ duration: 150 }}>
  <div class="dot-pulse"></div>
  <span class="awaiting-text">awaiting response</span>
</div>
{/if}

<style>
  .loading-indicator {
    background-color: #343541;
    border: 1px solid #444654;
    padding: 16px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
    width: fit-content;
    margin-top: 24px;
    margin-left: 0;
    align-self: flex-start;
    z-index: 10;
    position: relative;
  }

  .awaiting-text {
    font-style: italic;
    color: #c5c5d2;
    font-size: 14px;
  }

  /* Dot pulse animation */
  .dot-pulse {
    position: relative;
    width: 10px;
    height: 10px;
    border-radius: 5px;
    background-color: #10a37f;
    animation: pulse 1.5s infinite;
  }

  .dot-pulse::before,
  .dot-pulse::after {
    content: '';
    position: absolute;
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 5px;
    background-color: #10a37f;
    animation: pulse 1.5s infinite;
  }

  .dot-pulse::before {
    left: -15px;
    animation-delay: 0s;
  }

  .dot-pulse::after {
    left: 15px;
    animation-delay: 0.5s;
  }

  @keyframes pulse {
    0% {
      opacity: 0.6;
      transform: scale(0.8);
    }
    50% {
      opacity: 1;
      transform: scale(1);
    }
    100% {
      opacity: 0.6;
      transform: scale(0.8);
    }
  }
</style>