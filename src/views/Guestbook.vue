<template>
  <div class="guestbook-page">
    <div class="page-header animate-in">
      <h1 class="page-title">💬 留言板</h1>
      <p class="page-desc">留下你的想法和建议</p>
    </div>

    <!-- 留言表单 -->
    <div class="form-card animate-in animate-in-delay-1">
      <h3 class="form-title">📝 写留言</h3>
      <div class="form-body">
        <div class="form-row">
          <div class="form-group">
            <label>昵称 <span class="required">*</span></label>
            <input v-model="form.name" type="text" placeholder="你的名字" maxlength="30" />
          </div>
          <div class="form-group">
            <label>联系方式</label>
            <input v-model="form.contact" type="text" placeholder="邮箱 / GitHub / 微信（选填）" />
          </div>
        </div>
        <div class="form-group">
          <label>留言内容 <span class="required">*</span></label>
          <textarea v-model="form.content" rows="4" placeholder="写下你想说的话..." maxlength="1000"></textarea>
          <div class="char-count">{{ form.content.length }}/1000</div>
        </div>
        <div class="form-actions">
          <button class="submit-btn" @click="submitMessage" :disabled="submitting || !form.name || !form.content">
            {{ submitting ? '提交中...' : '💌 发布留言' }}
          </button>
        </div>
        <div v-if="submitError" class="submit-error">{{ submitError }}</div>
      </div>
    </div>

    <!-- 留言列表 -->
    <div class="messages-section animate-in animate-in-delay-2">
      <div class="section-header">
        <h3>💬 全部留言 <span class="count-badge">{{ messages.length }}</span></h3>
      </div>

      <div v-if="loading" class="loading-state">加载中...</div>

      <div v-if="!loading && messages.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <div class="empty-text">还没有留言</div>
        <div class="empty-hint">来写第一条留言吧！</div>
      </div>

      <div v-if="!loading" class="messages-list">
        <div
          v-for="msg in sortedMessages"
          :key="msg.id"
          class="message-card animate-in"
          :class="'animate-in-delay-' + Math.min(msg.id % 5 + 1, 5)"
        >
          <div class="message-header">
            <div class="message-avatar">
              {{ getAvatar(msg.name) }}
            </div>
            <div class="message-info">
              <div class="message-name">{{ msg.name }}</div>
              <div class="message-date">{{ formatDate(msg.date || msg.created_at) }}</div>
            </div>
            <div v-if="msg.contact" class="message-contact" :title="msg.contact">📎</div>
          </div>
          <div class="message-content">{{ msg.content }}</div>
          <div v-if="msg.reply" class="message-reply">
            <div class="reply-label">🦞 小熙的回复：</div>
            <div class="reply-text">{{ msg.reply }}</div>
          </div>
          <div class="message-footer">
            <span v-if="!msg.is_approved" class="pending-badge">⏳ 待审核</span>
            <span v-else class="approved-badge">✅ 已公开</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE = '/api'

