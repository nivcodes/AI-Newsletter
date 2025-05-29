#!/bin/bash
"""
Shell wrapper for AI Newsletter Scheduler
Handles environment setup and execution for launchd
"""

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/run_newsletter.log"
PYTHON_SCRIPT="$SCRIPT_DIR/newsletter_scheduler.py"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Function to log with timestamp
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to check if Python script exists
check_script() {
    if [ ! -f "$PYTHON_SCRIPT" ]; then
        log_message "ERROR: Newsletter scheduler script not found at $PYTHON_SCRIPT"
        exit 1
    fi
}

# Function to find Python executable
find_python() {
    # Try different Python executables in order of preference
    for python_cmd in python3 python /usr/bin/python3 /usr/local/bin/python3; do
        if command -v "$python_cmd" >/dev/null 2>&1; then
            echo "$python_cmd"
            return 0
        fi
    done
    
    log_message "ERROR: No Python executable found"
    exit 1
}

# Function to check Python dependencies
check_dependencies() {
    local python_cmd="$1"
    
    log_message "Checking Python dependencies..."
    
    # Check if required modules are available
    required_modules=("holidays" "smtplib" "email" "pathlib" "datetime")
    
    for module in "${required_modules[@]}"; do
        if ! "$python_cmd" -c "import $module" 2>/dev/null; then
            log_message "WARNING: Python module '$module' not found"
        fi
    done
}

# Function to set up environment
setup_environment() {
    # Change to script directory
    cd "$SCRIPT_DIR" || {
        log_message "ERROR: Cannot change to script directory: $SCRIPT_DIR"
        exit 1
    }
    
    # Set Python path to include current directory
    export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
    
    # Load environment variables if .env exists
    if [ -f "$SCRIPT_DIR/.env" ]; then
        log_message "Loading environment variables from .env"
        set -a  # automatically export all variables
        source "$SCRIPT_DIR/.env"
        set +a
    else
        log_message "WARNING: .env file not found at $SCRIPT_DIR/.env"
    fi
}

# Function to run the newsletter scheduler
run_scheduler() {
    local python_cmd="$1"
    
    log_message "Starting AI Newsletter Scheduler..."
    log_message "Python executable: $python_cmd"
    log_message "Working directory: $(pwd)"
    log_message "Script path: $PYTHON_SCRIPT"
    
    # Run the Python scheduler with output capture
    if "$python_cmd" "$PYTHON_SCRIPT" 2>&1 | tee -a "$LOG_FILE"; then
        local exit_code=${PIPESTATUS[0]}
        if [ $exit_code -eq 0 ]; then
            log_message "✅ Newsletter scheduler completed successfully"
            return 0
        else
            log_message "❌ Newsletter scheduler failed with exit code: $exit_code"
            return $exit_code
        fi
    else
        log_message "❌ Failed to execute newsletter scheduler"
        return 1
    fi
}

# Function to handle cleanup
cleanup() {
    log_message "Cleaning up..."
    
    # Remove old log files (keep last 30 days)
    find "$LOG_DIR" -name "*.log" -type f -mtime +30 -delete 2>/dev/null || true
    
    log_message "Cleanup completed"
}

# Function to send error notification (fallback)
send_error_notification() {
    local error_message="$1"
    
    # Try to send a simple error notification using the Python script
    if [ -f "$PYTHON_SCRIPT" ]; then
        python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
try:
    from newsletter_scheduler import send_admin_notification
    send_admin_notification('Shell Script Error', '''$error_message''', is_success=False)
except Exception as e:
    print(f'Failed to send error notification: {e}')
" 2>/dev/null || true
    fi
}

# Main execution
main() {
    log_message "=== AI Newsletter Scheduler Shell Wrapper Started ==="
    
    # Trap errors and cleanup
    trap 'cleanup; exit 1' ERR
    trap 'cleanup; exit 0' EXIT
    
    # Check if script exists
    check_script
    
    # Find Python executable
    PYTHON_CMD=$(find_python)
    log_message "Found Python executable: $PYTHON_CMD"
    
    # Set up environment
    setup_environment
    
    # Check dependencies
    check_dependencies "$PYTHON_CMD"
    
    # Run the scheduler
    if run_scheduler "$PYTHON_CMD"; then
        log_message "=== Newsletter scheduler completed successfully ==="
        exit 0
    else
        local error_msg="Newsletter scheduler failed. Check logs at $LOG_FILE"
        log_message "=== $error_msg ==="
        send_error_notification "$error_msg"
        exit 1
    fi
}

# Handle command line arguments
case "${1:-}" in
    --test)
        log_message "Running in test mode..."
        PYTHON_CMD=$(find_python)
        setup_environment
        "$PYTHON_CMD" "$PYTHON_SCRIPT" --test
        ;;
    --force)
        log_message "Running in force mode..."
        PYTHON_CMD=$(find_python)
        setup_environment
        "$PYTHON_CMD" "$PYTHON_SCRIPT" --force
        ;;
    --dry-run)
        log_message "Running in dry-run mode..."
        PYTHON_CMD=$(find_python)
        setup_environment
        "$PYTHON_CMD" "$PYTHON_SCRIPT" --dry-run
        ;;
    --help|-h)
        echo "AI Newsletter Scheduler Shell Wrapper"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --test      Test configuration"
        echo "  --force     Force run regardless of schedule"
        echo "  --dry-run   Generate newsletter without sending"
        echo "  --help      Show this help message"
        echo ""
        echo "Logs are written to: $LOG_FILE"
        ;;
    "")
        # Normal execution
        main
        ;;
    *)
        echo "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac
