import { defineStore } from 'pinia'
import api from '../services/api'

interface Story {
  id: string
  title: string
  languages: Language[]
  formats: Format[]
}

interface Language {
  code: string
  content: {
    [key: string]: string // Format type -> content mapping
  }
}

interface Format {
  type: 'text' | 'audio'
}

interface CreateStoryPayload {
  title: string
  content: string
  language: string
  format: string
}

interface DeleteContentPayload {
  storyId: string
  languageCode: string
  format: string
}

export const useStoryStore = defineStore('stories', {
  state: () => ({
    stories: [] as Story[],
    currentStory: null as Story | null,
    loading: false,
    error: null as string | null
  }),

  actions: {
    async fetchStories() {
      this.loading = true
      try {
        const response = await api.get('/stories')
        this.stories = response.data
      } catch (err) {
        this.error = 'Failed to fetch stories'
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchStory(id: string) {
      this.loading = true
      try {
        const response = await api.get(`/stories/${id}`)
        this.currentStory = response.data
      } catch (err) {
        this.error = 'Failed to fetch story'
        throw err
      } finally {
        this.loading = false
      }
    },

    async createStory(payload: CreateStoryPayload) {
      try {
        const response = await api.post('/stories', {
          title: payload.title,
          languages: [{
            code: payload.language,
            content: {
              [payload.format]: payload.content
            }
          }],
          formats: [{
            type: payload.format
          }]
        })
        this.stories.push(response.data)
        return response.data
      } catch (err) {
        this.error = 'Failed to create story'
        throw err
      }
    },

    async updateStory(payload: { id: string; title: string; content?: string }) {
      try {
        const response = await api.put(`/stories/${payload.id}`, payload)
        const index = this.stories.findIndex(s => s.id === payload.id)
        if (index !== -1) {
          this.stories[index] = response.data
        }
        if (this.currentStory?.id === payload.id) {
          this.currentStory = response.data
        }
        return response.data
      } catch (err) {
        this.error = 'Failed to update story'
        throw err
      }
    },

    async deleteStory(id: string) {
      try {
        await api.delete(`/stories/${id}`)
        this.stories = this.stories.filter(s => s.id !== id)
        if (this.currentStory?.id === id) {
          this.currentStory = null
        }
      } catch (err) {
        this.error = 'Failed to delete story'
        throw err
      }
    },

    async addLanguage({ storyId, formData }: { storyId: string, formData: FormData }) {
      try {
        console.log('Adding language with data:', {
          storyId,
          language: formData.get('language'),
          format: formData.get('format')
        })

        const response = await api.post(
          `/stories/${storyId}/languages`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )
        console.log('Server response:', response.data)
        
        if (this.currentStory?.id === storyId) {
          await this.fetchStory(storyId)
        }
        return response.data
      } catch (err) {
        console.error('Failed to add language:', err.response?.data || err)
        this.error = 'Failed to add language'
        throw err
      }
    },

    async updateLanguage({ 
      storyId, 
      languageCode, 
      formData 
    }: { 
      storyId: string
      languageCode: string
      formData: FormData 
    }) {
      try {
        const response = await api.put(
          `/stories/${storyId}/languages/${languageCode}`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )
        if (this.currentStory?.id === storyId) {
          this.currentStory = response.data
        }
        return response.data
      } catch (err) {
        this.error = 'Failed to update language'
        throw err
      }
    },

    async deleteLanguage({ storyId, languageCode }: { storyId: string, languageCode: string }) {
      try {
        await api.delete(`/stories/${storyId}/languages/${languageCode}`)
        await this.fetchStories() // Refresh the stories list
      } catch (err) {
        this.error = 'Failed to delete language'
        throw err
      }
    },

    async addFormat({ 
      storyId, 
      format, 
      content 
    }: { 
      storyId: string
      format: string
      content: string | File 
    }) {
      try {
        const formData = new FormData()
        formData.append('format', format)
        formData.append('content', content)

        const response = await api.post(
          `/stories/${storyId}/formats`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )
        if (this.currentStory?.id === storyId) {
          this.currentStory = response.data
        }
        return response.data
      } catch (err) {
        this.error = 'Failed to add format'
        throw err
      }
    },

    async deleteFormat({ 
      storyId, 
      format 
    }: { 
      storyId: string
      format: string 
    }) {
      try {
        const response = await api.delete(`/stories/${storyId}/formats/${format}`)
        if (this.currentStory?.id === storyId) {
          this.currentStory = response.data
        }
        return response.data
      } catch (err) {
        this.error = 'Failed to delete format'
        throw err
      }
    },

    async deleteContent({ storyId, languageCode, format }: DeleteContentPayload) {
      try {
        const formatId = format === 'text' ? 1 : 2
        const response = await api.delete(
          `/stories/${storyId}/languages/${languageCode}/formats/${formatId}`
        )
        return response.data
      } catch (err) {
        console.error('Failed to delete content:', err.response?.data || err)
        this.error = 'Failed to delete content'
        throw err
      }
    }
  }
})
