# OpenCode Installation and Configuration Guide
## Complete Setup Documentation with Troubleshooting

> **Version**: 1.0 | **Last Updated**: May 2026 | **Compatibility**: OpenCode 1.3.0+

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Initial Configuration](#initial-configuration)
4. [Provider Setup](#provider-setup)
5. [Project Initialization](#project-initialization)
6. [Configuration Files](#configuration-files)
7. [MCP Servers (Optional)](#mcp-servers-optional)
8. [Advanced Configuration](#advanced-configuration)
9. [Verification](#verification)
10. [Comprehensive Troubleshooting](#comprehensive-troubleshooting)
11. [Reference Documentation](#reference-documentation)
12. [Quick Reference](#quick-reference)

---

## Prerequisites

### Required Software

Before installing OpenCode, ensure you have:

#### 1. Modern Terminal Emulator

Choose one of the following:

| Terminal | Platform | Download Link |
|----------|----------|--------------|
| **WezTerm** | Cross-platform | https://wezterm.org |
| **Alacritty** | Cross-platform | https://alacritty.org |
| **Ghostty** | Linux, macOS | https://ghostty.org |
| **Kitty** | Linux, macOS | https://sw.kovidgoyal.net/kitty/ |
| **Windows Terminal** | Windows | Built-in on Windows 11 |

**Recommended for beginners**: WezTerm (best cross-platform support)

#### 2. Node.js (Required for npm installation)

- **Download**: https://nodejs.org/
- **Recommended**: Latest LTS version (20.x or higher)
- **Verify installation**:
  ```bash
  node --version
  npm --version
  ```

#### 3. Git (Optional but recommended)

- **Download**: https://git-scm.com/downloads
- **Verify installation**:
  ```bash
  git --version
  ```

### Windows-Specific Prerequisites

For Windows users, **Windows Subsystem for Linux (WSL)** is highly recommended:

#### Installing WSL 2

1. **Open PowerShell as Administrator** and run:
   ```powershell
   wsl --install
   ```
   This installs Ubuntu by default.

2. **Restart your computer**

3. **Verify installation**:
   ```powershell
   wsl --list --verbose
   ```

4. **Update WSL** (if needed):
   ```powershell
   wsl --update
   ```

5. **Set WSL 2 as default**:
   ```powershell
   wsl --set-default-version 2
   ```

#### Why WSL?

- Better performance
- Full compatibility with OpenCode features
- Native Linux environment
- Seamless integration with Windows

**Note**: While OpenCode runs natively on Windows, WSL is the recommended approach for the best experience.

---

## Installation

### Quick Decision Guide

| Method | Best For | Install Time |
|--------|----------|--------------|
| Quick Install Script | Most users, fastest setup | 1-2 min |
| npm/pnpm/yarn | Node.js developers | 2-3 min |
| Homebrew | macOS/Linux users | 2-3 min |
| Chocolatey/Scoop | Windows users | 2-3 min |
| Docker | Containerized environments | 5 min |
| Binary Download | Offline or restricted environments | 5-10 min |

### Method 1: Quick Install Script (Recommended)

**macOS / Linux / WSL:**
```bash
curl -fsSL https://opencode.ai/install | bash
```

**What it does**:
- Detects your operating system
- Downloads the appropriate binary
- Installs to `~/.local/bin/opencode`
- Adds to PATH automatically
- Verifies the installation

**After installation**:
```bash
# Restart your terminal, then verify
opencode --version
```

### Method 2: Package Managers

#### Using npm (Cross-platform)
```bash
npm install -g opencode-ai
```

#### Using pnpm
```bash
pnpm install -g opencode-ai
```

#### Using Yarn
```bash
yarn global add opencode-ai
```

#### Using Bun
```bash
bun install -g opencode-ai
```

#### Using Homebrew (macOS/Linux)

**Option A: OpenCode tap (recommended)**
```bash
brew install anomalyco/tap/opencode
```

**Option B: Official Homebrew formula**
```bash
brew install opencode
```

**Note**: The OpenCode tap provides more frequent updates.

**Update**:
```bash
brew update && brew upgrade opencode
```

#### Arch Linux

**Stable release**:
```bash
sudo pacman -S opencode
```

**Latest from AUR**:
```bash
paru -S opencode-bin
```

### Method 3: Windows-Specific Installers

#### Using Chocolatey
```powershell
choco install opencode
```

**Update**:
```powershell
choco upgrade opencode
```

#### Using Scoop
```powershell
scoop install opencode
```

**Update**:
```powershell
scoop update opencode
```

#### Using npm (Windows)
```powershell
npm install -g opencode-ai
```

### Method 4: Docker

```bash
# Run OpenCode in Docker
docker run -it --rm ghcr.io/anomalyco/opencode

# With volume mounting for persistence
docker run -it --rm \
  -v ~/.local/share/opencode:/root/.local/share/opencode \
  -v ~/.config/opencode:/root/.config/opencode \
  -v $(pwd):/workspace \
  ghcr.io/anomalyco/opencode
```

### Method 5: Direct Binary Download

1. **Visit GitHub Releases**:
   https://github.com/anomalyco/opencode/releases

2. **Download the appropriate binary** for your platform:
   - `opencode-linux-x64`
   - `opencode-macos-x64` or `opencode-macos-arm64`
   - `opencode-windows-x64.exe`

3. **Extract and move to a directory in your PATH**:

   **macOS/Linux**:
   ```bash
   chmod +x opencode-*
   sudo mv opencode-* /usr/local/bin/opencode
   ```

   **Windows**:
   - Move `opencode.exe` to `C:\Program Files\opencode\`
   - Add to PATH via System Environment Variables

4. **Verify**:
   ```bash
   opencode --version
   ```

---

## Initial Configuration

### First-Time Setup

1. **Verify installation**:
   ```bash
   opencode --version
   ```
   
   Expected output: `opencode version X.X.X`

2. **Launch OpenCode**:
   ```bash
   opencode
   ```
   
   You'll see the OpenCode TUI (Terminal User Interface).

3. **Explore built-in help**:
   ```
   /help
   ```

### Understanding OpenCode's Directory Structure

After first run, OpenCode creates these directories:

| Directory | Purpose | Location |
|-----------|---------|----------|
| **Config** | Configuration files | `~/.config/opencode/` |
| **Data** | Auth tokens, cache | `~/.local/share/opencode/` |
| **Agents** | Custom agents | `~/.config/opencode/agents/` |
| **Commands** | Custom commands | `~/.config/opencode/commands/` |
| **Plugins** | Custom plugins | `~/.config/opencode/plugins/` |
| **Themes** | Custom themes | `~/.config/opencode/themes/` |

**Windows equivalents**:
- Config: `%APPDATA%\opencode\`
- Data: `%LOCALAPPDATA%\opencode\`

---

## Provider Setup

OpenCode requires an LLM provider to function. Choose based on your needs:

### Provider Comparison

| Provider | Cost | Speed | Quality | Best For |
|----------|------|-------|---------|----------|
| **OpenCode Zen** | Pay-per-use | Fast | High | Beginners, tested models |
| **Anthropic (Claude)** | Subscription or API | Fast | Highest | Production work |
| **OpenAI (ChatGPT)** | Subscription or API | Fast | High | General use |
| **GitHub Copilot** | Subscription | Fast | High | GitHub users |
| **Ollama** | Free (local) | Medium | Medium-High | Privacy, offline use |
| **Groq** | Free tier + paid | Fastest | High | Speed-critical tasks |
| **DeepSeek** | Very low cost | Fast | High | Budget-conscious |

### Option 1: OpenCode Zen (Recommended for Beginners)

**Why choose this?**
- Curated models tested by OpenCode team
- Simple setup
- Reliable performance
- Good for getting started

**Setup steps**:

1. **In OpenCode TUI, run**:
   ```
   /connect
   ```

2. **Select "OpenCode Zen"** from the list

3. **Open browser and visit**: https://opencode.ai/auth
   - Sign in or create account
   - Add billing details
   - Click "Create API Key"
   - Copy the API key

4. **Paste API key** in terminal when prompted

5. **Select a model**:
   ```
   /models
   ```
   
   **Recommended models**:
   - `zen/claude-sonnet-4-5` - Best balance
   - `zen/qwen-3-coder-480b` - Best for coding
   - `zen/claude-haiku-4-5` - Fastest, cheapest

**Storage**: API key stored in `~/.local/share/opencode/auth.json`

### Option 2: Anthropic (Claude)

**Why choose this?**
- Highest quality responses
- Excellent coding capabilities
- Strong reasoning
- Claude Pro/Max subscriptions available

**Setup steps**:

1. **Sign up**: https://console.anthropic.com/

2. **In OpenCode TUI**:
   ```
   /connect
   ```

3. **Select "Anthropic"**

4. **Choose authentication**:
   - **Claude Pro/Max** (OAuth): Opens browser for authentication
   - **API Key**: Enter manually

5. **For API Key method**:
   - Go to https://console.anthropic.com/settings/keys
   - Click "Create Key"
   - Copy and paste in terminal

6. **Select model**:
   ```
   /models
   ```
   
   **Recommended**:
   - `anthropic/claude-sonnet-4-5` - Best overall
   - `anthropic/claude-opus-4` - Most capable
   - `anthropic/claude-haiku-4-5` - Fastest

**Pricing**: https://www.anthropic.com/pricing

### Option 3: OpenAI (ChatGPT)

**Why choose this?**
- Familiar interface
- ChatGPT Plus/Pro subscription available
- Good general performance

**Setup steps**:

1. **Sign up**: https://platform.openai.com/ or https://chatgpt.com/

2. **In OpenCode TUI**:
   ```
   /connect
   ```

3. **Select "OpenAI"**

4. **Choose authentication**:
   - **ChatGPT Plus/Pro** (OAuth): Opens browser
   - **API Key**: Enter manually

5. **For API Key method**:
   - Visit https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy and paste in terminal

6. **Select model**:
   ```
   /models
   ```
   
   **Recommended**:
   - `openai/gpt-5-nano` - Best for coding
   - `openai/gpt-4o` - Best overall
   - `openai/gpt-4o-mini` - Fastest, cheapest

### Option 4: GitHub Copilot

**Why choose this?**
- Already have subscription
- Native GitHub integration
- Multiple model options

**Setup steps**:

1. **Ensure you have**: GitHub Copilot subscription
   - Individual: https://github.com/features/copilot
   - Business: Contact your admin

2. **In OpenCode TUI**:
   ```
   /connect
   ```

3. **Select "GitHub Copilot"**

4. **Browser opens to**: https://github.com/login/device

5. **Enter code** displayed in terminal

6. **Authorize OpenCode**

7. **Select model**:
   ```
   /models
   ```
   
   **Available models**:
   - `github-copilot/claude-sonnet-4.5`
   - `github-copilot/gpt-5-nano`
   - `github-copilot/o1-preview`

**Note**: Some models require Copilot Pro+ subscription

### Option 5: Ollama (Local Models)

**Why choose this?**
- Complete privacy (runs locally)
- No internet required
- No per-token costs
- Full control

**Setup steps**:

1. **Install Ollama**: https://ollama.com/download

2. **Download a model**:
   ```bash
   ollama pull qwen2.5-coder:32b
   ```
   
   **Recommended models**:
   - `qwen2.5-coder:32b` - Best for coding
   - `llama3.3:70b` - Best overall
   - `deepseek-r1:32b` - Good reasoning

3. **Start Ollama server**:
   ```bash
   ollama serve
   ```

4. **Configure in OpenCode** (`~/.config/opencode/opencode.json`):
   ```json
   {
     "$schema": "https://opencode.ai/config.json",
     "provider": {
       "ollama": {
         "npm": "@ai-sdk/openai-compatible",
         "name": "Ollama (local)",
         "options": {
           "baseURL": "http://localhost:11434/v1"
         },
         "models": {
           "qwen2.5-coder:32b": {
             "name": "Qwen 2.5 Coder 32B"
           }
         }
       }
     },
     "model": "ollama/qwen2.5-coder:32b"
   }
   ```

5. **Restart OpenCode** and verify:
   ```
   /models
   ```

**Requirements**:
- 16GB+ RAM for 7B models
- 32GB+ RAM for 32B models
- 64GB+ RAM for 70B models

### Option 6: Other Popular Providers

#### DeepSeek (Very Low Cost)

1. **Sign up**: https://platform.deepseek.com/
2. **Generate API key**
3. **In OpenCode**:
   ```
   /connect
   ```
4. **Select "DeepSeek"**
5. **Recommended model**: `deepseek/deepseek-v4-pro`

#### Groq (Very Fast)

1. **Sign up**: https://console.groq.com/
2. **Create API key**
3. **In OpenCode**:
   ```
   /connect
   ```
4. **Select "Groq"**
5. **Recommended models**: 
   - `groq/llama-3.3-70b-versatile`
   - `groq/qwen-3-coder-480b`

#### Azure OpenAI

1. **Create Azure resource**: https://portal.azure.com/
2. **Deploy model** in Azure AI Foundry
3. **In OpenCode**:
   ```
   /connect
   ```
4. **Select "Azure OpenAI"**
5. **Set environment variables**:
   ```bash
   export AZURE_RESOURCE_NAME=your-resource-name
   export AZURE_API_KEY=your-api-key
   ```

### Full Provider List

For 75+ providers, see: https://opencode.ai/docs/providers

---

## Project Initialization

### Setting Up OpenCode for Your Project

1. **Navigate to project directory**:
   ```bash
   cd /path/to/your/project
   ```

2. **Launch OpenCode**:
   ```bash
   opencode
   ```

3. **Initialize the project**:
   ```
   /init
   ```

4. **OpenCode will**:
   - Analyze your codebase
   - Identify frameworks and languages
   - Detect coding patterns
   - Create `AGENTS.md` file

### Understanding AGENTS.md

The `AGENTS.md` file helps OpenCode understand your project:

**Example AGENTS.md**:
```markdown
# Project: My Awesome App

## Tech Stack
- Frontend: React 18 with TypeScript
- Backend: Node.js + Express
- Database: PostgreSQL
- Testing: Jest + React Testing Library

## Architecture
- Monorepo using Turborepo
- Microservices pattern
- RESTful API

## Coding Standards
- Use functional components
- Prefer TypeScript over JavaScript
- Follow Airbnb style guide
- Write tests for all new features

## Important Conventions
- All API routes start with `/api/v1/`
- Use named exports over default exports
- Environment variables in `.env.local`
```

**Best practices**:
- ✅ Commit `AGENTS.md` to Git
- ✅ Update when architecture changes
- ✅ Include team conventions
- ✅ Document important patterns
- ❌ Don't include sensitive information

### Project-Specific Configuration

Create `opencode.json` in your project root:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "instructions": [
    "CONTRIBUTING.md",
    "docs/coding-guidelines.md"
  ],
  "formatter": true,
  "lsp": true,
  "permission": {
    "bash": "ask",
    "edit": "allow"
  }
}
```

**Commit this file** to share configuration with your team.

---

## Configuration Files

### Configuration Hierarchy

OpenCode uses a hierarchical configuration system:

```
┌─────────────────────────────────────────┐
│  8. macOS Managed Preferences (MDM)     │  ← Highest Priority
│     (Cannot be overridden by user)      │
├─────────────────────────────────────────┤
│  7. Managed Config Files                │
│     /Library/Application Support/...    │
├─────────────────────────────────────────┤
│  6. Inline Config (OPENCODE_CONFIG_     │
│     CONTENT env var)                    │
├─────────────────────────────────────────┤
│  5. .opencode/ Directories              │
│     (agents, commands, plugins)         │
├─────────────────────────────────────────┤
│  4. Project Config                      │
│     ./opencode.json                     │
├─────────────────────────────────────────┤
│  3. Custom Config                       │
│     OPENCODE_CONFIG env var             │
├─────────────────────────────────────────┤
│  2. Global Config                       │
│     ~/.config/opencode/opencode.json    │
├─────────────────────────────────────────┤
│  1. Remote Config                       │
│     .well-known/opencode                │  ← Lowest Priority
└─────────────────────────────────────────┘
```

**Key principle**: Later configs override earlier ones, but non-conflicting settings are merged.

### Global Configuration

**Location**: `~/.config/opencode/opencode.json`

**Purpose**: User-wide settings (providers, models, permissions)

**Example**:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5",
  "autoupdate": true,
  "share": "manual",
  "snapshot": true,
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0"
  },
  "provider": {
    "anthropic": {
      "options": {
        "timeout": 600000,
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

### TUI Configuration

**Location**: `~/.config/opencode/tui.json`

**Purpose**: Terminal UI customization

**Example**:
```json
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "tokyonight",
  "scroll_speed": 3,
  "scroll_acceleration": {
    "enabled": true
  },
  "diff_style": "auto",
  "mouse": true,
  "keybinds": {
    "command_list": "ctrl+p",
    "send": "enter",
    "cancel": "ctrl+c",
    "undo": "ctrl+z",
    "redo": "ctrl+y"
  }
}
```

**Available themes**: https://opencode.ai/docs/themes

### Project Configuration

**Location**: `<project-root>/opencode.json`

**Purpose**: Project-specific settings (safe to commit to Git)

**Example**:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "instructions": [
    "CONTRIBUTING.md",
    "docs/architecture.md",
    ".cursor/rules/*.md"
  ],
  "formatter": {
    "prettier": {
      "disabled": false
    },
    "eslint": {
      "disabled": false
    }
  },
  "lsp": true,
  "tools": {
    "bash": true,
    "write": true,
    "edit": true
  },
  "permission": {
    "bash": "ask",
    "edit": "allow"
  },
  "command": {
    "test": {
      "template": "Run tests with coverage and show failures",
      "description": "Run project tests",
      "agent": "build"
    },
    "lint": {
      "template": "Run linter and fix issues",
      "description": "Lint and fix code"
    }
  }
}
```

### Environment-Based Configuration

**Using environment variables**:
```bash
# Custom config file
export OPENCODE_CONFIG=/path/to/custom-config.json

# Custom config directory
export OPENCODE_CONFIG_DIR=/path/to/config-dir

# Inline config
export OPENCODE_CONFIG_CONTENT='{"model": "anthropic/claude-sonnet-4-5"}'

# Run OpenCode
opencode
```

### Configuration Options Reference

#### Provider Configuration

```json
{
  "provider": {
    "provider-name": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Display Name",
      "options": {
        "baseURL": "https://api.example.com",
        "apiKey": "{env:API_KEY}",
        "timeout": 600000,
        "chunkTimeout": 30000,
        "headers": {
          "Custom-Header": "value"
        }
      },
      "models": {
        "model-id": {
          "name": "Model Display Name",
          "limit": {
            "context": 128000,
            "output": 8192
          }
        }
      }
    }
  },
  "model": "provider-name/model-id",
  "small_model": "provider-name/small-model-id"
}
```

#### Tool Configuration

```json
{
  "tools": {
    "bash": true,
    "write": true,
    "edit": true,
    "read": true,
    "glob": true,
    "grep": true,
    "task": true,
    "webfetch": true,
    "question": true,
    "todowrite": true
  }
}
```

#### Permission Configuration

```json
{
  "permission": {
    "*": "allow",
    "bash": {
      "*": "ask",
      "rm -rf *": "deny",
      "sudo *": "deny"
    },
    "edit": "ask",
    "write": "ask",
    "webfetch": "ask"
  }
}
```

Permission levels:
- `"allow"` - Always allow without asking
- `"ask"` - Prompt user for approval
- `"deny"` - Always deny

#### Formatter Configuration

```json
{
  "formatter": true
}
```

Or with customization:
```json
{
  "formatter": {
    "prettier": {
      "disabled": false,
      "command": ["npx", "prettier", "--write", "$FILE"],
      "extensions": [".js", ".ts", ".jsx", ".tsx", ".json"]
    },
    "black": {
      "disabled": false,
      "extensions": [".py"]
    }
  }
}
```

#### LSP Configuration

```json
{
  "lsp": true
}
```

Or with customization:
```json
{
  "lsp": {
    "typescript": {
      "disabled": false
    },
    "python": {
      "disabled": false
    }
  }
}
```

#### Custom Agents

```json
{
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices",
      "model": "anthropic/claude-sonnet-4-5",
      "prompt": "You are an expert code reviewer...",
      "tools": {
        "write": false,
        "edit": false
      }
    }
  },
  "default_agent": "build"
}
```

#### Custom Commands

```json
{
  "command": {
    "test": {
      "template": "Run full test suite with coverage",
      "description": "Execute project tests",
      "agent": "build",
      "model": "anthropic/claude-haiku-4-5"
    },
    "deploy": {
      "template": "Deploy to $ARGUMENTS environment",
      "description": "Deploy application"
    }
  }
}
```

#### Variable Substitution

```json
{
  "provider": {
    "openai": {
      "options": {
        "apiKey": "{env:OPENAI_API_KEY}"
      }
    }
  },
  "instructions": [
    "{file:~/.opencode/shared-rules.md}",
    "CONTRIBUTING.md"
  ]
}
```

Variables:
- `{env:VAR_NAME}` - Environment variable
- `{file:path}` - File contents

---

## MCP Servers (Optional)

MCP (Model Context Protocol) servers add external tools to OpenCode.

### What are MCP Servers?

MCP servers provide additional capabilities to OpenCode:
- Search documentation (Context7)
- Search GitHub code (Grep)
- Interact with services (Sentry, Jira)
- Custom integrations

**⚠️ Important**: MCP servers add to context usage. Be selective!

### Adding Local MCP Servers

**Configuration**:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "server-name": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-package"],
      "enabled": true,
      "environment": {
        "API_KEY": "{env:MY_API_KEY}"
      },
      "timeout": 5000
    }
  }
}
```

**Example - MCP Everything (test server)**:
```json
{
  "mcp": {
    "mcp_everything": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-everything"],
      "enabled": true
    }
  }
}
```

**Usage**:
```
use the mcp_everything tool to add 3 and 4
```

### Adding Remote MCP Servers

**Configuration**:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "server-name": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp",
      "enabled": true,
      "headers": {
        "Authorization": "Bearer {env:API_TOKEN}"
      },
      "timeout": 5000
    }
  }
}
```

### Popular MCP Servers

#### 1. Context7 - Documentation Search

**Purpose**: Search through 60,000+ documentation sources

**Setup**:
```json
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "enabled": true
    }
  }
}
```

**With API key** (higher rate limits):
```json
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "enabled": true,
      "headers": {
        "CONTEXT7_API_KEY": "{env:CONTEXT7_API_KEY}"
      }
    }
  }
}
```

**Sign up**: https://context7.com/

**Usage**:
```
How do I configure a Cloudflare Worker? use context7
```

#### 2. Grep by Vercel - GitHub Code Search

**Purpose**: Search code examples from GitHub repositories

**Setup**:
```json
{
  "mcp": {
    "gh_grep": {
      "type": "remote",
      "url": "https://mcp.grep.app",
      "enabled": true
    }
  }
}
```

**Usage**:
```
Show me examples of SST Astro custom domains. use gh_grep
```

#### 3. Sentry - Error Tracking

**Purpose**: Query Sentry projects and issues

**Setup**:
```json
{
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "enabled": true,
      "oauth": {}
    }
  }
}
```

**Authenticate**:
```bash
opencode mcp auth sentry
```

**Usage**:
```
Show me the latest unresolved issues. use sentry
```

### MCP Server Management

#### List all MCP servers
```bash
opencode mcp list
```

#### Authenticate with OAuth
```bash
opencode mcp auth <server-name>
```

#### Logout from MCP server
```bash
opencode mcp logout <server-name>
```

#### Debug MCP server
```bash
opencode mcp debug <server-name>
```

### Managing MCP Tools

#### Disable MCP globally
```json
{
  "tools": {
    "mcp_servername_*": false
  }
}
```

#### Enable per agent
```json
{
  "tools": {
    "context7_*": false
  },
  "agent": {
    "research-agent": {
      "tools": {
        "context7_*": true
      }
    }
  }
}
```

### OAuth for MCP Servers

OpenCode automatically handles OAuth for remote MCP servers.

**Automatic OAuth**:
```json
{
  "mcp": {
    "oauth-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp"
    }
  }
}
```

**Pre-registered client**:
```json
{
  "mcp": {
    "oauth-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "clientId": "{env:CLIENT_ID}",
        "clientSecret": "{env:CLIENT_SECRET}",
        "scope": "tools:read tools:execute"
      }
    }
  }
}
```

**Disable OAuth** (use API keys):
```json
{
  "mcp": {
    "api-key-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp",
      "oauth": false,
      "headers": {
        "Authorization": "Bearer {env:API_KEY}"
      }
    }
  }
}
```

### MCP Best Practices

✅ **Do**:
- Use MCP servers sparingly (they add to context)
- Disable unused MCP servers
- Enable per agent when possible
- Test MCP servers before deploying

❌ **Don't**:
- Enable all MCP servers at once
- Use MCP servers with excessive tools
- Share API keys in config files (use env vars)

---

## Advanced Configuration

### Custom Agents

Agents are specialized AI assistants for specific tasks.

#### Method 1: Markdown Files

**Location**: `~/.config/opencode/agents/code-reviewer.md`

```markdown
---
description: Reviews code for best practices and security
model: anthropic/claude-sonnet-4-5
tools:
  write: false
  edit: false
