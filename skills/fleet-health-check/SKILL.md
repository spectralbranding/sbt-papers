---
name: fleet-health-check
description: Comprehensive health monitoring for all 4 fleet machines
---

# Fleet Health Check Skill

**Version**: 1.0.0
**Created**: 2026-02-05
**Purpose**: Monitor fleet machine health and service status

---

## Overview

Performs comprehensive health checks across all 4 fleet machines (fmini, dbook, dmini, fbook). Verifies SSH connectivity, service status, disk space, system resources, VPN connectivity, and service-specific health indicators.

Provides actionable reports with severity-based alerts and concrete remediation steps.

## Fleet Architecture

| Machine | Role | Chip | IP | Priority |
|---------|------|------|----|----------|
| **fmini** | Hub/Server | M4 Pro 64GB | 192.168.1.7 | Critical |
| **dbook** | Portable Dev | M4 Pro 48GB | Dynamic | High |
| **dmini** | Support Node | Intel 32GB | 192.168.1.200 | Medium |
| **fbook** | Research | Intel 16GB | 192.168.1.12 | Low |

## When to Use This Skill

- **Daily monitoring**: Automated daily health checks
- **Pre-deployment**: Verify target machine health before deploys
- **Troubleshooting**: Diagnose connectivity or service issues
- **Post-incident**: Verify system recovery after issues
- **Quarterly reviews**: Infrastructure health assessments
- **Capacity planning**: Monitor trends in resource usage

## Health Check Categories

### 1. Connectivity Checks

**SSH Availability**:
- Can connect to each machine?
- Response time acceptable (<100ms local, <500ms VPN)?
- SSH keys valid and accepted?

**VPN Connectivity** (when applicable):
- All machines reachable via VPN?
- VPN latency acceptable?
- VPN routing correct?

### 2. System Resource Checks

**Disk Space**:
- Usage percentage per volume
- Free space in GB
- Thresholds: Warn >75%, Error >85%, Critical >95%

**Memory Usage**:
- Physical memory used/total
- Swap usage
- Threshold: Warn >80%

**CPU Load**:
- Average load (1min, 5min, 15min)
- Threshold: Warn if load > CPU count

**Uptime**:
- Days since last reboot
- Unexpected reboots detected?

### 3. Service-Specific Checks

**fmini (Hub/Server)**:
- ✓ LanceDB: Running and responding to queries?
- ✓ Ollama: Running with models available?
- ✓ MCP servers: All servers responding?
- ✓ ntfy: Accessible and sending notifications?
- ✓ Git sync: Recent sync timestamp?

**dbook (Portable Dev)**:
- ✓ Local dev environment: Configured correctly?
- ✓ MCP cache: Present and recent?
- ✓ Claude Code: Functional?
- ✓ Local Ollama: Running when needed?

**dmini (Support)**:
- ✓ Docker stack: All containers running?
- ✓ Plex: Media server accessible?
- ✓ qBittorrent: Running with VPN?
- ✓ Backup service: Recent backup timestamp?
- ✓ Monitoring stack: Prometheus/Grafana up?

**fbook (Research)**:
- ✓ Claude Desktop: Configured and functional?
- ✓ Research tools: Accessible?
- ✓ Knowledge base: Synced?

### 4. Security Checks

**System Updates**:
- Security patches current?
- Last update timestamp
- Pending critical updates?

**Firewall Status**:
- Firewall active?
- Rules configured correctly?

**Port Security**:
- No unexpected open ports?
- Reserved ports not conflicting?

### 5. Network Checks

**Port Allocation**:
- No port conflicts?
- Reserved ports available?

**DNS Resolution**:
- .local domains resolving?
- External DNS working?

**Internet Connectivity**:
- Can reach external hosts?
- Bandwidth acceptable?

## Workflow

### Phase 1: Connectivity Test

```bash
# Test SSH to all machines
for machine in fmini dbook dmini fbook; do
    echo "Testing $machine..."
    time ssh d@$machine.local "echo ok" || echo "FAILED: $machine"
done
```

**Checks**:
- SSH responds within timeout
- No authentication errors
- Response time logged

### Phase 2: System Resource Collection

