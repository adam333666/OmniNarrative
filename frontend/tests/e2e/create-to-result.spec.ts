import { expect, test } from "@playwright/test";
import { createGenerationThroughUi } from "./helpers/generation-flow";

test("browser can complete create -> generating -> result -> internal tools flow", async ({ page }) => {
  const generationId = await createGenerationThroughUi(
    page,
    "我想做一个关于时间旅行悖论的内容",
    "18到28岁，喜欢科幻设定和逻辑推理的观众",
    "保持一点烧脑感",
  );

  await page.goto(`/internal/checkpoints/${generationId}`);
  await expect(page.getByRole("heading", { level: 1, name: `Checkpoint · ${generationId}` })).toBeVisible();

  await page.goto("/internal/trends");
  await expect(page.getByRole("heading", { level: 1, name: "趋势控制台" })).toBeVisible();
});
