import { expect, test } from "@playwright/test";

import { createGenerationThroughUi } from "./helpers/generation-flow";

test("browser can inspect exports and internal console details after generation", async ({ page, request }) => {
  const generationId = await createGenerationThroughUi(
    page,
    "我想做一个关于黑洞时间膨胀的内容",
    "20到30岁，喜欢科学设定和强解释链的观众",
    "希望解释感更强，但不要太学术",
  );

  const jsonResponse = await request.get(`http://127.0.0.1:8100/api/v1/creations/${generationId}/export/json`);
  expect(jsonResponse.ok()).toBeTruthy();
  const jsonPayload = await jsonResponse.json();
  expect(jsonPayload.export_meta.generation_id).toBe(generationId);

  const markdownResponse = await request.get(`http://127.0.0.1:8100/api/v1/creations/${generationId}/export/md`);
  expect(markdownResponse.ok()).toBeTruthy();
  const markdownText = await markdownResponse.text();
  expect(markdownText).toContain("主标题");

  const videoPayloadResponse = await request.get(`http://127.0.0.1:8100/api/v1/creations/${generationId}/video-payload`);
  expect(videoPayloadResponse.ok()).toBeTruthy();
  const videoPayload = await videoPayloadResponse.json();
  expect(videoPayload.video_meta.platform).toBeTruthy();
  expect(Array.isArray(videoPayload.storyboard_frames)).toBeTruthy();

  await page.goto(`/internal/checkpoints/${generationId}`);
  await expect(page.getByText("执行状态与最近事件")).toBeVisible();
  await expect(page.getByText("最新状态快照")).toBeVisible();
  await expect(page.getByText("Checkpoint 列表")).toBeVisible();
});
