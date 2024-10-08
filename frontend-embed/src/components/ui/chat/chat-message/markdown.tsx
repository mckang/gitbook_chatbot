import "katex/dist/katex.min.css";
import React, { FC, memo } from "react";
import ReactMarkdown, { Options } from "react-markdown";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";

import { SourceData } from "..";
import { CodeBlock } from "./codeblock";

const MemoizedReactMarkdown: FC<Options> = memo(
  ReactMarkdown,
  (prevProps, nextProps) =>
    prevProps.children === nextProps.children &&
    prevProps.className === nextProps.className,
);

const preprocessLaTeX = (content: string) => {
  // Replace block-level LaTeX delimiters \[ \] with $$ $$
  const blockProcessedContent = content.replace(
    /\\\[([\s\S]*?)\\\]/g,
    (_, equation) => `$$${equation}$$`,
  );
  // Replace inline LaTeX delimiters \( \) with $ $
  const inlineProcessedContent = blockProcessedContent.replace(
    /\\\[([\s\S]*?)\\\]/g,
    (_, equation) => `$${equation}$`,
  );
  return inlineProcessedContent;
};

const preprocessMedia = (content: string) => {
  // Remove `sandbox:` from the beginning of the URL
  // to fix OpenAI's models issue appending `sandbox:` to the relative URL
  return content.replace(/(sandbox|attachment|snt):/g, "");
};

/**
 * Update the citation flag [citation:id]() to the new format [citation:index](url)
 */
const preprocessCitations = (content: string, sources?: SourceData) => {
  if (sources) {
    const citationRegex = /\[citation:(.+?)\]\(\)/g;
    let match;
    // Find all the citation references in the content
    while ((match = citationRegex.exec(content)) !== null) {
      const citationId = match[1];
      // Find the source node with the id equal to the citation-id, also get the index of the source node
      const sourceNode = sources.nodes.find((node) => node.id === citationId);
      // If the source node is found, replace the citation reference with the new format
      if (sourceNode !== undefined) {
        content = content.replace(
          match[0],
          `[citation:${sources.nodes.indexOf(sourceNode)}]()`,
        );
      } else {
        // If the source node is not found, remove the citation reference
        content = content.replace(match[0], "");
      }
    }
  }
  return content;
};

const preprocessContent = (content: string, sources?: SourceData) => {
  return preprocessCitations(
    preprocessMedia(preprocessLaTeX(content)),
    sources,
  );
};

export default function Markdown({
  content,
  sources,
}: {
  content: string;
  sources?: SourceData;
}) {
  const processedContent = preprocessContent(content, sources);
  // console.log(processedContent)
  return (
    <MemoizedReactMarkdown
      className="prose dark:prose-invert prose-p:leading-relaxed prose-pre:p-0 break-words custom-markdown"
      remarkPlugins={[remarkGfm, remarkMath]}
      rehypePlugins={[rehypeKatex as any]}
      components={{
        p({ children }) {
          return <p className="mb-2 last:mb-0">{children}</p>;
        },
        code({ node, inline, className, children, ...props }) {
          if (children.length) {
            if (children[0] == "▍") {
              return (
                <span className="mt-1 animate-pulse cursor-default">▍</span>
              );
            }

            children[0] = (children[0] as string).replace("`▍`", "▍");
          }

          const match = /language-(\w+)/.exec(className || "");

          if (inline) {
            return (
              <code className={className} {...props}>
                {children}
              </code>
            );
          }

          return (
            <CodeBlock
              key={Math.random()}
              language={(match && match[1]) || ""}
              value={String(children).replace(/\n$/, "")}
              {...props}
            />
          );
        },
        a({ href, children }) {
          const target = "_blank"

          return <a href={href} className="bold italic hover:underline cursor-pointer" target={target}>{children}</a>;
        },
      }}
    >
      {processedContent}
    </MemoizedReactMarkdown>
  );
}
