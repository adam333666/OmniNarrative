import { expect, type Page } from "@playwright/test";

export async function createGenerationThroughUi(page: Page, themeText: string, audienceText: string, customStyleText: string) {
  await page.goto("/create");

  await expect(page.getByLabel("输入你的创意主题")).toBeVisible();
  await page.getByLabel("输入你的创意主题").fill(themeText);
  await page.getByRole("button", { name: "下一步" }).click();
  await page.getByRole("button", { name: "下一步" }).click();
  await page.getByRole("button", { name: "下一步" }).click();

  await page.getByLabel("输入目标受众描述").fill(audienceText);
  await page.getByRole("button", { name: "下一步" }).click();
  await page.getByLabel("可选：补充更细的风格说明").fill(customStyleText);
  await page.locator("form").evaluate((form) => {
    (form as HTMLFormElement).requestSubmit();
  });

  await expect(page).toHaveURL(/\/generating\/gen_/);
  await expect(page.getByText("内容方案正在成形")).toBeVisible();

  await page.waitForURL(/\/result\/gen_/, { timeout: 60_000 });
  await expect(page.getByText("导出动作")).toBeVisible({ timeout: 60_000 });

  const generationId = page.url().split("/").at(-1);
  if (!generationId) {
    throw new Error("generation id missing from result page url");
  }

  return generationId;
}
