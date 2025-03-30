<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import ProfileButton from './ProfileButton.svelte';
  import type { UserPublic } from 'humangpt-client';
  
  export let title: string;
  export let user: UserPublic;
  
  const dispatch = createEventDispatcher();
  
  function handleProfileClick() {
    dispatch('profileClick');
  }
</script>

<div class="chat-header">
  <div class="title-container">
    <h2 class="title-text" title={title}>{title}</h2>
  </div>
  <div class="header-actions">
    <ProfileButton {user} on:profileClick={handleProfileClick} />
  </div>
</div>

<style>
  .chat-header {
    padding: 15px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 56px;
    box-sizing: border-box;
  }

  .title-container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    max-width: 70%;
    margin: 0 auto;
  }

  h2 {
    margin: 0;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
    font-size: 1.1rem;
  }
  
  .header-actions {
    display: flex;
    align-items: center;
    min-width: 40px; /* Ensure space for profile button */
  }
  
  @media (max-width: 768px) {
    .title-container {
      max-width: 50%;
    }
    
    h2 {
      font-size: 1rem;
    }
    
    .chat-header {
      padding-left: 48px;
      padding-right: 12px; /* Ensure profile button doesn't get cut off */
    }
  }
  
  @media (max-width: 480px) {
    .title-container {
      max-width: 40%;
    }
  }
</style>