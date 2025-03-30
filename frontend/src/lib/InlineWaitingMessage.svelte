<script lang="ts">
  import { fade, slide } from 'svelte/transition';
  import {createEventDispatcher, onMount} from 'svelte';
  import type {Session, UserPublic, Message} from "humangpt-client";
  import {apiClient} from "./api-client";

  export let visible = false;
  export let skipAnimation = false;
  export let user: UserPublic;

  const dispatch = createEventDispatcher();
  let sessions: Session[] = [];
  let selectedSession: Session | null = null;
  let responseText = '';
  let isSubmitting = false;

  function closePopup() {
    dispatch('close');
  }

  function getMinutesAgo(isoString: string): number {
    const time = new Date(isoString);
    const now = new Date();
    const diffMs = now.getTime() - time.getTime();
    return Math.floor(diffMs / 60000);
  }

  function selectSession(session: Session) {
    selectedSession = session;
    responseText = ''; // Clear any previous response
  }

  function backToQuestionsList() {
    selectedSession = null;
    responseText = '';
  }

  async function submitResponse() {
    if (!selectedSession || !responseText.trim() || isSubmitting) return;

    try {
      isSubmitting = true;
      await apiClient.submitSubmitPost(responseText, user.uuid, true, selectedSession.uuid);

      // After successful submission
      selectedSession = null;
      responseText = '';

      // Refresh the list of unanswered sessions
      await loadUnansweredSessions();

      // Show success message (temporary notification or state)
      showSubmitSuccess = true;
      setTimeout(() => {
        showSubmitSuccess = false;
      }, 3000);
    } catch (error) {
      console.error('Error submitting response:', error);
    } finally {
      isSubmitting = false;
    }
  }

  async function loadUnansweredSessions() {
    try {
      console.log("loading unanswered", user.uuid)
      const response = await apiClient.getUnansweredUnansweredSessionsGet(user.uuid);
      sessions = response.data;
    } catch (error) {
      console.error('Error loading unanswered sessions:', error);
      sessions = [];
    }
  }

  let showSubmitSuccess = false;


  let isLoaded = false;

  // This reactive statement runs whenever requiredProperty changes
  $: if (user && !isLoaded) {
    loadUnansweredSessions().then(() => {
      isLoaded = true;
    });
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submitResponse();
    }
  }
</script>