```bash
# Disk space
ssh fmini "df -h / | tail -1 | awk '{print \$5, \$4}'"

# Memory
ssh fmini "vm_stat | perl -ne '/page size of (\d+)/ and \$size=\$1; /Pages free.*: (\d+)/ and printf(\"Free: %.1f GB\n\", \$1 * \$size / 1073741824);'"

# CPU load
ssh fmini "uptime | awk '{print \$(NF-2), \$(NF-1), \$NF}'"

# Uptime
ssh fmini "uptime | awk '{print \$3, \$4}'"
```

**Collected metrics**:
- Disk usage percentage and free GB
- Memory usage
- CPU load averages (1, 5, 15 min)
- Days since last reboot

### Phase 3: Service Status Checks

**fmini services**:
```bash
# LanceDB
ssh fmini "curl -s http://localhost:8000/health || echo 'DOWN'"

# Ollama
ssh fmini "curl -s http://localhost:11434/api/tags | jq -r '.models[].name' | wc -l"

# MCP servers
ssh fmini "pgrep -f mcp-server | wc -l"

# ntfy
ssh fmini "curl -s http://localhost:8090/health || echo 'DOWN'"
```

**dmini services**:
```bash
# Docker containers
ssh dmini "docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -v NAMES"

# Plex
ssh dmini "curl -s http://localhost:32400/web/index.html >/dev/null && echo 'UP' || echo 'DOWN'"

# qBittorrent (check VPN)
ssh dmini "docker exec qbittorrent curl -s ifconfig.me"
```

### Phase 4: Report Generation

**Aggregate results**:
1. Connectivity status (pass/fail per machine)
2. Resource usage (per machine, with thresholds)
3. Service health (per machine, per service)
4. Issues detected (categorized by severity)
5. Recommendations (prioritized actions)

**Severity levels**:
- **Critical**: Service down, disk >95%, system unresponsive
- **Error**: Service degraded, disk >85%, high load
- **Warning**: Resource threshold approaching, service slow
- **Info**: All healthy, informational metrics

### Phase 5: Alerting (Optional)

```bash
# Send notification via ntfy if issues detected
if [ "$critical_issues" -gt 0 ]; then
    curl -d "Critical: $critical_issues fleet issues detected" \
         http://192.168.1.7:8090/fleet-health
fi
```

## Output Format

### Healthy Fleet Report

```
Fleet Health Report - 2026-02-05 10:30:15
==========================================

CONNECTIVITY STATUS:
✅ fmini - SSH OK (8ms)
✅ dbook - SSH OK (12ms)
✅ dmini - SSH OK (45ms)
✅ fbook - SSH OK (52ms)

SYSTEM RESOURCES:

fmini (Critical Priority):
  Disk:   45% used, 120GB free ✅
  Memory: 38.2GB / 64GB (60%) ✅
  CPU:    Load 2.1, 1.8, 1.5 (12 cores) ✅
  Uptime: 23 days ✅

dbook (High Priority):
  Disk:   62% used, 180GB free ✅
  Memory: 28.5GB / 48GB (59%) ✅
  CPU:    Load 1.2, 1.0, 0.9 (12 cores) ✅
  Uptime: 8 days ✅

dmini (Medium Priority):
  Disk:   55% used, 180GB free ✅
  Memory: 18.2GB / 32GB (57%) ✅
  CPU:    Load 0.8, 0.9, 1.1 (4 cores) ✅
  Uptime: 45 days ✅

fbook (Low Priority):
  Disk:   40% used, 90GB free ✅
  Memory: 8.1GB / 16GB (51%) ✅
  CPU:    Load 0.3, 0.2, 0.2 (2 cores) ✅
  Uptime: 12 days ✅

SERVICE HEALTH:

fmini:
  ✅ LanceDB - Running (response: 8ms)
  ✅ Ollama - 3 models loaded
  ✅ MCP Servers - 4 processes active
  ✅ ntfy - Running

dbook:
  ✅ Dev environment - Configured
  ✅ MCP cache - Updated 2h ago

dmini:
  ✅ Docker - 12/12 containers running
  ✅ Plex - Accessible
  ✅ qBittorrent - Running (VPN: Netherlands)
  ✅ Backups - Last run: 4h ago

fbook:
  ✅ Claude Desktop - Configured
  ✅ Research tools - Accessible

VPN & NETWORK:
✅ All machines reachable via VPN
✅ No port conflicts detected
✅ DNS resolution working

SECURITY:
✅ All systems updated (last check: 2 days ago)
✅ Firewalls active
✅ No unexpected open ports

SUMMARY:
Status: 🟢 ALL HEALTHY
Issues: 0 critical, 0 errors, 0 warnings
Compliance: 100%
Next check: 2026-02-06 10:30
```

