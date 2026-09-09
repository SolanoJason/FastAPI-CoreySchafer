(() => {
  const state = { posts: [], users: 0 };
  const list = document.querySelector('#postList');
  const dialog = document.querySelector('#postDialog');
  const form = document.querySelector('#postForm');
  const toast = document.querySelector('#toast');
  const notify = (message) => { toast.textContent = message; toast.classList.add('translate-y-0', 'opacity-100'); window.setTimeout(() => toast.classList.remove('translate-y-0', 'opacity-100'), 2600); };
  const request = async (url, options = {}) => {
    const response = await fetch(url, { headers: { 'Content-Type': 'application/json', ...(options.headers || {}) }, ...options });
    if (!response.ok) { let detail = 'Something went wrong'; try { detail = (await response.json()).detail || detail; } catch {} throw new Error(detail); }
    return response.status === 204 ? null : response.json();
  };
  const date = (value) => value ? new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(value)) : 'No date';
  const render = (items = state.posts) => {
    if (!items.length) { list.innerHTML = '<div class="px-2.5 py-8 text-center text-sm text-(--app-text-muted)">No stories yet. Start with a new post.</div>'; return; }
    list.innerHTML = items.map((post) => `<article class="grid gap-4 rounded-md border border-(--app-border-color) p-4 transition hover:-translate-y-0.5 hover:border-green-300 sm:grid-cols-[1fr_auto]"><div><h3 class="mb-2 text-base font-bold tracking-tight">${escapeHtml(post.title)}</h3><p class="text-sm leading-relaxed text-(--app-text-muted)">${escapeHtml(post.content)}</p><div class="mt-3 font-mono text-[11px] text-(--app-text-muted)"><span class="font-semibold text-(--app-accent)">${escapeHtml(post.user?.username || 'Unknown author')}</span> · ${date(post.date_posted)}</div></div><div class="flex items-start justify-end gap-1"><button class="p-1.5 text-xl leading-none text-(--app-text-muted) hover:text-(--app-accent)" data-edit="${post.id}" aria-label="Edit ${escapeHtml(post.title)}">&#9998;</button><button class="p-1.5 text-xl leading-none text-(--app-text-muted) hover:text-red-500" data-delete="${post.id}" aria-label="Delete ${escapeHtml(post.title)}">&#215;</button></div></article>`).join('');
  };
  const escapeHtml = (value) => String(value ?? '').replace(/[&<>'"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char]));
  const loadPosts = async () => { try { state.posts = await request('/api/posts'); render(); } catch (error) { list.innerHTML = `<div class="px-2.5 py-8 text-center text-sm text-(--app-text-muted)">${escapeHtml(error.message)}</div>`; } };
  const openComposer = (post) => { form.reset(); form.elements.id.value = post?.id || ''; form.elements.title.value = post?.title || ''; form.elements.content.value = post?.content || ''; document.querySelector('#dialogTitle').textContent = post ? 'Edit post' : 'New post'; dialog.showModal(); };
  document.querySelectorAll('[data-open-composer]').forEach((button) => button.addEventListener('click', () => openComposer()));
  document.querySelectorAll('[data-close-dialog]').forEach((button) => button.addEventListener('click', () => dialog.close()));
  form.addEventListener('submit', async (event) => { event.preventDefault(); const data = { title: form.elements.title.value.trim(), content: form.elements.content.value.trim() }; try { if (form.elements.id.value) await request(`/api/posts/${form.elements.id.value}`, { method: 'PUT', body: JSON.stringify(data) }); else await request('/api/posts', { method: 'POST', body: JSON.stringify(data) }); dialog.close(); notify(form.elements.id.value ? 'Post updated' : 'Post published'); await loadPosts(); } catch (error) { notify(error.message); } });
  list.addEventListener('click', async (event) => { const edit = event.target.closest('[data-edit]'); const remove = event.target.closest('[data-delete]'); if (edit) openComposer(state.posts.find((post) => post.id === Number(edit.dataset.edit))); if (remove && window.confirm('Delete this post?')) { try { await request(`/api/posts/${remove.dataset.delete}`, { method: 'DELETE' }); notify('Post deleted'); await loadPosts(); } catch (error) { notify(error.message); } } });
  document.querySelector('#postSearch').addEventListener('input', (event) => { const term = event.target.value.toLowerCase(); render(state.posts.filter((post) => `${post.title} ${post.content} ${post.user?.username || ''}`.toLowerCase().includes(term))); });
  document.querySelector('#userForm').addEventListener('submit', async (event) => { event.preventDefault(); const userForm = event.currentTarget; try { const user = await request('/api/users', { method: 'POST', body: JSON.stringify({ username: userForm.username.value.trim(), email: userForm.email.value.trim() }) }); state.users += 1; document.querySelector('#userCount').textContent = state.users; const result = document.querySelector('#userResult'); result.hidden = false; result.innerHTML = `<strong>${escapeHtml(user.username)}</strong><span>${escapeHtml(user.email)}</span><br><button type="button" data-user-posts="${user.id}">View this person's posts</button>`; userForm.reset(); notify('Person added'); } catch (error) { notify(error.message); } });
  document.querySelector('#userResult').addEventListener('click', async (event) => { const button = event.target.closest('[data-user-posts]'); if (!button) return; try { const posts = await request(`/api/users/${button.dataset.userPosts}/posts`); render(posts); document.querySelector('#postsHeading').scrollIntoView({ behavior: 'smooth' }); } catch (error) { notify(error.message); } });
  loadPosts();
})();
