# Atlassian MCP Installation Guide - Summary

## 📄 Document Created
**05_Atlassian_MCP_Installation_Guide.md** + **05_Atlassian_MCP_Installation_Guide.pdf**

## 🎯 Purpose
Complete step-by-step guide for installing and configuring the official Atlassian MCP server on OpenCode, enabling AI-powered Jira and Confluence operations.

## 📚 Document Structure

### 1. Overview (What & Why)
- What the Atlassian MCP server is
- Why you need it (Jira + Confluence integration)
- Architecture diagram showing integration with OpenCode
- What capabilities you'll gain

### 2. Prerequisites
- Node.js v18+ required
- npm package manager
- OpenCode 1.3.0+
- Atlassian account (Jira/Confluence access)
- API token and Cloud ID

### 3. Installation Methods (3 Options)

| Method | Best For | Command |
|--------|----------|---------|
| **Global Install** | Most users | `npm install -g @modelcontextprotocol/server-atlassian` |
| **NPX** | Testing, no install | Uses `npx` in config |
| **Local Install** | Project-specific | `npm install @modelcontextprotocol/server-atlassian` |

**Recommended**: Method 1 (Global Install)

### 4. Authentication Setup

#### Required Credentials
1. **Cloud ID** - Your Atlassian subdomain (e.g., `yourcompany.atlassian.net`)
2. **API Token** - Created at https://id.atlassian.com/manage-profile/security/api-tokens
3. **User Email** - Your Atlassian account email

