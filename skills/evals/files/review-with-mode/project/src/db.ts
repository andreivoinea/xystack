// In-memory storage. Only modules under src/services/ may import this file.

export type OrderStatus = "pending" | "paid" | "refunded";

export interface Order {
  id: string;
  userId: string;
  totalCents: number;
  status: OrderStatus;
  createdAt: string;
}

export interface Refund {
  orderId: string;
  amountCents: number;
  createdAt: string;
}

const orders = new Map<string, Order>();
const refunds: Refund[] = [];

export function insertOrder(order: Order): void {
  orders.set(order.id, { ...order });
}

export function findOrder(id: string): Order | undefined {
  const order = orders.get(id);
  return order && { ...order };
}

export function updateOrder(order: Order): void {
  if (!orders.has(order.id)) throw new Error(`no order ${order.id}`);
  orders.set(order.id, { ...order });
}

export function listOrdersByUser(userId: string): Order[] {
  return [...orders.values()]
    .filter((order) => order.userId === userId)
    .sort((a, b) => b.createdAt.localeCompare(a.createdAt))
    .map((order) => ({ ...order }));
}

export function insertRefund(refund: Refund): void {
  refunds.push({ ...refund });
}

export function listRefunds(orderId: string): Refund[] {
  return refunds.filter((refund) => refund.orderId === orderId).map((refund) => ({ ...refund }));
}

export function reset(): void {
  orders.clear();
  refunds.length = 0;
}
