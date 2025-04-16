<script lang="ts">
  import Sidebar from './lib/Sidebar.svelte';
  import ChatHeader from './lib/ChatHeader.svelte';
  import MessageList from './lib/MessageList.svelte';
  import ChatInput from './lib/ChatInput.svelte';
  import WelcomeInput from './lib/WelcomeInput.svelte';
  import AnimatedNames from './lib/AnimatedNames.svelte';
  import ProfilePage from './lib/ProfilePage.svelte';
  import ProfileButton from './lib/ProfileButton.svelte';
  import {apiClient} from "./lib/api-client";
  import type {Session, UserPublic} from "humangpt-client"
  import { onMount, onDestroy } from 'svelte';

  let user: UserPublic = {uuid: "", display_name: "loading...", pfp_url: ""};
  let chats: Session[] = [];
  let currentChat: Session | null = null;
  let showWaitingMessage = false;
  let skipWaitingAnimation = false;

  // Navigation state
  let showProfilePage = false;

  // Mobile sidebar state - default false for SSR, will be set correctly on mount
  let isSidebarOpen = false;

  // We'll stop using these global states and instead check per-chat status
  let isAwaitingResponse = false;
  let didCloseAwaiting = false;

  // Timer for auto-refreshing current chat
  let refreshTimer: number | null = null;

  // Helper function to deduplicate chats by UUID
  function deduplicateChats(newChat: Session, existingChats: Session[]): Session[] {
    // Remove any existing chat with the same UUID
    const filteredChats = existingChats.filter(chat => chat.uuid !== newChat.uuid);
    // Add the new/updated chat at the beginning
    return [newChat, ...filteredChats];
  }

  onMount(async () => {
    // Initialize sidebar state based on screen width after a small delay to prevent flash
    setTimeout(() => {
      isSidebarOpen = window.innerWidth > 768;
    }, 0);

    // Add window resize listener
    window.addEventListener('resize', handleResize);

    // Check URL parameters
    const params = new URLSearchParams(window.location.search);
    const sessionUuid = params.get('session');
    const inProfilePage = params.get('profile') === 'true';

    // Set profile page state based on URL
    showProfilePage = inProfilePage;

    if(!sessionUuid) {
      //make a guest user
      user = (await apiClient.guestGuestUserPost()).data
    }


    if (sessionUuid) {
      try {
        // Call the API to get the session by UUID
        const response = await apiClient.sessionEndpointSessionUuidGet(sessionUuid);
        if (response.data) {
          currentChat = response.data;
          chats = deduplicateChats(response.data, chats);

          //we make a user and base it off of who owns the chat we just loaded
          user = (await apiClient.getUserGetUserUuidGet(currentChat!.user_id)).data
          console.log("our user is", user)

          // Check message status upon loading a chat
          updateCurrentChatStatus();
          setTimeout(() => {
            skipWaitingAnimation = false; // Reset to ensure animation plays when showing
            showWaitingMessage = isAwaitingResponse;
            scrollChatToBottom(); // Scroll to bottom when popup appears
          }, 500);

          // Only start the refresh timer if we're not in profile view
          if (!showProfilePage) {
            startRefreshTimer();
          }
        }
      } catch (error) {
        console.error('Failed to load session:', error);
      }
    }

    console.log("mount finished", showWaitingMessage)
  });

  // Handle window resize
  function handleResize() {
    // Set sidebar to open by default on desktop, closed by default on mobile
    isSidebarOpen = window.innerWidth > 768;
  }

  // Clean up timer on component destroy
  onDestroy(() => {
    stopRefreshTimer();
    // Remove resize listener
    window.removeEventListener('resize', handleResize);
  });

  function newChatSplashScreen() {
    // Return to splash screen by setting currentChat to null
    currentChat = null;
    // Update URL to remove session but preserve profile state
    updateUrlWithSession(null, showProfilePage);

    // Reset status when returning to splash screen
    isAwaitingResponse = false;

    // Stop the refresh timer when returning to splash screen
    stopRefreshTimer();
  }

  function selectChat(event: CustomEvent<Session>) {
    didCloseAwaiting = false;
    currentChat = event.detail;
    // Update URL with selected session UUID, preserving profile state
    updateUrlWithSession(event.detail.uuid, showProfilePage);

    // Update status when switching to a different chat
    updateCurrentChatStatus();

    // Refresh the current chat when switching to it
    refreshCurrentChat();
  }

  // Function to refresh the current chat
  async function refreshCurrentChat() {
    if (!currentChat || !currentChat.uuid) return;

    try {
      const response = await apiClient.sessionEndpointSessionUuidGet(currentChat.uuid);
      if (response.data) {
        // Update current chat with fresh data
        currentChat = response.data;
        // Update chats list
        chats = deduplicateChats(response.data, chats);
        // Update status
        updateCurrentChatStatus();
        skipWaitingAnimation = true;
        showWaitingMessage = isAwaitingResponse;
      }
    } catch (error) {
      console.error('Failed to refresh session:', error);
    }
  }

  // Start the refresh timer
  function startRefreshTimer() {
    // Clear any existing timer first
    stopRefreshTimer();

    // Set up a new timer to refresh every 5 seconds
    refreshTimer = setInterval(() => {
      refreshCurrentChat();
    }, 5000);
  }

  // Stop the refresh timer
  function stopRefreshTimer() {
    if (refreshTimer !== null) {
      clearInterval(refreshTimer);
      refreshTimer = null;
    }
  }

  function updateUrlWithSession(sessionUuid: string | null, inProfilePage: boolean = false) {
    const url = new URL(window.location.href);

    // Update session parameter
    if (sessionUuid) {
      url.searchParams.set('session', sessionUuid);
    } else {
      url.searchParams.delete('session');
    }

    // Update profile page parameter
    if (inProfilePage) {
      url.searchParams.set('profile', 'true');
    } else {
      url.searchParams.delete('profile');
    }

    window.history.pushState({}, '', url.toString());
  }

  async function handleMessageSubmit(event: CustomEvent<string>) {
    const messageContent = event.detail;

    // First check current chat status
    updateCurrentChatStatus();

    // Don't allow sending if already waiting for a response in the current chat
    if (isAwaitingResponse) return;

    // Hide any existing waiting message without animation
    if (showWaitingMessage) {
      skipWaitingAnimation = true;
      showWaitingMessage = false;
    }

    // Set status to awaiting response immediately for this chat
    isAwaitingResponse = true;

    // Scroll to bottom immediately when sending a message
    scrollChatToBottom();

    try {
      console.log("We have the user id", user)
      const result = currentChat == null ?
        (await apiClient.submitSubmitPost(messageContent, user!.uuid, false)).data :
        (await apiClient.submitSubmitPost(messageContent, user!.uuid, false, currentChat.uuid)).data;

      currentChat = result;
      // Use deduplication helper to update chats list
      chats = deduplicateChats(result, chats);

      // Check if last message needs a response and update UI accordingly
      updateCurrentChatStatus();

      // Scroll to bottom when new messages arrive
      scrollChatToBottom();

      // Update URL with new session UUID, preserving profile state
      if (result.uuid) {
        updateUrlWithSession(result.uuid, showProfilePage);
      }

      // Start or restart the refresh timer for the current chat
      startRefreshTimer();

      // Show the waiting message after 1.5 seconds with animation
      setTimeout(() => {
        skipWaitingAnimation = false; // Reset to ensure animation plays when showing
        showWaitingMessage = true;
        scrollChatToBottom(); // Scroll to bottom when popup appears
      }, 1500);
    } catch (error) {
      console.error('Error submitting message:', error);
    } finally {
      //do not put code here
    }
  }

  function closeWaitingMessage() {
    didCloseAwaiting = true;
  }

  // Function to check if the last message in a chat is from the user (awaiting a response)
  function checkChatStatus(chat: Session | null) {
    if (!chat || !chat.content || chat.content.length === 0) {
      return {
        canSendMessage: true,
        isAwaitingResponse: false
      };
    }

    // Get the last message
    const lastMessage = chat.content[chat.content.length - 1];

    // If the last message is from the user (not an answer), we're awaiting a response
    const canSend = lastMessage.is_answer !== false;
    const isAwaiting = !canSend;

    console.log("chat status check!!!", isAwaitingResponse)

    return {
      canSendMessage: canSend,
      isAwaitingResponse: isAwaiting,
      lastMessage
    };
  }

  // Check status for current chat and update UI state
  function updateCurrentChatStatus() {
    if (!currentChat) {
      isAwaitingResponse = false;
      return;
    }

    const status = checkChatStatus(currentChat);
    isAwaitingResponse = status.isAwaitingResponse;
    if(!isAwaitingResponse) didCloseAwaiting = false

    console.log('Current chat status:', status);
  }

  // Helper function to force scroll to bottom
  function scrollChatToBottom() {
    // Use setTimeout to ensure it runs after DOM updates
    setTimeout(() => {
      const messagesContainer = document.querySelector('.messages-container');
      if (messagesContainer) {
        messagesContainer.scrollTo({
          top: messagesContainer.scrollHeight,
          behavior: 'smooth'
        });
      }
    }, 100);
  }

  function navigateToProfile() {
    showProfilePage = true;
    // Stop refreshing when navigating away from chat
    stopRefreshTimer();
    // Update URL to reflect profile page state
    updateUrlWithSession(currentChat?.uuid || null, true);
  }

  function navigateToChat() {
    showProfilePage = false;
    // Restart refreshing when returning to chat
    if (currentChat) {
      startRefreshTimer();
    }
    // Update URL to reflect chat page state
    updateUrlWithSession(currentChat?.uuid || null, false);
  }

  function toggleSidebar() {
    isSidebarOpen = !isSidebarOpen;
  }