#### API Token Creation
- Visit Atlassian account security settings
- Create token with label "OpenCode Atlassian MCP"
- Copy token immediately (starts with `ATATT`)
- Token inherits your user permissions

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
    "atlassian": {
      "type": "stdio",
      "command": "mcp-server-atlassian",
      "env": {
        "ATLASSIAN_CLOUD_ID": "{env:ATLASSIAN_CLOUD_ID}",
        "ATLASSIAN_API_TOKEN": "{env:ATLASSIAN_API_TOKEN}",
        "ATLASSIAN_USER_EMAIL": "{env:ATLASSIAN_USER_EMAIL}"
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
> Show me available Atlassian tools
> Show me open issues assigned to me
> Search Confluence for "API documentation"
```

### 7. Available Tools (40+ Operations)

#### Jira Tools
- **Issue Management**: Create, read, update, search, comment, log time
- **Workflows**: Transition issues, get available transitions
- **Linking**: Link issues (blocks, duplicates, relates to)
- **Projects**: List projects, get metadata, issue types, custom fields

#### Confluence Tools
- **Page Management**: Create, read, update, search pages and blog posts
- **Spaces**: List spaces, get space info, list pages in space
- **Comments**: Add footer/inline comments, get comments, replies
- **Hierarchy**: Get page descendants, navigate page trees

#### Search Tools
- **JQL (Jira Query Language)**: Advanced Jira issue search
- **CQL (Confluence Query Language)**: Advanced Confluence page search
- **Rovo Search**: AI-powered search across both Jira and Confluence

### 8. Real-World Usage Examples

**Example 1**: Create Jira issue from bug report
```
You: "Create a critical bug for SSO login failure in BACKEND project"
OpenCode: *Creates detailed issue with reproduction steps*
Result: BACKEND-456 created
```

**Example 2**: Search and update multiple issues
```
You: "Find all open bugs assigned to me and add comment"
OpenCode: *Finds 5 bugs, adds comment to all*
Result: 5 issues updated
```

**Example 3**: Create Confluence documentation from code
```
You: "Document the Authentication API in Confluence DEV space"
OpenCode: *Reads code, creates formatted documentation page*
Result: Page created with API endpoints and examples
```

**Example 4**: Link related issues
```
You: "Link database migration issue to BACKEND-456 as blocks"
OpenCode: *Finds issue, creates link*
Result: BACKEND-789 blocks BACKEND-456
```

**Example 5**: Weekly status report
```
You: "Create Confluence page with my completed tasks this week"
OpenCode: *Searches resolved issues, creates formatted report*
Result: Status report page with 12 completed items
```

**Example 6**: Transition issue with workflow
```
You: "Move BACKEND-456 to In Progress and log 3 hours"
OpenCode: *Checks transitions, moves issue, logs time*
Result: Issue in progress, 3h logged
```

**Example 7**: Create Epic with Stories
```
You: "Create Epic 'Mobile App Redesign' with 3 user stories"
OpenCode: *Creates epic and 3 linked stories*
Result: 1 epic + 3 stories created
```

**Example 8**: Bulk update Confluence pages
```
You: "Find pages mentioning API v1 and add v2 notice"
OpenCode: *Finds 8 pages, updates all*
Result: 8 pages updated with notice
```

### 9. Troubleshooting (7 Common Issues)

1. **"Server not found"** → Re-install, check PATH
2. **"Authentication failed"** → Check token, Cloud ID, email
3. **"Cloud ID not found"** → Verify format (no https://)
4. **"Permission denied"** → Check project/space permissions
5. **"Server crashed"** → Check Node.js version, increase timeout
6. **"JQL/CQL query failed"** → Test query in Jira/Confluence UI first
7. **"Rate limit exceeded"** → Wait for reset, reduce API call frequency

**Debug mode**:
```json
"env": {
  "DEBUG": "*"  // Enable all debug logs
}
```

### 10. Best Practices

#### Token Management ✅
- Use environment variables
- Create descriptive token labels
- Rotate every 90 days
- Store in secure credential manager
- Never commit to git

#### JQL/CQL Queries ✅
- Test queries in UI first
- Use field names correctly
- Filter by project/space
- Use pagination for large results

#### Content Creation ✅
- Validate before creating
- Check for duplicates
- Use templates for consistency
- Include required fields

#### Performance ✅
- Batch similar operations
- Use specific filters
- Cache frequently accessed data
- Monitor rate limits

#### Security ✅
- Use HTTPS (default)
- Check permissions before operations
- Audit token usage
- Revoke unused tokens

### 11. Advanced Configuration

#### Multiple Atlassian Sites
```json
"mcp": {
  "atlassian-work": { ... },
  "atlassian-personal": { ... }
}
```

#### Jira/Confluence Server/Data Center
```json
"env": {
  "ATLASSIAN_API_BASE_URL": "https://jira.company.local"
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

**Token Storage Security Ranking**:
1. Credential Manager (most secure)
2. User-level environment variables
3. Session-level environment variables
4. .env files (risky)
5. Hardcoded (never!)

**Token Rotation Schedule**:
- Personal use: 90 days
- Team automation: 60 days
- Production: 30 days

**Incident Response**:
- Immediate (5 min): Revoke token
- Short-term (1 hour): Generate new, audit logs
- Follow-up (24 hours): Review security, update docs

### 13. FAQ (15 Questions)

Key questions answered:
- Can I use username/password? (No, tokens only)
- Works with Jira/Confluence Server? (Yes, configure base URL)
- Multiple Atlassian sites? (Yes, configure multiple instances)
- Creates without asking? (OpenCode asks first)
- Works offline? (No, needs internet)
- Limit project access? (Use service account with limited permissions)
- Update MCP server? (`npm update -g`)
- Both Jira and Confluence? (Yes, one token works for both)
- JQL vs CQL? (JQL for Jira, CQL for Confluence)
- Custom fields? (Yes, use field metadata tools)

### 14. Quick Start (TL;DR)

```bash
# 1. Install
npm install -g @modelcontextprotocol/server-atlassian

# 2. Create token at Atlassian
# https://id.atlassian.com/manage-profile/security/api-tokens

# 3. Set environment variables
export ATLASSIAN_CLOUD_ID="yourcompany.atlassian.net"
export ATLASSIAN_API_TOKEN="ATATT3xFfGF0_your_token"
export ATLASSIAN_USER_EMAIL="your.email@company.com"

# 4. Configure OpenCode (paste config)

# 5. Test
opencode
> "Show me open issues assigned to me"
```

## 📊 Document Statistics

- **Total Length**: ~3,200 lines
- **Sections**: 14 major sections
- **Tables**: 10+ comparison tables
- **Code Examples**: 35+ snippets
- **Real-World Examples**: 8 detailed scenarios
- **Troubleshooting Items**: 7 common issues with solutions
- **Best Practices**: 5 categories
- **FAQ**: 15 questions
- **Architecture Diagrams**: 1 ASCII diagram
- **Estimated PDF Size**: 1.2-1.5 MB
- **Estimated PDF Pages**: 70-85 pages

## 🎯 Key Features

### Comprehensive Coverage
✅ 3 installation methods with pros/cons
✅ Complete authentication setup (token + Cloud ID)
✅ Multiple secure storage methods ranked
✅ Platform-specific instructions (Windows/macOS/Linux)
✅ Complete troubleshooting guide
✅ Real-world usage examples with full workflows
✅ Advanced configurations (Server/DC, proxy, multi-site)
✅ Security best practices and incident response

### Practical Focus
✅ Copy-paste ready commands
✅ Platform-specific examples
✅ Real error messages with solutions
✅ Step-by-step verification
✅ Complete configuration examples
✅ JQL/CQL query examples

### Beginner-Friendly
✅ Clear explanations of Jira and Confluence concepts
✅ "Why" and "What" explained
✅ Recommended approaches highlighted
✅ Common pitfalls called out
✅ Quick start section for fast setup
✅ Visual diagram for architecture

## 🔗 Related Documents

| Document | Purpose | Size |
|----------|---------|------|
| **OpenCode Installation Guide** | Install OpenCode itself | 1.24 MB, 60-70 pages |
| **Serena Code Intelligence Guide** | Use Serena (built-in) | 683 KB, 45-50 pages |
| **Understanding Serena vs MCP** | Built-in vs external | 490 KB, 35-40 pages |
| **GitHub MCP Installation Guide** | Install GitHub MCP | 1.28 MB, 80-100 pages |
| **Atlassian MCP Installation Guide** | Install Atlassian MCP (this doc) | 1.2-1.5 MB, 70-85 pages |

## 🎓 Use This Guide For

- ✅ First-time Atlassian MCP setup
- ✅ Troubleshooting connection issues
- ✅ Understanding JQL/CQL queries
- ✅ Secure token storage
- ✅ Jira Server/Data Center configuration
- ✅ Multi-site setup
- ✅ Team onboarding
- ✅ Security audits
- ✅ Reference for available operations

## 💡 Key Differentiators

### vs Official Docs
- ✅ More comprehensive troubleshooting
- ✅ Real-world usage examples (8 scenarios)
- ✅ Platform-specific instructions
- ✅ Security best practices emphasized
- ✅ Multiple installation methods compared
- ✅ Complete OpenCode integration steps
- ✅ JQL/CQL query examples

### vs Other Guides
- ✅ Covers both Jira AND Confluence
- ✅ Security-first approach
- ✅ Production-ready configuration
- ✅ Server/Data Center scenarios included
- ✅ Detailed error resolution
- ✅ Token management lifecycle

## 🚀 Quick Reference

### Minimum Setup (3 Steps)
```bash
1. npm install -g @modelcontextprotocol/server-atlassian
2. export ATLASSIAN_CLOUD_ID="company.atlassian.net"
   export ATLASSIAN_API_TOKEN="ATATT..."
   export ATLASSIAN_USER_EMAIL="user@company.com"
3. Configure opencode.json (copy from guide)
```

### Required Credentials
```
✅ Cloud ID: yourcompany.atlassian.net
✅ API Token: ATATT3xFfGF0...
✅ User Email: your.email@company.com
```

### Must-Have Config
```json
{
  "mcp": {
    "atlassian": {
      "type": "stdio",
      "command": "mcp-server-atlassian",
      "env": {
        "ATLASSIAN_CLOUD_ID": "{env:ATLASSIAN_CLOUD_ID}",
        "ATLASSIAN_API_TOKEN": "{env:ATLASSIAN_API_TOKEN}",
        "ATLASSIAN_USER_EMAIL": "{env:ATLASSIAN_USER_EMAIL}"
      },
      "enabled": true
    }
  }
}
```

### Verification Commands
```bash
# 1. Server installed?
which mcp-server-atlassian

# 2. Credentials set?
echo $ATLASSIAN_API_TOKEN

# 3. OpenCode configured?
opencode mcp list

# 4. Can connect?
opencode
> Show me open issues assigned to me
```

## ⚠️ Critical Warnings

### Security
- ❌ **NEVER** commit tokens to git
- ❌ **NEVER** hardcode tokens in config files
- ❌ **NEVER** share tokens between services
- ❌ **NEVER** use admin account tokens for automation

### Authentication
- ⚠️ API tokens inherit user permissions
- ⚠️ Tokens don't expire automatically (set expiration)
- ⚠️ One compromised token = full account access
- ⚠️ Basic auth (username/password) is deprecated

### Rate Limits
- ⚠️ Atlassian Cloud: varies by plan
- ⚠️ Rate limit applies per user, not per token
- ⚠️ Exceeded limits return 429 errors
- ⚠️ Wait for reset or upgrade plan

## 📋 Installation Checklist

Pre-Installation:
- [ ] Node.js v18+ installed
- [ ] npm available
- [ ] OpenCode 1.3.0+ installed
- [ ] Atlassian account active
- [ ] Access to Jira/Confluence

Installation:
- [ ] Atlassian MCP server installed
- [ ] Installation verified (`which`/`where`)
- [ ] Can run manually (test)

Authentication:
- [ ] Cloud ID identified
- [ ] API Token created
- [ ] Token copied and saved
- [ ] User email noted
- [ ] Credentials stored securely
- [ ] Token tested with curl

Configuration:
- [ ] OpenCode config file created/updated
- [ ] MCP section added
- [ ] Environment variables referenced
- [ ] Server enabled
- [ ] Config validated

Verification:
- [ ] `opencode mcp list` shows atlassian
- [ ] OpenCode session starts
- [ ] Atlassian tools available
- [ ] Test query works (list issues)
- [ ] Create/read operations successful

Security:
- [ ] Token not in git
- [ ] .gitignore updated (if using .env)
- [ ] Token rotation scheduled
- [ ] Appropriate permissions verified

---

**Created**: May 15, 2026  
**Format**: Markdown + PDF  
**Audience**: OpenCode users wanting Atlassian (Jira/Confluence) integration  
**Complexity**: Beginner to Advanced  
**Estimated Setup Time**: 15-30 minutes
