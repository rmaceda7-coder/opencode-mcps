# OpenCode Complete Documentation Suite
## Your Comprehensive Guide to OpenCode Setup and Usage

> **Created**: May 15, 2026  
> **Total Documents**: 13 files (4 main guides + summaries + config)  
> **Total Size**: ~3.8 MB  
> **Total Pages**: ~220-260 pages

---

## 📚 Quick Navigation

### Start Here Based on Your Goal

| Your Goal | Start With |
|-----------|------------|
| **I want to install OpenCode** | → [01_OpenCode_Installation_Guide.pdf](#1-opencode-installation-guide) |
| **I want to understand Serena** | → [02_Serena_Code_Intelligence_Guide.pdf](#2-serena-code-intelligence-guide) |
| **I'm confused about Serena vs MCP** | → [03_Understanding_Serena_vs_MCP.pdf](#3-understanding-serena-vs-mcp) |
| **I want GitHub integration** | → [04_GitHub_MCP_Installation_Guide.pdf](#4-github-mcp-installation-guide) |
| **I need quick reference** | → Check the Summary files |
| **I want to generate my own PDFs** | → [00_PDF_Generation_Instructions.md](#pdf-generation-instructions) |

---

## 📖 Complete Document List

### Configuration & Tools
- **00_md-to-pdf-config.json** - PDF generation configuration
- **00_PDF_Generation_Instructions.md** - How to generate PDFs from markdown

### Main Guides (Full Documentation)

#### 1. OpenCode Installation Guide
- **Files**: 
  - `01_OpenCode_Installation_Guide.md` (53.4 KB)
  - `01_OpenCode_Installation_Guide.pdf` (1.27 MB, 60-70 pages)
- **Contents**:
  - 5 installation methods (npm, Homebrew, prebuilt, source, Docker)
  - 6+ provider configurations (Anthropic, OpenAI, Google, etc.)
  - 30+ troubleshooting scenarios
  - Authentication setup
  - MCP server basics
  - Configuration best practices
- **Use When**: First-time setup, changing providers, troubleshooting

#### 2. Serena Code Intelligence Guide
- **Files**: 
  - `02_Serena_Code_Intelligence_Guide.md` (31.4 KB)
  - `02_Serena_Code_Intelligence_Guide.pdf` (683 KB, 45-50 pages)
  - `02_Serena_Guide_Summary.md` (8.7 KB) - Quick reference
- **Contents**:
  - What Serena is (built-in code intelligence)
  - 25+ Serena tools explained
  - Real-world workflows
  - LSP integration (optional enhancement)
  - Project onboarding
  - Memory system usage
  - Symbol navigation
  - Code refactoring tools
- **Use When**: Working with code, understanding OpenCode's built-in capabilities

#### 3. Understanding Serena vs MCP
- **Files**: 
  - `03_Understanding_Serena_vs_MCP.md` (24.5 KB)
  - `03_Understanding_Serena_vs_MCP.pdf` (490 KB, 35-40 pages)
  - `03_Serena_vs_MCP_Summary.md` (4.9 KB) - Quick reference
- **Contents**:
  - Critical clarification: Serena is NOT an MCP server
  - Architecture diagrams showing built-in vs external
  - Why you see Serena tools automatically
  - What your actual MCP servers are
  - Built-in vs MCP comparison table
  - Configuration examples
  - Common misconceptions
- **Use When**: Confused about Serena, trying to "install" Serena as MCP, understanding architecture

#### 4. GitHub MCP Installation Guide
- **Files**: 
  - `04_GitHub_MCP_Installation_Guide.md` (47.9 KB)
  - `04_GitHub_MCP_Installation_Guide.pdf` (1.31 MB, 80-100 pages)
  - `04_GitHub_MCP_Summary.md` (12.1 KB) - Quick reference
- **Contents**:
  - 4 installation methods for GitHub MCP
  - Personal Access Token setup (fine-grained vs classic)
  - Secure token storage (5-level security ranking)
  - OpenCode configuration for GitHub
  - 50+ GitHub operations available
  - 8 real-world workflow examples
  - Complete troubleshooting guide
  - Security best practices
  - Token rotation schedules
  - GitHub Enterprise configuration
  - Multi-account setup
- **Use When**: Setting up GitHub integration, troubleshooting GitHub MCP, learning GitHub operations

---

## 🎯 Recommended Learning Path

### For Complete Beginners

```
Day 1: Install OpenCode
├─ Read: 01_OpenCode_Installation_Guide.pdf
├─ Do: Install OpenCode
├─ Do: Configure your preferred provider (Claude/GPT)
└─ Verify: Run `opencode --version`

Day 2: Understand Built-in Features
├─ Read: 02_Serena_Code_Intelligence_Guide.pdf
├─ Read: 03_Understanding_Serena_vs_MCP.pdf
├─ Do: Try Serena in a test project
└─ Verify: Ask "Show me the structure of main.py"

Day 3: Add GitHub Integration
├─ Read: 04_GitHub_MCP_Installation_Guide.pdf
├─ Do: Create GitHub Personal Access Token
├─ Do: Configure GitHub MCP in opencode.json
└─ Verify: "List my GitHub repositories"

Day 4+: Master Advanced Features
├─ Explore: Real-world examples in each guide
├─ Practice: Workflow automation
└─ Customize: Add more MCP servers
```

### For Experienced Users

```
Quick Setup (1 hour):
├─ Skim: 01_OpenCode_Installation_Guide.pdf (installation method section)
├─ Install OpenCode
├─ Skim: 04_GitHub_MCP_Installation_Guide.pdf (quick start)
├─ Configure GitHub MCP
└─ Reference: Keep summary files handy
```

---

## 🔍 Quick Reference by Topic

### Installation & Setup
- **Install OpenCode**: → 01_OpenCode_Installation_Guide.pdf, pages 1-20
- **Choose Provider**: → 01_OpenCode_Installation_Guide.pdf, pages 20-35
- **First Configuration**: → 01_OpenCode_Installation_Guide.pdf, pages 35-45

### Code Intelligence (Serena)
- **What is Serena**: → 02_Serena_Code_Intelligence_Guide.pdf, pages 1-10
- **Available Tools**: → 02_Serena_Code_Intelligence_Guide.pdf, pages 10-25
- **Workflows**: → 02_Serena_Code_Intelligence_Guide.pdf, pages 25-35
- **Quick Reference**: → 02_Serena_Guide_Summary.md

### Architecture Understanding
- **Built-in vs MCP**: → 03_Understanding_Serena_vs_MCP.pdf, pages 1-15
- **Architecture Diagrams**: → 03_Understanding_Serena_vs_MCP.pdf, pages 5-10
- **Your MCP Servers**: → 03_Understanding_Serena_vs_MCP.pdf, pages 15-20

### GitHub Integration
- **Installation**: → 04_GitHub_MCP_Installation_Guide.pdf, pages 1-25
- **Authentication**: → 04_GitHub_MCP_Installation_Guide.pdf, pages 25-40
- **Configuration**: → 04_GitHub_MCP_Installation_Guide.pdf, pages 40-50
- **Available Operations**: → 04_GitHub_MCP_Installation_Guide.pdf, pages 50-60
- **Examples**: → 04_GitHub_MCP_Installation_Guide.pdf, pages 60-75
- **Quick Reference**: → 04_GitHub_MCP_Summary.md

### Troubleshooting
- **OpenCode Issues**: → 01_OpenCode_Installation_Guide.pdf, pages 45-60
- **Serena Not Working**: → 02_Serena_Code_Intelligence_Guide.pdf, pages 35-40
- **GitHub MCP Issues**: → 04_GitHub_MCP_Installation_Guide.pdf, pages 75-85

### Security
- **Token Storage**: → 04_GitHub_MCP_Installation_Guide.pdf, pages 85-90
- **Best Practices**: → 04_GitHub_MCP_Installation_Guide.pdf, pages 90-95
- **Incident Response**: → 04_GitHub_MCP_Installation_Guide.pdf, page 95

---

## 📊 Documentation Statistics

| Guide | Pages | Size | Topics Covered |
|-------|-------|------|----------------|
| OpenCode Installation | 60-70 | 1.27 MB | 5 install methods, 6+ providers, 30+ issues |
| Serena Intelligence | 45-50 | 683 KB | 25+ tools, workflows, LSP |
| Serena vs MCP | 35-40 | 490 KB | Architecture, comparisons, config |
| GitHub MCP | 80-100 | 1.31 MB | 4 install methods, 50+ operations, security |
| **Total** | **220-260** | **~3.8 MB** | **Complete OpenCode ecosystem** |

---

## 🎓 Common Questions

### Q: I'm new to OpenCode. Where do I start?
**A**: Start with `01_OpenCode_Installation_Guide.pdf`. Follow the recommended installation method (npm), configure a provider, and test it.

### Q: What is Serena and do I need to install it?
**A**: Serena is OpenCode's **built-in** code intelligence. It's automatically available when you install OpenCode. Read `03_Understanding_Serena_vs_MCP.pdf` for the full explanation.

### Q: How do I add GitHub integration?
**A**: Follow `04_GitHub_MCP_Installation_Guide.pdf`. You'll need to:
1. Install the GitHub MCP server: `npm install -g @modelcontextprotocol/server-github`
2. Create a GitHub Personal Access Token
3. Configure in `opencode.json`

### Q: I'm getting errors. Where's the troubleshooting section?
**A**: Each guide has a dedicated troubleshooting section:
- OpenCode errors: Guide 01, pages 45-60
- Serena issues: Guide 02, pages 35-40
- GitHub MCP issues: Guide 04, pages 75-85

### Q: Can I share these guides with my team?
**A**: Yes! All guides are comprehensive and designed for team onboarding. Consider sharing:
- Full PDF guides for deep learning
- Summary files for quick reference
- Specific sections for specific needs

### Q: How do I generate PDFs from the markdown files?
**A**: See `00_PDF_Generation_Instructions.md` for complete instructions. Short version:
```bash
npm install -g md-to-pdf
md-to-pdf your-file.md
```

### Q: Which guide do I need for [specific task]?
**A**: Use the "Quick Reference by Topic" section above, or:
- Installation → Guide 01
- Code work → Guide 02
- Understanding architecture → Guide 03
- GitHub operations → Guide 04

---

## 🔧 Using These Guides

### For Reading
- **PDF files**: Best for reading cover-to-cover, printing, sharing
- **Markdown files**: Best for searching, copying code examples, editing
- **Summary files**: Best for quick lookups, cheat sheets

### For Team Onboarding
1. Share `01_OpenCode_Installation_Guide.pdf` for initial setup
2. Share `02_Serena_Code_Intelligence_Guide.pdf` for daily usage
3. Share `04_GitHub_MCP_Installation_Guide.pdf` if using GitHub
4. Keep summary files accessible for quick reference

### For Troubleshooting
1. Identify the issue category (installation, Serena, GitHub)
2. Go to the relevant guide's troubleshooting section
3. Follow step-by-step solutions
4. Check summary files for quick fixes

### For Advanced Configuration
- **Custom MCP servers**: Guide 01, MCP section
- **LSP configuration**: Guide 02, LSP section
- **GitHub Enterprise**: Guide 04, advanced configuration
- **Multi-account setup**: Guide 04, multiple accounts section

---

## 📁 File Organization

```
Opencode guides/
├── 00_README_START_HERE.md              ← You are here
├── 00_md-to-pdf-config.json             ← PDF generation config
├── 00_PDF_Generation_Instructions.md    ← How to create PDFs
│
├── 01_OpenCode_Installation_Guide.md    ← Full markdown
├── 01_OpenCode_Installation_Guide.pdf   ← 60-70 pages
│
├── 02_Serena_Code_Intelligence_Guide.md ← Full markdown
├── 02_Serena_Code_Intelligence_Guide.pdf← 45-50 pages
├── 02_Serena_Guide_Summary.md           ← Quick reference
│
├── 03_Understanding_Serena_vs_MCP.md    ← Full markdown
├── 03_Understanding_Serena_vs_MCP.pdf   ← 35-40 pages
├── 03_Serena_vs_MCP_Summary.md          ← Quick reference
│
├── 04_GitHub_MCP_Installation_Guide.md  ← Full markdown
├── 04_GitHub_MCP_Installation_Guide.pdf ← 80-100 pages
└── 04_GitHub_MCP_Summary.md             ← Quick reference
```

**Naming Convention**:
- `00_` - Meta/configuration files
- `01_` - OpenCode installation and setup
- `02_` - Built-in features (Serena)
- `03_` - Architecture and concepts
- `04_` - External integrations (GitHub MCP)

---

## 🚀 Quick Start Commands

### Install OpenCode
```bash
# Recommended method
npm install -g opencode-ai

# Verify
opencode --version
```

### Configure OpenCode
```bash
# Create config file
mkdir -p ~/.config/opencode
cat > ~/.config/opencode/opencode.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "lsp": true
}
EOF
```

### Test Serena (Built-in)
```bash
# Navigate to a code project
cd /path/to/your/project

# Start OpenCode
opencode

# In OpenCode, type:
> Show me the structure of main.py
```

### Add GitHub MCP
```bash
# Install GitHub MCP server
npm install -g @modelcontextprotocol/server-github

# Set token (replace with your token)
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token_here"

# Add to opencode.json (see Guide 04 for full config)
```

---

## 💡 Pro Tips

### For Daily Use
- Keep summary files (`*_Summary.md`) in an easily accessible location
- Bookmark specific PDF sections for common tasks
- Use PDF search (Ctrl+F) to find specific topics quickly

### For Teams
- Share the full PDF guides for new team members
- Create a shared folder with all guides
- Update guides when OpenCode versions change
- Document your team-specific configurations

### For Troubleshooting
- Check the troubleshooting section FIRST before searching online
- Error messages often include file:line references - use those
- Debug mode instructions are in each guide

### For Advanced Users
- Combine guides - e.g., use Serena + GitHub MCP together
- Explore advanced configuration sections
- Customize MCP server setups
- Create your own MCP servers

---

## 🔄 Keeping Updated

### When to Re-read
- **OpenCode major version update**: Re-read Guide 01
- **New MCP server needed**: Reference Guide 01 (MCP section)
- **GitHub API changes**: Check Guide 04
- **Serena behavior changes**: Check Guide 02

### Version Compatibility
These guides are compatible with:
- **OpenCode**: 1.3.0+
- **GitHub MCP**: Latest (as of May 2026)
- **Node.js**: 18.0.0+

---

## 📞 Getting Help

### Self-Help Resources
1. **Check the troubleshooting section** of the relevant guide
2. **Search the PDF** for your error message
3. **Read the FAQ** in each guide
4. **Check summary files** for quick answers

### Community Resources
- **OpenCode Discord**: https://discord.gg/opencode
- **OpenCode Docs**: https://opencode.ai/docs
- **GitHub Discussions**: Model Context Protocol repositories
- **Stack Overflow**: Tags `opencode`, `model-context-protocol`

### When to Ask for Help
After you've:
- ✅ Read the relevant guide section
- ✅ Tried the troubleshooting steps
- ✅ Checked your configuration
- ✅ Verified prerequisites (Node.js version, etc.)

Include in your question:
- Guide section you're following
- Error message (exact text)
- Your configuration (sanitized - no tokens!)
- Steps you've already tried

---

## ✅ Checklist for Complete Setup

### Basic Setup
- [ ] OpenCode installed (`opencode --version` works)
- [ ] Provider configured (Anthropic/OpenAI/etc.)
- [ ] Can start OpenCode sessions
- [ ] Serena available (built-in, automatic)
- [ ] Read Guide 01 (at least installation section)

### Code Intelligence Setup
- [ ] Tested Serena in a project
- [ ] LSP enabled (optional, recommended)
- [ ] Understand built-in vs MCP (read Guide 03)
- [ ] Read Guide 02 (at least tools section)

### GitHub Integration (Optional)
- [ ] GitHub MCP installed
- [ ] Personal Access Token created
- [ ] Token stored securely
- [ ] GitHub MCP configured in opencode.json
- [ ] Tested GitHub operations
- [ ] Read Guide 04 (at least setup section)

### Documentation
- [ ] Saved guides to accessible location ✅ (You're here!)
- [ ] Bookmarked frequently used sections
- [ ] Shared with team (if applicable)
- [ ] Know where to find troubleshooting
- [ ] Summary files bookmarked

---

## 🎉 You're All Set!

You now have:
- ✅ Complete OpenCode documentation suite
- ✅ Installation guides for all components
- ✅ Troubleshooting resources
- ✅ Real-world usage examples
- ✅ Security best practices
- ✅ Quick reference summaries
- ✅ PDF versions for offline access

**Total Knowledge Base**: 220-260 pages covering the entire OpenCode ecosystem!

---

## 📝 Document Version Information

- **Created**: May 15, 2026
- **Last Updated**: May 15, 2026
- **Guide Suite Version**: 1.0
- **OpenCode Compatibility**: 1.3.0+
- **Total Files**: 13
- **Total Size**: ~3.8 MB

---

## 🙏 Happy Coding with OpenCode!

Remember:
- **Start with Guide 01** if you're new
- **Serena is built-in** - no installation needed
- **GitHub MCP is optional** - add when needed
- **Troubleshooting sections** are your friend
- **Summary files** for quick reference

**Your journey to AI-powered development starts here!** 🚀