### Degraded Fleet Report

```
Fleet Health Report - 2026-02-05 15:45:22
==========================================

CONNECTIVITY STATUS:
✅ fmini - SSH OK (10ms)
✅ dbook - SSH OK (15ms)
⚠️  dmini - SSH SLOW (280ms) - Investigate
✅ fbook - SSH OK (48ms)

SYSTEM RESOURCES:

fmini (Critical Priority):
  Disk:   45% used, 120GB free ✅
  Memory: 52.1GB / 64GB (81%) ⚠️  HIGH
  CPU:    Load 8.2, 6.1, 4.5 (12 cores) ⚠️  HIGH
  Uptime: 23 days ✅

dbook (High Priority):
  Disk:   78% used, 105GB free ⚠️  MONITOR
  Memory: 32.8GB / 48GB (68%) ✅
  CPU:    Load 2.1, 1.8, 1.5 (12 cores) ✅
  Uptime: 8 days ✅

dmini (Medium Priority):
  Disk:   55% used, 180GB free ✅
  Memory: 20.2GB / 32GB (63%) ✅
  CPU:    Load 1.2, 1.1, 1.0 (4 cores) ✅
  Uptime: 45 days ✅

fbook (Low Priority):
  Disk:   40% used, 90GB free ✅
  Memory: 9.1GB / 16GB (57%) ✅
  CPU:    Load 0.4, 0.3, 0.2 (2 cores) ✅
  Uptime: 12 days ✅

SERVICE HEALTH:

fmini:
  ✅ LanceDB - Running (response: 8ms)
  ⚠️  Ollama - SLOW (response: 2500ms)
  ✅ MCP Servers - 4 processes active
  ✅ ntfy - Running

dbook:
  ✅ Dev environment - Configured
  ⚠️  MCP cache - Stale (8 hours old)

dmini:
  ❌ Docker - 10/12 containers running (2 DOWN)
  ✅ Plex - Accessible
  ❌ qBittorrent - STOPPED
  ⚠️  Backups - Last run: 28h ago (overdue)

fbook:
  ✅ Claude Desktop - Configured
  ✅ Research tools - Accessible

VPN & NETWORK:
✅ All machines reachable via VPN
✅ No port conflicts detected
⚠️  dmini - High latency (280ms)

SECURITY:
✅ fmini, dbook, fbook - Updated
⚠️  dmini - 3 pending security updates

ISSUES DETECTED:

CRITICAL (Fix Immediately):
1. dmini - qBittorrent container stopped
   Action: ssh dmini "docker start qbittorrent"
   Impact: Downloads stopped, VPN exposure risk

2. dmini - 2 Docker containers down
   Containers: monitoring-exporter, backup-agent
   Action: ssh dmini "docker ps -a" to diagnose
   Impact: Monitoring blind spot, backup failures

ERROR (Fix Today):
3. dmini - Backup overdue by 4 hours
   Last: 28h ago (expected: 24h)
   Action: Check backup logs, restart if hung
   Impact: RPO extended, data at risk

WARNING (Fix This Week):
4. fmini - High memory usage (81%)
   Trend: +15% over 3 days
   Action: Investigate memory leaks (Ollama?)
   Impact: Risk of OOM killer

5. fmini - Ollama responding slowly (2.5s)
   Normal: <100ms
   Action: Check model size, restart Ollama
   Impact: Claude Code delays

6. dbook - Disk space at 78%
   Growth: +5% per week
   Action: Run cleanup (Docker images, logs)
   Impact: Risk of disk full in 4 weeks

7. dbook - MCP cache stale (8h old)
   Expected: <4h
   Action: Verify MCP sync service
   Impact: Outdated knowledge base

8. dmini - High SSH latency (280ms)
   Normal: <100ms
   Action: Check network, restart router
   Impact: Slow operations, poor UX

9. dmini - 3 pending security updates
   Action: ssh dmini "brew upgrade && brew update"
   Impact: Security vulnerabilities

RECOMMENDATIONS (Priority Order):
1. ⚡ IMMEDIATE: Restart qBittorrent on dmini
2. ⚡ IMMEDIATE: Restart 2 stopped containers on dmini
3. 🔥 TODAY: Investigate dmini backup failure
4. 🔥 TODAY: Investigate fmini high memory usage
5. 🔥 TODAY: Restart Ollama on fmini (resolve slow responses)
6. 📅 THIS WEEK: Clean up dbook disk space (target: <70%)
7. 📅 THIS WEEK: Verify MCP sync on dbook
8. 📅 THIS WEEK: Investigate dmini network latency
9. 📅 THIS WEEK: Apply security updates to dmini

SUMMARY:
Status: 🟡 DEGRADED
Issues: 2 critical, 1 error, 6 warnings
Compliance: 78%
Next check: 2026-02-05 16:45 (1 hour - frequent due to issues)

TREND (vs. previous check 24h ago):
- Critical issues: 0 → 2 (NEW ISSUES)
- Disk usage trend: +2% (fmini), +3% (dbook)
- Memory trend: +8% (fmini - concerning)
```