---

You are an expert code reviewer with 15 years of experience.

Focus on:
- Security vulnerabilities
- Performance issues
- Code maintainability
- Best practices
- Documentation quality

Provide specific, actionable feedback with examples.
```

#### Method 2: JSON Configuration

```json
{
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices",
      "model": "anthropic/claude-sonnet-4-5",
      "prompt": "You are an expert code reviewer...",
      "tools": {
        "write": false,
        "edit": false,
        "bash": false
      }
    },
    "test-writer": {
      "description": "Writes comprehensive tests",
      "model": "anthropic/claude-haiku-4-5",
      "prompt": "You write thorough unit and integration tests...",
      "tools": {
        "write": true,
        "edit": true
      }
    }
  }
}
```

**Usage**:
```
/agent code-reviewer
Review this function for security issues @src/auth.ts
```

### Custom Commands

Commands are shortcuts for common tasks.

**Configuration**:
```json
{
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report.\nFocus on failing tests and suggest fixes.",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-haiku-4-5"
    },
    "component": {
      "template": "Create a new React component named $ARGUMENTS with TypeScript.\nInclude proper typing, PropTypes, and basic structure.",
      "description": "Create a new component"
    },
    "deploy": {
      "template": "Deploy the application to $ARGUMENTS environment.\nRun build, tests, and deployment checks.",
      "description": "Deploy application"
    },
    "refactor": {
      "template": "Refactor $ARGUMENTS to improve:\n- Code quality\n- Performance\n- Maintainability\nPreserve all existing functionality.",
      "description": "Refactor code"
    }
  }
}
```

**Usage**:
```
/test
/component UserProfile
/deploy staging
/refactor src/utils/parser.ts
```

### Custom Themes

**Location**: `~/.config/opencode/tui.json`

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "tokyonight"
}
```

