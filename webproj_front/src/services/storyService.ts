import api from './api'

export interface Story {
  id: string
  title: string
  languages: Language[]
  formats: Format[]
}

export interface Language {
  code: string
  content: {
    [key: string]: string // Format type -> content mapping
  }
}

export interface Format {
  type: 'text' | 'audio'
}

export interface CreateStoryPayload {
  title: string
  content: string
  language: string
  format: string
}

export interface UpdateStoryPayload {
  id: string
  title: string
  content?: string
}

class StoryService {
  async getStories() {
    const response = await api.get<Story[]>('/stories')
    return response.data
  }

  async getStory(id: string) {
    const response = await api.get<Story>(`/stories/${id}`)
    return response.data
  }

  async createStory(payload: CreateStoryPayload) {
    const response = await api.post<Story>('/stories', {
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
    return response.data
  }

  async updateStory(payload: UpdateStoryPayload) {
    const response = await api.put<Story>(`/stories/${payload.id}`, payload)
    return response.data
  }

  async deleteStory(id: string) {
    await api.delete(`/stories/${id}`)
  }

  async addLanguage(storyId: string, formData: FormData) {
    const response = await api.post<Story>(
      `/stories/${storyId}/languages`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    return response.data
  }

  async updateLanguage(storyId: string, languageCode: string, formData: FormData) {
    const response = await api.put<Story>(
      `/stories/${storyId}/languages/${languageCode}`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    return response.data
  }

  async deleteLanguage(storyId: string, languageCode: string) {
    const response = await api.delete<Story>(
      `/stories/${storyId}/languages/${languageCode}`
    )
    return response.data
  }

  async addFormat(storyId: string, format: string, content: string | File) {
    const formData = new FormData()
    formData.append('format', format)
    formData.append('content', content)

    const response = await api.post<Story>(
      `/stories/${storyId}/formats`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    return response.data
  }

  async deleteFormat(storyId: string, format: string) {
    const response = await api.delete<Story>(`/stories/${storyId}/formats/${format}`)
    return response.data
  }
}

export default new StoryService()
