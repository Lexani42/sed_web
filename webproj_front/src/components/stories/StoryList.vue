<template>
  <div class="story-list">
    <div class="header">
      <h2>Stories</h2>
      <button @click="showCreateForm = true" class="btn-primary">
        Add New Story
      </button>
    </div>

    <div v-if="loading" class="loading">
      Loading stories...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else class="stories-grid">
      <div v-for="story in stories" :key="story.id" class="story-card">
        <div class="story-header">
          <h3>{{ story.title }}</h3>
          <div class="story-actions">
            <button @click="navigateToDetails(story.id)" class="btn-primary btn-sm">
              View Details
            </button>
          </div>
        </div>
        
        <div class="languages-section">
          <h4>Languages:</h4>
          <div v-for="language in story.languages" :key="language.id" class="language-item">
            <div class="language-header">
              <span class="language-code">{{ language.code }}</span>
              <button @click="deleteLanguage(story.id, language.code)" class="btn-danger btn-sm">
                Delete
              </button>
            </div>
            <div class="contents">
              <div v-for="(content, format) in language.formatted_contents" 
                   :key="format" 
                   class="content-item">
                <strong>{{ format }}:</strong> {{ content }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <StoryForm
      v-if="showCreateForm"
      :story="selectedStory"
      @close="closeForm"
      @save="handleStorySaved"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useStoryStore } from '../../store/stories'
import StoryForm from './StoryForm.vue'

const router = useRouter()
const storyStore = useStoryStore()
const { stories, loading, error } = storeToRefs(storyStore)

const showCreateForm = ref(false)
const selectedStory = ref(null)

onMounted(async () => {
  await storyStore.fetchStories()
})

const navigateToDetails = (storyId: string) => {
  router.push(`/stories/${storyId}`)
}

const editStory = (story) => {
  selectedStory.value = story
  showCreateForm.value = true
}

const deleteStory = async (id: string) => {
  if (confirm('Are you sure you want to delete this story?')) {
    await storyStore.deleteStory(id)
  }
}

const closeForm = () => {
  showCreateForm.value = false
  selectedStory.value = null
}

const handleStorySaved = () => {
  closeForm()
  storyStore.fetchStories()
}

const deleteLanguage = async (storyId: string, languageCode: string) => {
  if (confirm('Are you sure you want to delete this language?')) {
    await storyStore.deleteLanguage({ storyId, languageCode })
  }
}

const showAddLanguageForm = (story) => {
  // Implementation of showAddLanguageForm
}
</script>

<style scoped>
.story-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.stories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.story-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  background: white;
}

.story-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.story-actions {
  display: flex;
  gap: 8px;
}

.language-item {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 4px;
}

.language-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.language-code {
  font-weight: bold;
  text-transform: uppercase;
}

.content-item {
  margin: 4px 0;
  font-size: 0.9em;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 0.9em;
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
