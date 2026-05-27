# Azure DevOps / TFS MCP Guide - Summary

## 📄 Document Created
**06_Azure_DevOps_TFS_MCP_Guide.md** + **06_Azure_DevOps_TFS_MCP_Guide.pdf**

## ⚠️ Important Disclosure

**As of May 2026, there is NO official Azure DevOps/TFS MCP server available.**

This guide provides:
1. ✅ **Alternative solutions** that work today
2. ✅ **How to build a custom MCP server**
3. ✅ **Workarounds** using existing tools

## 🎯 Purpose
Comprehensive guide for integrating Azure DevOps/TFS with OpenCode, covering available alternatives and how to create custom MCP server integration.

## 📚 Document Structure

### 1. Understanding TFS vs Azure DevOps
- **TFS (Legacy)**: Team Foundation Server 2018 (final version)
- **Azure DevOps (Modern)**: Cloud and on-premises, actively developed
- **Migration Path**: TFS → Azure DevOps Server → Azure DevOps Services
- **Recommendation**: Use Azure DevOps (TFS is end-of-life)

### 2. Current State of MCP Support

**Available** ✅:
- GitHub MCP (official)
- GitLab MCP (community)
- Atlassian MCP (official)

**NOT Available** ❌:
- Azure DevOps MCP
- TFS MCP
- Azure Repos MCP

**Why?**
- Microsoft focuses on GitHub Copilot
- Smaller MCP community for Azure DevOps
- Complex multi-service platform

### 3. Alternative Solutions (3 Options)

#### Solution 1: Azure DevOps CLI ⭐ RECOMMENDED
**Best for**: Immediate use, official support

**Setup**:
```bash
# Install Azure CLI
winget install -e --id Microsoft.AzureCLI

# Install DevOps extension
az extension add --name azure-devops

# Login and configure
az login
az devops configure --defaults \
  organization=https://dev.azure.com/yourorg \
  project=YourProject

# Create PAT and set
export AZURE_DEVOPS_EXT_PAT="your_pat"
```

**Usage with OpenCode**:
```
You: "List active work items"
OpenCode: *Uses bash: az boards query*

You: "Create a bug for login issue"
OpenCode: *Uses bash: az boards work-item create*
```

**Pros**:
- ✅ Works immediately (no development needed)
- ✅ Official Microsoft tool
- ✅ Full Azure DevOps functionality
- ✅ Well-documented

**Cons**:
- ❌ Not native MCP integration
- ❌ Requires bash tool calls
- ❌ Less seamless than true MCP

---

#### Solution 2: Custom MCP Server
**Best for**: Best integration experience

**Overview**:
Build your own MCP server using:
- MCP SDK (TypeScript or Python)
- Azure DevOps Node.js/Python API
- stdio communication

**Complexity**: Medium to High

**Time to Build**: 1-8 weeks depending on features

**Example Implementation**:
The guide includes a complete TypeScript example with:
- MCP server setup
- Azure DevOps API integration
- 5 core tools implemented
- Full source code provided

**Tools Example**:
- `azuredevops_list_work_items`
- `azuredevops_get_work_item`
- `azuredevops_create_work_item`
- `azuredevops_list_repositories`
- `azuredevops_list_pull_requests`

**Pros**:
- ✅ Native MCP integration
- ✅ Seamless OpenCode experience
- ✅ Full control over features
- ✅ Can open-source for community

**Cons**:
- ❌ Requires development effort (40-80 hours)
- ❌ Must maintain and update
- ❌ Need TypeScript/Python knowledge

---

#### Solution 3: Direct REST API
**Best for**: Full control, one-off operations

**Example**:
```bash
# Query work items
curl -u :$AZURE_DEVOPS_PAT \
  https://dev.azure.com/yourorg/YourProject/_apis/wit/wiql?api-version=7.0 \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT [System.Id] FROM WorkItems"}'
```

**Pros**:
- ✅ Direct API access
- ✅ Maximum flexibility
- ✅ No additional dependencies

**Cons**:
- ❌ Complex syntax
- ❌ Requires API knowledge
- ❌ More error-prone
- ❌ Less user-friendly

### 4. Creating a Custom MCP Server

**Complete TypeScript Example Provided**:

The guide includes a full working implementation:

**Project Structure**:
```
mcp-server-azuredevops/
├── package.json
├── tsconfig.json
└── src/
    └── index.ts (complete implementation)
```

**Features Implemented**:
1. List work items (WIQL queries)
2. Get work item details
3. Create work items
4. List repositories
5. List pull requests

**Build & Deploy**:
```bash
# Build
npm run build

# Install globally
npm install -g .

# Configure OpenCode
{
  "mcp": {
    "azuredevops": {
      "type": "stdio",
      "command": "mcp-server-azuredevops",
      "env": {
        "AZURE_DEVOPS_ORG_URL": "{env:AZURE_DEVOPS_ORG_URL}",
        "AZURE_DEVOPS_PAT": "{env:AZURE_DEVOPS_PAT}"
      },
      "enabled": true
    }
  }
}
```

### 5. Azure DevOps CLI Complete Setup

**Step-by-Step**:

