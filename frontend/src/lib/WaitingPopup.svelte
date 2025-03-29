<script lang="ts">
  import { fade } from 'svelte/transition';
  import { createEventDispatcher } from 'svelte';
  
  export let visible = false;
  
  const dispatch = createEventDispatcher();
  
  function closePopup() {
    dispatch('close');
  }
  
  // Sample questions for the list
  const sampleQuestions = [
    { id: 1, question: "How do I configure a React app to use TypeScript?", timeAgo: "5 minutes ago" },
    { id: 2, question: "What's the best way to deploy a Svelte application to Vercel?", timeAgo: "8 minutes ago" },
    { id: 3, question: "Can someone explain Docker networking between containers?", timeAgo: "12 minutes ago" },
    { id: 4, question: "How do I fix CORS errors in my Node.js API?", timeAgo: "15 minutes ago" },
    { id: 5, question: "What's the difference between useMemo and useCallback in React?", timeAgo: "18 minutes ago" },
    { id: 6, question: "How can I optimize my PostgreSQL queries for better performance?", timeAgo: "25 minutes ago" },
    { id: 7, question: "What's the best library for handling form validation in Vue.js?", timeAgo: "30 minutes ago" },
    { id: 8, question: "How do I set up a CI/CD pipeline for my Django application?", timeAgo: "35 minutes ago" },
    { id: 9, question: "What are the pros and cons of using Tailwind CSS?", timeAgo: "40 minutes ago" },
    { id: 10, question: "How can I implement authentication with JWT in my Express app?", timeAgo: "45 minutes ago" }
  ];
</script>

{#if visible}
<div class="popup-overlay" transition:fade={{ duration: 400 }}>
  <div class="popup-container">
    <button class="close-button" on:click={closePopup}>
      <svg viewBox="0 0 24 24" width="24" height="24">
        <path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path>
      </svg>
    </button>
    
    <h2 class="popup-title">Hey there, while you wait for someone to answer your question, consider helping out a fellow human.</h2>
    
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
</div>
{/if}

<style>
  .popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 20px;
  }
  
  .popup-container {
    background-color: #343541;
    border-radius: 12px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
    width: 90%;
    max-width: 900px;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    position: relative;
    padding: 28px;
    border: 1px solid #444654;
  }
  
  .close-button {
    position: absolute;
    top: 20px;
    right: 20px;
    background: none;
    border: none;
    color: #c5c5d2;
    cursor: pointer;
    padding: 4px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .close-button:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  .popup-title {
    font-size: 24px;
    margin-bottom: 24px;
    text-align: center;
    color: #ffffff;
    line-height: 1.4;
    padding: 0 40px;
  }
  
  .questions-container {
    overflow-y: auto;
    flex: 1;
    padding-right: 8px;
  }
  
  .question-card {
    background-color: #40414f;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    border: 1px solid #565869;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .question-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }
  
  .question-content {
    font-size: 16px;
    margin-bottom: 12px;
    color: #ffffff;
  }
  
  .question-metadata {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
  }
  
  .time-ago {
    color: #8e8ea0;
  }
  
  .help-button {
    background-color: #10a37f;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s;
  }
  
  .help-button:hover {
    background-color: #0c8063;
  }
  
  /* Custom scrollbar for the questions container */
  .questions-container::-webkit-scrollbar {
    width: 8px;
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