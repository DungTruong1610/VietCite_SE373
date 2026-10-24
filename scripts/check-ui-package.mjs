#!/usr/bin/env node
// Verify the company UI package tarball is present and is the expected build.
// Usage: node scripts/check-ui-package.mjs   (exit 0 = OK, 1 = missing or wrong file)
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const EXPECTED_PACKAGES = [
  {
    file: "cnma-react-ui-1.1.4.tgz",
    sha256: "1c7926fc569a528ca12585b93607cbcb307f557bf1a1a9f8e7d2aa41ecf3bd1f",
  },
];

const packagesDir = join(dirname(fileURLToPath(import.meta.url)), "..", "packages");
let allOk = true;

for (const { file, sha256 } of EXPECTED_PACKAGES) {
  const path = join(packagesDir, file);
  if (!existsSync(path)) {
    console.error(`MISSING  packages/${file}: xin TV1 gửi file rồi đặt vào packages/ (xem packages/README.md)`);
    allOk = false;
    continue;
  }
  const actual = createHash("sha256").update(readFileSync(path)).digest("hex");
  if (actual !== sha256) {
    console.error(`MISMATCH packages/${file}: sha256 ${actual} khác bản mong đợi ${sha256}`);
    allOk = false;
    continue;
  }
  console.log(`OK       packages/${file}`);
}

process.exit(allOk ? 0 : 1);
