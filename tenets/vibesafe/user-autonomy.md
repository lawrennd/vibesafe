---
id: "user-autonomy"
title: "User Autonomy Over Prescription"
status: "Active"
created: "2025-05-05"
last_reviewed: "2026-01-03"
review_frequency: "Annual"
conflicts_with: ["simplicity-of-use"]
tags:
  - design
  - philosophy
  - user-experience
---

## Tenet: user-autonomy

**Title**: User Autonomy Over Prescription

**Description**: We provide tools and frameworks that respect users' freedom to make their own architectural and implementation choices. We avoid making decisions that restrict users unnecessarily. When designing solutions, we build flexibility in from the start rather than imposing our preferred approach.

**Quote**: *"We optimize for configurability over our own preferences."*

**Examples**:
- The gist integration system (CIP-0003) provides multiple implementation options and a flexible architecture
- The installation system offers both minimal shell scripts and more feature-rich Python implementations
- Configuration files allow customization of default behaviors

**Counter-examples**:
- Forcing users to adopt a rigid directory structure with no configuration options
- Hardcoding assumptions about development environments
- Requiring specific tools or platforms without alternatives

**Conflicts**:
- Can conflict with "Simplicity at the Point of Use" when too many options create complexity
- Resolution: Provide sensible defaults while allowing configuration

**Version**: 1.0 (2025-05-05) 