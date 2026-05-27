# SQL Server MCP - Quick Reference

## 📍 Project Location
```
C:\Users\ramiro.maceda\Documents\Opencode guides\sql-server-mcp
```

## 🚀 Quick Start

### 1. Installation
```powershell
cd "C:\Users\ramiro.maceda\Documents\Opencode guides\sql-server-mcp"
.\install.ps1
```

### 2. OpenCode Configuration
The installer will update your config, or you can manually edit:

**File:** `C:\Users\ramiro.maceda\.config\opencode\config.json`

**Add:**
```json
{
  "mcpServers": {
    "sql-server": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "C:/Users/ramiro.maceda/Documents/Opencode guides/sql-server-mcp",
      "env": {
        "PYTHONPATH": "C:/Users/ramiro.maceda/Documents/Opencode guides/sql-server-mcp",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### 3. Restart OpenCode

## 📚 Documentation Files

| File | Description |
|------|-------------|
| **README.md** | Quick start guide and tool reference |
| **docs/COMPLETE_GUIDE.md** | Comprehensive 1,500+ line technical guide |
| **docs/COMPLETE_GUIDE.html** | HTML version for PDF printing (Ctrl+P) |
| **PROJECT_SUMMARY.md** | Project overview and specifications |
| **docs/PDF_GENERATION_GUIDE.md** | How to create PDF from markdown |

## 🔧 Available Tools (15 Total)

### Table Operations (6 tools)
- `list_tables` - List all dbo tables
- `get_table_schema` - View table structure
- `query_table` - SELECT queries
- `update_table` - UPDATE (DEV only: DOA/DOB)
- `insert_into_table` - INSERT (DEV only: DOA/DOB)
- `delete_from_table` - DELETE (DEV only: DOA/DOB)

### SQL Agent Jobs (4 tools)
- `list_agent_jobs` - List all jobs
- `get_job_history` - Execution history
- `get_job_status` - Current job status
- `get_failed_jobs` - Recent failures

### Instance Management (5 tools)
- `get_instance_status` - Server information
- `restart_sql_service` - Restart SQL Server (admin required)
- `restart_agent_service` - Restart Agent (admin required)
- `get_service_status` - Check service status
- `test_connection` - Test connectivity

## 💡 Example Usage

```
You: "List all tables in DOA-SERVER\INSTANCE database CustomerDB"
You: "Show me users where status is active"
You: "Update status to inactive for user ID 123 in DOA database"
You: "Show me failed jobs in the last 24 hours"
You: "Test connection to DOA-SERVER\INSTANCE"
```

## 🔒 Security Features

- ✅ UPDATE/INSERT/DELETE only on DOA or DOB servers
- ✅ Production servers automatically protected
- ✅ WHERE clause mandatory for UPDATE/DELETE
- ✅ Windows Authentication (uses your UCN credentials)
- ✅ SQL injection prevention (parameterized queries)
- ✅ Full audit logging

## 📄 Generate PDF Documentation

### Method 1: Browser Print (Easiest)
1. Open `docs\COMPLETE_GUIDE.html` in browser
2. Press **Ctrl+P**
3. Select "Save as PDF"

### Method 2: PowerShell Script
```powershell
cd "C:\Users\ramiro.maceda\Documents\Opencode guides\sql-server-mcp"
.\generate_pdf_simple.ps1
```

## 📞 Support

For detailed information, see:
- Full documentation: `docs\COMPLETE_GUIDE.md`
- Troubleshooting: `docs\COMPLETE_GUIDE.md` (Section 8)
- Installation help: `README.md`

---

**Version:** 1.0.0  
**Last Updated:** May 21, 2026  
**Location:** C:\Users\ramiro.maceda\Documents\Opencode guides\sql-server-mcp