{#if visible}
<div class="waiting-message" class:no-animation={skipAnimation}
  in:fade={{duration: skipAnimation ? 0 : 300}}
  out:fade={{duration: skipAnimation ? 0 : 300}}>

  <div class="message-header">
    {#if selectedSession}
      <h3>
        <button class="back-button" on:click={backToQuestionsList}>
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
          </svg>
        </button>
        Responding to question
      </h3>
    {:else}
      <h3>Hey there, while you wait for someone to answer your question, consider helping out a fellow human.</h3>
    {/if}

    <button class="close-button" on:click={closePopup} aria-label="Close">
      <svg viewBox="0 0 24 24" width="18" height="18">
        <path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path>
      </svg>
    </button>
  </div>

  <div class="content-container">
    {#if selectedSession}
      <!-- Question details and response area -->
      <div class="question-details" in:slide={{duration: 200}}>
        <div class="question-title">{selectedSession.title}</div>

        <!-- Show conversation context -->
        <div class="conversation-context">
          {#each selectedSession.content as message}
            <div class="context-message {message.is_answer ? 'answer' : 'question'}">
              <div class="message-author">{message.name}</div>
              <div class="message-text">{message.content}</div>
            </div>
          {/each}
        </div>

        <!-- Response textarea and submit button -->
        <div class="response-area">
          <textarea
            bind:value={responseText}
            placeholder="Type your response here..."
            rows="3"
            on:keydown={handleKeydown}
            disabled={isSubmitting}
          ></textarea>

          <button
            class="submit-button"
            on:click={submitResponse}
            disabled={!responseText.trim() || isSubmitting}
          >
            {isSubmitting ? 'Sending...' : 'Submit Response'}
          </button>
        </div>
      </div>
    {:else}
      <!-- List of questions to answer -->
      <div class="questions-container" in:slide={{duration: 200}}>
        {#if showSubmitSuccess}
          <div class="success-message" in:fade={{duration: 200}} out:fade={{duration: 300}}>
            Thanks for helping out! Your response has been submitted.
          </div>
        {/if}

        {#if sessions.length === 0}
          <div class="no-questions-message">
            There are no questions waiting for answers right now. Check back later!
          </div>
        {:else}
          {#each sessions as session}
            <div class="question-card">
              <div class="question-header">
                <div class="question-content">{session.title}</div>
                <button class="help-button" on:click={() => selectSession(session)}>Help Answer</button>
              </div>
              <div class="question-metadata">
                <span class="time-ago">{getMinutesAgo(session.updated_timestamp)} minutes ago</span>
              </div>
            </div>
          {/each}
        {/if}
      </div>
    {/if}
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
    width: 95%; /* Slightly narrower to prevent scrollbar */
    max-width: 900px;
    align-self: center;
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
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .back-button {
    background: none;
    border: none;
    color: #8e8ea0;
    cursor: pointer;
    padding: 4px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .back-button:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: #c5c5d2;
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

  .content-container {
    padding: 0;
    max-height: 500px; /* Increased height for taller window */
    overflow: hidden;
    width: 100%;
    box-sizing: border-box;
  }

  .questions-container {
    padding: 16px;
    max-height: 500px; /* Increased to match content-container */
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

  .question-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    width: 100%;
  }

  .question-content {
    font-size: 14px;
    color: #ffffff;
    flex: 1;
    margin-right: 12px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .question-metadata {
    display: flex;
    font-size: 12px;
  }

  .time-ago {
    color: #8e8ea0;
    font-style: italic;
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

  /* Question details view */
  .question-details {
    padding: 16px;
    max-height: 500px; /* Increased to match other containers */
    overflow-y: auto;
    width: 100%;
    box-sizing: border-box;
  }

  .question-title {
    font-size: 15px;
    font-weight: 500;
    margin-bottom: 16px;
    color: #ffffff;
    padding-bottom: 8px;
    border-bottom: 1px solid #444654;
  }

  .conversation-context {
    margin-bottom: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 100%;
    box-sizing: border-box;
    padding-right: 4px; /* Add padding to account for scrollbar width */
  }

  .context-message {
    padding: 10px;
    border-radius: 6px;
    font-size: 13px;
  }

  .context-message.question {
    background-color: #40414f;
    border: 1px solid #565869;
    align-self: flex-start; /* User questions on the left */
    max-width: 85%;
    box-sizing: border-box;
    word-break: break-word;
  }

  .context-message.answer {
    background-color: #444654;
    align-self: flex-end; /* Answers on the right */
    max-width: 85%;
    box-sizing: border-box;
    word-break: break-word;
  }

  .message-author {
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 4px;
    color: #8e8ea0;
  }

  .message-text {
    color: #ffffff;
    white-space: pre-wrap;
  }

  .response-area {
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 100%;
    box-sizing: border-box;
  }

  textarea {
    width: 100%;
    padding: 12px;
    border-radius: 6px;
    background-color: #40414f;
    border: 1px solid #565869;
    resize: vertical;
    color: white;
    font-family: inherit;
    min-height: 80px;
    box-sizing: border-box;
  }

  textarea:focus {
    outline: none;
    border-color: #10a37f;
  }

  .submit-button {
    background-color: #10a37f;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s;
    align-self: flex-end;
  }

  .submit-button:hover:not(:disabled) {
    background-color: #0c8063;
  }

  .submit-button:disabled {
    background-color: #2a2b32;
    cursor: not-allowed;
  }

  .success-message {
    background-color: rgba(16, 163, 127, 0.2);
    color: #10a37f;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 16px;
    font-size: 14px;
    text-align: center;
    border: 1px solid rgba(16, 163, 127, 0.4);
  }

  .no-questions-message {
    color: #8e8ea0;
    text-align: center;
    padding: 20px;
    font-style: italic;
  }

  /* Custom scrollbar */
  .questions-container::-webkit-scrollbar,
  .question-details::-webkit-scrollbar {
    width: 6px;
  }

  .questions-container::-webkit-scrollbar-track,
  .question-details::-webkit-scrollbar-track {
    background: #2a2b32;
    border-radius: 4px;
  }

  .questions-container::-webkit-scrollbar-thumb,
  .question-details::-webkit-scrollbar-thumb {
    background-color: #565869;
    border-radius: 4px;
  }
</style>
