import Image from "next/image";
import { LinksData, type ImageData } from "../index";
import { useConfigUI } from "@/app/hooks/ChatContext";

export function ChatLinks({ data }: { data: LinksData }) {
  const { handleDocumentUrlChange } = useConfigUI();


  return (
    <div className="flex flex-col space-y-2">
      <strong>[[참고 링크]]</strong>
      <ul className="list-disc list-inside">
      {
        data.map((link, index)=>{
          const target = link.url.startsWith(process.env.NEXT_PUBLIC_GITBOOK_URL+"") ? "gitbook" : "_blank"

          if (link.url?.startsWith(process.env.NEXT_PUBLIC_GITBOOK_URL+"")) {
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
                >{link.desc}</a>
              </li>
            )
          }          
        })
      }
      </ul>
    </div>
  );
}
