import React, { Fragment, useState, useRef, useEffect} from "react";
import { LinksData, type ImageData } from "../index";
import { useConfigUI } from "../../../../ChatUIContext";

export function ChatLinks({ data }: { data: LinksData }) {
  const { gitbookUrl, handleDocumentUrlChange } = useConfigUI();
  return (
    <div className="flex flex-col space-y-2">
      <strong style={{fontSize: '16px'}}>[[참고 링크]]</strong>
      <ul className="list-disc list-inside" style={{fontSize: '15px'}}>
      {
        data.map((link, index)=>{
          const target = link.url.startsWith(gitbookUrl) ? "gitbook" : "_blank"

          if (link.url?.startsWith(gitbookUrl)) {
            return (
              <li key={index}>
                <a
                  href={link.url}
                  className="italic hover:underline cursor-pointer"
                  onClick={(e) => handleDocumentUrlChange(e, link.url)}
                >{link.desc}</a>
              </li>
            )
          } else {
            return (
              <li key={index}>
                <a
                  href={link.url}
                  className="italic hover:underline cursor-pointer"
                  // target="_blank"
                  target={target}
                >{link.desc} ↗️</a>
              </li>
            )
          } 
        })
      }
      </ul>
    </div>
  );
}
