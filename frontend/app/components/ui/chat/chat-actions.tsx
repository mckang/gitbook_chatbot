import { PauseCircle } from "lucide-react";

import { Button } from "../button";
import { ChatHandler } from "./chat.interface";

import { UserFeedbackComponent } from "./user-feedback";

export default function ChatActions(
  props: Pick<ChatHandler, "messages" | "stop" | "reload"> & {
    showReload?: boolean;
    showStop?: boolean;
  },
) {
  if (!props.showStop && props.showReload) {
    // console.log("messages",props.messages[props.messages.length-2])
    // console.log("messages",props.messages[props.messages.length-1])
  }
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
          <UserFeedbackComponent
            question={props.messages[props.messages.length - 2]}
            answer={props.messages[props.messages.length - 1]}
            reload={props.reload}
          />
        </>
      )}
    </div>
  );
}
