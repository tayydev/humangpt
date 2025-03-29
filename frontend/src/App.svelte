<script lang="ts">
  import type { Chat, Message } from './lib/types';
  import Sidebar from './lib/Sidebar.svelte';
  import ChatHeader from './lib/ChatHeader.svelte';
  import MessageList from './lib/MessageList.svelte';
  import ChatInput from './lib/ChatInput.svelte';
  import WelcomeInput from './lib/WelcomeInput.svelte';
  import AnimatedNames from './lib/AnimatedNames.svelte';
  import {apiClient} from "./lib/api-client";
  import type {Session} from "humangpt-client"

  let chats: Session[] = [];
  let currentChat: Session | null = null;

  function newChatSplashScreen() {
    // Return to splash screen by setting currentChat to null
    currentChat = null;
  }

  function selectChat(event: CustomEvent<Session>) {
    currentChat = event.detail;
  }

  async function handleMessageSubmit(event: CustomEvent<string>) {
    const messageContent = event.detail;

    const result: Session = (await apiClient.submitSubmitPost(messageContent, "User:", false)).data

    currentChat = result
    chats = [result, ...chats];
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
      <ChatHeader title={currentChat.title} />
      <MessageList messages={currentChat.messages} />
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
