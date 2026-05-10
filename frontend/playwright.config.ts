import { defineConfig } from "@playwright/test";

const useExternalServers = process.env.PLAYWRIGHT_USE_EXTERNAL_SERVERS === "1";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 90_000,
  expect: {
    timeout: 15_000,
  },
  fullyParallel: false,
  workers: 1,
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL ?? "http://127.0.0.1:3100",
    trace: "retain-on-failure",
    headless: true,
  },
  webServer: useExternalServers
    ? undefined
    : [
        {
          command:
            "cd /home/admin2/smy/multi-media/backend && HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost DATABASE_URL=sqlite+pysqlite:////tmp/multi_media_playwright.db INTERNAL_API_KEY=playwright-internal-key GENERATION_AUTO_START_ENABLED=true ./.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8100",
          url: "http://127.0.0.1:8100/api/v1/health",
          reuseExistingServer: false,
          timeout: 120_000,
        },
        {
          command:
            "cd /home/admin2/smy/multi-media/frontend && HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8100/api/v1 INTERNAL_API_KEY=playwright-internal-key npm run dev -- --hostname 127.0.0.1 --port 3100",
          url: "http://127.0.0.1:3100",
          reuseExistingServer: false,
          timeout: 120_000,
        },
      ],
  projects: [
    {
      name: "chromium",
      use: {
        browserName: "chromium",
      },
    },
  ],
});