export default {
  name: 'GuestbookPage',
  data() {
    return {
      messages: [],
      loading: true,
      submitting: false,
      submitError: '',
      form: {
        name: '',
        contact: '',
        content: ''
      }
    }
  },
  computed: {
    sortedMessages() {
      // 已审核的在前，按时间倒序
      return [...this.messages].sort((a, b) => {
        if (a.is_approved && !b.is_approved) return -1
        if (!a.is_approved && b.is_approved) return 1
        return new Date(b.date || b.created_at) - new Date(a.date || a.created_at)
      })
    }
  },
  methods: {
    getAvatar(name) {
      return name ? name.charAt(0).toUpperCase() : '?'
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const d = new Date(dateStr)
      return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`
    },
    async loadMessages() {
      try {
        const res = await fetch(`${API_BASE}/messages`)
        const data = await res.json()
        this.messages = Array.isArray(data) ? data : (data.data || [])
      } catch (e) {
        console.error('加载留言失败:', e)
      } finally {
        this.loading = false
      }
    },
    async submitMessage() {
      if (!this.form.name.trim() || !this.form.content.trim()) return
      this.submitting = true
      this.submitError = ''
      try {
        const newMsg = {
          id: Date.now(),
          name: this.form.name.trim(),
          contact: this.form.contact.trim() || '',
          content: this.form.content.trim(),
          date: new Date().toISOString(),
          is_approved: false,
          reply: ''
        }
        const allMessages = [...this.messages, newMsg]
        const res = await fetch(`${API_BASE}/messages`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(allMessages)
        })
        if (!res.ok) throw new Error('提交失败')
        this.messages = allMessages
        this.form = { name: '', contact: '', content: '' }
        // 提示成功
        this.submitError = '' // 清空错误
        alert('✅ 留言已提交，审核后将会显示！')
      } catch (e) {
        this.submitError = '提交失败，请稍后重试'
        console.error('提交留言失败:', e)
      } finally {
        this.submitting = false
      }
    }
  },
  mounted() {
    this.loadMessages()
  }
}
</script>

<style scoped>
.guestbook-page {
  padding: 32px 16px;
  max-width: 700px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 8px;
}

.page-desc {
  color: var(--text-secondary);
  font-size: 1rem;
}

/* 表单卡片 */
.form-card {
  background: var(--card-bg, #fff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 32px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.form-title {
  padding: 16px 20px;
  font-size: 1rem;
  font-weight: 700;
  border-bottom: 1px solid var(--border, #e2e8f0);
}

.form-body {
  padding: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-group {
  margin-bottom: 14px;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-secondary, #475569);
  margin-bottom: 4px;
}

.required {
  color: #ef4444;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border, #cbd5e1);
  border-radius: 10px;
  font-size: 0.9rem;
  background: var(--bg, #f8fafc);
  color: var(--text-primary, #0f172a);
  font-family: inherit;
  transition: all 0.2s;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
  background: var(--card-bg, #fff);
}

.char-count {
  text-align: right;
  font-size: 0.8rem;
  color: var(--text-muted, #94a3b8);
  margin-top: 4px;
}

.form-actions {
  margin-top: 4px;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  background: linear-gradient(135deg, #4f46e5, #818cf8);
  color: white;
  transition: all 0.2s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-error {
  margin-top: 8px;
  padding: 8px 12px;
  background: #fee2e2;
  color: #991b1b;
  border-radius: 8px;
  font-size: 0.85rem;
}

/* 留言列表 */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 1.1rem;
  font-weight: 700;
}

.count-badge {
  font-size: 0.8rem;
  background: var(--bg, #f1f5f9);
  padding: 2px 8px;
  border-radius: 999px;
  color: var(--text-secondary, #64748b);
  font-weight: 500;
  margin-left: 6px;
}

.loading-state {
  text-align: center;
  padding: 40px;
  color: var(--text-muted, #94a3b8);
}

/* 留言卡片 */
.messages-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-card {
  background: var(--card-bg, #fff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 14px;
  padding: 16px 20px;
  transition: all 0.2s;
}

.message-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.message-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4f46e5, #818cf8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.message-info {
  flex: 1;
}

.message-name {
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-primary, #0f172a);
}

.message-date {
  font-size: 0.8rem;
  color: var(--text-muted, #94a3b8);
}

.message-contact {
  font-size: 1rem;
  cursor: help;
  opacity: 0.6;
}

.message-content {
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--text-primary, #0f172a);
  white-space: pre-wrap;
  word-break: break-word;
}

.message-reply {
  margin-top: 12px;
  padding: 12px;
  background: #eef2ff;
  border-radius: 10px;
  border-left: 3px solid #4f46e5;
}

.reply-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #4f46e5;
  margin-bottom: 4px;
}

.reply-text {
  font-size: 0.9rem;
  color: var(--text-primary, #0f172a);
  line-height: 1.5;
}

.message-footer {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}

.pending-badge {
  font-size: 0.75rem;
  color: #92400e;
  background: #fef3c7;
  padding: 2px 8px;
  border-radius: 4px;
}

.approved-badge {
  font-size: 0.75rem;
  color: #065f46;
  background: #d1fae5;
  padding: 2px 8px;
  border-radius: 4px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 12px;
}

.empty-text {
  font-size: 1.1rem;
  color: var(--text-secondary, #64748b);
  margin-bottom: 4px;
}

.empty-hint {
  font-size: 0.9rem;
  color: var(--text-muted, #94a3b8);
}

/* 动画 */
.animate-in {
  opacity: 0;
  transform: translateY(20px);
  animation: slideUp 0.4s ease forwards;
}

.animate-in-delay-1 { animation-delay: 0.1s; }
.animate-in-delay-2 { animation-delay: 0.2s; }
.animate-in-delay-3 { animation-delay: 0.3s; }
.animate-in-delay-4 { animation-delay: 0.4s; }
.animate-in-delay-5 { animation-delay: 0.5s; }

@keyframes slideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
