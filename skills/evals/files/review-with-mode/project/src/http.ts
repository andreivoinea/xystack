export interface Request {
  /** Set by the auth middleware from the session cookie, never from client input. */
  userId: string;
  params: Record<string, string | undefined>;
  query: Record<string, string | undefined>;
  body: Record<string, string | undefined>;
}

export interface Response {
  status: number;
  body?: unknown;
}

export type Handler = (request: Request) => Response;
