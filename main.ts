#!/usr/bin/env node
/**
 * Sunday 22 November 2026 — The World in One Page
 *
 * make.fun bounty "news-image-20261122": sum up 22 November's world news
 * in one image. The image itself is entry.png, drawn by tools/render.py
 * (Python + Pillow, original flat vector art, no photos). This program is
 * the entrypoint the harness runs: it places entry.png at
 * $MAKEFUN_OUTPUT_DIR/entry.png.
 *
 * Node 22, standard library only. No network, no dependencies.
 */

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const buildDossier = {
  title: "Sunday 22 November 2026 — The World in One Page",
  competition: "news-image-20261122",
  image: "entry.png",
  size: [1024, 1024],
  stories: 35,
  regions: 7,
  renderer: "tools/render.py (Python + Pillow, original vector art)",
  deterministic: true,
};

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const source = join(here, "entry.png");
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  console.error("entry.png is missing; render it first with: python3 tools/render.py");
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`wrote ${target} — ${buildDossier.title}`);