**Built-in themes**:
- `tokyonight`
- `dracula`
- `nord`
- `gruvbox`
- `solarized-dark`
- `solarized-light`
- `monokai`
- `github-dark`
- `github-light`

**Full list**: https://opencode.ai/docs/themes

### Custom Keybindings

**Configuration**:
```json
{
  "$schema": "https://opencode.ai/tui.json",
  "keybinds": {
    "command_list": "ctrl+p",
    "send": "enter",
    "cancel": "ctrl+c",
    "undo": "ctrl+z",
    "redo": "ctrl+y",
    "new_session": "ctrl+n",
    "close_session": "ctrl+w",
    "next_session": "ctrl+tab",
    "prev_session": "ctrl+shift+tab",
    "scroll_up": "up",
    "scroll_down": "down",
    "page_up": "pageup",
    "page_down": "pagedown"
  }
}
```

**Full list**: https://opencode.ai/docs/keybinds

### Sharing Configuration

```json
{
  "share": "manual"
}
```

Options:
- `"manual"` - Share via `/share` command (default)
- `"auto"` - Auto-share new conversations
- `"disabled"` - Disable sharing entirely

### Autoupdate Configuration

```json
{
  "autoupdate": true
}
```

Options:
- `true` - Auto-update (default)
- `false` - Never update
- `"notify"` - Show notification only

