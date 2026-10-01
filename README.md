# Charlie Kirk - Docusaurus Site

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Node.js** (version 18.0 or higher)
- **npm** or **yarn** (package manager)
- **Git** (version control system)

### Installing Prerequisites

**Windows:**
- Download Node.js from [nodejs.org](https://nodejs.org/)
- Download Git from [git-scm.com](https://git-scm.com/download/win)

**macOS:**
```bash
# Using Homebrew
brew install node
brew install git
```

**Linux (Ubuntu/Debian):**
```bash
# Update package list
sudo apt update

# Install Node.js and npm
sudo apt install nodejs npm

# Install Git
sudo apt install git
```

**Linux (Fedora/RHEL):**
```bash
# Install Node.js and npm
sudo dnf install nodejs npm

# Install Git
sudo dnf install git
```

## Cloning the Repository

### All Platforms (Windows, macOS, Linux)

Open your terminal (or Command Prompt/PowerShell on Windows) and run:

```bash
# Clone the repository
git clone <repository-url>

# Navigate into the project directory
cd charlie-kirk
```

Replace `<repository-url>` with the actual URL of your Git repository (e.g., `https://github.com/username/charlie-kirk.git`).

### Alternative: Clone with SSH

If you have SSH keys set up with your Git provider:

```bash
git clone git@github.com:username/charlie-kirk.git
cd charlie-kirk
```

## Initializing the Project

After cloning the repository, install the project dependencies:

### Using npm:

```bash
npm install
```

### Using yarn:

```bash
yarn install
```

This will install all required packages listed in `package.json`.

## Local Development

Start the local development server:

### Using npm:

```bash
npm start
```

### Using yarn:

```bash
yarn start
```

This command starts a local development server (typically at `http://localhost:3000`) and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

Generate static content for production:

### Using npm:

```bash
npm run build
```

### Using yarn:

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Git Commands Reference

### Essential Git Commands

**Check repository status:**
```bash
git status
```

**Pull latest changes from remote:**
```bash
# Pull from the current branch
git pull

# Pull from a specific branch
git pull origin main
```

**Add changes to staging:**
```bash
# Add specific file
git add filename.ext

# Add all changes
git add .

# Add all changes in a specific directory
git add src/
```

**Commit changes:**
```bash
# Commit with a message
git commit -m "Your descriptive commit message"

# Add and commit in one command
git commit -am "Your commit message"
```

**Push changes to remote:**
```bash
# Push to current branch
git push

# Push to a specific branch
git push origin main

# Push and set upstream
git push -u origin branch-name
```

**View commit history:**
```bash
# View full history
git log

# View condensed history
git log --oneline

# View last 5 commits
git log -5
```

**Create and switch branches:**
```bash
# Create a new branch
git branch branch-name

# Switch to a branch
git checkout branch-name

# Create and switch in one command
git checkout -b branch-name

# Switch branches (modern way)
git switch branch-name

# Create and switch (modern way)
git switch -c branch-name
```

**View remote repositories:**
```bash
git remote -v
```

**Discard local changes:**
```bash
# Discard changes in a specific file
git checkout -- filename.ext

# Discard all local changes
git reset --hard

# Discard uncommitted changes but keep new files
git reset --hard HEAD
```

**Stash changes (temporarily save work):**
```bash
# Stash current changes
git stash

# List all stashes
git stash list

# Apply most recent stash
git stash apply

# Apply and remove most recent stash
git stash pop
```

### Typical Workflow

1. **Before starting work:**
   ```bash
   git pull origin main
   ```

2. **Make your changes** in the code editor

3. **Check what changed:**
   ```bash
   git status
   git diff
   ```

4. **Stage and commit:**
   ```bash
   git add .
   git commit -m "Describe what you changed"
   ```

5. **Push to remote:**
   ```bash
   git push origin main
   ```

## Deployment

### GitHub Pages

**Using SSH:**
```bash
USE_SSH=true yarn deploy
```

**Not using SSH:**
```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub Pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## Troubleshooting

### Common Issues

**Port already in use:**
If port 3000 is already in use, you can specify a different port:
```bash
npm start -- --port 3001
```

**Node version issues:**
Check your Node.js version:
```bash
node --version
```
Ensure it's version 18.0 or higher.

**Permission errors (Linux/macOS):**
If you encounter permission errors, avoid using `sudo` with npm. Instead, configure npm to use a different directory:
```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

## Additional Resources

- [Docusaurus Documentation](https://docusaurus.io/docs)
- [Git Documentation](https://git-scm.com/doc)
- [Node.js Documentation](https://nodejs.org/docs/)

## License

See the LICENSE file for details.
