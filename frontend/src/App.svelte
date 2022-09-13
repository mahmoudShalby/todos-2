<script lang="ts">
  import { onMount } from 'svelte'
import { prevent_default } from 'svelte/internal';
  import { fade } from 'svelte/transition'

  const serverUrl = `http://192.168.1.4:8000`
  async function api(path: string) {
    const response = await fetch(`${serverUrl}/${path}`)
    const data = await response.json()
    return JSON.parse(data)
  }

  let loading = { active: true, message: 'Loading...' }
  let todos = []
  onMount(async () => {
    const connectionTimeout = setTimeout(() => {
      loading.message = 'Some thing went wrong.'
    }, 2000)
    todos = await api('all')
    clearTimeout(connectionTimeout)
    loading.active = false
  })

  let inputValue: string
  async function submitHandler(event: MouseEvent) {
    if (inputValue) {
      todos = [...todos, (await api(`new?content=${inputValue}`))[0]]
      event.target.firstChild.value = ''
    }
  }

  async function deleteTodo(id: number) {
    if (await api(`delete?id=${id}`)) {
      let newTodos = []
      todos.forEach((todo, index) => {
        if (todo.pk !== id)
          newTodos.push(todo)
      })
      todos = newTodos
    }
    else
      loading = { active: true, message: 'Some thing went wrong.' }
  }

  function editTodo(event: MouseEvent) {
    const parent = event.target.parentNode
    const content = event.target.innerText
    parent.children[0].style.display = 'none'
    parent.children[1].style.display = 'none'
    const input = document.createElement('input')
    input.value = content
    input.className = 'outline-none rounded-lg px-2 h-8 w-full text-black'
    parent.appendChild(input)
    input.focus()
    input.addEventListener('keydown', async (event) => {
      if (event.key === 'Enter' && input.value !== '' && input.value.length <= 255) {
        const result = await api(`edit?id=${parent.dataset.id}&new-content=${input.value}`)
        if (result) {
          parent.getElementsByTagName('p')[0].innerText = input.value
          parent.removeChild(input)
          parent.children[0].style.display = 'initial'
          parent.children[1].style.display = 'initial'
        }
        else
          loading = { active: true, message: 'Some thing went wrong.' }
      }
    })
  }

  function focusInput(event: FocusEvent) {
    event.target.classList.add('w-full')
  }
</script>

<div class="h-screen bg-slate-900 text-white grid justify-center pt-3">
  {#if loading.active}
    <span class="grid place-items-center text-3xl text-center" in:fade>{loading.message}</span>
  {:else}
    <div class="flex flex-col items-center gap-3 w-[250px] sm:w-[350px] md:w-[450px] lg:w-[800px]" in:fade={{ delay: 500 }}>
      <h1 class="text-4xl text-center">Todos</h1>
      <form on:submit|preventDefault={submitHandler} class="w-full flex justify-center">
        <input
          bind:value={inputValue}
          type="text"
          class="outline-none rounded-lg px-2 h-7 w-full transition text-black"
          placeholder="Write a new todo"
          on:focus={focusInput}
        >
      </form>
      <div class="flex flex-col gap-1 w-full">
        {#each todos as todo}
          <div data-id={todo.pk} class="flex justify-between items-center px-2 min-h-[45px] hover:bg-slate-700 transition rounded-xl">
            <p on:dblclick={editTodo} class="text-xl break-all">{todo.fields.content}</p>
            <span class="cursor-pointer h-fit" on:click={() => deleteTodo(todo.pk)}>❌</span>
          </div>
        {:else}
          <span class="text-xl text-center">No todos</span>
        {/each}
      </div>
    </div>
  {/if}
</div>
