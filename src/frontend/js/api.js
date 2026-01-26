/**
 * Global Process ID: Generated ONCE per page load.
 * This links all actions a user takes on a specific screen visit.
 * Used for observability in the backend.
 */
const currentProcessId = self.crypto.randomUUID();
console.log("Session Process ID:", currentProcessId);

/**
 * Common Authenticated Fetch Wrapper
 * Automatically adds: Token, Process-ID, and Request-ID
 */
async function authFetch(url, options = {}) {
    const token = localStorage.getItem("token");

    if (!token) {
        console.warn("No token found, redirecting to login.");
        logout();
        return null;
    }

    // Generate a unique ID for THIS specific network request
    const requestId = self.crypto.randomUUID();

    const headers = {
        ...options.headers,
        "Authorization": `Bearer ${token}`,
        "X-Process-Id": currentProcessId, // Consistent for this page load
        "X-Request-Id": requestId         // Unique for this request
    };

    console.log(`[Req: ${requestId}] Sending request to ${url}...`);

    try {
        const response = await fetch(url, { ...options, headers });

        // Debug logging of server response ID
        const serverReqId = response.headers.get("X-Request-Id");
        console.log(`[Req: ${serverReqId || requestId}] Status: ${response.status}`);

        // Global Error Handling
        if (response.status === 401) {
            alert("Session expired. Please login again.");
            logout();
            return null;
        }
        if (response.status === 403) {
            alert("Permission Denied: Only Managers can perform this action.");
            return null;
        }

        return response;
    } catch (error) {
        console.error("Network error in authFetch:", error);
        alert("Network error occurred. Please try again.");
        return null;
    }
}

/**
 * Global Logout Function
 * Clears storage and redirects to login.
 */
function logout() {
    localStorage.clear();
    window.location.href = "/login.html";
}