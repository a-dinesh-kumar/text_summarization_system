const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000")
  .replace(/\/+$/, "");

export async function checkBackendHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) {
    throw new Error(`Backend health check failed (${response.status}).`);
  }
  return response.json();
}

export async function requestSummary({ text, file }) {
  const formData = new FormData();

  if (file) {
    formData.append("file", file);
  } else {
    formData.append("text", text);
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}/api/v1/summarize`, {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error(
      "Could not connect to the backend. Make sure the FastAPI Docker container is running."
    );
  }

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    const detail = payload.detail;
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg || "Invalid input").join(", ")
      : detail || `Request failed with status ${response.status}.`;
    throw new Error(message);
  }

  return payload;
}