## Automation Options

### Scheduled Health Checks

**Daily via launchd** (`~/Library/LaunchAgents/com.fleet.health-check.plist`):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.fleet.health-check</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/d/projects/fleet-standards/scripts/fleet_health.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>10</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/d/.logs/fleet-health.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/d/.logs/fleet-health-error.log</string>
</dict>
</plist>
```

Load:
```bash
launchctl load ~/Library/LaunchAgents/com.fleet.health-check.plist
```

### On-Demand via Skill

```bash
# In Claude Code
User: "Run fleet health check"

# Agent invokes this skill
# Generates report
# Alerts if critical issues
```

### Pre-Deployment Check

```bash
# Before deploying to fmini
./scripts/fleet_health.sh --machine fmini --mode pre-deploy

# Checks:
# - Disk space available for deployment
# - Services responsive
# - No high load (deployment safe)
# - No pending reboots
```

### Integration with ntfy Alerts

```bash
# In fleet_health.sh
if [ "$critical_count" -gt 0 ]; then
    curl -H "Priority: urgent" \
         -H "Tags: warning" \
         -d "Fleet Health: $critical_count critical issues detected" \
         http://192.168.1.7:8090/fleet-alerts
fi
```

### Prometheus Integration

Export metrics for monitoring:
```bash
# fleet_health_exporter.sh
cat <<EOF > /tmp/fleet_health.prom
# HELP fleet_machine_up Machine SSH connectivity (1=up, 0=down)
# TYPE fleet_machine_up gauge
fleet_machine_up{machine="fmini"} 1
fleet_machine_up{machine="dbook"} 1
fleet_machine_up{machine="dmini"} 1
fleet_machine_up{machine="fbook"} 1

# HELP fleet_disk_usage_percent Disk usage percentage
# TYPE fleet_disk_usage_percent gauge
fleet_disk_usage_percent{machine="fmini"} 45
fleet_disk_usage_percent{machine="dbook"} 78
fleet_disk_usage_percent{machine="dmini"} 55
fleet_disk_usage_percent{machine="fbook"} 40
EOF

