<template>
  <div class="story-details">
    <div class="header">
      <h2>{{ story?.title }}</h2>
      <div class="header-actions">
        <button @click="showLanguageForm = true" class="btn-primary">
          Add Language
        </button>
        <button @click="$router.push('/stories')" class="btn-secondary">
          Back to Stories
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      Loading story...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else class="content">
      <div class="languages-section">
        <h3>Available Languages</h3>
        <div class="language-tabs">
          <button
            v-for="lang in story?.languages"
            :key="lang.code"
            :class="['lang-tab', { active: selectedLang === lang.code }]"
            @click="selectLanguage(lang.code)"
          >
            {{ lang.code.toUpperCase() }}
          </button>
        </div>

        <div class="formats-section">
          <div 
            v-for="format in story?.formats" 
            :key="format.type"
            class="format-content"
          >
            <h4>{{ format.type.charAt(0).toUpperCase() + format.type.slice(1) }}</h4>
            <div v-if="format.type === 'text'" class="text-content">
              {{ getContent(selectedLang, format.type) }}
            </div>
            <div v-else-if="format.type === 'audio'" class="audio-content">
              <audio 
                :src="getContent(selectedLang, format.type)" 
                controls
              ></audio>
            </div>
          </div>
        </div>
      </div>

      <div class="actions">
        <button 
          @click="deleteLanguage(selectedLang)" 
          class="btn-danger"
          v-if="story?.languages.length > 1"
        >
          Delete Current Language
        </button>
      </div>
    </div>

    <LanguageForm
      v-if="showLanguageForm"
      :story-id="storyId"
      @close="showLanguageForm = false"
      @save="handleLanguageAdded"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useStoryStore } from '../../store/stories'
import LanguageForm from './LanguageForm.vue'

const route = useRoute()
const storyStore = useStoryStore()
const storyId = route.params.id as string

const showLanguageForm = ref(false)
const selectedLang = ref('')

const { story, loading, error } = storeToRefs(storyStore)

onMounted(async () => {
  await storyStore.fetchStory(storyId)
  if (story.value?.languages.length) {
    selectedLang.value = story.value.languages[0].code
  }
})

const selectLanguage = (langCode: string) => {
  selectedLang.value = langCode
}

const getContent = (langCode: string, format: string) => {
  const language = story.value?.languages.find(l => l.code === langCode)
  return language?.content[format] || ''
}

const deleteLanguage = async (langCode: string) => {
  if (confirm(`Are you sure you want to delete the ${langCode.toUpperCase()} version?`)) {
    try {
      await storyStore.deleteLanguage({
        storyId: storyId,
        languageCode: langCode
      })
      if (story.value?.languages.length) {
        selectedLang.value = story.value.languages[0].code
      }
    } catch (error) {
      console.error('Failed to delete language:', error)
    }
  }
}

const handleLanguageAdded = () => {
  showLanguageForm.value = false
  storyStore.fetchStory(storyId)
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

.header-actions {
  display: flex;
  gap: 12px;
}

.content {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.languages-section {
  margin-bottom: 24px;
}

.language-tabs {
  display: flex;
  gap: 8px;
  margin: 16px 0;
  border-bottom: 1px solid #ddd;
  padding-bottom: 8px;
}

.lang-tab {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background: #f8f9fa;
}

.lang-tab.active {
  background: #2196F3;
  color: white;
}

.formats-section {
  margin-top: 20px;
}

.format-content {
  margin-bottom: 20px;
}

.text-content {
  white-space: pre-wrap;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 4px;
}

.audio-content {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 4px;
}

.actions {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
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

.loading,
.error {
  text-align: center;
  padding: 20px;
}

.error {
  color: #f44336;
}
</style>
