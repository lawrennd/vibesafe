# Example: Web Application Requirements Discovery

This document demonstrates a requirements discovery conversation using the AI-Requirements framework.

## Initial User Request

```
# Requirements Discovery Conversation

## Project Context

I'm looking to create a project management web application for small teams (5-15 people). 

The main goals of this project are:
1. Simplify task tracking and assignment for remote teams
2. Provide clear visibility into project progress
3. Integrate with common tools like email and calendar systems

I anticipate this software will be used by small businesses and startup teams who need to coordinate work without complex enterprise tools.

## Current Situation

Currently, these teams are using a mix of spreadsheets, email, and messaging apps to track work. 

The main challenges or pain points are:
1. Information is scattered across different tools
2. It's hard to see who's responsible for what
3. Deadlines are missed because there's no centralized reminder system
4. New team members struggle to get up to speed on project status

## Initial Requirements

I think the software should:
1. Allow creation and assignment of tasks with deadlines
2. Show a dashboard of project progress and upcoming deadlines
3. Send notifications for approaching deadlines
4. Provide a simple way to upload and share files related to tasks
5. Have a mobile-friendly interface for on-the-go updates

## Constraints and Assumptions

Some important constraints to consider:
1. The budget is limited - we need to build an MVP within 3 months
2. Users may have varying levels of technical sophistication
3. The system needs to work well on both desktop and mobile devices

I'm making these assumptions:
1. Users will have reliable internet access
2. Most users are comfortable with basic web interfaces
3. Email is a universally acceptable notification method

## Questions

I'm particularly unsure about:
1. What's the most intuitive way to present project progress?
2. How much customization should we allow in the initial version?
3. Should we prioritize mobile apps or focus on a responsive web interface?

Can you help me explore these requirements further and identify what I might be missing?
```

## AI Response

Based on your requirements for a project management web application for small teams, I'll help explore these further and identify potential gaps.

### Requirements Analysis

Your goals and initial requirements provide a good foundation. Let's expand on them and identify additional considerations:

#### Core Functionality Considerations

*Task Management*:
- Will tasks need subtasks or nested structures?
- How will task dependencies be handled?
- What task states are needed beyond "to do" and "done"? (e.g., blocked, in progress, in review)
- Will you need time tracking capabilities?

*Dashboard/Visibility*:
- Consider different views: calendar view, kanban board, list view, timeline/Gantt view
- Filtering and sorting capabilities will be important
- Role-based visibility (what can different team members see?)

*Notifications*:
- Beyond deadline reminders, what other notifications would be valuable?
- Notification preferences: email, in-app, browser push notifications
- Frequency options to prevent notification fatigue

*File Sharing*:
- File size limitations
- Version control for documents
- Preview capabilities for common file types
- Permission management for sensitive files

*Additional Considerations*:
- Search functionality across tasks and files
- Reporting capabilities for completed work
- Templates for recurring tasks or projects
- Activity logs to see who changed what

#### User Experience Considerations

*Onboarding Experience*:
- How will new users learn the system?
- What sample data or templates can help users get started?
- What help documentation will be provided?

*Collaboration Features*:
- Will users need to comment on tasks?
- Should there be @mention capabilities to tag specific users?
- How will team discussions be facilitated?

*Integration Needs*:
- Specific calendar systems for integration (Google, Outlook, etc.)
- Email integration details
- Any other tools the teams commonly use (Slack, Google Drive, etc.)

### Addressing Your Specific Questions

*1. What's the most intuitive way to present project progress?*

For small teams, consider a multi-view approach:
- A high-level dashboard showing key metrics (tasks by status, upcoming deadlines)
- A kanban board for visual workflow management
- A calendar view for deadline-centric planning
- A simple list view for quick scanning

The MVP could start with two key views (dashboard + one task management view) with others added based on user feedback.

*2. How much customization should we allow in the initial version?*

For an MVP with a tight timeline, I recommend:
- Essential customizations: task statuses, basic project/team settings
- Limited but intentional color/label systems
- Configurable notifications
- User-level display preferences

Defer complex customizations like custom fields, workflow rules, and advanced permissions to future versions.

*3. Should we prioritize mobile apps or focus on a responsive web interface?*

Given your constraints:
- Start with a responsive web interface that works well on both desktop and mobile browsers
- This gives you the broadest reach without the overhead of maintaining native apps
- Focus on core mobile use cases: checking tasks, quick updates, and receiving notifications
- Consider native apps in a future phase based on user feedback

### Additional Stakeholders to Consider

- *Team Leaders*: Need visibility into team workload and progress
- *Project Sponsors*: May need high-level views without daily interaction
- *IT Support*: If deployed in organizations with IT departments
- *External Collaborators*: Occasional users who may need limited access

### Potential MVP Scope

Based on the 3-month timeline and budget constraints, here's a suggested MVP scope:

*Must-Have*:
- Task creation, assignment, and deadline management
- Basic dashboard with project status
- Email notifications for deadlines
- Responsive web interface
- File attachments for tasks
- User management and basic permissions

*Should-Have* (if time permits):
- Kanban and list views
- Basic reporting
- Task commenting
- @mentions for team members
- Task templates

*Future Enhancements* (post-MVP):
- Time tracking
- Native mobile apps
- Advanced customization
- Integration with additional tools
- Advanced reporting
- Guest/client access portal

### Next Steps

1. *Prioritize requirements* based on this expanded list
2. *Create user personas* for the different types of users
3. *Map user journeys* for common scenarios
4. *Define key metrics* for measuring project success
5. *Start detailing specific features* using the requirements refinement template

Would you like to explore any particular aspect of these requirements in more detail? 