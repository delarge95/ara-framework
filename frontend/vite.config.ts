import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true,
    host: true,
    hmr: {
      overlay: true,
    },
  },
  build: {
    outDir: "dist",
  },
  define: {
    __HMR_CONFIG_NAME__: JSON.stringify("ara-frontend"),
  },
});
