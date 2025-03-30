<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { UserPublic } from 'humangpt-client';
  
  export let user: UserPublic;
  
  const dispatch = createEventDispatcher();
  
  function handleClick() {
    dispatch('profileClick');
  }
</script>

<div class="profile-button" on:click={handleClick}>
  {#if user.pfp_url && user.pfp_url !== 'guest_url'}
    <img src={user.pfp_url} alt="Profile" class="profile-image" />
  {:else}
    <div class="profile-icon">
      <svg viewBox="0 0 24 24" width="24" height="24">
        <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
      </svg>
    </div>
  {/if}
  <span class="profile-name">{user.display_name || 'Guest'}</span>
</div>

<style>
  .profile-button {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    background-color: rgba(16, 163, 127, 0.2);
    padding: 8px 12px;
    border-radius: 4px;
    border: 1px solid rgba(16, 163, 127, 0.4);
    transition: background-color 0.2s;
  }
  
  .profile-button:hover {
    background-color: rgba(16, 163, 127, 0.3);
  }
  
  .profile-image {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    object-fit: cover;
  }
  
  .profile-icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background-color: #10a37f;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .profile-name {
    font-size: 14px;
    color: #c5c5d2;
    max-width: 120px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
</style>