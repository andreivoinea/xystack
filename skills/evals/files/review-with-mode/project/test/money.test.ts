import assert from "node:assert/strict";
import { test } from "node:test";
import { formatCents, toCents } from "../src/money.ts";

test("toCents rounds half up without floating-point error", () => {
  assert.equal(toCents("0.285"), 29);
  assert.equal(toCents("12.34"), 1234);
  assert.equal(toCents("7"), 700);
});

test("toCents rejects malformed amounts", () => {
  assert.throws(() => toCents("1,50"));
  assert.throws(() => toCents("-3"));
});

test("formatCents pads cents", () => {
  assert.equal(formatCents(1205), "12.05");
  assert.equal(formatCents(-5), "-0.05");
});
