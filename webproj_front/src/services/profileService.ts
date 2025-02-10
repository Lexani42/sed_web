import api from './api'

export interface Profile {
  id: string
  name: string
  age: number
  source: string
  telegram_tag?: string
  birth_date?: string
  photo: string
  photo_url: string
  opener_id?: string
  story_id?: string
  answered_opener: boolean
  story_discussed: boolean
  closed_for_meet: boolean
  closed_for_sex: boolean
  hobbies: Hobby[]
  notes: Note[]
}

export interface Hobby {
  id: string
  name: string
  profile_id: string
}

export interface Note {
  id: string
  key: string
  value: string
  profile_id: string
}

export interface CreateProfilePayload {
  name: string
  age: number
  source: string
  telegram_tag?: string
  birth_date?: string
  photo?: string
  opener_id?: string
  story_id?: string
  answered_opener?: boolean
  story_discussed?: boolean
  closed_for_meet?: boolean
  closed_for_sex?: boolean
}

export interface UpdateProfilePayload {
  id: string
  name?: string
  age?: number
  source?: string
  telegram_tag?: string
  birth_date?: string
  photo?: string
  opener_id?: string
  story_id?: string
  answered_opener?: boolean
  story_discussed?: boolean
  closed_for_meet?: boolean
  closed_for_sex?: boolean
}

class ProfileService {
  async getProfiles() {
    const response = await api.get<Profile[]>('/profiles')
    return response.data
  }

  async getProfile(id: string) {
    const response = await api.get<Profile>(`/profiles/${id}`)
    return response.data
  }

  async createProfile(payload: CreateProfilePayload) {
    const response = await api.post<Profile>('/profiles', payload)
    return response.data
  }

  async updateProfile(payload: UpdateProfilePayload) {
    const response = await api.put<Profile>(`/profiles/${payload.id}`, payload)
    return response.data
  }

  async deleteProfile(id: string) {
    await api.delete(`/profiles/${id}`)
  }

  // Hobby management
  async addHobby(profileId: string, name: string) {
    const response = await api.post<Hobby>(`/profiles/${profileId}/hobbies`, { name })
    return response.data
  }

  async deleteHobby(profileId: string, hobbyId: string) {
    await api.delete(`/profiles/${profileId}/hobbies/${hobbyId}`)
  }

  // Note management
  async addNote(profileId: string, key: string, value: string) {
    const response = await api.post<Note>(
      `/profiles/${profileId}/notes`,
      { key, value }
    )
    return response.data
  }

  async updateNote(profileId: string, noteId: string, key: string, value: string) {
    const response = await api.put<Note>(
      `/profiles/${profileId}/notes/${noteId}`,
      { key, value }
    )
    return response.data
  }

  async deleteNote(profileId: string, noteId: string) {
    await api.delete(`/profiles/${profileId}/notes/${noteId}`)
  }

  async uploadAvatar(profileId: string, file: File) {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post<Profile>(
        `/profiles/${profileId}/avatar`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }
    )
    return response.data
  }
}

export default new ProfileService()
