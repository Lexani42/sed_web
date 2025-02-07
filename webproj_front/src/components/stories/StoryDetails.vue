<template>
  <div class="story-details" v-if="story">
    <div class="header">
      <h2>{{ story.title }}</h2>
      <button @click="showAddLanguageForm = true" class="btn-primary">
        Add Language
      </button>
    </div>

    <div class="languages-section">
      <h3>Languages</h3>
      <div class="languages-grid">
        <div v-for="language in story.languages" :key="language.code" class="language-card">
          <div class="language-header">
            <h4>
              {{ getLanguageName(language.code) }}
              <span class="language-formats">
                ({{ getFormatsString(language) }})
              </span>
            </h4>
            <div class="language-actions">
              <button 
                @click="openLanguageContent(language)" 
                class="btn-secondary btn-sm"
              >
                Open
              </button>
              <button 
                @click="deleteLanguage(story.id, language.code)" 
                class="btn-danger btn-sm"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <AddLanguageForm
      v-if="showAddLanguageForm"
      :story-id="String(story.id)"
      @close="showAddLanguageForm = false"
      @save="handleLanguageAdded"
    />

    <!-- Content View Modal -->
    <div v-if="showContentModal" class="modal-overlay" @click.self="closeContentModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ getLanguageName(selectedContent.language) }} Contents</h3>
          <button @click="closeContentModal" class="btn-close">&times;</button>
        </div>
        <div class="modal-body">
          <div v-for="(content, format) in selectedContent.contents" :key="format" class="content-section">
            <div class="content-header">
              <h4>{{ format.charAt(0).toUpperCase() + format.slice(1) }}</h4>
              <button 
                @click="deleteContent(selectedContent.language, format)" 
                class="btn-danger btn-sm"
              >
                Delete
              </button>
            </div>
            <div class="text-content">
              {{ content }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useStoryStore } from '../../store/stories'
import AddLanguageForm from './AddLanguageForm.vue'

const route = useRoute()
const storyStore = useStoryStore()
const { currentStory: story } = storeToRefs(storyStore)
const showAddLanguageForm = ref(false)
const showContentModal = ref(false)
const selectedContent = ref({
  language: '',
  contents: {} as Record<string, string>
})

const languages = {
  'en': 'English',
  'es': 'Spanish',
  'fr': 'French',
  'de': 'German',
  'it': 'Italian',
  'pt': 'Portuguese',
  'ru': 'Russian',
  'zh': 'Chinese',
  'ja': 'Japanese',
  'ko': 'Korean'
}

onMounted(async () => {
  const storyId = route.params.id as string
  console.log('Mounting StoryDetails, fetching story:', storyId)
  await storyStore.fetchStory(storyId)
  console.log('Story data:', story.value)
})

const getLanguageName = (code: string) => {
  return languages[code] || code
}

const getFormatsString = (language: any) => {
    if (!language || !language.contents || !Array.isArray(language.contents)) {
        return ''
    }
    
    const formats = language.contents.map(content => {
        return content.format_id === 1 ? 'Text' : 'Audio'
    })
    
    return [...new Set(formats)].join(' / ')
}

const openLanguageContent = (language: any) => {
    if (!language || !language.contents) {
        console.log('No language contents found')
        return
    }

    const formattedContents = language.contents.reduce((acc: Record<string, string>, content: any) => {
        const formatName = content.format_id === 1 ? 'text' : 'audio'
        acc[formatName] = content.content
        return acc
    }, {})

    selectedContent.value = {
        language: language.code,
        contents: formattedContents
    }
    showContentModal.value = true
    console.log('Selected content:', selectedContent.value)
}

const closeContentModal = () => {
  showContentModal.value = false
}

const deleteLanguage = async (storyId: string, languageCode: string) => {
  if (confirm('Are you sure you want to delete this language?')) {
    await storyStore.deleteLanguage({ storyId, languageCode })
    await storyStore.fetchStory(storyId)
  }
}

const handleLanguageAdded = async () => {
  showAddLanguageForm.value = false
  if (story.value) {
    await storyStore.fetchStory(story.value.id)
  }
}

const deleteContent = async (languageCode: string, format: string) => {
  if (!story.value) return
  
  const formatDisplay = format.charAt(0).toUpperCase() + format.slice(1)
  if (confirm(`Are you sure you want to delete ${formatDisplay} content for ${getLanguageName(languageCode)}?`)) {
    try {
      await storyStore.deleteContent({
        storyId: story.value.id,
        languageCode,
        format
      })
      await storyStore.fetchStory(story.value.id)
      
      // Remove the format from modal contents
      const updatedContents = { ...selectedContent.value.contents }
      delete updatedContents[format]
      selectedContent.value.contents = updatedContents
      
      // Close modal if no contents left
      if (Object.keys(updatedContents).length === 0) {
        closeContentModal()
      }
    } catch (error) {
      console.error('Failed to delete content:', error)
    }
  }
}
</script>

<style scoped>
.story-details {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.languages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 16px;
}

.language-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  background: white;
}

.language-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.language-formats {
  color: #666;
  font-size: 0.9em;
}

.language-actions {
  display: flex;
  gap: 8px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.content-section {
  margin-bottom: 24px;
}

.content-section:last-child {
  margin-bottom: 0;
}

.text-content {
  white-space: pre-wrap;
  font-family: monospace;
  background: #f8f8f8;
  padding: 16px;
  border-radius: 4px;
}

.audio-content {
  display: flex;
  justify-content: center;
  padding: 16px;
}

audio {
  width: 100%;
}

/* Modal styles */
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

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 4px 8px;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 0.9em;
}
</style>
