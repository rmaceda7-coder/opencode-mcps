# GitHub MCP Installation Guide - Summary

## 📄 Document Created
**GitHub_MCP_Installation_Guide.md** + **GitHub_MCP_Installation_Guide.pdf**

## 🎯 Purpose
Complete step-by-step guide for installing and configuring the official GitHub MCP server on OpenCode, enabling AI-powered GitHub operations.

## 📚 Document Structure

### 1. Overview (What & Why)
- What the GitHub MCP server is
- Why you need it
- Architecture diagram showing how it integrates with OpenCode
- What capabilities you'll gain

### 2. Prerequisites
- Node.js v18+ required
- npm package manager
- OpenCode 1.3.0+
- GitHub account
- Personal Access Token

### 3. Installation Methods (4 Options)

| Method | Best For | Command |
|--------|----------|---------|
| **Global Install** | Most users | `npm install -g @modelcontextprotocol/server-github` |
| **NPX** | Testing, no install | Uses `npx` in config |
| **Local Install** | Project-specific | `npm install @modelcontextprotocol/server-github` |
| **From Source** | Development, customization | Clone and build from GitHub |

**Recommended**: Method 1 (Global Install)

### 4. Authentication Setup

#### Token Creation Options
- **Fine-Grained Token** (recommended) - Repository-specific, more secure
- **Classic Token** - Simpler but broader permissions

#### Required Permissions
Minimum:
```
✅ Contents: Read and Write
✅ Pull requests: Read and Write
✅ Issues: Read and Write
✅ Metadata: Read-only
```

Full functionality:
```
✅ All of the above, plus:
✅ Actions, Workflows, Deployments, etc.
```

#### Secure Storage Methods
1. ⭐⭐⭐ Credential Manager (macOS Keychain, Windows Credential Manager)
2. ⭐⭐ Environment Variables (user-level, persistent)
3. ⭐ Environment Variables (session-level, temporary)
4. ❌ .env files (risk of commit, must be in .gitignore)
5. ❌❌ Hardcoded (NEVER!)

### 5. OpenCode Configuration

**Global config** (`~/.config/opencode/opencode.json`):
```json
{
  "mcp": {
    "github": {
      "type": "stdio",
      "command": "mcp-server-github",
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "{env:GITHUB_PERSONAL_ACCESS_TOKEN}"
      },
      "enabled": true
    }
  }
}
```

### 6. Verification & Testing

```bash
# 1. Validate config
opencode --validate-config

# 2. List MCP servers
opencode mcp list

# 3. Test in OpenCode
opencode
> Show me available GitHub tools
> List my GitHub repositories
```

### 7. Available Tools (50+ Operations)

#### Categories
- 📋 **Issues**: Create, list, update, search, comment
- 🔀 **Pull Requests**: Create, review, merge, update, comment
- 📦 **Repositories**: Create, fork, search, manage
- 🌿 **Branches**: Create, list, delete
- 📝 **Commits**: List, view, compare
- 🔍 **Search**: Code, issues, PRs, users, repos
- 🏷️ **Releases**: Create, list, update
- 📁 **Files**: Read, create, update, push multiple

### 8. Real-World Usage Examples

**Example 1**: Create issue from bug report
```
You: "Create an issue for the login bug"
OpenCode: *Creates issue with labels and assignees*
```

**Example 2**: Create PR with AI-generated description
```
You: "Create a PR for this feature"
OpenCode: *Analyzes changes, creates PR with detailed description*
```

**Example 3**: Search codebase across repos
```
You: "Where do I use fetchUser?"
OpenCode: *Searches all repos, shows locations*
```

**Example 4**: Review and merge PR
```
You: "Review PR #42 and merge if good"
OpenCode: *Reviews changes, checks tests, merges*
```

**Example 5**: Create release
```
You: "Create release v2.1.0"
OpenCode: *Generates changelog, creates release*
```

**Example 6**: Close stale issues
```
You: "Close issues inactive for 6 months"
OpenCode: *Finds, comments, closes stale issues*
```

**Example 7**: Multi-repo code search
```
You: "Find all uses of process.env.API_KEY"
OpenCode: *Searches all repos, creates refactor issues*
```

**Example 8**: Multi-repo update
```
You: "Update README in all my repos"
OpenCode: *Updates 10 repositories with new content*
```

### 9. Troubleshooting (8 Common Issues)

