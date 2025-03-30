<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { UserPublic } from 'humangpt-client';
  
  export let user: UserPublic;
  
  const dispatch = createEventDispatcher();
  
  function handleClick() {
    dispatch('profileClick');
  }
</script>

<button class="profile-button" on:click={handleClick} aria-label="Profile">
  <svg viewBox="0 0 24 24" width="24" height="24">
    <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
  </svg>
</button>

<style>
  .profile-button {
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    background: none;
    padding: 8px;
    border: none;
    border-radius: 50%;
    color: rgba(255, 255, 255, 0.8);
    transition: all 0.2s ease;
    width: 40px;
    height: 40px;
    min-width: 40px;
  }
  
  @media (max-width: 480px) {
    .profile-button {
      padding: 6px;
      width: 36px;
      height: 36px;
      min-width: 36px;
    }
    
    .profile-button svg {
      width: 22px;
      height: 22px;
    }
  }
  
  .profile-button:hover {
    color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.08);
    transform: scale(1.05);
  }
  
  .profile-button:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2);
  }
</style>