### Snapshot Configuration

```json
{
  "snapshot": true
}
```

**Disable for large repos**:
```json
{
  "snapshot": false
}
```

**Note**: Disabling snapshots prevents undo/redo functionality.

### Context Compaction

```json
{
  "compaction": {
    "auto": true,
    "prune": true,
    "reserved": 10000
  }
}
```

Options:
- `auto` - Auto-compact when context full (default: `true`)
- `prune` - Remove old tool outputs (default: `true`)
- `reserved` - Token buffer (default: `10000`)

### File Watcher Configuration

```json
{
  "watcher": {
    "ignore": [
      "node_modules/**",
      "dist/**",
      "build/**",
      ".git/**",
      "**/*.log",
      "**/.DS_Store"
    ]
  }
}
```

### Disabled/Enabled Providers

**Disable specific providers**:
```json
{
  "disabled_providers": ["openai", "gemini"]
}
```

**Enable only specific providers**:
```json
{
  "enabled_providers": ["anthropic", "openai"]
}
```

**Note**: `disabled_providers` takes precedence over `enabled_providers`.

---

## Verification

### Basic Verification

1. **Check version**:
   ```bash
   opencode --version
   ```
   
   Expected: `opencode version X.X.X`

2. **Check config location**:
   ```bash
   ls -la ~/.config/opencode/
   ```

