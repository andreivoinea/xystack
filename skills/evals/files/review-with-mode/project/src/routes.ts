import { handleDiscount, handleGetOrder } from "./handlers/orders.ts";
import type { Handler } from "./http.ts";

export const routes: Record<string, Handler> = {
  "GET /orders/:id": handleGetOrder,
  "POST /orders/:id/discount": handleDiscount,
};
