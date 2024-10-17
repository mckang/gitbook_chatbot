import { Message } from "ai";
import {
  CheckCircle,
  RefreshCw,
  ThumbsDown,
  ThumbsUp,
  XCircle,
} from "lucide-react";
import { useState } from "react";
import { Button } from "../button";
import { ChatHandler } from "./chat.interface";
import { useClientConfig } from "./hooks/use-config";

export function UserFeedbackComponent(
  props: Pick<ChatHandler, "reload"> & {
    question: Message;
    answer: Message;
    comment: string;
  },
) {
  const [feedback, setFeedback] = useState<string | null>(null); // null, 'good', 'bad'
  const [isModalOpen, setIsModalOpen] = useState(false); // Modal visibility
  const [comment, setComment] = useState(""); // Store user's comment
  const { backend } = useClientConfig();

  const handleUserFeedback = async (value: string) => {
    setFeedback(value);
    setIsModalOpen(true);
  };

  const sendFeedback = async (
    score: string,
    question: Message,
    answer: Message,
    comment: string,
  ): Promise<void> => {
    try {
      const response = await fetch(`${backend}/api/chat/score`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          score: score,
          question: question,
          answer: answer,
          comment: comment,
        }),
      });
      if (!response.ok) {
        throw new Error("Failed to send feedback");
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleSubmitComment = async () => {
    await sendFeedback(feedback, props.question, props.answer, comment);
    setIsModalOpen(false); // 모달 닫기
  };

  const handleCancel = async () => {
    await sendFeedback(feedback, props.question, props.answer);
    setIsModalOpen(false); // 모달 닫기
  };

  return (
    <div className="flex flex-col items-center">
      <div className="flex justify-between w-full max-w-md">
        <div className="flex gap-2  ml-auto">
          {feedback === null || feedback === "good" ? (
            <Button
              onClick={() => handleUserFeedback("good")}
              size="sm"
              disabled={feedback !== null}
              className={`transition-transform bg-transparent p-2 rounded-full hover:bg-green-100 ${feedback === "good" ? "scale-125" : ""} ${feedback !== null ? "cursor-not-allowed" : "cursor-pointer"}`}
              aria-label="Thumbs Up"
            >
              <ThumbsUp color={feedback === "good" ? "green" : "black"} />
            </Button>
          ) : null}
          {feedback === null || feedback === "bad" ? (
            <Button
              onClick={() => handleUserFeedback("bad")}
              size="sm"
              disabled={feedback !== null}
              className={`transition-transform bg-transparent p-2 rounded-full hover:bg-red-100 ${feedback === "bad" ? "scale-125" : ""} ${feedback !== null ? "cursor-not-allowed" : "cursor-pointer"}`}
              aria-label="Thumbs Down"
            >
              <ThumbsDown color={feedback === "bad" ? "red" : "black"} />
            </Button>
          ) : null}
          <Button
            size="sm"
            onClick={props.reload}
            className="bg-transparent  hover:bg-gray-100 cursor-pointer"
          >
            <RefreshCw color="black" />
          </Button>
        </div>
      </div>
      {isModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <h2 className="w-full text-left border-b border-gray-300 font-bold mt-2">
              의견을 남겨주세요
            </h2>
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="여기에 의견을 남겨주세요"
              className="w-full p-2 border rounded mt-1 text-sm"
              rows={1}
            />
            <div className="flex justify-end gap-0 p-0 m-0">
              <Button
                onClick={handleSubmitComment}
                className={`transition-transform bg-transparent p-3 rounded-full hover:bg-green-100`}
              >
                <CheckCircle color="black" />
              </Button>
              <Button
                onClick={handleCancel}
                className={`transition-transform bg-transparent p-3 rounded-full hover:bg-red-100`}
              >
                <XCircle color="black" />
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
