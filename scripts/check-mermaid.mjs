import { execFileSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import { JSDOM } from "jsdom";

const dom = new JSDOM("<!doctype html><html><body></body></html>");
globalThis.window = dom.window;
globalThis.document = dom.window.document;
const { default: mermaid } = await import("mermaid");

const files = execFileSync("rg", [
  "--files",
  "--hidden",
  "-g",
  "*.md",
  "-g",
  "!.git/**",
  "-g",
  "!node_modules/**",
  "-g",
  "!target/**",
], {
  encoding: "utf8",
}).trim().split("\n").filter(Boolean).sort();

const openingFence = /^ {0,3}```mermaid[ \t]*$/i;
const closingFence = /^ {0,3}```[ \t]*$/;
const blocks = [];
let failures = 0;

for (const file of files) {
  const lines = (await readFile(file, "utf8")).split(/\r?\n/);
  let content = [];
  let startLine = 0;
  let inBlock = false;

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    if (!inBlock && openingFence.test(line)) {
      startLine = index + 1;
      content = [];
      inBlock = true;
      continue;
    }
    if (inBlock && closingFence.test(line)) {
      blocks.push({ file, startLine, source: content.join("\n") });
      content = [];
      inBlock = false;
      startLine = 0;
      continue;
    }
    if (inBlock) {
      content.push(line);
    }
  }

  if (inBlock) {
    failures += 1;
    console.error(`FAIL: ${file}:${startLine}: unterminated mermaid fence`);
  }
}

mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });

for (const [index, block] of blocks.entries()) {
  try {
    await mermaid.parse(block.source, { suppressErrors: false });
  } catch (error) {
    failures += 1;
    const message = error instanceof Error ? error.message : String(error);
    console.error(`FAIL: ${block.file}:${block.startLine} (block ${index + 1}): ${message}`);
  }
}

if (failures > 0) {
  console.error(`FAILED: ${failures} of ${blocks.length} mermaid block(s) did not parse. Fix and re-run.`);
  process.exitCode = 1;
} else {
  console.log(`OK: ${blocks.length} mermaid block(s) parse successfully.`);
}
