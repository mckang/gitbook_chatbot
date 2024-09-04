import React, { Fragment, useState, useRef, useEffect} from "react";
import { ChatHandler, SuggestedQuestionsData } from "..";

export function SuggestedQuestions({
  questions,
  append,
}: {
  questions: SuggestedQuestionsData;
  append: Pick<ChatHandler, "append">["append"];
}) {
  const [showQuestions, setShowQuestions] = useState(questions.length > 0);

  return (
    showQuestions &&
    append !== undefined && (
      <div className="flex flex-col space-y-2">
        <strong style={{fontSize: '16px'}}>[[추가 질문]]</strong>
        {questions.map((question, index) => (
          <a
            key={index}
            onClick={() => {
              append({ role: "user", content: question });
              setShowQuestions(false);
            }}
            className="text-sm italic hover:underline cursor-pointer"
          >
            {"->"} {question}
          </a>
        ))}
      </div>
    )
  );
}
