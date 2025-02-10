<template>
  <div class="profile-list">
    <div class="header">
      <h2>Profiles</h2>
      <button @click="showCreateForm = true" class="btn-primary">
        Add New Profile
      </button>
    </div>

    <div v-if="loading" class="loading">
      Loading profiles...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div class="profiles-grid">
      <div v-for="profile in profiles" :key="profile.id" class="profile-card">
        <div class="profile-header">
          <h3>{{ profile.name }}</h3>
          <span class="age">{{ profile.age }} years</span>
        </div>
        
        <div class="profile-info">
          <p><strong>Source:</strong> {{ profile.source }}</p>
          <p v-if="profile.telegram_tag">
            <strong>Telegram:</strong> {{ profile.telegram_tag }}
          </p>
          <p v-if="profile.birth_date">
            <strong>Birth Date:</strong> {{ formatDate(profile.birth_date) }}
          </p>
        </div>

        <div class="profile-stats">
          <span class="stat">
            {{ profile.hobbies?.length || 0 }} hobbies
          </span>
          <span class="stat">
            {{ profile.notes?.length || 0 }} notes
          </span>
        </div>

        <div class="card-actions">
          <button @click="viewProfile(profile)" class="btn-secondary">
            View Details
          </button>
          <button @click="editProfile(profile)" class="btn-secondary">
            Edit
          </button>
          <button @click="deleteProfile(profile.id)" class="btn-danger">
            Delete
          </button>
        </div>
      </div>
    </div>

    <ProfileForm
      v-if="showCreateForm"
      :profile="selectedProfile"
      @close="closeForm"
      @save="handleProfileSaved"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useProfileStore } from '../../store/profiles'
import ProfileForm from './ProfileForm.vue'

const router = useRouter()
const profileStore = useProfileStore()
const showCreateForm = ref(false)
const selectedProfile = ref(null)

const { sortedProfiles: profiles, loading, error } = storeToRefs(profileStore)

onMounted(async () => {
  await profileStore.fetchProfiles()
})

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
}

const viewProfile = (profile) => {
  router.push(`/profiles/${profile.id}`)
}

const editProfile = (profile) => {
  selectedProfile.value = profile
  showCreateForm.value = true
}

const deleteProfile = async (id: string) => {
  if (confirm('Are you sure you want to delete this profile?')) {
    await profileStore.deleteProfile(id)
  }
}

const closeForm = () => {
  showCreateForm.value = false
  selectedProfile.value = null
}

const handleProfileSaved = () => {
  closeForm()
  profileStore.fetchProfiles()
}
</script>

<style scoped>
.profile-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.profile-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.age {
  background: #e9ecef;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.9em;
}

.profile-info {
  margin: 12px 0;
}

.profile-stats {
  display: flex;
  gap: 12px;
  margin: 12px 0;
}

.stat {
  background: #f8f9fa;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
}

.card-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

.btn-primary,
.btn-secondary,
.btn-danger {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: #4CAF50;
  color: white;
}

.btn-secondary {
  background: #2196F3;
  color: white;
}

.btn-danger {
  background: #f44336;
  color: white;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: #f44336;
  padding: 20px;
  text-align: center;
}
</style>
