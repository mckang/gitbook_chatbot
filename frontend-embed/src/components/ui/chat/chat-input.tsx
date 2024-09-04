import { JSONValue } from "ai";
import { Button } from "../button";
import FileUploader from "../file-uploader";
import { Input } from "../input";
import { ChatHandler } from "./chat.interface";
import { useFile } from "./hooks/use-file";
import React from "react";
import { House } from "lucide-react";

const ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "csv", "pdf", "txt", "docx"];

export default function ChatInput(
  props: Pick<
    ChatHandler,
    | "isLoading"
    | "input"
    | "onFileUpload"
    | "onFileError"
    | "handleSubmit"
    | "handleInputChange"
    | "messages"
    | "setMessages"
    | "setInput"
    | "append"
  > & {
    requestParams?: any;
    setRequestData?: React.Dispatch<any>;
  },
) {
  const {
    imageUrl,
    setImageUrl,
    uploadFile,
    files,
    removeDoc,
    reset,
    getAnnotations,
  } = useFile();

  // default submit function does not handle including annotations in the message
  // so we need to use append function to submit new message with annotations
  const handleSubmitWithAnnotations = (
    e: React.FormEvent<HTMLFormElement>,
    annotations: JSONValue[] | undefined,
  ) => {
    e.preventDefault();
    props.append!({
      content: props.input,
      role: "user",
      createdAt: new Date(),
      annotations,
    });
    props.setInput!("");
  };

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    const annotations = getAnnotations();
    if (annotations.length) {
      handleSubmitWithAnnotations(e, annotations);
      return reset();
    }
    props.handleSubmit(e);
  };

  const handleUploadFile = async (file: File) => {
    if (imageUrl || files.length > 0) {
      alert("You can only upload one file at a time.");
      return;
    }
    try {
      await uploadFile(file, props.requestParams);
      props.onFileUpload?.(file);
    } catch (error: any) {
      const onFileUploadError = props.onFileError || window.alert;
      onFileUploadError(error.message);
    }
  };

  return (
    <form
      onSubmit={onSubmit}
      className="rounded-xl bg-white p-4 shadow-xl space-y-4 shrink-0"
    >
      <div className="flex w-full items-start justify-between gap-4 ">
        <Button type="button" disabled={props.isLoading} onClick={(e)=>{e.preventDefault(); props.setMessages([])}}>
          <House className="h-4 w-4"/>
        </Button>        
        <Input
          autoFocus
          name="message"
          placeholder="Type a message"
          className="flex-1"
          value={props.input}
          onChange={props.handleInputChange}
        />
        <Button type="submit" disabled={props.isLoading || !props.input.trim()}>
          Send message
        </Button>
      </div>
    </form>
  );
}
