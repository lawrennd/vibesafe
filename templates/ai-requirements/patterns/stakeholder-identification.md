# Stakeholder Identification Pattern

## Purpose

This conversation pattern helps identify all relevant stakeholders for a software project and understand their needs, priorities, and influence. Proper stakeholder identification is essential for gathering comprehensive requirements and ensuring the project meets the needs of all affected parties.

## Pattern Structure

The stakeholder identification conversation follows this general pattern:

1. *Direct Users*: Identify who will directly interact with the system
2. *Indirect Users*: Identify who will be affected by the system without directly using it
3. *Decision Makers*: Identify who has authority over the project's scope, budget, and priorities
4. *Domain Experts*: Identify who has specialized knowledge relevant to the problem domain
5. *System Integrators*: Identify who will need to connect with or maintain the system
6. *Regulators/Compliance*: Identify relevant regulatory or compliance stakeholders
7. *Stakeholder Analysis*: Analyze each stakeholder's influence, interest, and priority

## Example Questions

### Direct Users

* "Who will be the primary day-to-day users of this system?"
* "Are there different types of users with different access levels or permissions?"
* "How technically sophisticated are the intended users?"
* "What is the users' familiarity with similar systems?"

### Indirect Users

* "Who will receive outputs from the system without directly using it?"
* "Whose workflows might be affected by this system?"
* "Are there stakeholders who need to be informed about the system's operations?"
* "Who might benefit from or be impacted by the data collected by the system?"

### Decision Makers

* "Who has budget authority for this project?"
* "Who can approve changes to the project scope?"
* "Who will sign off on the final deliverables?"
* "Who is ultimately accountable for the project's success?"

### Domain Experts

* "Who has specialized knowledge about the problem we're trying to solve?"
* "Who understands the current processes most thoroughly?"
* "Who can provide insights about industry best practices?"
* "Who can validate that our solution will work in the real world?"

### System Integrators

* "What other systems will this need to integrate with?"
* "Who maintains those systems?"
* "Who will be responsible for deploying and maintaining this system?"
* "Are there third-party vendors or partners we need to consider?"

### Regulators/Compliance

* "Are there regulatory requirements that apply to this system?"
* "Who is responsible for ensuring compliance?"
* "Are there audit or reporting requirements to consider?"
* "Are there security or privacy stakeholders to consult?"

## Stakeholder Analysis Matrix

After identifying stakeholders, create a matrix to analyze their relationship to the project:

| Stakeholder | Role | Interest Level | Influence Level | Priority | Key Concerns | Communication Channel |
|-------------|------|---------------|-----------------|----------|--------------|------------------------|
| [Name] | [Role] | High/Medium/Low | High/Medium/Low | High/Medium/Low | [Main concerns] | [How to reach them] |

## Integration with Requirements Process

Use the stakeholder analysis to:

1. *Prioritize requirements gathering* efforts based on stakeholder influence and interest
2. *Identify potential conflicts* between stakeholder needs
3. *Develop personas* based on direct user stakeholders
4. *Plan validation strategies* with appropriate stakeholders
5. *Design communication plans* for different stakeholder groups

## Example

See `/ai-requirements/examples/healthcare-app-stakeholders.md` for a complete example of stakeholder identification for a healthcare application.

## Common Pitfalls

* *Missing indirect stakeholders*: Often overlooked but can be crucial for adoption
* *Over-focusing on technical users*: Missing non-technical stakeholders' perspectives
* *Treating all stakeholders equally*: Not prioritizing based on influence and interest
* *Static stakeholder analysis*: Not updating the analysis as the project evolves
* *Assuming homogeneous user groups*: Not identifying different user personas within a stakeholder group 