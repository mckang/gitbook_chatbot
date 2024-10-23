import { PauseCircle, RefreshCw } from "lucide-react";

import { Button } from "../button";
import { ChatHandler } from "./chat.interface";
import React from "react";
import { UserFeedbackComponent } from "./chat-message/user-feedback";
export default function ChatActions(
  props: Pick<ChatHandler, "messages" | "stop" | "reload"> & {
    showReload?: boolean;
    showStop?: boolean;
  },
) {
  return (
    <div className="space-x-4">
      {props.showStop && (
        <Button variant="outline" size="sm" onClick={props.stop}>
          <PauseCircle className="mr-2 h-4 w-4" />
          Stop generating
        </Button>
      )}
      {props.showReload && (
        <>
        <UserFeedbackComponent question={props.messages[props.messages.length-2]} answer={props.messages[props.messages.length-1]} reload={props.reload}/>
        </>
      )}
    </div>
  );
}
