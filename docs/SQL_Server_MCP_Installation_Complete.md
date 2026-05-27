# SQL Server MCP - Installation Complete! ✅

## Status: Successfully Added to OpenCode

**Date:** May 21, 2026  
**Configuration File:** `C:\Users\ramiro.maceda\.config\opencode\opencode.json`

---

## ✅ What Was Done

### 1. Files Moved ✓
- **From:** `C:\Users\ramiro.maceda\AppData\Local\Temp\opencode\sql-server-mcp`
- **To:** `C:\Users\ramiro.maceda\Documents\Opencode guides\sql-server-mcp`
- **Files:** 17 files (128.91 KB)

### 2. OpenCode Configuration Updated ✓
Added SQL Server MCP to your OpenCode configuration:
```json
"sql-server": {
  "type": "local",
  "command": ["python", "-m", "src.server"],
  "enabled": true,
  "workingDirectory": "C:\\Users\\ramiro.maceda\\Documents\\Opencode guides\\sql-server-mcp",
  "environment": {
    "PYTHONPATH": "C:\\Users\\ramiro.maceda\\Documents\\Opencode guides\\sql-server-mcp",
    "LOG_LEVEL": "INFO"
  }
}
```

### 3. Python Dependencies Installed ✓
Successfully installed:
- `pyodbc` 5.3.0
- `sql-server-mcp` 1.0.0
- `mcp` SDK (dependency)

### 4. Import Test Passed ✓
All Python modules load successfully without errors.

---

## 🎯 Next Steps

### Step 1: Restart OpenCode (REQUIRED)
**You MUST restart OpenCode for the new MCP server to be loaded.**

Close and reopen OpenCode completely.

### Step 2: Verify Installation
After restarting OpenCode, test the SQL Server MCP:

**Test Query:**
```
"Test connection to localhost"
```

or

```
"List all MCP servers"
```

You should see `sql-server` in the list of available servers.

### Step 3: First Real Use
Try a real SQL Server operation:
```
"List tables in [YOUR-SERVER]\[INSTANCE] database [DATABASE-NAME]"
```

Example:
```
"List tables in DOA-SERVER\DEV database CustomerDB"
```

---

## 🔧 Available Tools (15 Total)

Once OpenCode restarts, you'll have access to:

### Table Operations (6 tools)
- `list_tables` - List all dbo schema tables
- `get_table_schema` - View table structure and columns
- `query_table` - Execute SELECT queries with filters
- `update_table` - UPDATE records (DEV only: DOA/DOB)
- `insert_into_table` - INSERT records (DEV only: DOA/DOB)
- `delete_from_table` - DELETE records (DEV only: DOA/DOB)

### SQL Agent Jobs (4 tools)
- `list_agent_jobs` - List all SQL Server Agent jobs
- `get_job_history` - Get job execution history
- `get_job_status` - Get current status of a job
- `get_failed_jobs` - Get jobs that failed recently

### Instance Management (5 tools)
- `get_instance_status` - Get SQL Server instance info
- `restart_sql_service` - Restart SQL Server (admin required)
- `restart_agent_service` - Restart Agent (admin required)
- `get_service_status` - Check service status
- `test_connection` - Test connectivity and auth

---

## 🔒 Security Features

### Environment Protection
- ✅ **DOA** servers - Write operations ALLOWED
- ✅ **DOB** servers - Write operations ALLOWED
- ❌ **Production** servers - Write operations BLOCKED
- ❌ **Unknown** servers - Write operations BLOCKED

### Safety Features
- WHERE clause mandatory for UPDATE/DELETE
- Parameterized queries (SQL injection protection)
- Windows Authentication (uses your UCN credentials)
- No passwords stored in configuration
- Full audit logging of all operations

---

## 💡 Usage Examples

### Example 1: Query Tables
```
You: "List all tables in DOA-SERVER\DEV database CustomerDB"
Result: Shows all dbo tables with row counts and sizes
```

### Example 2: View Table Structure
```
You: "Show me the schema for the Users table in DOA-SERVER\DEV CustomerDB"
Result: Displays columns, data types, nullability, primary keys
```

### Example 3: Query Data
```
You: "Show me active users from DOA-SERVER\DEV CustomerDB Users table"
Result: Returns filtered user records
```

### Example 4: Update Dev Data
```
You: "Update user status to 'inactive' for user ID 123 in DOA-SERVER database"
Result: Updates 1 row (only works on DOA/DOB servers)
```

### Example 5: Production Protection
```
You: "Update user status in PROD-SERVER"
Result: ERROR - Write operations not allowed on production
```

### Example 6: Monitor Jobs
```
You: "Show me SQL Agent jobs that failed in the last 24 hours on PROD-SERVER"
Result: Lists failed jobs with error messages
```

---

## 🐛 Troubleshooting

### Issue: MCP Server Not Showing Up
**Solution:** Restart OpenCode completely (close and reopen)

### Issue: Connection Timeout
**Cause:** Server offline, network issue, or firewall blocking
**Solution:** 
- Verify server is online
- Check network connectivity
- Test with: `sqlcmd -S SERVER\INSTANCE -E -Q "SELECT @@VERSION"`

### Issue: Authentication Failed
**Cause:** No SQL Server permissions
**Solution:**
- Contact your DBA to grant SQL Server access
- Verify Windows Authentication is enabled on the server

### Issue: "UPDATE operations not allowed"
**This is by design!** Write operations only work on DOA/DOB servers.

---

## 📚 Documentation

All documentation is in your Documents folder:

### Quick References
- **Quick Start:** `SQL_Server_MCP_QuickRef.md` (in parent folder)
- **README:** `sql-server-mcp\README.md`

### Complete Documentation
- **Full Guide:** `sql-server-mcp\docs\COMPLETE_GUIDE.md` (1,500+ lines)
- **HTML Version:** `sql-server-mcp\docs\COMPLETE_GUIDE.html`
- **Project Summary:** `sql-server-mcp\PROJECT_SUMMARY.md`

### Generate PDF
1. Open `docs\COMPLETE_GUIDE.html` in browser
2. Press **Ctrl+P**
3. Select "Save as PDF"

Or run: `.\generate_pdf_simple.ps1`

---

## 📋 Configuration Details

### OpenCode Config Location
```
C:\Users\ramiro.maceda\.config\opencode\opencode.json
```

### MCP Server Location
```
C:\Users\ramiro.maceda\Documents\Opencode guides\sql-server-mcp
```

### Python Environment
- **Python:** 3.13 (detected)
- **pyodbc:** 5.3.0
- **MCP SDK:** Installed via dependencies

---

## ⚠️ Important Reminders

1. **RESTART OPENCODE** to load the new MCP server
2. **Test connection first** before trying complex operations
3. **Write operations** only work on DOA/DOB servers (by design)
4. **Service restarts** require administrator privileges
5. **WHERE clauses** are mandatory for UPDATE/DELETE operations

---

## 🎉 You're All Set!

The SQL Server MCP is now fully integrated into your OpenCode project.

**Next Action:** **RESTART OPENCODE** and test with:
```
"Test connection to localhost"
```

For detailed documentation, see:
```
C:\Users\ramiro.maceda\Documents\Opencode guides\sql-server-mcp\docs\COMPLETE_GUIDE.md
```

---

**Installation Date:** May 21, 2026  
**Version:** 1.0.0  
**Status:** ✅ Ready to Use (after OpenCode restart)
