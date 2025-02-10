<template>
  <div class="hobby-list">
    <div class="header">
      <h3>Hobbies</h3>
      <button @click="showAddForm = true" class="btn-primary">
        Add Hobby
      </button>
    </div>

    <div v-if="hobbies.length === 0" class="empty-state">
      No hobbies added yet
    </div>

    <ul v-else class="hobbies">
      <li v-for="hobby in hobbies" :key="hobby.id" class="hobby-item">
        <span>{{ hobby.name }}</span>
        <button @click="deleteHobby(hobby.id)" class="btn-danger">
          Delete
        </button>
      </li>
    </ul>

    <div v-if="showAddForm" class="add-form">
      <form @submit.prevent="handleSubmit">
        <input
          v-model="newHobby"
          type="text"
          placeholder="Enter hobby name"
          required
        />
        <div class="form-actions">
          <button type="button" @click="showAddForm = false" class="btn-secondary">
            Cancel
          </button>
          <button type="submit" class="btn-primary">
            Add
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useProfileStore } from '../../store/profiles'

const profileStore = useProfileStore()
// Remove the hobbies prop if you’re not using it from parent:
// const props = defineProps({ profileId: { type: String, required: true } })

// Create a computed property that derives hobbies from the store
const hobbies = computed(() => profileStore.currentProfile?.hobbies || [])

const showAddForm = ref(false)
const newHobby = ref('')

const handleSubmit = async () => {
  try {
    await profileStore.addHobby({
      profileId: profileStore.currentProfile?.id || '', // or use props.profileId if needed
      name: newHobby.value
    })
    newHobby.value = ''
    showAddForm.value = false
  } catch (error) {
    console.error('Failed to add hobby:', error)
  }
}

const deleteHobby = async (hobbyId: string) => {
  if (confirm('Are you sure you want to delete this hobby?')) {
    try {
      await profileStore.deleteHobby({
        profileId: profileStore.currentProfile?.id || '',
        hobbyId
      })
    } catch (error) {
      console.error('Failed to delete hobby:', error)
    }
  }
}
</script>

<style scoped>
.hobby-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hobbies {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hobby-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 4px;
}

.empty-state {
  text-align: center;
  color: #666;
  padding: 16px;
}

.add-form form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.add-form input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn-primary,
.btn-secondary,
.btn-danger {
  padding: 6px 12px;
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
</style>
