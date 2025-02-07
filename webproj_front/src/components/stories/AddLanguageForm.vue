<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>Add Language</h3>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="language">Language</label>
          <select id="language" v-model="form.language" required @change="updateAvailableFormats">
            <option value="">Select language</option>
            <option v-for="lang in languages" :key="lang.code" :value="lang.code">
              {{ lang.name }} ({{ lang.code }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="format">Format</label>
          <select id="format" v-model="form.format" required>
            <option value="">Select format</option>
            <option v-for="format in availableFormats" :key="format" :value="format">
              {{ format }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="content">Content</label>
          <textarea
            id="content"
            v-model="form.content"
            required
            rows="3"
            :placeholder="getContentPlaceholder()"
          ></textarea>
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
import { ref } from 'vue'
import { useStoryStore } from '../../store/stories'
import { storeToRefs } from 'pinia'

const props = defineProps<{
  storyId: string | number
}>()

const emit = defineEmits(['close', 'save'])
const storyStore = useStoryStore()
const { currentStory: story } = storeToRefs(storyStore)

const languages = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Spanish' },
  { code: 'fr', name: 'French' },
  { code: 'de', name: 'German' },
  { code: 'it', name: 'Italian' },
  { code: 'pt', name: 'Portuguese' },
  { code: 'ru', name: 'Russian' },
  { code: 'zh', name: 'Chinese' },
  { code: 'ja', name: 'Japanese' },
  { code: 'ko', name: 'Korean' }
]

const formats = ['text', 'audio']

const form = ref({
  language: '',
  format: '',
  content: ''
})

const availableFormats = ref(formats)

const updateAvailableFormats = () => {
  console.log('Updating formats for language:', form.value.language)
  if (!form.value.language || !story.value) {
    availableFormats.value = formats
    return
  }

  const existingLanguage = story.value.languages.find(l => l.code === form.value.language)
  if (existingLanguage) {
    console.log('Existing language contents:', existingLanguage.contents)
    const usedFormats = existingLanguage.contents.map(c => c.format_id === 1 ? 'text' : 'audio')
    availableFormats.value = formats.filter(f => !usedFormats.includes(f))
    console.log('Available formats:', availableFormats.value)
  } else {
    availableFormats.value = formats
  }
}

const getContentPlaceholder = () => {
  if (form.value.format === 'text') {
    return 'Enter text content...'
  } else if (form.value.format === 'audio') {
    return 'Enter audio URL or path...'
  }
  return 'Select a format first'
}

const handleSubmit = async () => {
  try {
    const formData = new FormData()
    formData.append('language', form.value.language)
    formData.append('content', form.value.content)
    formData.append('format', form.value.format)

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

input,
textarea,
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

select {
  background-color: white;
}

.form-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 24px;
}
</style> 