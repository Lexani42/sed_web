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
        <div class="profile-header">
          <div class="avatar-container">
            <img :src="profile?.photo_url" alt="Profile photo" class="profile-photo" />
            <input
              type="file"
              ref="fileInput"
              @change="handleAvatarChange"
              accept="image/*"
              class="hidden"
            />
            <button @click="triggerFileInput" class="btn-change-avatar">
              Change Avatar
            </button>
          </div>
          <div class="profile-main-info">
            <h3>{{ profile?.name }}</h3>
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
        </div>
      </div>

      <div class="checkpoints card">
        <h3>Progress Checkpoints</h3>
        <div class="checkpoint-list">
          <div v-for="checkpoint in checkpoints" 
               :key="checkpoint.key" 
               class="checkpoint" 
               :class="{ completed: profile?.[checkpoint.key] }">
            <span class="checkpoint-icon">✓</span>
            <span>{{ checkpoint.label }}</span>
            <button 
              @click="toggleCheckpoint(checkpoint.key)" 
              class="btn-toggle"
              :class="{ 'btn-toggle-on': profile?.[checkpoint.key] }">
              {{ profile?.[checkpoint.key] ? 'Not Done' : 'Done' }}
            </button>
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

const { currentProfile: profile, loading, error } = storeToRefs(profileStore)

const fileInput = ref<HTMLInputElement | null>(null)

const checkpoints = [
  { key: 'answered_opener', label: 'Answered to opener' },
  { key: 'story_discussed', label: 'Story told and discussed' },
  { key: 'closed_for_meet', label: 'Closed for meet' },
  { key: 'closed_for_sex', label: 'Closed for sex' }
]

onMounted(async () => {
  await profileStore.fetchProfile(profileId)
})

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleAvatarChange = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files?.length) return
  
  const file = input.files[0]
  try {
    await profileStore.uploadAvatar(profileId, file)
  } catch (error) {
    console.error('Failed to upload avatar:', error)
  }
}

const toggleCheckpoint = async (key: string) => {
  if (!profile.value) return
  
  try {
    await profileStore.updateProfile({
      id: profileId,
      [key]: !profile.value[key]
    })
  } catch (error) {
    console.error(`Failed to update ${key}:`, error)
  }
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

.avatar-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.profile-photo {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.btn-change-avatar {
  padding: 4px 8px;
  font-size: 0.9em;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.hidden {
  display: none;
}

.profile-header {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.checkpoint-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
}

.checkpoint {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 4px;
  color: #666;
}

.checkpoint.completed {
  background: #e8f5e9;
  color: #2e7d32;
}

.checkpoint-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: currentColor;
  color: white;
  font-size: 12px;
}

.btn-toggle {
  padding: 4px 12px;
  border-radius: 4px;
  border: 1px solid #ccc;
  background: white;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-toggle-on {
  background: #4CAF50;
  color: white;
  border-color: #4CAF50;
}
</style>
