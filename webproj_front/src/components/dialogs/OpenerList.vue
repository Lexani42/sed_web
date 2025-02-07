<template>
    <div class="opener-list">
        <div class="header">
            <h2>Dialog Openers</h2>
            <button @click="showCreateForm = true" class="btn-primary">
                Add New Opener
            </button>
        </div>

        <div v-if="loading" class="loading">
            Loading openers...
        </div>

        <div v-else-if="error" class="error">
            {{ error }}
        </div>

        <div v-else class="openers-grid">
            <div v-for="opener in openers" :key="opener.id" class="opener-card">
                <div class="opener-content">
                    <h3>{{ opener.text }}</h3>
                    <p class="context">Context: {{ opener.context }}</p>
                </div>
                
                <div class="continue-options">
                    <h4>Continue Options:</h4>
                    <ul>
                        <div v-for="option in opener.continue_options" :key="option.id">
                            {{ option.text }}
                            <span class="weight">[Weight: {{ option.weight }}]</span><br>
                            <button @click="deleteOption(opener.id, option.id)" class="btn-danger btm-sm">
                                Delete
                            </button>
                        </div>
                    </ul><br>
                    <button 
                        @click="showAddOptionForm(opener)" 
                        class="btn-secondary"
                    >
                        Add Option
                    </button>
                </div>

                <div class="card-actions">
                    <button @click="editOpener(opener)" class="btn-secondary">
                        Edit
                    </button>
                    <button @click="deleteOpener(opener.id)" class="btn-danger">
                        Delete
                    </button>
                </div>
            </div>
        </div>

        <OpenerForm
            v-if="showCreateForm"
            @close="showCreateForm = false"
            @save="handleOpenerCreated"
        />

        <ContinueOptionForm
            v-if="showOptionForm"
            :opener="selectedOpener"
            @close="showOptionForm = false"
            @save="handleOptionCreated"
        />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useDialogStore } from '../../store/dialogs'
import OpenerForm from './OpenerForm.vue'
import ContinueOptionForm from './ContinueOptionForm.vue'

const dialogStore = useDialogStore()
const showCreateForm = ref(false)
const showOptionForm = ref(false)
const selectedOpener = ref(null)

const { openers, loading, error } = storeToRefs(dialogStore)

onMounted(async () => {
    await dialogStore.fetchOpeners()
})

const showAddOptionForm = (opener) => {
    selectedOpener.value = opener
    showOptionForm.value = true
}

const editOpener = (opener) => {
    selectedOpener.value = opener
    showCreateForm.value = true
}

const deleteOpener = async (id: string) => {
    if (confirm('Are you sure you want to delete this opener?')) {
        await dialogStore.deleteOpener(id)
    }
}

const deleteOption = async (openerId: string, optionId: string) => {
    if (confirm('Are you sure you want to delete this option?')) {
        try {
            await dialogStore.deleteContinueOption({
                openerId,
                optionId
            })
            await dialogStore.fetchOpeners()
        } catch (error) {
            console.error('Error deleting option:', error)
        }
    } 
}

const handleOpenerCreated = () => {
    showCreateForm.value = false
    dialogStore.fetchOpeners()
}

const handleOptionCreated = () => {
    showOptionForm.value = false
    dialogStore.fetchOpeners()
}
</script>

<style scoped>
.opener-list {
    padding: 20px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.openers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
}

.opener-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 16px;
    background: white;
}

.opener-content {
    margin-bottom: 16px;
}

.context {
    color: #666;
    font-size: 0.9em;
}

.continue-options {
    margin: 16px 0;
    padding: 8px;
    background: #f5f5f5;
    border-radius: 4px;
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

.option-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px;
    border-bottom: 1px solid #eee;
}

.option-item:last-child {
    border-bottom: none;
}

.option-text {
    flex: 1;
}

.option-actions {
    display: flex;
    align-items: center;
    gap: 8px;
}

.weight-badge {
    font-size: 0.9em;
    color: #666;
    background: #f0f0f0;
    padding: 2px 6px;
    border-radius: 4px;
}

.btn-sm {
    padding: 4px 8px;
    font-size: 0.9em;
}
</style>