1. **"Server not found"** → Re-install, check PATH
2. **"Authentication failed"** → Check token validity and permissions
3. **"Rate limit exceeded"** → Wait for reset, check usage
4. **"Server crashed"** → Check Node.js version, increase timeout
5. **"Permission denied"** → Update token permissions, check repo access
6. **"Cannot create PR"** → Ensure branch has commits
7. **"SSL/TLS errors"** → Configure for GitHub Enterprise
8. **"Works in terminal not OpenCode"** → Check environment variables loaded

**Debug mode**:
```json
"env": {
  "DEBUG": "*"  // Enable all debug logs
}
```

### 10. Best Practices

#### Token Management ✅
- Use environment variables
- Use fine-grained tokens
- Set 90-day expiration
- Rotate regularly
- Never commit to git

#### Rate Limiting ✅
- Be mindful of 5000/hour limit
- Cache when appropriate
- Batch operations

#### Security ✅
- Minimal permissions principle
- Use secure credential managers
- Audit token usage
- Revoke unused tokens

#### Performance ✅
- Use pagination for large results
- Filter server-side
- Cache frequently accessed data

### 11. Advanced Configuration

#### GitHub Enterprise
```json
"env": {
  "GITHUB_API_URL": "https://github.enterprise.com/api/v3",
  "GITHUB_PERSONAL_ACCESS_TOKEN": "{env:TOKEN}"
}
```

#### Multiple GitHub Accounts
```json
"mcp": {
  "github-personal": { ... },
  "github-work": { ... }
}
```

#### Proxy Configuration
```json
"env": {
  "HTTP_PROXY": "http://proxy.company.com:8080",
  "HTTPS_PROXY": "http://proxy.company.com:8080"
}
```

#### Custom Timeouts
```json
"timeout": 60000  // 60 seconds
```

### 12. Security Considerations

**5-Level Token Storage Security**:
1. Credential Manager (most secure)
2. User-level environment variables
3. Session-level environment variables
4. .env files (risky)
5. Hardcoded (never!)

**Token Rotation Schedule**:
- Personal projects: 90 days
- Team projects: 60 days
- Production: 30 days

**Incident Response**:
- Immediate (5 min): Revoke token
- Short-term (1 hour): Generate new token, audit
- Follow-up (24 hours): Review logs, update docs

### 13. FAQ (15 Questions)

Key questions answered:
- Can I use SSH keys? (No, needs PAT)
- Works with GitHub Enterprise? (Yes, configure API URL)
- GitHub App authentication? (Not yet supported)
- Will it push without asking? (OpenCode asks first)
- Works for org repos? (Yes, with proper token access)
- Works offline? (No, needs internet)
- How to limit repo access? (Use fine-grained tokens)
- How to update? (`npm update -g`)
- GitLab/Bitbucket? (No, GitHub only)
- vs `gh` CLI? (Different purposes, both can coexist)

### 14. Quick Start (TL;DR)

```bash
# 1. Install
npm install -g @modelcontextprotocol/server-github

# 2. Create token at github.com/settings/tokens

# 3. Set environment variable
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token"

# 4. Configure OpenCode (paste config)

# 5. Test
opencode
> "List my GitHub repositories"
```

## 📊 Document Statistics

- **Total Length**: ~3,800 lines
- **Sections**: 15 major sections
- **Tables**: 12+ comparison tables
- **Code Examples**: 40+ snippets
- **Real-World Examples**: 8 detailed scenarios
- **Troubleshooting Items**: 8 common issues with solutions
- **Best Practices**: 5 categories
- **FAQ**: 15 questions
- **Architecture Diagrams**: 2 ASCII diagrams
- **Estimated PDF Size**: 1.5-1.8 MB
- **Estimated PDF Pages**: 80-100 pages

## 🎯 Key Features

### Comprehensive Coverage
✅ Multiple installation methods with pros/cons
✅ Two token types (fine-grained vs classic) with permission details
✅ Multiple secure storage methods ranked by security
✅ Platform-specific instructions (Windows/macOS/Linux)
✅ Complete troubleshooting guide
✅ Real-world usage examples with full workflows
✅ Advanced configurations (Enterprise, proxy, multi-account)
✅ Security best practices and incident response

### Practical Focus
✅ Copy-paste ready commands
✅ Platform-specific examples
✅ Real error messages with solutions
✅ Step-by-step verification
✅ Complete configuration examples
✅ Debug mode instructions

### Beginner-Friendly
✅ Clear explanations of concepts
✅ "Why" and "What" explained
✅ Recommended approaches highlighted
✅ Common pitfalls called out
✅ Quick start section for fast setup
✅ Visual diagrams for architecture

