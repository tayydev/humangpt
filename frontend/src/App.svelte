<script lang="ts">
  import Sidebar from './lib/Sidebar.svelte';
  import ChatHeader from './lib/ChatHeader.svelte';
  import MessageList from './lib/MessageList.svelte';
  import ChatInput from './lib/ChatInput.svelte';
  import WelcomeInput from './lib/WelcomeInput.svelte';
  import AnimatedNames from './lib/AnimatedNames.svelte';
  import WaitingPopup from './lib/WaitingPopup.svelte';
  import {apiClient} from "./lib/api-client";
  import type {Session} from "humangpt-client"
  import { onMount } from 'svelte';

  let chats: Session[] = [];
  let currentChat: Session | null = null;
  let showWaitingPopup = false;

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
          chats = [response.data, ...chats];
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

    const result = currentChat == null ? (await apiClient.submitSubmitPost(messageContent, "User:", false)).data
            : (await  apiClient.submitSubmitPost(messageContent, "UserFollowup", false, currentChat.uuid)).data

    currentChat = result
    chats = [result, ...chats];

    // Update URL with new session UUID
    if (result.uuid) {
      updateUrlWithSession(result.uuid);
    }

    // Show the waiting popup after 3 seconds
    setTimeout(() => {
      showWaitingPopup = true;
    }, 3000);
  }

  function closeWaitingPopup() {
    showWaitingPopup = false;
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
      <MessageList messages={currentChat.content || []} />
      <ChatInput on:submit={handleMessageSubmit} />
    {:else}
      <div class="empty-state">
        <div class="welcome-container">
          <h1>HumanGPT</h1>
          <p class="welcome-text">How can <AnimatedNames /> help you today?</p>
          <div class="centered-input">
            <WelcomeInput on:submit={handleMessageSubmit} />
          </div>
        </div>
      </div>
    {/if}
  </main>

  <WaitingPopup visible={showWaitingPopup} on:close={closeWaitingPopup} />
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

  .centered-input {
    width: 100%;
  }
</style>
