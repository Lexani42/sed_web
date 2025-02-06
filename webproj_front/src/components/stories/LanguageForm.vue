<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>Add New Language</h3>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="language">Language</label>
          <select 
            id="language" 
            v-model="form.language"
            required
          >
            <option value="">Select language</option>
            <option 
              v-for="lang in availableLanguages" 
              :key="lang.code"
              :value="lang.code"
            >
              {{ lang.name }}
            </option>
          </select>
        </div>

        <div v-for="format in story?.formats" :key="format.type" class="form-group">
          <label :for="format.type">
            {{ format.type.charAt(0).toUpperCase() + format.type.slice(1) }} Content
          </label>
          
          <textarea
            v-if="format.type === 'text'"
            :id="format.type"
            v-model="form.content[format.type]"
            rows="6"
            required
          ></textarea>

          <input
            v-else-if="format.type === 'audio'"
            :id="format.type"
            type="file"
            accept="audio/*"
            @change="handleAudioUpload($event, format.type)"
            required
          />
        </div>

        <div class="form-actions">
          <button type="button" @click="$emit('close')" class="btn-secondary">
            Cancel
          </button>
          <button type="submit" class="btn-primary">
            Add Language
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useStoryStore } from '../../store/stories'

const props = defineProps({
  storyId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close', 'save'])
const storyStore = useStoryStore()

const form = ref({
  language: '',
  content: {
    text: '',
    audio: null as File | null
  }
})

const availableLanguages = ref([
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Spanish' },
  { code: 'fr', name: 'French' },
  { code: 'de', name: 'German' },
  { code: 'it', name: 'Italian' }
  // Add more languages as needed
])

const { story } = storeToRefs(storyStore)

onMounted(async () => {
  if (!story.value) {
    await storyStore.fetchStory(props.storyId)
  }
  
  // Filter out already used languages
  if (story.value?.languages) {
    availableLanguages.value = availableLanguages.value.filter(
      lang => !story.value?.languages.find(l => l.code === lang.code)
    )
  }
})

const handleAudioUpload = (event: Event, format: string) => {
  const input = event.target as HTMLInputElement
  if (input.files?.length) {
    form.value.content[format] = input.files[0]
  }
}

const handleSubmit = async () => {
  try {
    const formData = new FormData()
    formData.append('language', form.value.language)
    
    for (const [format, content] of Object.entries(form.value.content)) {
      if (content) {
        formData.append(`content[${format}]`, content)
      }
    }

    await storyStore.addLanguage({
      storyId: props.storyId,
      formData
    })
    
    emit('save')
  } catch (error) {
    console.error('Failed to add language:', error)
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
  max-height: 90vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 16px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

select,
textarea {
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
