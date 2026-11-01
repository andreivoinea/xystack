import * as db from "../db.ts";
import { NotFoundError, ValidationError } from "../errors.ts";
import { toCents } from "../money.ts";

/** Returns the order if it belongs to the user. Other users' orders look missing. */
export function getOrderForUser(orderId: string, userId: string): db.Order {
  const order = db.findOrder(orderId);
  if (!order || order.userId !== userId) throw new NotFoundError(`order ${orderId}`);
  return order;
}

export function listOrdersForUser(userId: string): db.Order[] {
  return db.listOrdersByUser(userId);
}

export function applyDiscount(orderId: string, userId: string, amount: string): db.Order {
  const order = getOrderForUser(orderId, userId);
  if (order.status !== "pending") throw new ValidationError("only pending orders can be discounted");
  const discountCents = toCents(amount);
  if (discountCents > order.totalCents) throw new ValidationError("discount exceeds order total");
  const updated = { ...order, totalCents: order.totalCents - discountCents };
  db.updateOrder(updated);
  return updated;
}
