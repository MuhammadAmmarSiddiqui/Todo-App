# Quickstart Guide: UI Upgrade

## Prerequisites
- Node.js v18+ installed
- npm or yarn package manager
- Access to design mockups (home.png, signin.png, register.png, dashboard.png)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd full-stack-todo-web-app
   git checkout 001-ui-upgrade  # Feature branch for UI upgrade
   ```

2. **Install dependencies**
   ```bash
   # Navigate to frontend directory
   cd frontend
   
   # Install dependencies including Tailwind CSS and Shadcn UI
   npm install
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   
   # Install Shadcn UI components
   npm install @radix-ui/react-slot class-variance-authority clsx tailwind-merge
   ```

3. **Configure Tailwind CSS**
   ```bash
   # Create Tailwind config file
   npx tailwindcss init
   ```
   
   Update `tailwind.config.js`:
   ```js
   /** @type {import('tailwindcss').Config} */
   module.exports = {
     content: [
       "./pages/**/*.{js,ts,jsx,tsx}",
       "./components/**/*.{js,ts,jsx,tsx}",
     ],
     theme: {
       extend: {},
     },
     plugins: [],
   }
   ```

4. **Add Tailwind directives to CSS**
   Update `frontend/src/styles/globals.css`:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

5. **Implementation Steps**
   - Examine the design mockups (home.png, signin.png, register.png, dashboard.png) in the root folder
   - Create new UI components using Shadcn UI library following the design specifications
   - Update the existing pages (index.jsx, login.jsx, register.jsx, dashboard.jsx) to use the new components
   - Ensure responsive design works across all screen sizes (320px to 2560px)
   - Test that all functionality remains intact after UI changes

6. **Running the Application**
   ```bash
   # From the frontend directory
   npm run dev
   ```

## Testing
- Verify all UI elements match the design mockups
- Test responsiveness on different screen sizes
- Ensure all existing functionality works as before
- Run existing test suite to confirm no regressions