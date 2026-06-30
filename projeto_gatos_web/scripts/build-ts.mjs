import { mkdir, readFile, writeFile } from "node:fs/promises";
import { watch } from "node:fs";
import { dirname, resolve } from "node:path";
import { stripTypeScriptTypes } from "node:module";

const source = resolve("src/app.ts");
const output = resolve("public/app.js");

async function build() {
  const ts = await readFile(source, "utf8");
  const js = stripTypeScriptTypes(ts, { mode: "strip" });

  await mkdir(dirname(output), { recursive: true });
  await writeFile(output, js, "utf8");
  console.log(`built ${output}`);
}

await build();

if (process.argv.includes("--watch")) {
  console.log("watching src/app.ts");
  watch(source, async () => {
    try {
      await build();
    } catch (error) {
      console.error(error);
    }
  });
}
