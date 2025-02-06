<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>{{ isEditing ? 'Edit Profile' : 'Create New Profile' }}</h3>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="name">Name</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
          />
        </div>

        <div class="form-group">
          <label for="age">Age</label>
          <input
            id="age"
            v-model.number="form.age"
            type="number"
            required
            min="0"
            max="150"
          />
        </div>

        <div class="form-group">
          <label for="source">Source</label>
          <input
            id="source"
            v-model="form.source"
            type="text"
            required
          />
        </div>

        <div class="form-group">
          <label for="telegram_tag">Telegram Tag (optional)</label>
          <input
            id="telegram_tag"
            v-model="form.telegram_tag"
            type="text"
          />
        </div>

        <div class="form-group">
          <label for="birth_date">Birth Date (optional)</label>
          <input
            id="birth_date"
            v-model="form.birth_date"
            type="date"
          />
        </div>

        <div class="form-actions">
          <button type="button" @click="$emit('close')" class="btn-secondary">
            Cancel
          </button>
          <button type="submit" class="btn-primary">
            {{ isEditing ? 'Update' : 'Create' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'
import { useProfileStore } from '../../store/profiles'

const props = defineProps({
  profile: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'save'])
const profileStore = useProfileStore()

const isEditing = !!props.profile
const form = ref({
  name: props.profile?.name || '',
  age: props.profile?.age || null,
  source: props.profile?.source || '',
  telegram_tag: props.profile?.telegram_tag || '',
  birth_date: props.profile?.birth_date || ''
})

const handleSubmit = async () => {
  try {
    if (isEditing) {
      await profileStore.updateProfile({
        id: props.profile.id,
        ...form.value
      })
    } else {
      await profileStore.createProfile(form.value)
    }
    emit('save')
  } catch (error) {
    console.error('Failed to save profile:', error)
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 24px;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
}

.form-group {
  margin-bottom: 16px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn-primary,
.btn-secondary {
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
</style>
