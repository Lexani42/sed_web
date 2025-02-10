<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>{{ isEditing ? 'Edit Story' : 'Create New Story' }}</h3>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="title">Title</label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            required
          />
        </div>

        <div class="form-group">
          <label for="content">Content</label>
          <textarea
            id="content"
            v-model="form.content"
            rows="6"
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label>Initial Language</label>
          <select v-model="form.language" required>
            <option value="">Select language</option>
            <option value="en">English</option>
            <option value="ru">Russian</option>
            <option value="ua">Ukrainian</option>
            <!-- Add more language options as needed -->
          </select>
        </div>

        <div class="form-group">
          <label>Format</label>
          <select v-model="form.format" required>
            <option value="">Select format</option>
            <option value="text">Text</option>
            <option value="audio">Audio</option>
          </select>
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
import { useStoryStore } from '../../store/stories'

const props = defineProps({
  story: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'save'])
const storyStore = useStoryStore()

const isEditing = !!props.story
const form = ref({
  title: props.story?.title || '',
  content: props.story?.content || '',
  language: props.story?.languages?.[0]?.code || '',
  format: props.story?.formats?.[0]?.type || ''
})

const handleSubmit = async () => {
  try {
    if (isEditing) {
      await storyStore.updateStory({
        id: props.story.id,
        title: form.value.title,
        content: form.value.content
      })
    } else {
      await storyStore.createStory({
        title: form.value.title,
        content: form.value.content,
        language: form.value.language,
        format: form.value.format
      })
    }
    emit('save')
  } catch (error) {
    console.error('Failed to save story:', error)
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
  max-width: 600px;
}

.form-group {
  margin-bottom: 16px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

input,
textarea,
select {
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
