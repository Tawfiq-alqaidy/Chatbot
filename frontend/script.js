// Configuration
const CONFIG = {
  API_BASE_URL: "http://localhost:8001/api/v1",
  MAX_RETRIES: 3,
  RETRY_DELAY: 1000, // ms
  AUTO_SCROLL_DELAY: 100, // ms
  TYPING_SPEED: 20, // ms per character
};

// Application state
class ChatApp {
  constructor() {
    this.isLoading = false;
    this.currentModel = "mistral:latest";
    this.messageHistory = [];
    this.retryCount = 0;

    this.initializeElements();
    this.bindEvents();
    this.checkAPIStatus();
    this.loadTheme();
  }

  initializeElements() {
    this.chatMessages = document.getElementById("chat-messages");
    this.chatInput = document.getElementById("chat-input");
    this.sendButton = document.getElementById("send-button");
    this.statusIndicator = document.getElementById("status-indicator");
    this.statusDot = this.statusIndicator.querySelector(".status-dot");
    this.statusText = this.statusIndicator.querySelector(".status-text");
    this.themeToggle = document.getElementById("theme-toggle");
    this.charCount = document.querySelector(".char-count");
    this.currentModelSpan = document.getElementById("current-model");
  }

  bindEvents() {
    // Send button click
    this.sendButton.addEventListener("click", () => this.sendMessage());

    // Enter key to send (Shift+Enter for new line)
    this.chatInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    // Input changes
    this.chatInput.addEventListener("input", () => {
      this.handleInputChange();
      this.autoResizeTextarea();
    });

    // Theme toggle
    this.themeToggle.addEventListener("click", () => this.toggleTheme());

    // Auto-resize textarea
    this.chatInput.addEventListener("input", () => this.autoResizeTextarea());
  }

  handleInputChange() {
    const text = this.chatInput.value.trim();
    const charCount = this.chatInput.value.length;

    // Update character count
    this.charCount.textContent = `${charCount}/2000`;

    // Update send button state
    this.sendButton.disabled = !text;

    // Update character count color
    if (charCount > 1800) {
      this.charCount.style.color = "var(--error-color)";
    } else if (charCount > 1500) {
      this.charCount.style.color = "var(--warning-color)";
    } else {
      this.charCount.style.color = "var(--text-secondary)";
    }
  }

  autoResizeTextarea() {
    this.chatInput.style.height = "auto";
    this.chatInput.style.height =
      Math.min(this.chatInput.scrollHeight, 200) + "px";
  }

  async sendMessage() {
    const message = this.chatInput.value.trim();
    if (!message || this.isLoading) return;

    try {
      // Add user message to UI
      this.addMessage("user", message);

      // Clear input
      this.chatInput.value = "";
      this.handleInputChange();
      this.autoResizeTextarea();

      // Create assistant message placeholder for streaming
      const assistantMessageDiv = this.createAssistantMessagePlaceholder();

      // Stream response from API
      await this.streamChatResponse(message, assistantMessageDiv);

      // Reset retry count on success
      this.retryCount = 0;
    } catch (error) {
      console.error("Error sending message:", error);
      this.showError(`Failed to send message: ${error.message}`);
    }
  }

  createAssistantMessagePlaceholder() {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message assistant";

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = "🤖";

    const messageContent = document.createElement("div");
    messageContent.className = "message-content";

    const messageText = document.createElement("div");
    messageText.className = "message-text";
    messageText.textContent = "";

    const messageMeta = document.createElement("div");
    messageMeta.className = "message-meta";
    messageMeta.style.display = "none"; // Hide until we have metadata

    messageContent.appendChild(messageText);
    messageContent.appendChild(messageMeta);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);

    // Add to chat and scroll
    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();

