<template>
  <div class="app">
    <nav class="navbar">
      <router-link to="/" class="logo">
        Story Manager
      </router-link>
      <div class="nav-links">
        <router-link to="/dialogs" class="nav-link">
          Dialogs
        </router-link>
        <router-link to="/profiles" class="nav-link">
          Profiles
        </router-link>
        <router-link to="/stories" class="nav-link">
          Stories
        </router-link>
      </div>
    </nav>

    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<style>
/* Reset and global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  background: #f8f9fa;
  color: #333;
}

/* App layout */
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navigation */
.navbar {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2196F3;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: #666;
  text-decoration: none;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.nav-link:hover {
  color: #2196F3;
  background: #f8f9fa;
}

.router-link-active {
  color: #2196F3;
  font-weight: 500;
}

/* Main content */
.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Common utility classes */
.btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.btn-primary {
  background: #2196F3;
  color: white;
}

.btn-primary:hover {
  background: #1976D2;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
}

/* Form styles */
.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

/* Card styles */
.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 1.5rem;
}

/* Loading and error states */
.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #dc3545;
  padding: 1rem;
  border: 1px solid #dc3545;
  border-radius: 4px;
  margin-bottom: 1rem;
}
</style> 