# Expose for Prometheus scraping
```

## Related Skills

- **fleet-ops**: Fleet operations and deployment
- **pre-commit**: Pre-deployment quality checks

## Related Commands

- `/fleet-sync` - Synchronize fleet configuration
- `/security-scan` - Security vulnerability scanning

## Related Documentation

- `knowledge-base/FLEET_ROLES.md` - Machine roles and responsibilities
- `knowledge-base/SERVICES.md` - Service management (launchd)
- `knowledge-base/PORT_ALLOCATION.md` - Port reservations
- `knowledge-base/REMOTE_ACCESS.md` - SSH and VPN setup

## Examples

### Example 1: Daily Automated Health Check

**Schedule**: Daily at 10:00 AM via launchd

**Agent workflow**:
1. Connects to all 4 machines
2. Collects system metrics (disk, memory, CPU, uptime)
3. Checks service status per machine
4. Generates health report
5. No issues detected (all healthy)
6. Logs report to `/Users/d/.logs/fleet-health.log`
7. Compliance: 100%

**Report**: See "Healthy Fleet Report" example above

**Action**: None required (all healthy)

### Example 2: Pre-Deployment Health Check

**User**: "Health check fmini before deploying LanceDB update"

**Agent workflow**:
1. Focuses health check on fmini specifically
2. Checks disk space (45% used, 120GB free) ✅
3. Checks current load (2.1, normal) ✅
4. Verifies LanceDB running and responsive ✅
5. Confirms no pending reboots ✅
6. Reports: All clear for deployment

**Result**: ✅ Deployment approved

### Example 3: Troubleshooting Connectivity Issue

**User**: "Can't connect to dmini services, run health check"

**Agent workflow**:
1. Runs connectivity tests
2. SSH to dmini succeeds but slow (280ms) ⚠️
3. Checks dmini services:
   - Docker: 10/12 containers running ❌
   - qBittorrent: Stopped ❌
   - Plex: Running ✅
4. Identifies root cause: qBittorrent and 2 containers down
5. Reports issue with remediation steps

**Report**: See "Degraded Fleet Report" example above

**Agent action**:
1. Restarts qBittorrent: `ssh dmini "docker start qbittorrent"`
2. Checks stopped containers: `ssh dmini "docker ps -a"`
3. Identifies: monitoring-exporter, backup-agent stopped
4. Restarts both containers
5. Re-runs health check: All services restored ✅

**Result**: Issue resolved, services restored

### Example 4: Quarterly Infrastructure Review

**User**: "Quarterly fleet health review (Q1 2026)"

**Agent workflow**:
1. Runs comprehensive health check on all machines
2. Collects 90 days of historical data (if available)
3. Analyzes trends:
   - Disk usage growth: dbook +15% over 3 months
   - Memory usage growth: fmini +20% over 3 months
   - Uptime stability: All machines stable
4. Identifies capacity planning needs:
   - dbook: Disk upgrade needed by Q3
   - fmini: Investigate memory growth trend
5. Generates quarterly report with recommendations

**Key findings**:
- Overall health: 95% (excellent)
- Disk growth: dbook requires attention (Q3 upgrade)
- Memory growth: fmini needs investigation (possible leak)
- Service uptime: 99.8% (target: 99%)
- Security compliance: 100% (all systems updated)

**Recommendations**:
1. Q2 Action: Investigate fmini memory growth (Ollama? LanceDB?)
2. Q3 Planning: Budget for dbook disk upgrade (1TB → 2TB)
3. Ongoing: Continue daily health checks
4. Improvement: Add Prometheus monitoring for trend analysis

### Example 5: Alert-Triggered Health Check

**Context**: ntfy alert received: "dmini high CPU load"

**Agent workflow**:
1. Receives alert via ntfy
2. Automatically triggers targeted health check on dmini
3. Collects detailed metrics:
   - CPU load: 3.8 (4 cores) - High but not critical
   - Top process: Plex transcoding (causing load)
   - Memory: 85% (high due to Plex)
   - Disk: 55% (normal)
4. Identifies cause: Plex actively transcoding multiple streams
5. Determines: Expected behavior, not an issue

**Report**:
```
dmini Targeted Health Check - 2026-02-05 14:22
==============================================

TRIGGER: ntfy alert - high CPU load

FINDINGS:
CPU Load: 3.8, 3.2, 2.1 (4 cores) - HIGH
Cause: Plex transcoding 3 simultaneous streams

Top Processes:
  Plex Media Server - 280% CPU (3 transcodes)
  Docker (qBittorrent) - 15% CPU
  System - 10% CPU

Memory: 27.2GB / 32GB (85%) - HIGH but expected
Disk: 55% - Normal

