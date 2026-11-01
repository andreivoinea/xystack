import { NotFoundError, ValidationError } from "../errors.ts";
import type { Response } from "../http.ts";

export function errorResponse(error: unknown): Response {
  if (error instanceof NotFoundError) return { status: 404, body: { error: error.message } };
  if (error instanceof ValidationError) return { status: 400, body: { error: error.message } };
  throw error;
}
