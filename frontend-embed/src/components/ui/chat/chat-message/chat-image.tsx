import React, { useState, useRef, useEffect} from "react";
import { type ImageData } from "../index";

export function ChatImage({ data }: { data: ImageData }) {
  return (
    <div className="rounded-md max-w-[200px] shadow-md">
      <img
        src={data.url}
        width={0}
        height={0}
        sizes="100vw"
        style={{ width: "100%", height: "auto" }}
        alt=""
      />
    </div>
  );
}
