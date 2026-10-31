/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        orbit: {
          bg: '#07090E',
          sidebar: '#080C14',
          card: '#0D111C',
          cardHover: '#111625',
          border: '#182030',
          borderLight: '#222D44',
          cyan: '#00F2FE',
          cyanMuted: '#06B6D4',
          teal: '#14B8A6',
          textBright: '#F8FAFC',
          textMuted: '#94A3B8',
          textDim: '#64748B',
        },
        research: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        },
        navy: {
          800: '#111b2b',
          900: '#0a101d',
          950: '#060a12',
        },
        accent: {
          blue: '#2563eb',
          cyan: '#06b6d4',
          amber: '#f59e0b',
          emerald: '#10b981',
          rose: '#f43f5e',
        }
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'Fira Code', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
