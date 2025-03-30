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
  <h2>{title}</h2>
  <div class="header-actions">
    <ProfileButton {user} on:profileClick={handleProfileClick} />
  </div>
</div>

<style>
  .chat-header {
    padding: 16px;
    border-bottom: 1px solid #444654;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  h2 {
    margin: 0;
    flex: 1;
    text-align: center;
  }
  
  .header-actions {
    display: flex;
    align-items: center;
  }
</style>