ASSESSMENT:
Status: ⚠️  HIGH LOAD - Expected behavior
Cause: Plex transcoding multiple 4K streams
Action: None required (normal operation)
```

**Result**: Alert acknowledged, no action needed (expected behavior)

### Example 6: Post-Incident Verification

**Context**: dmini experienced kernel panic and rebooted

**User**: "Verify dmini recovered from kernel panic"

**Agent workflow**:
1. Runs comprehensive health check on dmini
2. Checks uptime: 5 minutes (confirms recent reboot) ✅
3. Verifies all services started:
   - Docker: 12/12 containers running ✅
   - Plex: Accessible ✅
   - qBittorrent: Running with VPN ✅
   - Backup service: Running ✅
4. Checks system logs for panic cause
5. Verifies no data corruption
6. Reports: Full recovery confirmed

**Report**:
```
dmini Post-Incident Health Check - 2026-02-05 16:30
===================================================

INCIDENT: Kernel panic at 2026-02-05 16:20
RECOVERY: System rebooted, all services restored

VERIFICATION:
✅ System responsive (uptime: 10 minutes)
✅ All Docker containers running (12/12)
✅ Plex accessible and serving media
✅ qBittorrent running with VPN connected
✅ Backup service operational
✅ No filesystem corruption detected
✅ Network connectivity normal

LOGS REVIEW:
Panic cause: USB device disconnect during I/O
No data loss detected
All services auto-started via Docker

ASSESSMENT:
Status: 🟢 FULLY RECOVERED
Action: Monitor for 24h, no immediate action required
Recommendation: Review USB device stability
```

**Result**: ✅ Full recovery confirmed, monitoring continues

## Implementation Script

Basic implementation (`scripts/fleet_health.sh`):

```bash
#!/bin/bash
# Fleet health check script
# Usage: ./fleet_health.sh [--machine MACHINE] [--mode MODE]

set -euo pipefail

# Configuration
MACHINES=("fmini" "dbook" "dmini" "fbook")
TIMEOUT=10
REPORT_FILE="/tmp/fleet-health-$(date +%Y%m%d-%H%M%S).txt"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Functions
log_info() { echo -e "${GREEN}✅${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠️ ${NC} $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }

check_ssh() {
    local machine=$1
    local start=$(date +%s%3N)

    if ssh -o ConnectTimeout=$TIMEOUT "d@${machine}.local" "echo ok" &>/dev/null; then
        local end=$(date +%s%3N)
        local duration=$((end - start))
        log_info "$machine - SSH OK (${duration}ms)"
        return 0
    else
        log_error "$machine - SSH FAILED"
        return 1
    fi
}

check_disk() {
    local machine=$1
    local usage=$(ssh "d@${machine}.local" "df -h / | tail -1 | awk '{print \$5}' | tr -d '%'")
    local free=$(ssh "d@${machine}.local" "df -h / | tail -1 | awk '{print \$4}'")

    if [ "$usage" -lt 75 ]; then
        log_info "$machine - Disk ${usage}% used, ${free} free"
    elif [ "$usage" -lt 85 ]; then
        log_warn "$machine - Disk ${usage}% used (monitor)"
    else
        log_error "$machine - Disk ${usage}% used (critical)"
    fi
}

# Main execution
echo "Fleet Health Check - $(date)"
echo "========================================"

for machine in "${MACHINES[@]}"; do
    echo ""
    echo "Checking $machine..."
    check_ssh "$machine" || continue
    check_disk "$machine"
done

echo ""
echo "Report saved to: $REPORT_FILE"
```

## Thresholds and Alerting

### Resource Thresholds

| Metric | Warning | Error | Critical |
|--------|---------|-------|----------|
| Disk usage | >75% | >85% | >95% |
| Memory usage | >80% | >90% | >95% |
| CPU load | >cores | >2×cores | >4×cores |
| Swap usage | >0 | >1GB | >5GB |

### Alert Priorities

| Priority | Response Time | Notification |
|----------|---------------|--------------|
| Critical | Immediate | ntfy urgent |
| Error | <1 hour | ntfy high |
| Warning | <24 hours | Daily digest |
| Info | N/A | Log only |

---

**Version History**:
- v1.0.0 (2026-02-05): Initial skill creation
