<script lang="ts">
  import { fade } from 'svelte/transition';
  import { createEventDispatcher } from 'svelte';

  export let visible = false;
  export let skipAnimation = false;

  const dispatch = createEventDispatcher();

  function closePopup() {
    dispatch('close');
  }

  // Sample questions for the list
  const sampleQuestions = [
    { id: 1, question: "How do I configure a React app to use TypeScript?", timeAgo: "5 minutes ago" },
    { id: 2, question: "What's the best way to deploy a Svelte application to Vercel?", timeAgo: "8 minutes ago" },
    { id: 3, question: "Can someone explain Docker networking between containers?", timeAgo: "12 minutes ago" },
  ];
</script>

{#if visible}
<div class="waiting-message" class:no-animation={skipAnimation} 
  in:fade={{duration: skipAnimation ? 0 : 300}} 
  out:fade={{duration: skipAnimation ? 0 : 300}}>
  <div class="message-header">
    <h3>Hey there, while you wait for someone to answer your question, consider helping out a fellow human.</h3>
    <button class="close-button" on:click={closePopup} aria-label="Close">
      <svg viewBox="0 0 24 24" width="18" height="18">
        <path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path>
      </svg>
    </button>
  </div>

  <div class="questions-container">
    {#each sampleQuestions as question}
      <div class="question-card">
        <div class="question-content">{question.question}</div>
        <div class="question-metadata">
          <span class="time-ago">{question.timeAgo}</span>
          <button class="help-button">Help Answer</button>
        </div>
      </div>
    {/each}
  </div>
</div>
{/if}

<style>
  .waiting-message {
    margin: 12px 0;
    background-color: #343541;
    border-radius: 8px;
    border: 1px solid #444654;
    overflow: hidden;
    width: 100%;
  }

  .message-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 16px;
    border-bottom: 1px solid #444654;
  }

  h3 {
    font-size: 16px;
    font-weight: 500;
    margin: 0;
    color: #ffffff;
    line-height: 1.4;
    flex: 1;
    padding-right: 12px;
  }

  .close-button {
    background: none;
    border: none;
    color: #8e8ea0;
    cursor: pointer;
    padding: 4px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    min-width: 24px;
    height: 24px;
  }

  .close-button:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: #c5c5d2;
  }

  .questions-container {
    padding: 16px;
    max-height: 300px;
    overflow-y: auto;
  }

  .question-card {
    background-color: #40414f;
    border-radius: 6px;
    padding: 12px;
    margin-bottom: 8px;
    border: 1px solid #565869;
    transition: background-color 0.2s;
  }

  .question-card:hover {
    background-color: #4c4d5e;
  }

  .question-content {
    font-size: 14px;
    margin-bottom: 10px;
    color: #ffffff;
  }

  .question-metadata {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
  }

  .time-ago {
    color: #8e8ea0;
  }

  .help-button {
    background-color: #10a37f;
    color: white;
    border: none;
    padding: 4px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    transition: background-color 0.2s;
  }

  .help-button:hover {
    background-color: #0c8063;
  }

  /* Custom scrollbar */
  .questions-container::-webkit-scrollbar {
    width: 6px;
  }

  .questions-container::-webkit-scrollbar-track {
    background: #2a2b32;
    border-radius: 4px;
  }

  .questions-container::-webkit-scrollbar-thumb {
    background-color: #565869;
    border-radius: 4px;
  }
</style>
