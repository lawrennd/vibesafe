
# VibeSafe Project Backlog System

> **Note**: This file provides context to AI coding assistants (Cursor, Claude Code, GitHub Copilot, etc.).  
> The content is standard markdown and works with any AI assistant that can read project files.

## What is the Backlog System?

The Backlog System is a structured approach to tracking tasks, issues, and improvements that need to be implemented in the Lynguine project. The backlog serves as:

1. *Task management* for organizing and prioritizing work items
2. *Documentation* of planned features and improvements
3. *Project planning* tool for coordinating work across the team
4. *Historical record* of completed and abandoned tasks

## When to Use the Backlog System

Add items to the backlog when:

- You identify a bug that doesn't need immediate fixing
- You have an idea for a new feature or enhancement
- You discover technical debt that should be addressed
- You need to track documentation improvements
- You want to propose infrastructure changes

## Backlog Directory Structure

The `backlog/` directory contains all task files and follows this structure:

```
backlog/
├── README.md                 # Overview of the backlog system
├── task_template.md          # Template for creating new tasks
├── index.md                  # Auto-generated index of all tasks
├── update_index.py           # Script to maintain the index
├── documentation/            # Documentation-related tasks
├── infrastructure/           # Infrastructure-related tasks
├── features/                 # Feature-related tasks
└── bugs/                     # Bug-related tasks
```

## VibeSafe File Classification

**⚠️ IMPORTANT: VibeSafe System vs User Files**

When working with VibeSafe projects, be aware of the distinction between system files and user content:

### 🔧 VibeSafe System Files (Don't commit these unless updating VibeSafe itself)
- `backlog/README.md` - System documentation 
- `backlog/task_template.md` - Template file
- `backlog/update_index.py` - Index generation script
- `backlog/index.md` - Auto-generated index (updates frequently)
- `.cursor/rules/*` - Cursor AI rules (all files)
- `scripts/whats_next.py` - Status script
- `install-whats-next.sh` - Installation script
- `whats-next` - Wrapper script

### 📝 User Content (Always commit these)
- `backlog/features/*.md` - User-created feature tasks
- `backlog/bugs/*.md` - User-created bug tasks  
- `backlog/documentation/*.md` - User-created documentation tasks
- `backlog/infrastructure/*.md` - User-created infrastructure tasks
- Any task files following the `YYYY-MM-DD_description.md` pattern

**Tip**: Focus on committing your actual work (tasks you create) rather than VibeSafe infrastructure files.

## Task Naming Convention

Task files follow one of these naming conventions:

1. `YYYY-MM-DD_short-description.md` (e.g., `2025-05-05_readthedocs-setup.md`)
2. `YYYYMMDD-short-description.md` (e.g., `20250505-readthedocs-setup.md`)

The date-based naming ensures uniqueness and provides a chronological reference.

## Using the Template

To create a new task:

1. Copy the `task_template.md` file to the appropriate category directory
2. Name the file according to the convention (using today's date)
3. Fill out all required sections following the template structure
4. Run the `update_index.py` script to update the index

Example:
```bash
# Copy the template to the appropriate category
cp backlog/task_template.md backlog/features/2023-06-15_search-functionality.md

# Edit the new task
vim backlog/features/2023-06-15_search-functionality.md

# Update the index
python backlog/update_index.py
```

## Using the Backlog System Effectively

Follow these guidelines to make the most of the backlog system:

### 1. Categorize Appropriately

*Rule*: Place tasks in the correct category directory to help with organization.

```
✅ documentation/ for documentation tasks
✅ infrastructure/ for deployment, CI/CD, and system architecture tasks
✅ features/ for new functionality
✅ bugs/ for defect tracking
```

### 2. Status Workflow

*Rule*: Follow the standard status workflow for tasks.

```
Proposed → Ready → In Progress → Completed/Abandoned
```

- *Proposed*: Initial idea or concept
- *Ready*: Fully described and ready for implementation
- *In Progress*: Currently being worked on
- *Completed*: Successfully implemented
- *Abandoned*: Will not be implemented (with explanation)

### 3. Priority Levels

*Rule*: Assign appropriate priority levels to tasks.

```
- High: Critical tasks that should be addressed soon
- Medium: Important tasks that should be addressed in the near future
- Low: Nice-to-have tasks that can be addressed when time permits
```

### 4. Unique Identifiers

*Rule*: Each task should have a unique identifier based on the creation date.

```
✅ 2025-05-05_search-functionality
✅ 2025-05-16_lynguine-compatibility
❌ search-functionality
```

### 5. Update Task Status

*Rule*: Keep the task status up-to-date as implementation progresses.

```
## Progress Updates

### 2025-05-04
Task created with Proposed status.

### 2025-05-20
Updated to Ready status after refining the requirements.

### 2025-06-25
Changed to In Progress as implementation has started.
```

### 6. Integration with GitHub

*Rule*: Link backlog tasks to GitHub issues when applicable.

```
- **GitHub Issue**: #42
```

### 7. Integration with CIPs

*Rule*: Create backlog tasks only when a CIP is **Accepted**, not when it's Proposed.

**Workflow**:
- **CIP Proposed** → Design and discussion phase, no backlog tasks yet
- **CIP Accepted** → Break down into specific backlog tasks for implementation
- **Backlog tasks** → Link back to the CIP they implement

```
✅ CIP-0012: Accepted → Create backlog tasks for each phase
❌ CIP-0012: Proposed → Wait for acceptance before creating tasks

## Related

- CIP: 0002
```

**Why?** Don't create implementation tasks until the design is approved. This avoids wasted effort if the CIP changes or is rejected.

## Task Template Structure

Each task should include these sections:

1. *Title* - Task title (e.g., `# Task: Implement User Authentication`)
2. *Metadata* - ID, title, status, priority, dates, owner, and dependencies
3. *Description* - Detailed description of the task
4. *Acceptance Criteria* - Clear criteria for when the task is complete
5. *Implementation Notes* - Technical approach or considerations
6. *Related* - Links to CIPs, PRs, or documentation
7. *Progress Updates* - Chronological updates on task progress

The template file (`task_template.md`) contains placeholders for all these sections.

## Benefits of Following the Backlog System

- *Improved organization* of project work items
- *Better visibility* into project progress and priorities
- *Clearer communication* about what needs to be done
- *Historical tracking* of completed and abandoned tasks
- *Integration* with CIPs and GitHub issues
- *Categorization* for easier management of different types of tasks
