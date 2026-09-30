const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";


export async function sendMessage(
  conversationId,
  message
) {
  const response = await fetch(
    `${API_BASE_URL}/api/chat`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        conversation_id: conversationId,
        message: message,
      }),
    }
  );

  if (!response.ok) {

    let errorMessage =
      `Request failed with status ${response.status}`;

    try {

      const errorData =
        await response.json();

      if (errorData.detail) {
        errorMessage =
          errorData.detail;
      }

    } catch {
      // Keep default error.
    }

    throw new Error(errorMessage);
  }

  const data =
    await response.json();

  return data.response;
}


export async function checkBackend() {

  try {

    const response =
      await fetch(
        `${API_BASE_URL}/health`
      );

    return response.ok;

  } catch {

    return false;
  }
}