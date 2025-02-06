import api from './api'

export interface Opener {
  id: string
  text: string
  context: string
  continueOptions: ContinueOption[]
}

export interface ContinueOption {
  id: string
  text: string
  weight: number
  opener_id: string
}

export interface CreateOpenerPayload {
  text: string
  context: string
}

export interface UpdateOpenerPayload extends CreateOpenerPayload {
  id: string
}

export interface CreateOptionPayload {
  text: string
  weight: number
}

class DialogService {
  async getOpeners() {
    const response = await api.get<Opener[]>('/openers')
    return response.data
  }

  async getOpener(id: string) {
    const response = await api.get<Opener>(`/openers/${id}`)
    return response.data
  }

  async createOpener(payload: CreateOpenerPayload) {
    const response = await api.post<Opener>('/openers', payload)
    return response.data
  }

  async updateOpener(payload: UpdateOpenerPayload) {
    const response = await api.put<Opener>(`/openers/${payload.id}`, payload)
    return response.data
  }

  async deleteOpener(id: string) {
    await api.delete(`/openers/${id}`)
  }

  async addContinueOption(openerId: string, payload: CreateOptionPayload) {
    const response = await api.post<ContinueOption>(
      `/openers/${openerId}/options`,
      payload
    )
    return response.data
  }

  async updateContinueOption(
    openerId: string,
    optionId: string,
    payload: CreateOptionPayload
  ) {
    const response = await api.put<ContinueOption>(
      `/openers/${openerId}/options/${optionId}`,
      payload
    )
    return response.data
  }

  async deleteContinueOption(openerId: string, optionId: string) {
    await api.delete(`/openers/${openerId}/options/${optionId}`)
  }
}

export default new DialogService()