1. **Install Azure CLI**
   - Windows: `winget install Microsoft.AzureCLI`
   - macOS: `brew install azure-cli`
   - Linux: `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`

2. **Install DevOps Extension**
   ```bash
   az extension add --name azure-devops
   ```

3. **Authenticate**
   ```bash
   az login
   # Or use PAT
   export AZURE_DEVOPS_EXT_PAT="your_pat"
   ```

4. **Configure Defaults**
   ```bash
   az devops configure --defaults \
     organization=https://dev.azure.com/yourorg \
     project=YourProject
   ```

5. **Test Commands**
   ```bash
   az boards query --wiql "SELECT [System.Id] FROM WorkItems"
   az boards work-item create --title "Bug" --type Bug
   az repos list
   az repos pr list --status active
   ```

### 6. REST API Integration

**Authentication**:
- Create PAT at: `https://dev.azure.com/yourorg/_usersSettings/tokens`
- Required scopes: Work Items (Read, Write), Code (Read, Write)

**Common Endpoints**:

**Work Items**:
```bash
# Query
POST https://dev.azure.com/{org}/{project}/_apis/wit/wiql?api-version=7.0

# Get
GET https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{id}?api-version=7.0

# Create
POST https://dev.azure.com/{org}/{project}/_apis/wit/workitems/$Bug?api-version=7.0
```

**Git Repos**:
```bash
# List repos
GET https://dev.azure.com/{org}/{project}/_apis/git/repositories?api-version=7.0

# List PRs
GET https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repo}/pullrequests?api-version=7.0
```

### 7. Feature Comparison: Ideal MCP Features

What an ideal Azure DevOps MCP server should have:

#### Work Items (Azure Boards)
- ✅ Create work items (Bug, Task, Story, Epic, Feature)
- ✅ Query work items (WIQL)
- ✅ Update work items
- ✅ Add comments
- ✅ Link work items
- ✅ Attach files
- ✅ Get history
- ✅ Sprint management

#### Repositories (Azure Repos)
- ✅ List repositories
- ✅ File operations (read, create, update)
- ✅ Branch management
- ✅ Commit history

#### Pull Requests
- ✅ List PRs
- ✅ Create PRs
- ✅ Comment on PRs
- ✅ Approve/reject
- ✅ Complete (merge)
- ✅ Get diff

#### Pipelines
- ✅ List pipelines
- ✅ Trigger runs
- ✅ Get status
- ✅ Get logs

### 8. Roadmap: Building Your Own MCP

**Phase 1: MVP (1-2 weeks)**
- Work item query, get, create
- List repos and PRs
- 5 core tools

**Phase 2: Enhanced (2-4 weeks)**
- Update work items
- Add comments
- Create PRs
- Get PR details
- File operations

**Phase 3: Advanced (4-8 weeks)**
- Pipeline integration
- Work item linking
- PR reviews
- Test plans

**Phase 4: Polish (2-4 weeks)**
- Error handling
- Rate limiting
- Documentation
- Tests
- Publish to npm

**Total Effort**: 40-80 development hours

### 9. Community Alternatives

**Request Official Support**:
- Open issue on MCP GitHub
- Explain use case and demand
- Offer to help build

**Check Community**:
- MCP Registry: https://github.com/modelcontextprotocol/servers
- npm: `npm search mcp azure devops`

**Hire Development**:
- Estimated cost: $2,000-$8,000
- Can open-source result

### 10. FAQ (10 Questions)

Key questions answered:
- Can I use GitHub MCP with Azure Repos? (No, different platforms)
- Does Azure DevOps CLI work with OpenCode? (Yes, best current solution)
- Can I migrate from TFS? (Yes, Microsoft provides tools)
- What PAT permissions needed? (Work Items R/W, Code R/W)
- Works with on-premises? (Yes, change URL)
- Python version? (Yes, adapt TypeScript example)
- Can OpenCode help build it? (Yes, use Serena)
- Where's API docs? (learn.microsoft.com/rest/api/azure/devops/)
- Can I contribute? (Yes, build and open-source)

## 📊 Document Statistics

- **Total Length**: ~2,800 lines
- **Sections**: 10 major sections
- **Code Examples**: 40+ snippets
- **API Endpoints**: 10+ documented
- **Complete MCP Server**: Full TypeScript implementation
- **CLI Commands**: 20+ examples
- **Estimated PDF Size**: 900 KB - 1.1 MB
- **Estimated PDF Pages**: 60-75 pages

## 🎯 Key Features

### Honest Assessment
✅ Clear about NO official MCP server (as of May 2026)
✅ Provides working alternatives immediately
✅ Full custom MCP server code included
✅ Three solutions ranked by ease/power

### Practical Solutions
✅ Azure DevOps CLI method (works now)
✅ Complete custom MCP implementation
✅ REST API examples
✅ Real authentication setup

### Development Guide
✅ Complete TypeScript MCP server code
✅ Package.json and tsconfig included
✅ Build and deployment instructions
✅ OpenCode configuration examples

### Comprehensive Coverage
✅ TFS vs Azure DevOps explained
✅ Migration path documented
✅ On-premises and cloud support
✅ Work items, repos, PRs, pipelines