## 🔗 Related Documents

| Document | Purpose | Size |
|----------|---------|------|
| **OpenCode_Installation_Guide_Enhanced.pdf** | Install OpenCode itself | 1.3 MB, 60-70 pages |
| **Serena_Code_Intelligence_Guide.pdf** | Use Serena (built-in) | 700 KB, 45-50 pages |
| **Serena_NOT_An_MCP_Guide.pdf** | Understand built-in vs MCP | 600 KB, 35-40 pages |
| **GitHub_MCP_Installation_Guide.pdf** | Install GitHub MCP (this doc) | 1.5-1.8 MB, 80-100 pages |

## 🎓 Use This Guide For

- ✅ First-time GitHub MCP setup
- ✅ Troubleshooting connection issues
- ✅ Understanding token permissions
- ✅ Secure token storage
- ✅ Enterprise GitHub configuration
- ✅ Multi-account setup
- ✅ Team onboarding
- ✅ Security audits
- ✅ Reference for available operations

## 💡 Key Differentiators

### vs Official Docs
- ✅ More comprehensive troubleshooting
- ✅ Real-world usage examples
- ✅ Platform-specific instructions
- ✅ Security best practices emphasized
- ✅ Multiple installation methods compared
- ✅ Complete OpenCode integration steps

### vs Other Guides
- ✅ Covers all aspects in one place
- ✅ Security-first approach
- ✅ Production-ready configuration
- ✅ Enterprise scenarios included
- ✅ Detailed error resolution
- ✅ Token management lifecycle

## 🚀 Quick Reference

### Minimum Setup (3 Steps)
```bash
1. npm install -g @modelcontextprotocol/server-github
2. export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_xxx"
3. Configure opencode.json (copy from guide)
```

### Minimum Token Permissions
```
✅ Contents: Read and Write
✅ Pull requests: Read and Write
✅ Issues: Read and Write
```

### Must-Have Config
```json
{
  "mcp": {
    "github": {
      "type": "stdio",
      "command": "mcp-server-github",
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "{env:GITHUB_PERSONAL_ACCESS_TOKEN}"
      },
      "enabled": true
    }
  }
}
```

### Verification Commands
```bash
# 1. Server installed?
which mcp-server-github

# 2. Token set?
echo $GITHUB_PERSONAL_ACCESS_TOKEN

# 3. OpenCode configured?
opencode mcp list

# 4. Can connect?
opencode
> List my repositories
```

## ⚠️ Critical Warnings

### Security
- ❌ **NEVER** commit tokens to git
- ❌ **NEVER** hardcode tokens in config files
- ❌ **NEVER** share tokens between services
- ❌ **NEVER** use `NODE_TLS_REJECT_UNAUTHORIZED=0` in production

### Rate Limits
- ⚠️ Authenticated: 5000 requests/hour
- ⚠️ Unauthenticated: 60 requests/hour
- ⚠️ Search API: 30 requests/minute
- ⚠️ Creating content: Secondary rate limits may apply

### Token Expiration
- ⚠️ Fine-grained tokens expire (default 90 days)
- ⚠️ Classic tokens can be set to never expire (not recommended)
- ⚠️ Set calendar reminders to rotate tokens

## 📋 Installation Checklist

Pre-Installation:
- [ ] Node.js v18+ installed
- [ ] npm available
- [ ] OpenCode 1.3.0+ installed
- [ ] GitHub account active

Installation:
- [ ] GitHub MCP server installed
- [ ] Installation verified (`which`/`where`)
- [ ] Can run manually (test)

Authentication:
- [ ] Personal Access Token created
- [ ] Correct permissions granted
- [ ] Token copied and saved
- [ ] Token stored securely
- [ ] Token tested with curl

Configuration:
- [ ] OpenCode config file created/updated
- [ ] MCP section added
- [ ] Environment variable referenced
- [ ] Server enabled
- [ ] Config validated

Verification:
- [ ] `opencode mcp list` shows github
- [ ] OpenCode session starts
- [ ] GitHub tools available
- [ ] Test query works (list repos)
- [ ] Create/read operations successful

Security:
- [ ] Token not in git
- [ ] .gitignore updated (if using .env)
- [ ] Minimal permissions used
- [ ] Expiration date set
- [ ] Credential manager used (preferred)

---

**Created**: May 15, 2026  
**Format**: Markdown + PDF  
**Audience**: OpenCode users wanting GitHub integration  
**Complexity**: Beginner to Advanced  
**Estimated Setup Time**: 15-30 minutes
