# VibeSafe Update Script

The VibeSafe Update Script is a tool that allows you to easily check for and add missing components to your VibeSafe installation. This ensures that you always have the latest features, tools, and improvements.

## Usage

```bash
./vibesafe-update [OPTIONS]
```

## Options

- `--check`: Only check for missing components without installing them
- `--force`: Force update of all components even if already installed
- `--version`: Show version information
- `--workspace PATH`: Path to the VibeSafe workspace directory (default: current directory)

## Examples

### Check for missing components

```bash
./vibesafe-update --check
```

This will display a list of all VibeSafe components and whether they are installed or missing.

### Update missing components

```bash
./vibesafe-update
```

This will install any missing components in your VibeSafe installation.

### Force update all components

```bash
./vibesafe-update --force
```

This will reinstall all components, even if they are already present.

## Components

The Update Script currently manages the following components:

1. **What's Next Script**: A script that provides an overview of project status and recommends next steps
2. **YAML Frontmatter Scripts**: Scripts to add YAML frontmatter to CIP and backlog files

## How It Works

The Update Script follows these steps:

1. Detects the current state of your VibeSafe installation
2. Identifies which components are missing
3. Installs any missing components
4. Provides feedback on what has been updated

## Adding to an Existing Installation

If you already have VibeSafe installed but don't have the Update Script, you can add it manually:

1. Download the `vibesafe_update.py` script from the repository and place it in your `scripts/` directory
2. Download the `vibesafe-update` wrapper script and place it in your VibeSafe root directory
3. Make the wrapper script executable: `chmod +x vibesafe-update`

## Development

The Update Script is designed to be extensible. New components can be added by:

1. Creating a new class that extends the `Component` base class
2. Implementing the `is_installed` and `install` methods
3. Adding the new component to the `get_components()` function

## Troubleshooting

If you encounter issues with the Update Script:

1. **Script fails to run**: Ensure you have Python 3.6+ installed
2. **Component installation fails**: Check the error message for details
3. **Script doesn't recognize your VibeSafe workspace**: Ensure you have the basic VibeSafe directory structure (cip/ and backlog/ directories)

For more help, please open an issue in the VibeSafe repository. 