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

    <div class="stories-grid">
      <div v-for="story in stories" :key="story.id" class="story-card">
        <div class="story-header">
          <h3>{{ story.title }}</h3>
          <div class="story-meta">
            <span class="language-count">
              {{ story.languages?.length || 0 }} languages
            </span>
            <span class="format-count">
              {{ story.formats?.length || 0 }} formats
            </span>
          </div>
        </div>

        <div class="languages">
          <span 
            v-for="lang in story.languages" 
            :key="lang.code" 
            class="language-tag"
          >
            {{ lang.code }}
          </span>
        </div>

        <div class="card-actions">
          <button @click="viewStory(story)" class="btn-secondary">
            View Details
          </button>
          <button @click="editStory(story)" class="btn-secondary">
            Edit
          </button>
          <button @click="deleteStory(story.id)" class="btn-danger">
            Delete
          </button>
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

const viewStory = (story) => {
  router.push(`/stories/${story.id}`)
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
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.story-card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.story-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.story-meta {
  display: flex;
  gap: 8px;
  font-size: 0.9em;
  color: #666;
}

.languages {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 12px 0;
}

.language-tag {
  background: #e9ecef;
  padding: 4px 8px;
  border-radius: 12px;
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

.loading,
.error {
  text-align: center;
  padding: 20px;
}

.error {
  color: #f44336;
}
</style>