    return messageDiv;
  }

  async streamChatResponse(message, messageDiv) {
    const url = `${CONFIG.API_BASE_URL}/chat/stream`;
    const messageText = messageDiv.querySelector(".message-text");
    const messageMeta = messageDiv.querySelector(".message-meta");

    let fullResponse = "";
    let currentModel = this.currentModel;
    let timestamp = new Date().toISOString();

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
          model: this.currentModel,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6).trim();
            if (data) {
              try {
                const parsed = JSON.parse(data);

                if (parsed.error) {
                  throw new Error(parsed.error);
                }

                if (parsed.done) {
                  // Update metadata when done
                  const timestampDisplay = new Date(
                    timestamp
                  ).toLocaleTimeString();
                  messageMeta.innerHTML = `
                    <span>Model: ${currentModel}</span>
                    <span>${timestampDisplay}</span>
                  `;
                  messageMeta.style.display = "block";
                  return;
                }

                if (parsed.chunk) {
                  fullResponse += parsed.chunk;
                  messageText.textContent = fullResponse;
                  currentModel = parsed.model || currentModel;
                  timestamp = parsed.timestamp || timestamp;

                  // Auto-scroll to keep the message in view
                  this.scrollToBottom();
                }
              } catch (e) {
                console.warn("Failed to parse chunk:", data, e);
              }
            }
          }
        }
      }
    } catch (error) {
      messageText.textContent = `Error: ${error.message}`;
      messageText.style.color = "var(--error-color)";
      throw error;
    }
  }

  async callChatAPI(message) {
    const url = `${CONFIG.API_BASE_URL}/chat`;

    for (let attempt = 0; attempt < CONFIG.MAX_RETRIES; attempt++) {
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: message,
            model: this.currentModel,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || `HTTP ${response.status}`);
        }

        return await response.json();
      } catch (error) {
        console.warn(`API call attempt ${attempt + 1} failed:`, error);

        if (attempt === CONFIG.MAX_RETRIES - 1) {
          throw error;
        }

        // Wait before retry
        await new Promise((resolve) =>
          setTimeout(resolve, CONFIG.RETRY_DELAY * (attempt + 1))
        );
      }
    }
  }

  addMessage(role, content, metadata = {}) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = role === "user" ? "👤" : "🤖";

    const messageContent = document.createElement("div");
    messageContent.className = "message-content";

    const messageText = document.createElement("div");
    messageText.className = "message-text";
    messageText.textContent = content;

    messageContent.appendChild(messageText);

    // Add metadata for assistant messages
    if (role === "assistant" && metadata.timestamp) {
      const messageMeta = document.createElement("div");
      messageMeta.className = "message-meta";

      const timestamp = new Date(metadata.timestamp).toLocaleTimeString();
      const model = metadata.model || this.currentModel;

      messageMeta.innerHTML = `
                <span>Model: ${model}</span>
                <span>${timestamp}</span>
            `;

      messageContent.appendChild(messageMeta);
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);

    // Remove welcome message if it exists
    const welcomeMessage = this.chatMessages.querySelector(".welcome-message");
    if (welcomeMessage) {
      welcomeMessage.remove();
    }

    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();

    // Store in history
    this.messageHistory.push({
      role,
      content,
      metadata,
      timestamp: new Date().toISOString(),
    });
  }

  addTypingIndicator() {
    const typingId = "typing-" + Date.now();
    const messageDiv = document.createElement("div");
    messageDiv.className = "message assistant";
    messageDiv.id = typingId;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = "🤖";

    const messageContent = document.createElement("div");
    messageContent.className = "message-content";

    const typingIndicator = document.createElement("div");
    typingIndicator.className = "typing-indicator";
    typingIndicator.innerHTML = `
            <span>Thinking</span>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;

    messageContent.appendChild(typingIndicator);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);

    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();

    return typingId;
  }

  removeTypingIndicator(typingId) {
    if (typingId) {
      const typingElement = document.getElementById(typingId);
      if (typingElement) {
        typingElement.remove();
      }
    } else {
      // Remove any typing indicators
      const typingElements =
        this.chatMessages.querySelectorAll(".typing-indicator");
      typingElements.forEach((el) => el.closest(".message").remove());
    }
  }

  showError(message) {
    const errorDiv = document.createElement("div");
    errorDiv.className = "error-message";
    errorDiv.textContent = message;

    this.chatMessages.appendChild(errorDiv);
    this.scrollToBottom();

    // Auto-remove error after 5 seconds
    setTimeout(() => {
      if (errorDiv.parentNode) {
        errorDiv.remove();
      }
    }, 5000);
  }

  scrollToBottom() {
    setTimeout(() => {
      if (this.chatMessages) {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        // Force scroll for webkit browsers
        this.chatMessages.scrollTo({
          top: this.chatMessages.scrollHeight,
          behavior: "smooth",
        });
      }
    }, CONFIG.AUTO_SCROLL_DELAY);
  }

  async checkAPIStatus() {
    try {
      this.updateStatus("connecting", "Connecting...");

      const response = await fetch(`${CONFIG.API_BASE_URL}/health`);
      const data = await response.json();

      if (response.ok && data.status === "healthy") {
        this.updateStatus("connected", "Connected");
        this.loadAvailableModels();
      } else {
        this.updateStatus("error", `API ${data.status || "unavailable"}`);
      }
    } catch (error) {
      console.error("API status check failed:", error);
      this.updateStatus("error", "API unreachable");
    }
  }

  async loadAvailableModels() {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/models`);
      const data = await response.json();

      if (data.success && data.models.length > 0) {
        // Update current model if available
        if (data.models.includes(this.currentModel)) {
          this.currentModelSpan.textContent = this.currentModel;
        } else {
          this.currentModel = data.models[0];
          this.currentModelSpan.textContent = this.currentModel;
        }
      }
    } catch (error) {
      console.warn("Failed to load models:", error);
    }
  }

  updateStatus(status, message) {
    this.statusText.textContent = message;
    this.statusDot.className = `status-dot ${status}`;
  }

  toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";

    document.documentElement.setAttribute("data-theme", newTheme);
    this.saveTheme(newTheme);

    // Update theme toggle icon
    const themeIcon = this.themeToggle.querySelector(".theme-icon");
    themeIcon.textContent = newTheme === "dark" ? "☀️" : "🌙";
  }

  loadTheme() {
    const savedTheme = localStorage.getItem("ollama-chat-theme") || "light";
    document.documentElement.setAttribute("data-theme", savedTheme);

    // Update theme toggle icon
    const themeIcon = this.themeToggle.querySelector(".theme-icon");
    themeIcon.textContent = savedTheme === "dark" ? "☀️" : "🌙";
  }

  saveTheme(theme) {
    localStorage.setItem("ollama-chat-theme", theme);
  }
}

// Utility functions
function formatTimestamp(timestamp) {
  return new Date(timestamp).toLocaleString();
}

function sanitizeHTML(str) {
  const temp = document.createElement("div");
  temp.textContent = str;
  return temp.innerHTML;
}

// Initialize app when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  window.chatApp = new ChatApp();
});

// Handle app visibility changes
document.addEventListener("visibilitychange", () => {
  if (!document.hidden && window.chatApp) {
    // Re-check API status when app becomes visible
    window.chatApp.checkAPIStatus();
  }
});

// Handle online/offline status
window.addEventListener("online", () => {
  if (window.chatApp) {
    window.chatApp.checkAPIStatus();
  }
});

window.addEventListener("offline", () => {
  if (window.chatApp) {
    window.chatApp.updateStatus("error", "Offline");
  }
});

// Export for potential external use
window.ChatApp = ChatApp;
