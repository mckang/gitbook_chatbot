import { Langfuse, LangfuseWeb } from "langfuse";
import { NextRequest, NextResponse } from "next/server";
import { v4 as uuidv4 } from "uuid";

const langfuseWeb = new LangfuseWeb({
  publicKey: process.env.NEXT_LANGFUSE_PUBLIC_KEY,
  baseUrl: process.env.NEXT_LANGFUSE_HOST,
});
const langfuse = new Langfuse({
  publicKey: process.env.NEXT_LANGFUSE_PUBLIC_KEY,
  secretKey: process.env.NEXT_LANGFUSE_SECRET_KEY,
  baseUrl: process.env.NEXT_LANGFUSE_HOST,
});

export async function POST(req: NextRequest) {
  const message = await req.json();
  //   console.log('Received feedback:', score, question, answer);
  const traceId = uuidv4();

  await langfuse.trace({
    id: traceId,
    input: message.question,
    output: message.answer,
  });
  await langfuseWeb.score({
    traceId: traceId,
    name: "user_feedback",
    value: message.score,
    comment: message.comment,
  });

  return NextResponse.json({ message: "Feedback received" });
}

export const runtime = "edge";
