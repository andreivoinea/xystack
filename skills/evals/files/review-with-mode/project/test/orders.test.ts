import assert from "node:assert/strict";
import { beforeEach, test } from "node:test";
import * as db from "../src/db.ts";
import { handleDiscount, handleGetOrder } from "../src/handlers/orders.ts";
import { request, seedOrder } from "./helpers.ts";

beforeEach(() => db.reset());

test("users can't see other users' orders", () => {
  seedOrder();
  assert.equal(handleGetOrder(request({ userId: "mallory", params: { id: "o1" } })).status, 404);
});

test("discount lowers the total", () => {
  seedOrder();
  const response = handleDiscount(request({ params: { id: "o1" }, body: { amount: "10.50" } }));
  assert.equal(response.status, 200);
  assert.equal(db.findOrder("o1")?.totalCents, 3950);
});

test("discount can't exceed the total", () => {
  seedOrder();
  assert.equal(handleDiscount(request({ params: { id: "o1" }, body: { amount: "51" } })).status, 400);
});
