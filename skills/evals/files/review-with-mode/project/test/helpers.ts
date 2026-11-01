import * as db from "../src/db.ts";
import type { Request } from "../src/http.ts";

export function seedOrder(overrides: Partial<db.Order> = {}): db.Order {
  const order: db.Order = {
    id: "o1",
    userId: "alice",
    totalCents: 5000,
    status: "pending",
    createdAt: "2026-01-01T00:00:00Z",
    ...overrides,
  };
  db.insertOrder(order);
  return order;
}

export function request(overrides: Partial<Request> = {}): Request {
  return { userId: "alice", params: {}, query: {}, body: {}, ...overrides };
}