3. **Check auth credentials**:
   ```bash
   cat ~/.local/share/opencode/auth.json
   ```

4. **Launch OpenCode**:
   ```bash
   opencode
   ```

### Functional Testing

#### Test 1: Basic Communication
```
Hello! Can you confirm you're working?
```

Expected: Friendly response confirming functionality.

#### Test 2: File Operations
```
Create a test file called hello.txt with "Hello World"
```

Verify:
```bash
cat hello.txt
```

#### Test 3: Code Analysis
```
What programming languages does this project use?
```

#### Test 4: Model Selection
```
/models
```

Expected: List of available models.

#### Test 5: Help System
```
/help
```

Expected: List of available commands.

### Performance Testing

**Test context usage**:
```
How much context have we used so far?
```

**Test large file handling**:
```
Read and summarize @large-file.json
```

### Configuration Verification

**View active config**:
```
/config
```

**Debug config loading**:
```bash
opencode debug config
```

---

## Comprehensive Troubleshooting

### Installation Issues

#### Issue: "opencode: command not found"

**Symptoms**: Command not recognized after installation.

**Solution 1 - Check PATH**:
```bash
# macOS/Linux
echo $PATH
which opencode

# Windows
echo %PATH%
where opencode
```

**Solution 2 - Add to PATH**:

**macOS/Linux** (add to `~/.bashrc` or `~/.zshrc`):
```bash
export PATH="$PATH:$HOME/.local/bin"
export PATH="$PATH:/usr/local/bin"
```

**Windows** (PowerShell):
```powershell
$env:PATH += ";C:\Program Files\opencode"
# Or via System Properties > Environment Variables
```

**Solution 3 - Reinstall**:
```bash
# Using npm
npm uninstall -g opencode-ai
npm install -g opencode-ai

# Using Homebrew
brew uninstall opencode
brew install anomalyco/tap/opencode
```

#### Issue: Permission denied during installation

**Solution - macOS/Linux**:
```bash
# Fix npm permissions
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) /usr/local/lib/node_modules

# Or use nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
npm install -g opencode-ai
```

**Solution - Windows**:
```powershell
# Run as Administrator
npm install -g opencode-ai
```

#### Issue: Node.js version incompatibility

**Check Node version**:
```bash
node --version
```

**Required**: Node.js 18.0.0 or higher

**Solution**:
```bash
# Install latest LTS
# Using nvm (recommended)
nvm install --lts
nvm use --lts

# Or download from nodejs.org
```

#### Issue: Installation fails with EACCES error

**Solution**:
```bash
# Change npm's default directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g opencode-ai
```

---

### Provider Issues

#### Issue: "No API key found" or authentication failures

**Diagnosis**:
```bash
cat ~/.local/share/opencode/auth.json
```

**Solution 1 - Reconnect provider**:
```
/connect
```
Select provider and re-enter credentials.

**Solution 2 - Check environment variables**:
```bash
# List all OpenCode-related env vars
env | grep -i "api"
env | grep -i "anthropic\|openai\|github"
```

**Solution 3 - Manually edit auth file**:
```bash
nano ~/.local/share/opencode/auth.json
```

Format:
```json
{
  "provider-name": {
    "apiKey": "your-api-key-here"
  }
}
```

**Solution 4 - Use environment variables**:
```bash
# Add to ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY=your-key-here
export OPENAI_API_KEY=your-key-here
```

#### Issue: "Rate limit exceeded"

**Symptoms**: Too many requests to provider API.

**Solution 1 - Wait and retry**:
Most rate limits reset after a few minutes.

**Solution 2 - Upgrade plan**:
- Anthropic: https://console.anthropic.com/settings/plans
- OpenAI: https://platform.openai.com/settings/organization/billing/overview

**Solution 3 - Use different provider**:
```
/connect
```
Add backup provider with different limits.

**Solution 4 - Add timeout configuration**:
```json
{
  "provider": {
    "anthropic": {
      "options": {
        "timeout": 900000,
        "chunkTimeout": 60000
      }
    }
  }
}
```

#### Issue: "Context length exceeded"

**Symptoms**: Message too long for model's context window.

**Solution 1 - Use model with larger context**:
```
/models
```
Select model like `claude-sonnet-4-5` (200k tokens).

