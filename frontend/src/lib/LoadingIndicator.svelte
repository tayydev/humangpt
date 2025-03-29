<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fade } from 'svelte/transition';

  export let visible = false;

  // Animation frames
  const frames = [
    "(awaiting response)",
    // "awaiting response.  ",
    // "awaiting response.. ",
    // "awaiting response..."
  ];

  let currentFrame = 0;
  let intervalId: number | null = null;
  let displayText = frames[0];

  function startAnimation() {
    if (intervalId) return;

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

  $: if (visible && !intervalId) {
    startAnimation();
  } else if (!visible && intervalId) {
    stopAnimation();
  }

  onMount(() => {
    if (visible) startAnimation();
  });

  onDestroy(() => {
    stopAnimation();
  });
</script>

{#if visible}
<div class="loading-indicator" in:fade={{ duration: 200 }} out:fade={{ duration: 50 }}>
  <span class="ascii-animation">{displayText}</span>
</div>
{/if}

<style>
  .loading-indicator {
    background-color: #343541;
    border: 1px solid #444654;
    padding: 10px 14px;
    margin-top: 16px;
    align-self: flex-start;
    border-radius: 8px;
  }

  .ascii-animation {
    font-family: inherit;
    font-style: italic;
    color: #8e8ea0;
    font-size: 13px;
    white-space: pre;
  }
</style>
