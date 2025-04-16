<script lang="ts">
  import Sidebar from './lib/Sidebar.svelte';
  import ChatHeader from './lib/ChatHeader.svelte';
  import MessageList from './lib/MessageList.svelte';
  import ChatInput from './lib/ChatInput.svelte';
  import WelcomeInput from './lib/WelcomeInput.svelte';
  import AnimatedNames from './lib/AnimatedNames.svelte';
  import ProfilePage from './lib/ProfilePage.svelte';
  import ProfileButton from './lib/ProfileButton.svelte';
  import {apiClient, WebSocketClient} from "./lib/api-client";
  import type {Message, Session, SessionDTO, UserPublic} from "humangpt-client"
  import {onDestroy, onMount} from 'svelte';
  import {writable} from "svelte/store";

  // WebSocket client
  let wsClient: WebSocketClient | null = null;

  //data state
  let user: UserPublic = {uuid: "", display_name: "loading...", pfp_url: ""};
  let chatIds: string[] = []
  let chats: SessionDTO[] = [];
  let currentSession: SessionDTO | null = null;
  let messages = writable<Message[]>([])
  let isAwaitingResponse = false;

  //data runes
  $: isAwaitingResponse = $messages.length > 0 && $messages[$messages.length - 1].user_id == currentSession!.user_id;
  $: if(currentSession) {
    chatIds = loadSessionChatIds() //make sure we have loaded before pushing
    if (!chatIds.includes(currentSession.uuid)) {
      // Only add the UUID if it doesn't exist yet (don't reorder)
      chatIds.push(currentSession.uuid)
    }
    console.log("updated ids", chatIds)
    saveSessionChatIds(chatIds)
    loadSessionDTOFromChatIds().then() //kick this off
  }

  //ui state
  let showWaitingMessage = false;
  let skipWaitingAnimation = false;
  let showProfilePage = false;
  let isSidebarOpen = false;
  let didCloseAwaiting = false;

  function saveSessionChatIds(chats: string[]) {
    localStorage.setItem("humangpt_chat_ids", JSON.stringify(chats));
  }

  function loadSessionChatIds(): string[] {
    try {
      const savedChats = localStorage.getItem("humangpt_chat_ids");
      console.log("got saved", savedChats)
      return savedChats ? JSON.parse(savedChats) : [];
    } catch (error) {
      console.error("Failed to load chats from localStorage:", error);
      return [];
    }
  }

  async function loadSessionDTOFromChatIds() {
    chats = (await Promise.all(chatIds.map(async id =>
            (await apiClient.sessionEndpointGetSessionGet(id)).data
    )));
    console.log("loaded dtos", chats)
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
    // Set profile page state based on URL
    showProfilePage = params.get('profile') === 'true';

    if(!sessionUuid) { //starting fresh
      user = (await apiClient.guestGuestUserPost()).data; //make guest user
    }
    else {
      currentSession = (await apiClient.sessionEndpointGetSessionGet(sessionUuid)).data //dto
      user = (await apiClient.getUserEndpointGetUserGet(currentSession.user_id)).data //old user data
      wsClient = new WebSocketClient(messages, sessionUuid, user.uuid); //make client
      wsClient.connect(); //tell it to connect

      // Check message status upon loading a chat
      setTimeout(() => {
        skipWaitingAnimation = false; // Reset to ensure animation plays when showing
        showWaitingMessage = isAwaitingResponse;
        queueScrollChatToBottom(); // Scroll to bottom when popup appears
      }, 500);
    }

    chatIds = loadSessionChatIds()
    await loadSessionDTOFromChatIds()
  });

  // Handle window resize
  function handleResize() {
    // Set sidebar to open by default on desktop, closed by default on mobile
    isSidebarOpen = window.innerWidth > 768;
  }

  // Clean up timer and websocket on component destroy
  onDestroy(() => {
    // Disconnect websocket if it exists
    if (wsClient) {
      wsClient.disconnect();
    }
    // Remove resize listener
    window.removeEventListener('resize', handleResize);
  });

  function newChatSplashScreen() {
    // Return to splash screen by setting currentChat to null
    currentSession = null;
    wsClient?.disconnect()
    messages.set([]) //reset message

    // Update URL to remove session but preserve profile state
    updateUrlWithSession(null, showProfilePage);

    // Reset status when returning to splash screen
    isAwaitingResponse = false;

    // Disconnect WebSocket if it exists
    if (wsClient) {
      wsClient.disconnect();
      wsClient = null;
    }
  }

  async function selectChat(event: CustomEvent<SessionDTO>) {
    didCloseAwaiting = false; //reset popup close

    wsClient?.disconnect()
    messages.set([]) //reset message

    currentSession = event.detail;

    // Update URL with selected session UUID, preserving profile state
    updateUrlWithSession(event.detail.uuid, showProfilePage);

    //api calls
    user = (await apiClient.getUserEndpointGetUserGet(currentSession.user_id)).data //old user data
    wsClient = new WebSocketClient(messages, currentSession.uuid, user.uuid); //make client
    wsClient.connect(); //tell it to connect

    showWaitingMessage = false;

    setTimeout(() => {
      skipWaitingAnimation = false; // Reset to ensure animation plays when showing
      showWaitingMessage = isAwaitingResponse;
      queueScrollChatToBottom(); // Scroll to bottom when popup appears
    }, 500);
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

    // Hide any existing waiting message without animation
    if (showWaitingMessage) {
      skipWaitingAnimation = true;
      showWaitingMessage = false;
    }

    console.log("We have the user id", user);
    if(currentSession == null) { //make new session
      currentSession = (await apiClient.createSessionCreateSessionPost(messageContent, user!.uuid)).data
      wsClient = new WebSocketClient(messages, currentSession.uuid, user.uuid);
      wsClient.connect()

      // For new sessions, add to the beginning of the list
      chatIds = loadSessionChatIds()
      chatIds.unshift(currentSession.uuid)
      chatIds = [...new Set(chatIds)]; // unique filter
      saveSessionChatIds(chatIds)
    }

    const msg: Message = {
      user_id: user.uuid,
      name: user.display_name,
      pfp_url: user.pfp_url,
      content: messageContent,
      is_answer: false //todo make this more flexible?
    }

    wsClient!.send(msg) //send message

    // Scroll to bottom when new messages arrive
    queueScrollChatToBottom();

    // Update URL with new session UUID, preserving profile state
    if (currentSession.uuid) {
      updateUrlWithSession(currentSession.uuid, showProfilePage);
    }

    // Show the waiting message after 1.5 seconds with animation
    setTimeout(() => {
      skipWaitingAnimation = false; // Reset to ensure animation plays when showing
      showWaitingMessage = true;
      queueScrollChatToBottom(); // Scroll to bottom when popup appears
    }, 1500);
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



  // Helper function to force scroll to bottom
  function queueScrollChatToBottom() {
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

    // Disconnect websocket when navigating away
    if (wsClient) {
      wsClient.disconnect();
    }

    // Update URL to reflect profile page state
    updateUrlWithSession(currentSession?.uuid || null, true);
  }

  function navigateToChat() {
    showProfilePage = false;

    // Reconnect websocket if we have a chat
    if (currentSession && currentSession.uuid && user.uuid) {
      if (wsClient) {
        wsClient.disconnect();
      }
      wsClient = new WebSocketClient(messages, currentSession.uuid, user.uuid);
      wsClient.connect();
    }

    // Update URL to reflect chat page state
    updateUrlWithSession(currentSession?.uuid || null, false);
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
            {currentSession}
            {isSidebarOpen}
            on:newchat={newChatSplashScreen}
            on:select={selectChat}
            on:toggleSidebar={toggleSidebar}
    />

    <div class="overlay" class:active={isSidebarOpen} on:click={toggleSidebar}></div>

    <main class="chat-main">
      {#if currentSession}
        <ChatHeader
          title={currentSession.title || ""}
          {user}
          on:profileClick={navigateToProfile}
        />
        <MessageList
          messages={$messages}
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