**Solution 2 - Enable auto-compaction**:
```json
{
  "compaction": {
    "auto": true,
    "prune": true
  }
}
```

**Solution 3 - Start new conversation**:
```
/new
```

**Solution 4 - Disable MCP servers**:
```json
{
  "tools": {
    "mcp_*": false
  }
}
```

#### Issue: OAuth authentication fails

**Solution 1 - Clear browser cache**:
Clear cookies for the provider's domain.

**Solution 2 - Try incognito/private window**:
Some ad blockers interfere with OAuth.

**Solution 3 - Use API key instead**:
```
/connect
```
Choose "Manually enter API Key" option.

**Solution 4 - Check firewall/proxy**:
```bash
# Test connectivity
curl https://api.anthropic.com
curl https://api.openai.com
```

---

### Configuration Issues

#### Issue: Configuration file not loading

**Diagnosis**:
```bash
opencode debug config
```

**Solution 1 - Check file location**:
```bash
# Global config
ls -la ~/.config/opencode/opencode.json

# Project config
ls -la ./opencode.json
```

**Solution 2 - Validate JSON syntax**:
```bash
# macOS/Linux
python3 -m json.tool ~/.config/opencode/opencode.json

# Or use jq
jq . ~/.config/opencode/opencode.json
```

**Solution 3 - Check file permissions**:
```bash
chmod 644 ~/.config/opencode/opencode.json
```

**Solution 4 - Start with minimal config**:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5"
}
```

#### Issue: Schema validation errors

**Solution - Update schema URL**:
```json
{
  "$schema": "https://opencode.ai/config.json"
}
```

**For TUI config**:
```json
{
  "$schema": "https://opencode.ai/tui.json"
}
```

#### Issue: Environment variables not expanding

**Check syntax**:
```json
{
  "provider": {
    "openai": {
      "options": {
        "apiKey": "{env:OPENAI_API_KEY}"
      }
    }
  }
}
```

**Verify variable is set**:
```bash
echo $OPENAI_API_KEY
```

**Set if missing**:
```bash
# Temporary
export OPENAI_API_KEY=your-key

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export OPENAI_API_KEY=your-key' >> ~/.bashrc
source ~/.bashrc
```

#### Issue: Project config ignored

**Solution 1 - Check location**:
Config must be in project root or Git root.

```bash
# Find Git root
git rev-parse --show-toplevel

# Place config there
cp opencode.json $(git rev-parse --show-toplevel)/
```

**Solution 2 - Use custom config path**:
```bash
export OPENCODE_CONFIG=/path/to/opencode.json
opencode
```

---

### Performance Issues

#### Issue: OpenCode slow to start

**Diagnosis**:
```bash
time opencode --version
```

**Solution 1 - Disable autoupdate**:
```json
{
  "autoupdate": false
}
```

**Solution 2 - Disable snapshot for large repos**:
```json
{
  "snapshot": false
}
```

**Solution 3 - Reduce MCP servers**:
```json
{
  "mcp": {
    "server1": {
      "enabled": false
    }
  }
}
```

**Solution 4 - Clear cache**:
```bash
rm -rf ~/.local/share/opencode/cache/
```

#### Issue: High memory usage

**Diagnosis**:
```bash
# macOS/Linux
ps aux | grep opencode

# Windows
tasklist | findstr opencode
```

**Solution 1 - Use smaller model**:
```json
{
  "model": "anthropic/claude-haiku-4-5"
}
```

**Solution 2 - Enable context compaction**:
```json
{
  "compaction": {
    "auto": true,
    "prune": true,
    "reserved": 5000
  }
}
```

**Solution 3 - Restart OpenCode regularly**:
```
/new
```

**Solution 4 - Check for runaway processes**:
```bash
pkill -f opencode
opencode
```

#### Issue: Slow response times

**Solution 1 - Use faster provider**:
- Groq (fastest)
- Claude Haiku
- GPT-4o-mini

**Solution 2 - Reduce context**:
```
/new
```

**Solution 3 - Disable LSP**:
```json
{
  "lsp": false
}
```

**Solution 4 - Check network**:
```bash
ping api.anthropic.com
```

---

### MCP Server Issues

#### Issue: MCP server not starting

**Diagnosis**:
```bash
opencode mcp list
opencode mcp debug <server-name>
```

**Solution 1 - Check command**:
```json
{
  "mcp": {
    "myserver": {
      "type": "local",
      "command": ["npx", "-y", "correct-package-name"]
    }
  }
}
```

**Solution 2 - Test command manually**:
```bash
npx -y @modelcontextprotocol/server-everything
```

**Solution 3 - Check dependencies**:
```bash
npm list -g | grep mcp
```

**Solution 4 - Reinstall MCP package**:
```bash
npm cache clean --force
npx -y @modelcontextprotocol/server-everything
```

#### Issue: MCP OAuth authentication fails

**Diagnosis**:
```bash
opencode mcp auth list
opencode mcp debug <server-name>
```

**Solution 1 - Retry authentication**:
```bash
opencode mcp logout <server-name>
opencode mcp auth <server-name>
```

**Solution 2 - Check stored tokens**:
```bash
cat ~/.local/share/opencode/mcp-auth.json
```

**Solution 3 - Disable OAuth and use API key**:
```json
{
  "mcp": {
    "myserver": {
      "type": "remote",
      "url": "https://mcp.example.com",
      "oauth": false,
      "headers": {
        "Authorization": "Bearer {env:API_KEY}"
      }
    }
  }
}
```

#### Issue: MCP server timeout

**Solution - Increase timeout**:
```json
{
  "mcp": {
    "myserver": {
      "type": "remote",
      "url": "https://mcp.example.com",
      "timeout": 30000
    }
  }
}
```

#### Issue: Too many MCP tools in context

**Solution 1 - Disable globally, enable per agent**:
```json
{
  "tools": {
    "mcp_*": false
  },
  "agent": {
    "research": {
      "tools": {
        "mcp_context7_*": true
      }
    }
  }
}
```

**Solution 2 - Disable specific MCP server**:
```json
{
  "mcp": {
    "excessive-server": {
      "enabled": false
    }
  }
}
```

---

### File Operation Issues

#### Issue: "Permission denied" when writing files

**Solution 1 - Check file permissions**:
```bash
ls -la filename
```

**Solution 2 - Change ownership**:
```bash
sudo chown $(whoami) filename
```

**Solution 3 - Check directory permissions**:
```bash
ls -la directory/
chmod 755 directory/
```

**Solution 4 - Use different directory**:
```bash
cd ~/Documents/projects/
opencode
```

#### Issue: Files not being read

**Diagnosis**:
```
Read the file @path/to/file.txt
```

**Solution 1 - Use absolute path**:
```
Read /full/path/to/file.txt
```

**Solution 2 - Check file exists**:
```bash
ls -la path/to/file.txt
```

**Solution 3 - Check file encoding**:
```bash
file path/to/file.txt
```

**Solution 4 - Check .gitignore**:
```bash
cat .gitignore
```

#### Issue: Unable to undo changes

**Verify snapshot enabled**:
```json
{
  "snapshot": true
}
```

**Check snapshot storage**:
```bash
ls -la ~/.local/share/opencode/snapshots/
```

**Restart OpenCode**:
```bash
pkill opencode
opencode
```

---

### WSL-Specific Issues (Windows)

#### Issue: WSL not installed

**Solution**:
```powershell
# Run as Administrator
wsl --install
# Restart computer
```

#### Issue: WSL version 1 instead of 2

**Check version**:
```powershell
wsl --list --verbose
```

**Upgrade to WSL 2**:
```powershell
wsl --set-version Ubuntu 2
wsl --set-default-version 2
```

#### Issue: Cannot access Windows files from WSL

**Solution**:
```bash
# Access C:\Users\username\Documents
cd /mnt/c/Users/username/Documents
```

#### Issue: Node.js not found in WSL

**Install Node.js in WSL**:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install --lts
node --version
```

