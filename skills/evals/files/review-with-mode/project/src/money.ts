import { ValidationError } from "./errors.ts";

/** Converts a decimal amount such as "12.34" to whole cents, rounding half up. */
export function toCents(amount: string): number {
  const match = /^(\d+)(?:\.(\d{1,3}))?$/.exec(amount.trim());
  if (!match) throw new ValidationError(`invalid amount: ${amount}`);
  const [, whole, fraction = ""] = match;
  const thousandths = Number(whole) * 1000 + Number(fraction.padEnd(3, "0"));
  return Math.floor((thousandths + 5) / 10);
}

export function formatCents(cents: number): string {
  const sign = cents < 0 ? "-" : "";
  const abs = Math.abs(cents);
  return `${sign}${Math.floor(abs / 100)}.${String(abs % 100).padStart(2, "0")}`;
}
