<script lang="ts">
  import Sidebar from './lib/Sidebar.svelte';
  import ChatHeader from './lib/ChatHeader.svelte';
  import MessageList from './lib/MessageList.svelte';
  import ChatInput from './lib/ChatInput.svelte';
  import WelcomeInput from './lib/WelcomeInput.svelte';
  import AnimatedNames from './lib/AnimatedNames.svelte';
  import {apiClient} from "./lib/api-client";
  import type {Session} from "humangpt-client"
  import { onMount } from 'svelte';

  let chats: Session[] = [];
  let currentChat: Session | null = null;
  let showWaitingMessage = false;
  let skipWaitingAnimation = false;
  let isAwaitingResponse = false;

  // Helper function to deduplicate chats by UUID
  function deduplicateChats(newChat: Session, existingChats: Session[]): Session[] {
    // Remove any existing chat with the same UUID
    const filteredChats = existingChats.filter(chat => chat.uuid !== newChat.uuid);
    // Add the new/updated chat at the beginning
    return [newChat, ...filteredChats];
  }

  onMount(async () => {
    // Check if a session UUID is present in the URL
    const params = new URLSearchParams(window.location.search);
    const sessionUuid = params.get('session');

    if (sessionUuid) {
      try {
        // Call the API to get the session by UUID
        const response = await apiClient.getSessionSessionUuidGet(sessionUuid);
        if (response.data) {
          currentChat = response.data;
          chats = deduplicateChats(response.data, chats);
        }
      } catch (error) {
        console.error('Failed to load session:', error);
      }
    }
  });

  function newChatSplashScreen() {
    // Return to splash screen by setting currentChat to null
    currentChat = null;
    // Remove session from URL
    updateUrlWithSession(null);
  }

  function selectChat(event: CustomEvent<Session>) {
    currentChat = event.detail;
    // Update URL with selected session UUID
    updateUrlWithSession(event.detail.uuid);
  }

  function updateUrlWithSession(sessionUuid: string | null) {
    const url = new URL(window.location.href);
    if (sessionUuid) {
      url.searchParams.set('session', sessionUuid);
    } else {
      url.searchParams.delete('session');
    }
    window.history.pushState({}, '', url.toString());
  }

  async function handleMessageSubmit(event: CustomEvent<string>) {
    const messageContent = event.detail;

    // Hide any existing waiting message without animation
    if (showWaitingMessage) {
      skipWaitingAnimation = true;
      showWaitingMessage = false;
    }

    // Immediately hide any existing awaiting response indicator
    isAwaitingResponse = false;

    // Show loading indicator after a 500ms delay
    let loadingTimeout = setTimeout(() => {
      isAwaitingResponse = true;
      console.log('Setting awaiting response to true');
    }, 250);

    try {
      const result = currentChat == null ?
        (await apiClient.submitSubmitPost(messageContent, "User:", false)).data :
        (await apiClient.submitSubmitPost(messageContent, "UserFollowup", false, currentChat.uuid)).data;

      currentChat = result;
      // Use deduplication helper to update chats list
      chats = deduplicateChats(result, chats);

      // Update URL with new session UUID
      if (result.uuid) {
        updateUrlWithSession(result.uuid);
      }

      // Show the waiting message after 1.5 seconds with animation
      setTimeout(() => {
        skipWaitingAnimation = false; // Reset to ensure animation plays when showing
        showWaitingMessage = true;
      }, 1500);
    } catch (error) {
      console.error('Error submitting message:', error);
    } finally {
      //do not put code here
    }
  }

  function closeWaitingMessage() {
    showWaitingMessage = false;
  }
</script>

<div class="chat-container">
  <Sidebar
          {chats}
          {currentChat}
          on:newchat={newChatSplashScreen}
          on:select={selectChat}
  />

  <main class="chat-main">
    {#if currentChat}
      <ChatHeader title={currentChat.title || ""} />
      <MessageList
        messages={currentChat.content || []}
        showWaitingMessage={showWaitingMessage}
        skipWaitingAnimation={skipWaitingAnimation}
        isAwaitingResponse={isAwaitingResponse}
        on:closeWaiting={() => closeWaitingMessage()}
      />
      <ChatInput on:submit={handleMessageSubmit} />
    {:else}
      <div class="empty-state">
        <div class="welcome-container">
          <h1>HumanGPT</h1>
          <p class="welcome-text">How can <AnimatedNames /> help you today?</p>
          <div class="centered-input">
            <WelcomeInput on:submit={handleMessageSubmit} />
          </div>
          <p class="description-text">When you ask HumanGPT a question, a real human being will answer. Please be considerate of your fellow humans.</p>
        </div>
      </div>
    {/if}
  </main>
</div>

<style>
  .chat-container {
    display: flex;
    height: 100vh;
    width: 100%;
    overflow: hidden;
  }

  .chat-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: #343541;
    color: white;
  }

  .empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #8e8ea0;
    padding-bottom: 15vh; /* Shift content up by adding padding to the bottom */
  }

  .welcome-container {
    max-width: 780px;
    width: 85%;
    text-align: center;
    padding: 0 20px;
  }

  .welcome-container h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: #10a37f;
  }

  .welcome-text {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    color: #c5c5d2;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.2em;
  }

  .description-text {
    font-size: 1rem;
    margin-top: 2rem;
    color: #8e8ea0;
    text-align: center;
  }

  .centered-input {
    width: 100%;
  }
</style>
