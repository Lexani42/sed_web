<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <h3>{{ isEditing ? 'Edit Opener' : 'Create New Opener' }}</h3>
        
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="text">Opener Text</label>
            <textarea
              id="text"
              v-model="form.text"
              required
              rows="3"
            ></textarea>
          </div>
  
          <div class="form-group">
            <label for="context">Context</label>
            <input
              id="context"
              v-model="form.context"
              type="text"
              required
            />
          </div>
  
          <div class="form-actions">
            <button type="button" @click="$emit('close')" class="btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn-primary">
              {{ isEditing ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, defineProps, defineEmits } from 'vue'
  import { useDialogStore } from '../../store/dialogs'
  
  const props = defineProps({
    opener: {
      type: Object,
      default: null
    }
  })
  
  const emit = defineEmits(['close', 'save'])
  const dialogStore = useDialogStore()
  
  const isEditing = !!props.opener
  const form = ref({
    text: props.opener?.text || '',
    context: props.opener?.context || ''
  })
  
  const handleSubmit = async () => {
    try {
      if (isEditing) {
        await dialogStore.updateOpener({
          id: props.opener.id,
          ...form.value
        })
      } else {
        await dialogStore.createOpener(form.value)
      }
      emit('save')
    } catch (error) {
      console.error('Failed to save opener:', error)
    }
  }
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background: white;
    padding: 24px;
    border-radius: 8px;
    width: 100%;
    max-width: 500px;
  }
  
  .form-group {
    margin-bottom: 16px;
  }
  
  label {
    display: block;
    margin-bottom: 8px;
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
    margin-top: 24px;
  }
  </style>