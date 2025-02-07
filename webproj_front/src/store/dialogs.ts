import { defineStore } from 'pinia'
import api from '../services/api'

interface Opener {
  id: string
  text: string
  context: string
  continueOptions: ContinueOption[]
}

interface ContinueOption {
  id: string
  text: string
  weight: number
  opener_id: string
}

interface DeleteContinueOptionPayload {
  openerId: string
  optionId: string
}

export const useDialogStore = defineStore('dialogs', {
  state: () => ({
    openers: [] as Opener[],
    loading: false,
    error: null as string | null
  }),

  actions: {
    async fetchOpeners() {
      this.loading = true
      try {
        const response = await api.get('/openers')
        this.openers = response.data
      } catch (err) {
        this.error = 'Failed to fetch openers'
      } finally {
        this.loading = false
      }
    },

    async createOpener(opener: { text: string; context: string }) {
      try {
        const response = await api.post('/openers', opener)
        this.openers.push(response.data)
        return response.data
      } catch (err) {
        this.error = 'Failed to create opener'
        throw err
      }
    },

    async updateOpener(opener: { id: string; text: string; context: string }) {
      try {
        const response = await api.put(`/openers/${opener.id}`, opener)
        const index = this.openers.findIndex(o => o.id === opener.id)
        if (index !== -1) {
          this.openers[index] = response.data
        }
        return response.data
      } catch (err) {
        this.error = 'Failed to update opener'
        throw err
      }
    },

    async deleteOpener(id: string) {
      try {
        await api.delete(`/openers/${id}`)
        this.openers = this.openers.filter(o => o.id !== id)
      } catch (err) {
        this.error = 'Failed to delete opener'
        throw err
      }
    },

    async addContinueOption(option: { openerId: string; text: string; weight: number }) {
      try {
        const response = await api.post(`/openers/${option.openerId}/options`, option)
        const opener = this.openers.find(o => o.id === option.openerId)
        if (opener) {
          opener.continueOptions.push(response.data)
        }
        return response.data
      } catch (err) {
        this.error = 'Failed to add continue option'
        throw err
      }
    },

    async deleteContinueOption(payload: DeleteContinueOptionPayload) {
      this.loading = true
      try {
        await api.delete(`/openers/${payload.openerId}/options/${payload.optionId}`)
      } catch (err) {
        this.error = 'Failed to delete continue option'
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})
