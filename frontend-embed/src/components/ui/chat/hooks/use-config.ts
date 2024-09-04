export interface ChatConfig {
  backend?: string;
}

function getBackendOrigin(): string {
  const chatAPI = window.socialbizChat.getBackendUrl();
  if (chatAPI) {
    return new URL(chatAPI).origin;
  } else {
    if (typeof window !== "undefined") {
      // Use BASE_URL from window.ENV
      return (window as any).ENV?.BASE_URL || "";
    }
    return "";
  }
}

export function useClientConfig(): ChatConfig {
  return {
    backend: getBackendOrigin(),
  };
}
