<template>
  <div class="note-list">
    <div class="header">
      <h3>Notes</h3>
      <button @click="showAddForm = true" class="btn-primary">
        Add Note
      </button>
    </div>

    <div v-if="notes.length === 0" class="empty-state">
      No notes added yet
    </div>

    <div v-else class="notes">
      <div v-for="note in notes" :key="note.id" class="note-item">
        <div class="note-content">
          <div class="note-key">{{ note.key }}</div>
          <div class="note-value">{{ note.value }}</div>
        </div>
        <div class="note-actions">
          <button @click="editNote(note)" class="btn-secondary">
            Edit
          </button>
          <button @click="deleteNote(note.id)" class="btn-danger">
            Delete
          </button>
        </div>
      </div>
    </div>

    <div v-if="showAddForm || editingNote" class="note-form">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="key">Key</label>
          <input
            id="key"
            v-model="form.key"
            type="text"
            required
            placeholder="Enter note key"
          />
        </div>

        <div class="form-group">
          <label for="value">Value</label>
          <textarea
            id="value"
            v-model="form.value"
            required
            placeholder="Enter note value"
            rows="3"
          ></textarea>
        </div>

        <div class="form-actions">
          <button type="button" @click="cancelEdit" class="btn-secondary">
            Cancel
          </button>
          <button type="submit" class="btn-primary">
            {{ editingNote ? 'Update' : 'Add' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps } from 'vue'
import { useProfileStore } from '../../store/profiles'

const props = defineProps({
  profileId: {
    type: String,
    required: true
  },
  notes: {
    type: Array,
    default: () => []
  }
})

const profileStore = useProfileStore()
const showAddForm = ref(false)
const editingNote = ref(null)
const form = ref({
  key: '',
  value: ''
})

const editNote = (note) => {
  editingNote.value = note
  form.value = {
    key: note.key,
    value: note.value
  }
}

const cancelEdit = () => {
  showAddForm.value = false
  editingNote.value = null
  form.value = {
    key: '',
    value: ''
  }
}

const handleSubmit = async () => {
  try {
    if (editingNote.value) {
      await profileStore.updateNote({
        profileId: props.profileId,
        noteId: editingNote.value.id,
        ...form.value
      })
    } else {
      await profileStore.addNote({
        profileId: props.profileId,
        ...form.value
      })
    }
    cancelEdit()
  } catch (error) {
    console.error('Failed to save note:', error)
  }
}

const deleteNote = async (noteId: string) => {
  if (confirm('Are you sure you want to delete this note?')) {
    try {
      await profileStore.deleteNote({
        profileId: props.profileId,
        noteId
      })
    } catch (error) {
      console.error('Failed to delete note:', error)
    }
  }
}
</script>

<style scoped>
.note-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notes {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.note-item {
  background: #f8f9fa;
  border-radius: 4px;
  padding: 12px;
}

.note-content {
  margin-bottom: 8px;
}

.note-key {
  font-weight: 500;
  margin-bottom: 4px;
}

.note-value {
  color: #666;
  white-space: pre-wrap;
}

.note-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.empty-state {
  text-align: center;
  color: #666;
  padding: 16px;
}

.note-form {
  margin-top: 16px;
}

.form-group {
  margin-bottom: 12px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: 500;
}

input,
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn-primary,
.btn-secondary,
.btn-danger {
  padding: 6px 12px;
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
</style>