#### Issue: OpenCode installed in Windows but not WSL

**Install separately in WSL**:
```bash
curl -fsSL https://opencode.ai/install | bash
```

---

### Terminal Issues

#### Issue: Colors not displaying correctly

**Solution 1 - Check terminal support**:
```bash
echo $TERM
```

**Solution 2 - Set TERM variable**:
```bash
export TERM=xterm-256color
```

**Solution 3 - Use different terminal**:
Try WezTerm, Alacritty, or iTerm2.

#### Issue: Mouse input not working

**Enable in config**:
```json
{
  "$schema": "https://opencode.ai/tui.json",
  "mouse": true
}
```

#### Issue: Scroll not working

**Configure scroll**:
```json
{
  "$schema": "https://opencode.ai/tui.json",
  "scroll_speed": 3,
  "scroll_acceleration": {
    "enabled": true
  }
}
```

#### Issue: Unicode characters not displaying

**Check terminal encoding**:
```bash
locale
```

**Set UTF-8**:
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

---

### Network Issues

#### Issue: Cannot connect to provider API

**Test connectivity**:
```bash
curl https://api.anthropic.com
curl https://api.openai.com
curl https://api.opencode.ai
```

**Solution 1 - Check firewall**:
Allow outbound HTTPS connections.

**Solution 2 - Configure proxy**:
```bash
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

**Solution 3 - Try different network**:
Test with mobile hotspot or different WiFi.

#### Issue: SSL/TLS certificate errors

**Solution 1 - Update certificates**:
```bash
# macOS
brew update && brew upgrade openssl

# Linux
sudo apt update && sudo apt install ca-certificates

# Windows
# Update Windows certificates via Windows Update
```

**Solution 2 - Bypass SSL verification (not recommended)**:
```bash
export NODE_TLS_REJECT_UNAUTHORIZED=0
```

---

### Update Issues

#### Issue: Auto-update fails

**Manual update**:
```bash
# Using npm
npm update -g opencode-ai

# Using Homebrew
brew update && brew upgrade opencode

# Using install script
curl -fsSL https://opencode.ai/install | bash
```

#### Issue: Cannot disable updates

**Solution**:
```json
{
  "autoupdate": false
}
```

---

### Debugging Tools

#### Get detailed logs

**Enable debug mode**:
```bash
export DEBUG=opencode:*
opencode
```

**Check logs**:
```bash
# macOS/Linux
tail -f ~/.local/share/opencode/logs/opencode.log

# Windows
type %LOCALAPPDATA%\opencode\logs\opencode.log
```

#### Debug configuration

```bash
opencode debug config
```

#### Debug MCP servers

```bash
opencode mcp debug <server-name>
```

#### Check OpenCode version and build info

```bash
opencode --version
opencode --help
```

---

## Reference Documentation

### Official Documentation Links

| Topic | URL |
|-------|-----|
| **Main Documentation** | https://opencode.ai/docs |
| **Installation Guide** | https://opencode.ai/docs |
| **Configuration** | https://opencode.ai/docs/config |
| **Providers** | https://opencode.ai/docs/providers |
| **Models** | https://opencode.ai/docs/models |
| **Tools** | https://opencode.ai/docs/tools |
| **Agents** | https://opencode.ai/docs/agents |
| **Commands** | https://opencode.ai/docs/commands |
| **Themes** | https://opencode.ai/docs/themes |
| **Keybindings** | https://opencode.ai/docs/keybinds |
| **Formatters** | https://opencode.ai/docs/formatters |
| **LSP Servers** | https://opencode.ai/docs/lsp |
| **MCP Servers** | https://opencode.ai/docs/mcp-servers |
| **Permissions** | https://opencode.ai/docs/permissions |
| **Skills** | https://opencode.ai/docs/skills |
| **Custom Tools** | https://opencode.ai/docs/custom-tools |
| **Plugins** | https://opencode.ai/docs/plugins |
| **Rules** | https://opencode.ai/docs/rules |
| **TUI Usage** | https://opencode.ai/docs/tui |
| **CLI Usage** | https://opencode.ai/docs/cli |
| **Web Interface** | https://opencode.ai/docs/web |
| **IDE Integration** | https://opencode.ai/docs/ide |
| **Zen** | https://opencode.ai/docs/zen |
| **Go** | https://opencode.ai/docs/go |
| **Sharing** | https://opencode.ai/docs/share |
| **GitHub Integration** | https://opencode.ai/docs/github |
| **GitLab Integration** | https://opencode.ai/docs/gitlab |
| **Network Config** | https://opencode.ai/docs/network |
| **Enterprise** | https://opencode.ai/docs/enterprise |
| **Troubleshooting** | https://opencode.ai/docs/troubleshooting |
| **Windows/WSL** | https://opencode.ai/docs/windows-wsl |
| **SDK** | https://opencode.ai/docs/sdk |
| **Server** | https://opencode.ai/docs/server |
| **Ecosystem** | https://opencode.ai/docs/ecosystem |

### Configuration Schema References

| Schema | URL |
|--------|-----|
| **OpenCode Config Schema** | https://opencode.ai/config.json |
| **TUI Config Schema** | https://opencode.ai/tui.json |

### Provider-Specific Documentation

| Provider | Documentation |
|----------|--------------|
| **OpenCode Zen** | https://opencode.ai/zen |
| **OpenCode Go** | https://opencode.ai/go |
| **Anthropic** | https://docs.anthropic.com |
| **OpenAI** | https://platform.openai.com/docs |
| **GitHub Copilot** | https://docs.github.com/copilot |
| **Azure OpenAI** | https://learn.microsoft.com/azure/ai-services/openai/ |
| **Google Vertex AI** | https://cloud.google.com/vertex-ai/docs |
| **Amazon Bedrock** | https://docs.aws.amazon.com/bedrock/ |
| **Ollama** | https://ollama.ai/docs |
| **DeepSeek** | https://platform.deepseek.com/docs |
| **Groq** | https://console.groq.com/docs |

### Community Resources

| Resource | URL |
|----------|-----|
| **GitHub Repository** | https://github.com/anomalyco/opencode |
| **GitHub Releases** | https://github.com/anomalyco/opencode/releases |
| **GitHub Issues** | https://github.com/anomalyco/opencode/issues |
| **Discord Community** | https://opencode.ai/discord |
| **Example Conversations** | https://opencode.ai/s/4XP1fce5 |

### Additional Resources

| Resource | URL |
|----------|-----|
| **AI SDK Documentation** | https://ai-sdk.dev/ |
| **Models.dev** | https://models.dev |
| **Model Context Protocol** | https://modelcontextprotocol.io/ |

---

## Quick Reference

### Essential Commands

```bash
# Installation
curl -fsSL https://opencode.ai/install | bash