## 🔗 Related Documents

| Document | Purpose | Size |
|----------|---------|------|
| **OpenCode Installation Guide** | Install OpenCode | 1.24 MB |
| **GitHub MCP Installation Guide** | GitHub integration | 1.28 MB |
| **Atlassian MCP Installation Guide** | Jira/Confluence integration | 1.10 MB |
| **Azure DevOps/TFS MCP Guide** | Azure DevOps (this doc) | 900 KB - 1.1 MB |

## 🎓 Use This Guide For

- ✅ Understanding Azure DevOps/TFS MCP status
- ✅ Setting up Azure DevOps CLI with OpenCode (works now!)
- ✅ Building custom Azure DevOps MCP server
- ✅ Learning Azure DevOps REST APIs
- ✅ Migrating from TFS to Azure DevOps
- ✅ Comparing solution options
- ✅ Understanding what features you'd want

## 💡 Key Differentiators

### Unique to This Guide
- ✅ **Only comprehensive Azure DevOps + OpenCode guide**
- ✅ **Honest about lack of official MCP**
- ✅ **Three working solutions provided**
- ✅ **Complete custom MCP server code**
- ✅ **Works today (CLI method)**
- ✅ **Clear development roadmap**

### vs Other Guides
- ❌ No official MCP (unlike GitHub/Atlassian guides)
- ✅ Multiple alternative solutions
- ✅ DIY custom server tutorial
- ✅ More developer-focused
- ✅ Community contribution pathway

## 🚀 Quick Reference

### Fastest Setup (Azure DevOps CLI)
```bash
# 1. Install
winget install Microsoft.AzureCLI
az extension add --name azure-devops

# 2. Authenticate
az login
export AZURE_DEVOPS_EXT_PAT="your_pat"

# 3. Configure
az devops configure --defaults \
  organization=https://dev.azure.com/yourorg \
  project=YourProject

# 4. Test
az boards query --wiql "SELECT [System.Id] FROM WorkItems"

# 5. Use with OpenCode
opencode
> "List active work items"
```
**Setup Time**: 10-15 minutes

### Custom MCP Server (Best Experience)
```bash
# 1. Clone/create project (code provided in guide)
# 2. Build: npm run build
# 3. Install: npm install -g .
# 4. Configure OpenCode (config provided)
# 5. Test with OpenCode
```
**Development Time**: 40-80 hours

### Required Credentials
```
✅ Organization URL: https://dev.azure.com/yourorg
✅ Personal Access Token (PAT)
✅ Project name
```

## ⚠️ Critical Notes

### This is Different from Other Guides
- ❌ **NO official MCP server exists** (as of May 2026)
- ✅ **Azure DevOps CLI works today**
- ✅ **Can build custom MCP** (code provided)
- ⏳ **Official support may come later**

### Recommended Approach
**For most users**: Use **Azure DevOps CLI**
- Works immediately
- Official Microsoft tool
- Full functionality
- No development needed

**For best experience**: Build **Custom MCP Server**
- Native integration
- Seamless experience
- Can share with community
- Requires development skills

### Migration Context
- TFS 2018 is end-of-life
- Microsoft recommends Azure DevOps
- Migration tools available
- On-premises option exists (Azure DevOps Server)

## 📋 Solution Comparison

| Solution | Ease | Power | Dev Time | When to Use |
|----------|------|-------|----------|-------------|
| **Azure CLI** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 10 min | Quick setup, works now |
| **Custom MCP** | ⭐⭐ | ⭐⭐⭐⭐⭐ | 40-80 hrs | Best integration |
| **REST API** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Varies | One-off tasks |

## 🎯 What You Can Do

### With Azure DevOps CLI (Today)
```
You: "List my active work items"
OpenCode: *Runs: az boards query ...*
Result: Lists your work items

You: "Create a bug for login issue"
OpenCode: *Runs: az boards work-item create ...*
Result: Creates Bug #123

You: "Show my pull requests"
OpenCode: *Runs: az repos pr list --creator @me*
Result: Lists your PRs
```

### With Custom MCP (After Building)
```
You: "List my active work items"
OpenCode: *Uses: azuredevops_query_work_items*
Result: Seamless integration

You: "Create a bug for login issue"
OpenCode: *Uses: azuredevops_create_work_item*
Result: Native MCP experience
```

## 📞 Getting Help

### Resources
- **Azure DevOps REST API**: https://learn.microsoft.com/rest/api/azure/devops/
- **Azure CLI Docs**: https://learn.microsoft.com/cli/azure/devops/
- **MCP SDK**: https://github.com/modelcontextprotocol/typescript-sdk
- **Node.js Azure DevOps SDK**: https://github.com/microsoft/azure-devops-node-api

### Community
- Request official MCP support in GitHub
- Share your custom MCP server
- Contribute to documentation

---

**Created**: May 15, 2026  
**Format**: Markdown + PDF  
**Status**: No official MCP (alternatives provided)  
**Recommended**: Azure DevOps CLI (works today)  
**Alternative**: Build custom MCP (code included)
