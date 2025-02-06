<template>
  <div class="profile-details">
    <div class="header">
      <h2>{{ profile?.name }}'s Profile</h2>
      <button @click="$router.push('/profiles')" class="btn-secondary">
        Back to Profiles
      </button>
    </div>

    <div v-if="loading" class="loading">
      Loading profile...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else class="content">
      <div class="profile-info card">
        <h3>Profile Information</h3>
        <div class="info-grid">
          <div class="info-item">
            <label>Age:</label>
            <span>{{ profile?.age }}</span>
          </div>
          <div class="info-item">
            <label>Source:</label>
            <span>{{ profile?.source }}</span>
          </div>
          <div class="info-item" v-if="profile?.telegram_tag">
            <label>Telegram:</label>
            <span>{{ profile?.telegram_tag }}</span>
          </div>
          <div class="info-item" v-if="profile?.birth_date">
            <label>Birth Date:</label>
            <span>{{ formatDate(profile?.birth_date) }}</span>
          </div>
        </div>
      </div>

      <div class="sections">
        <div class="section card">
          <HobbyList 
            :profile-id="profileId" 
            :hobbies="profile?.hobbies || []" 
          />
        </div>

        <div class="section card">
          <NoteList 
            :profile-id="profileId" 
            :notes="profile?.notes || []" 
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useProfileStore } from '../../store/profiles'
import HobbyList from './HobbyList.vue'
import NoteList from './NoteList.vue'

const route = useRoute()
const profileStore = useProfileStore()
const profileId = route.params.id as string

const { profile, loading, error } = storeToRefs(profileStore)

onMounted(async () => {
  await profileStore.fetchProfile(profileId)
})

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
}
</script>

<style scoped>
.profile-details {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item label {
  font-weight: 500;
  color: #666;
}

.sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.section {
  height: fit-content;
}

.btn-secondary {
  background: #2196F3;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}
</style>
