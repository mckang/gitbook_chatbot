import { User2, BotMessageSquare } from "lucide-react";
import React, { useState, useRef, useEffect} from "react";

export default function ChatAvatar({ role }: { role: string }) {
  if (role === "user") {
    return (
      <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border bg-background shadow">
        <User2 className="h-4 w-4" />
      </div>
    );
  }

  return (
    <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border bg-black text-white shadow">
      <BotMessageSquare className="h-4 w-4"/>
      {/* <img
        className="rounded-md"
        src="/llama.png"
        alt="Llama Logo"
        width={24}
        height={24}
        // priority
      /> */}
    </div>
  );
}
