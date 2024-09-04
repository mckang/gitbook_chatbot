import React, { Fragment, useState, useRef, useEffect} from "react";
import { LinksData, type ImageData } from "../index";

export function ChatLinks({ data }: { data: LinksData }) {
  console.log(data)
  return (
    <div className="flex flex-col space-y-2">
      <strong style={{fontSize: '16px'}}>[[참고 링크]]</strong>
      <ul className="list-disc list-inside">
      {
        data.map((link, index)=>{
          const target = link.url.startsWith(process.env.NEXT_PUBLIC_GITBOOK_URL+"") ? "gitbook" : "_blank"
          return (
            <li key={index} style={{fontSize: '15px'}}>
              <a
                href={link.url}
                className="bold italic hover:underline cursor-pointer"
                // target="_blank"
                target={target}
              >{link.desc}</a>
            </li>
          )
        })
      }
      </ul>
    </div>
  );
}
