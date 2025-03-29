<script lang="ts">
  import Sidebar from './lib/Sidebar.svelte';
  import ChatHeader from './lib/ChatHeader.svelte';
  import MessageList from './lib/MessageList.svelte';
  import ChatInput from './lib/ChatInput.svelte';
  import WelcomeInput from './lib/WelcomeInput.svelte';
  import AnimatedNames from './lib/AnimatedNames.svelte';
  import {apiClient} from "./lib/api-client";
  import type {Session, UserPublic} from "humangpt-client"
  import { onMount } from 'svelte';

  let user: UserPublic | null = null;
  let chats: Session[] = [];
  let currentChat: Session | null = null;
  let showWaitingMessage = false;
  let skipWaitingAnimation = false;
  
  // We'll stop using these global states and instead check per-chat status
  let isAwaitingResponse = false; 
  let canSendMessage = true;

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

    user = (await apiClient.guestGuestUserPost()).data

    if (sessionUuid) {
      try {
        // Call the API to get the session by UUID
        const response = await apiClient.getSessionSessionUuidGet(sessionUuid);
        if (response.data) {
          currentChat = response.data;
          chats = deduplicateChats(response.data, chats);
          
          // Check message status upon loading a chat
          updateCurrentChatStatus();
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
    
    // Reset status when returning to splash screen
    isAwaitingResponse = false;
    canSendMessage = true;
  }

  function selectChat(event: CustomEvent<Session>) {
    currentChat = event.detail;
    // Update URL with selected session UUID
    updateUrlWithSession(event.detail.uuid);
    
    // Update status when switching to a different chat
    updateCurrentChatStatus();
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
    
    // First check current chat status
    updateCurrentChatStatus();
    
    // Don't allow sending if already waiting for a response in the current chat
    if (!canSendMessage) return;

    // Hide any existing waiting message without animation
    if (showWaitingMessage) {
      skipWaitingAnimation = true;
      showWaitingMessage = false;
    }

    // Set status to awaiting response immediately for this chat
    isAwaitingResponse = true;
    canSendMessage = false;

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

      // Update URL with new session UUID
      if (result.uuid) {
        updateUrlWithSession(result.uuid);
      }

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
    showWaitingMessage = false;
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
    
    return {
      canSendMessage: canSend,
      isAwaitingResponse: isAwaiting,
      lastMessage
    };
  }
  
  // Check status for current chat and update UI state
  function updateCurrentChatStatus() {
    if (!currentChat) {
      canSendMessage = true;
      isAwaitingResponse = false;
      return;
    }
    
    const status = checkChatStatus(currentChat);
    canSendMessage = status.canSendMessage;
    isAwaitingResponse = status.isAwaitingResponse;
    
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
      <ChatInput 
        on:submit={handleMessageSubmit}
        isAwaitingResponse={isAwaitingResponse}
        canSendMessage={canSendMessage}
      />
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
