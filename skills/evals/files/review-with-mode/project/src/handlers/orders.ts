import type { Request, Response } from "../http.ts";
import { formatCents } from "../money.ts";
import * as orders from "../services/orders.ts";
import { errorResponse } from "./errors.ts";

export function handleGetOrder(request: Request): Response {
  try {
    const order = orders.getOrderForUser(request.params.id ?? "", request.userId);
    return { status: 200, body: { ...order, total: formatCents(order.totalCents) } };
  } catch (error) {
    return errorResponse(error);
  }
}

export function handleDiscount(request: Request): Response {
  try {
    const order = orders.applyDiscount(request.params.id ?? "", request.userId, request.body.amount ?? "");
    return { status: 200, body: { ...order, total: formatCents(order.totalCents) } };
  } catch (error) {
    return errorResponse(error);
  }
}
