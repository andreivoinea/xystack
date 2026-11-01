// Storage in a JSON file. Only modules under src/services/ may import this file.
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

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

interface Data {
  orders: Order[];
  refunds: Refund[];
}

function dataFile(): string {
  return process.env.ORDERS_DB ?? "data/orders.json";
}

function load(): Data {
  const file = dataFile();
  if (!existsSync(file)) return { orders: [], refunds: [] };
  return JSON.parse(readFileSync(file, "utf8")) as Data;
}

function save(data: Data): void {
  const file = dataFile();
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`);
}

export function insertOrder(order: Order): void {
  const data = load();
  data.orders = data.orders.filter((existing) => existing.id !== order.id);
  data.orders.push(order);
  save(data);
}

export function findOrder(id: string): Order | undefined {
  return load().orders.find((order) => order.id === id);
}

export function updateOrder(order: Order): void {
  const data = load();
  const index = data.orders.findIndex((existing) => existing.id === order.id);
  if (index === -1) throw new Error(`no order ${order.id}`);
  data.orders[index] = order;
  save(data);
}

export function listOrdersByUser(userId: string): Order[] {
  return load()
    .orders.filter((order) => order.userId === userId)
    .sort((a, b) => b.createdAt.localeCompare(a.createdAt));
}

export function insertRefund(refund: Refund): void {
  const data = load();
  data.refunds.push(refund);
  save(data);
}

export function listRefunds(orderId: string): Refund[] {
  return load().refunds.filter((refund) => refund.orderId === orderId);
}

export function reset(): void {
  rmSync(dataFile(), { force: true });
}
