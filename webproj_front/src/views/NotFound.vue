<template>
  <div class="not-found">
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for doesn't exist.</p>
    <router-link to="/" class="btn-primary">
      Return to Home
    </router-link>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.not-found {
  text-align: center;
  padding: 40px 20px;
}

h1 {
  color: #f44336;
  margin-bottom: 16px;
}

p {
  color: #666;
  margin-bottom: 24px;
}

.btn-primary {
  background: #2196F3;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  display: inline-block;
}

.btn-primary:hover {
  background: #1976D2;
}
</style>
