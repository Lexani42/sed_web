<template>
  <div class="home">
    <h1>Welcome to Story Management</h1>
    
    <div class="navigation-grid">
      <router-link to="/dialogs" class="nav-card">
        <h2>Dialogs</h2>
        <p>Manage dialog openers and continue options</p>
      </router-link>

      <router-link to="/profiles" class="nav-card">
        <h2>Profiles</h2>
        <p>Manage profiles, hobbies, and notes</p>
      </router-link>

      <router-link to="/stories" class="nav-card">
        <h2>Stories</h2>
        <p>Manage stories in multiple languages and formats</p>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.home {
  padding: 20px;
}

.navigation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 24px;
}

.nav-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s;
}

.nav-card:hover {
  transform: translateY(-2px);
}

.nav-card h2 {
  margin: 0 0 12px 0;
  color: #2196F3;
}

.nav-card p {
  margin: 0;
  color: #666;
}
</style>
