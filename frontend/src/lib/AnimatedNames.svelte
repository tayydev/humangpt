<script lang="ts">
  import { onMount } from 'svelte';
  import { fly } from 'svelte/transition';

  const names = ['Susan', 'Mark', 'Dillan', 'Joanne', 'Alex', 'Rachel', 'Michael', 'Emma', 'Noah', 'Olivia', 'Sophia', 'James'];
  let currentName = 'I';
  let visible = true;
  let intervalId: number;

  onMount(() => {
    let nameIndex = 0;

    // Initial timeout to start with "I" for a moment
    setTimeout(() => {
      // Start the animation cycle
      intervalId = window.setInterval(() => {
        // Trigger the slide out
        visible = false;

        // Wait for transition and then change the name and slide in
        setTimeout(() => {
          currentName = names[nameIndex];
          nameIndex = (nameIndex + 1) % names.length;
          visible = true;
        }, 300); // Half of the transition time
      }, 1750); // Change every 1.75 seconds
    }, 0); // Initial delay

    return () => {
      clearInterval(intervalId);
    };
  });
</script>

<div class="name-container">
  {#if visible}
    <span
      class="animated-name"
      in:fly={{ y: 20, duration: 400 }}
      out:fly={{ y: -20, duration: 400 }}
    >
      {currentName}
    </span>
  {:else}
    <span class="animated-name placeholder">{currentName}</span>
  {/if}
</div>

<style>
  .name-container {
    display: inline-flex;
    position: relative;
    min-width: 6ch;
    height: 1.2em;
    overflow: hidden;
    vertical-align: middle;
    text-align: center;
    align-items: center;
    justify-content: center;
  }

  .animated-name {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 500;
    color: #10a37f;
    width: 100%;
    height: 100%;
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    margin: auto;
  }

  .placeholder {
    opacity: 0;
    visibility: hidden;
  }
</style>