</script>

{#if showProfilePage}
  <div class="profile-wrapper">
    <ProfilePage {user} on:back={navigateToChat} />
  </div>
{:else}
  <div class="chat-container">
    <button class="menu-toggle" on:click={toggleSidebar} aria-label="Toggle sidebar">
      <span class="menu-icon">☰</span>
    </button>

    <Sidebar
            {chats}
            {currentChat}
            {isSidebarOpen}
            on:newchat={newChatSplashScreen}
            on:select={selectChat}
            on:toggleSidebar={toggleSidebar}
    />

    <div class="overlay" class:active={isSidebarOpen} on:click={toggleSidebar}></div>

    <main class="chat-main">
      {#if currentChat}
        <ChatHeader
          title={currentChat.title || ""}
          {user}
          on:profileClick={navigateToProfile}
        />
        <MessageList
          messages={currentChat.content || []}
          showWaitingMessage={showWaitingMessage && !didCloseAwaiting}
          skipWaitingAnimation={skipWaitingAnimation}
          user={user}
          on:closeWaiting={() => closeWaitingMessage()}
        />
        <ChatInput
          on:submit={handleMessageSubmit}
          isAwaitingResponse={isAwaitingResponse}
        />
      {:else}
        <div class="profile-header-container">
          <div class="profile-spacer"></div>
          <div class="profile-button-container">
            <ProfileButton {user} on:profileClick={navigateToProfile} />
          </div>
        </div>
        <div class="empty-state">
          <div class="welcome-container">
            <h1>HumanGPT</h1>
            <p class="welcome-text">How can <AnimatedNames /> help you today?</p>
            <div class="centered-input">
              <WelcomeInput on:submit={handleMessageSubmit} />
            </div>
            <p class="description-text">When you ask HumanGPT a question, a real human being will answer. Please be considerate of your fellow meat sacks.</p>
          </div>
        </div>
      {/if}
    </main>
  </div>
{/if}

<style>
  .chat-container {
    display: flex;
    height: 100vh;
    width: 100%;
    overflow: hidden;
    position: relative;
  }

  .chat-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: #343541;
    color: white;
    position: relative;
    overflow: hidden;
  }

  /* Safari-specific fixes */
  @supports (-webkit-touch-callout: none) {
    .chat-main {
      height: -webkit-fill-available;
    }
  }

  .menu-toggle {
    display: none;
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 998; /* Lower than sidebar z-index to get covered */
    background-color: transparent;
    color: white;
    border: none;
    border-radius: 4px;
    width: 36px;
    height: 36px;
    font-size: 22px;
    cursor: pointer;
    padding: 0;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s ease;
  }

  .menu-toggle:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }

  .menu-icon {
    line-height: 1;
  }

  .overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
  }

  .overlay.active {
    display: block;
  }

  /* Fix for initial page load dark screen */
  @media (min-width: 769px) {
    .overlay.active {
      display: none;
    }
  }

  @media (max-width: 768px) {
    .menu-toggle {
      display: flex;
    }

    .chat-main {
      padding-left: 0;
    }

    /* Add spacing on the welcome screen for the menu button */
    .profile-header-container {
      padding-left: 48px;
    }
  }

  .profile-wrapper {
    width: 100vw;
    max-width: 100%;
    overflow-x: hidden;
    position: relative;
    height: 100vh;
  }

  .profile-header-container {
    display: flex;
    justify-content: flex-end;
    padding: 8px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    height: 56px;
    box-sizing: border-box;
  }

  .profile-spacer {
    flex: 1;
  }

  .profile-button-container {
    display: flex;
    justify-content: flex-end;
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
