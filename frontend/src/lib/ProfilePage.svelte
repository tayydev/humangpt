<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { UserPublic } from 'humangpt-client';
  
  export let user: UserPublic;
  
  const dispatch = createEventDispatcher();
  
  function goBack() {
    dispatch('back');
  }
  
  function mockGoogleSignIn() {
    // This would actually connect to Google OAuth in a real app
    alert('This would connect to Google Sign-In in a real implementation');
  }
</script>

<div class="profile-page-container">
  <div class="profile-page">
    <header>
      <button class="back-button" on:click={goBack}>
        <svg viewBox="0 0 24 24" width="24" height="24">
          <path fill="currentColor" d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
        </svg>
        Back to Chat
      </button>
      <h1>Profile Settings</h1>
    </header>

    <div class="profile-content">
      <div class="profile-section">
        <div class="profile-header">
          {#if user.pfp_url && user.pfp_url !== 'guest_url'}
            <img src={user.pfp_url} alt="Profile" class="profile-image" />
          {:else}
            <div class="profile-icon">
              <svg viewBox="0 0 24 24" width="48" height="48">
                <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
              </svg>
            </div>
          {/if}
          <div class="profile-info">
            <h2>{user.display_name || 'Guest User'}</h2>
            <div class="account-info">
              <p class="account-status">Account Status: <span class="guest">Guest</span></p>
              <p class="account-id">User ID: {user.uuid}</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="divider"></div>
      
      <div class="section">
        <h3>Sign In Options</h3>
        <div class="signin-options">
          <button class="google-signin" on:click={mockGoogleSignIn}>
            <div class="google-icon">
              <svg viewBox="0 0 24 24" width="20" height="20">
                <path d="M12.545 10.239v3.821h5.445c-0.712 2.315-2.647 3.972-5.445 3.972-3.332 0-6.033-2.701-6.033-6.032s2.701-6.032 6.033-6.032c1.498 0 2.866 0.549 3.921 1.453l2.814-2.814c-1.798-1.677-4.198-2.707-6.735-2.707-5.523 0-10 4.477-10 10s4.477 10 10 10c8.396 0 10.249-7.85 9.426-11.748l-9.426 0.087z" fill="#4285F4"/>
              </svg>
            </div>
            Sign in with Google
          </button>
        </div>
      </div>
      
      <div class="divider"></div>
      
      <div class="section">
        <h3>Data & Privacy</h3>
        <p class="privacy-notice">
          Sign in to save your chat history and access it from any device.
          Your data is secure and private - we only store information needed
          to provide the service.
        </p>
        <div class="data-options">
          <button class="option-button">Delete Guest Data</button>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .profile-page-container {
    height: 100vh;
    width: 100%;
    background-color: #343541;
    display: flex;
    overflow-y: auto;
  }
  
  .profile-page {
    display: flex;
    flex-direction: column;
    min-height: 100%;
    background-color: #343541;
    color: white;
    width: 100%;
    padding: 0;
    box-sizing: border-box;
  }
  
  header {
    padding: 15px max(40px, 10%);
    display: flex;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    background-color: rgba(40, 40, 48, 0.3);
    width: 100%;
    height: 56px;
    box-sizing: border-box;
  }
  
  .back-button {
    display: flex;
    align-items: center;
    gap: 8px;
    background: none;
    border: none;
    color: #c5c5d2;
    cursor: pointer;
    padding: 8px;
    border-radius: 4px;
    margin-right: 16px;
    font-size: 14px;
  }
  
  .back-button:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  h1 {
    margin: 0;
    font-size: 18px;
    color: white;
    font-weight: 500;
  }
  
  .profile-content {
    padding: 0 max(40px, 10%);
    overflow-y: auto;
    flex: 1;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
  }
  
  .profile-section {
    padding: 32px 0 20px 0;
  }
  
  .profile-header {
    display: flex;
    align-items: flex-start;
    gap: 20px;
  }
  
  .profile-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  
  .profile-image {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  }
  
  .profile-icon {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background-color: #10a37f;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  }
  
  h2 {
    margin: 0 0 8px 0;
    font-size: 22px;
    font-weight: 500;
    color: #ffffff;
  }
  
  .account-info {
    font-size: 14px;
    color: #c5c5d2;
  }
  
  .account-status {
    margin-bottom: 4px;
    margin-top: 0;
  }
  
  .guest {
    color: #f9a825;
    font-weight: 500;
    margin-left: 4px;
  }
  
  .account-id {
    color: #8e8ea0;
    font-family: monospace;
    margin: 0;
  }
  
  .divider {
    height: 1px;
    background: linear-gradient(to right, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.03));
    margin: 10px 0;
  }
  
  .section {
    padding: 32px 0 20px 0;
    text-align: left;
  }
  
  h3 {
    margin-top: 0;
    margin-bottom: 18px;
    font-size: 18px;
    font-weight: 500;
    color: white;
    position: relative;
    padding-bottom: 10px;
    text-align: left;
  }
  
  h3::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 30px;
    height: 2px;
    background-color: #10a37f;
    border-radius: 1px;
  }
  
  .signin-options {
    display: flex;
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .google-signin {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    background-color: white;
    color: #202124;
    border: none;
    padding: 12px 20px;
    border-radius: 4px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .google-signin:hover {
    background-color: #f1f1f1;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  }
  
  .google-icon {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .privacy-notice {
    font-size: 14px;
    color: #c5c5d2;
    margin-bottom: 24px;
    line-height: 1.6;
    text-align: left;
  }
  
  .data-options {
    display: flex;
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .option-button {
    background-color: transparent;
    color: #c5c5d2;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 10px 16px;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .option-button:hover {
    background-color: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.3);
  }
</style>