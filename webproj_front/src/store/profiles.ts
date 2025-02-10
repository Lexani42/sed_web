import { defineStore } from 'pinia'
import api from '../services/api'
import profileService from '../services/profileService'

interface Profile {
  id: string
  name: string
  age: number
  source: string
  telegram_tag?: string
  birth_date?: string
  hobbies: Hobby[]
  notes: Note[]
}

interface Hobby {
  id: string
  name: string
  profile_id: string
}

interface Note {
  id: string
  key: string
  value: string
  profile_id: string
}

export const useProfileStore = defineStore('profiles', {
  state: () => ({
    profiles: [] as Profile[],
    currentProfile: null as Profile | null,
    loading: false,
    error: null as string | null
  }),

  actions: {
    async fetchProfiles() {
      this.loading = true
      try {
        const response = await api.get('/profiles')
        this.profiles = response.data
      } catch (err) {
        this.error = 'Failed to fetch profiles'
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchProfile(id: string) {
      this.loading = true
      try {
        const response = await api.get(`/profiles/${id}`)
        this.currentProfile = response.data
      } catch (err) {
        this.error = 'Failed to fetch profile'
        throw err
      } finally {
        this.loading = false
      }
    },

    async createProfile(profile: Omit<Profile, 'id' | 'hobbies' | 'notes'>) {
      try {
        const response = await api.post('/profiles', profile)
        this.profiles.push(response.data)
        return response.data
      } catch (err) {
        this.error = 'Failed to create profile'
        throw err
      }
    },

    async updateProfile(profile: Partial<Profile> & { id: string }) {
      try {
        const response = await api.put(`/profiles/${profile.id}`, profile)
        const index = this.profiles.findIndex(p => p.id === profile.id)
        if (index !== -1) {
          this.profiles[index] = response.data
        }
        if (this.currentProfile?.id === profile.id) {
          this.currentProfile = response.data
        }
        return response.data
      } catch (err) {
        this.error = 'Failed to update profile'
        throw err
      }
    },

    async deleteProfile(id: string) {
      try {
        await api.delete(`/profiles/${id}`)
        this.profiles = this.profiles.filter(p => p.id !== id)
        if (this.currentProfile?.id === id) {
          this.currentProfile = null
        }
      } catch (err) {
        this.error = 'Failed to delete profile'
        throw err
      }
    },

    // Hobby management
    async addHobby({ profileId, name }: { profileId: string; name: string }) {
      try {
        const response = await api.post(`/profiles/${profileId}/hobbies`, { name })
        if (this.currentProfile?.id === profileId) {
          this.currentProfile.hobbies.push(response.data)
        }
        return response.data
      } catch (err) {
        this.error = 'Failed to add hobby'
        throw err
      }
    },

    async deleteHobby({ profileId, hobbyId }: { profileId: string; hobbyId: string }) {
      try {
        await api.delete(`/profiles/${profileId}/hobbies/${hobbyId}`)
        if (this.currentProfile?.id === profileId) {
          this.currentProfile.hobbies = this.currentProfile.hobbies.filter(
            h => h.id !== hobbyId
          )
        }
      } catch (err) {
        this.error = 'Failed to delete hobby'
        throw err
      }
    },

    // Note management
    async addNote({ profileId, key, value }: { profileId: string; key: string; value: string }) {
      try {
        const trimmedKey = key.trim()
        const trimmedValue = value.trim()
        
        if (!trimmedKey || !trimmedValue) {
          throw new Error('Key and value cannot be empty')
        }

        const response = await api.post(`/profiles/${profileId}/notes`, {
          key: trimmedKey,
          value: trimmedValue
        })
        
        if (this.currentProfile?.id === profileId) {
          this.currentProfile = {
            ...this.currentProfile,
            notes: [...this.currentProfile.notes, response.data]
          }
        }
        return response.data
      } catch (err) {
        this.error = err.message || 'Failed to add note'
        throw err
      }
    },

    async updateNote({ 
      profileId, 
      noteId, 
      key, 
      value 
    }: { 
      profileId: string
      noteId: string
      key: string
      value: string 
    }) {
      try {
        const response = await api.put(`/profiles/${profileId}/notes/${noteId}`, { key, value })
        if (this.currentProfile?.id === profileId) {
          const index = this.currentProfile.notes.findIndex(n => n.id === noteId)
          if (index !== -1) {
            this.currentProfile.notes[index] = response.data
          }
        }
        return response.data
      } catch (err) {
        this.error = 'Failed to update note'
        throw err
      }
    },

    async deleteNote({ profileId, noteId }: { profileId: string; noteId: string }) {
      try {
        await api.delete(`/profiles/${profileId}/notes/${noteId}`)
        if (this.currentProfile?.id === profileId) {
          this.currentProfile.notes = this.currentProfile.notes.filter(
            n => n.id !== noteId
          )
        }
      } catch (err) {
        this.error = 'Failed to delete note'
        throw err
      }
    },

    async uploadAvatar(profileId: string, file: File) {
      try {
        const updatedProfile = await profileService.uploadAvatar(profileId, file)
        if (this.currentProfile?.id === profileId) {
          this.currentProfile = updatedProfile
        }
        // Update profile in the profiles list
        const index = this.profiles.findIndex(p => p.id === profileId)
        if (index !== -1) {
          this.profiles[index] = updatedProfile
        }
      } catch (err) {
        this.error = 'Failed to upload avatar'
        throw err
      }
    }
  }
})