# Launch OpenCode
opencode

# Check version
opencode --version

# Update OpenCode
npm update -g opencode-ai
# OR
brew upgrade opencode
```

### TUI Commands

```
/help           - Show available commands
/connect        - Connect to a provider
/models         - Select a model
/init           - Initialize project
/new            - Start new conversation
/share          - Share current conversation
/undo           - Undo last changes
/redo           - Redo undone changes
/agent          - Switch agent
/config         - View current configuration
```

### Configuration Locations

```bash
# Global config
~/.config/opencode/opencode.json

# TUI config
~/.config/opencode/tui.json

# Project config
<project-root>/opencode.json

# Auth credentials
~/.local/share/opencode/auth.json

# MCP auth
~/.local/share/opencode/mcp-auth.json
```

### Environment Variables

```bash
# Custom config path
export OPENCODE_CONFIG=/path/to/config.json

# Custom config directory
export OPENCODE_CONFIG_DIR=/path/to/config-dir

# Inline config
export OPENCODE_CONFIG_CONTENT='{"model":"..."}'

# Provider API keys
export ANTHROPIC_API_KEY=your-key
export OPENAI_API_KEY=your-key
export GITHUB_TOKEN=your-token

# Debug mode
export DEBUG=opencode:*
```

### Common File Paths

**macOS/Linux**:
- Config: `~/.config/opencode/`
- Data: `~/.local/share/opencode/`
- Cache: `~/.cache/opencode/`
- Logs: `~/.local/share/opencode/logs/`

**Windows**:
- Config: `%APPDATA%\opencode\`
- Data: `%LOCALAPPDATA%\opencode\`
- Cache: `%TEMP%\opencode\`

### Keyboard Shortcuts (Default)

| Action | Shortcut |
|--------|----------|
| **Send message** | Enter |
| **Cancel** | Ctrl+C |
| **Undo** | Ctrl+Z |
| **Redo** | Ctrl+Y |
| **Command list** | Ctrl+P |
| **New session** | Ctrl+N |
| **Close session** | Ctrl+W |
| **Next session** | Ctrl+Tab |
| **Previous session** | Ctrl+Shift+Tab |
| **Scroll up** | ↑ or Page Up |
| **Scroll down** | ↓ or Page Down |

### Minimal Configurations

**Minimal opencode.json**:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5"
}
```

**Minimal tui.json**:
```json
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "tokyonight"
}
```

### Getting Help

1. **In-app help**: `/help`
2. **Documentation**: https://opencode.ai/docs
3. **GitHub Issues**: https://github.com/anomalyco/opencode/issues
4. **Discord**: https://opencode.ai/discord
5. **Email**: support@opencode.ai

---

## Appendix A: Example Configurations

### Example 1: Basic Setup

**~/.config/opencode/opencode.json**:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5",
  "autoupdate": true,
  "share": "manual"
}
```

### Example 2: Developer Setup

**~/.config/opencode/opencode.json**:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "formatter": true,
  "lsp": true,
  "tools": {
    "bash": true,
    "write": true,
    "edit": true
  },
  "permission": {
    "bash": "ask",
    "edit": "allow"
  },
  "command": {
    "test": {
      "template": "Run tests with coverage",
      "agent": "build"
    },
    "lint": {
      "template": "Run linter and fix issues"
    }
  }
}
```

### Example 3: Team Setup

**project/opencode.json** (commit to Git):
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "instructions": [
    "CONTRIBUTING.md",
    "docs/architecture.md"
  ],
  "formatter": {
    "prettier": {},
    "eslint": {}
  },
  "lsp": true,
  "share": "manual",
  "command": {
    "test": {
      "template": "Run full test suite with coverage",
      "agent": "build"
    },
    "deploy": {
      "template": "Deploy to $ARGUMENTS environment"
    }
  }
}
```

### Example 4: Privacy-Focused Setup

**~/.config/opencode/opencode.json**:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": {
        "baseURL": "http://localhost:11434/v1"
      },
      "models": {
        "qwen2.5-coder:32b": {
          "name": "Qwen 2.5 Coder 32B"
        }
      }
    }
  },
  "model": "ollama/qwen2.5-coder:32b",
  "share": "disabled",
  "autoupdate": "notify"
}
```

---

## Appendix B: Glossary

| Term | Definition |
|------|------------|
| **TUI** | Terminal User Interface - OpenCode's interactive terminal mode |
| **LLM** | Large Language Model - The AI that powers OpenCode |
| **Provider** | Service that provides access to LLM models (e.g., Anthropic, OpenAI) |
| **Agent** | Specialized AI assistant for specific tasks (e.g., code reviewer) |
| **MCP** | Model Context Protocol - Standard for adding external tools |
| **LSP** | Language Server Protocol - Provides code intelligence |
| **Formatter** | Tool that automatically formats code (e.g., Prettier) |
| **Context** | Information provided to the LLM (messages, files, etc.) |
| **Token** | Unit of text that LLMs process (roughly 4 characters) |
| **Snapshot** | Internal Git repository for tracking changes and undo/redo |
| **Compaction** | Process of reducing context size to fit in model limits |
| **OAuth** | Open Authorization - Standard for secure authentication |
| **AGENTS.md** | Project file that helps OpenCode understand your codebase |
| **Schema** | JSON Schema that defines valid configuration structure |
| **WSL** | Windows Subsystem for Linux - Runs Linux on Windows |

---

## Appendix C: Changelog

### Version 1.0 (May 2026)
- Initial comprehensive guide
- Complete installation instructions
- Provider setup for 75+ providers
- Configuration hierarchy documentation
- MCP server setup
- Comprehensive troubleshooting
- Reference documentation

---

**Document Information**:
- **Version**: 1.0
- **Last Updated**: May 15, 2026
- **OpenCode Compatibility**: 1.3.0+
- **Author**: OpenCode Documentation Team
- **License**: MIT

**Feedback**: For corrections or improvements, open an issue at:
https://github.com/anomalyco/opencode/issues

---

**End of Document**
