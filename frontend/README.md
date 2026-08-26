# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.


# Step to run the project//
/Users/shaurya/Desktop/deepfake
1. Open Terminal and go to the project
cd ~/Desktop/deepfake
2. Run your Flask backend
python3 app.py
You should see:
Running on http://127.0.0.1:5000
Keep this Terminal window running. Don't close it.
3. Open a second Terminal window for the frontend
cd ~/Desktop/deepfake/frontend
Then:
npm run dev
You'll get something like:
Local: http://localhost:5173/
Open that address in your browser.