import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:5000"
});

// Track when login happens to prevent immediate token clearing
let lastLoginTime = 0;
const LOGIN_GRACE_PERIOD = 2000; // 2 seconds grace period after login

// ===============================
// REQUEST INTERCEPTOR (FIXED)
// ===============================
API.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");

        // 🚫 Do NOT attach JWT to auth routes
        const isAuthRoute = config.url && config.url.startsWith("/auth");

        // Ensure headers object exists
        if (!config.headers) {
            config.headers = {};
        }

        // Set Content-Type for POST/PUT requests if not already set
        if ((config.method === "post" || config.method === "put" || config.method === "patch") 
            && !config.headers["Content-Type"]) {
            config.headers["Content-Type"] = "application/json";
        }

        // Attach JWT ONLY for protected routes
        if (token && !isAuthRoute) {
            config.headers["Authorization"] = `Bearer ${token}`;
            console.log(
                "[API REQUEST]",
                config.method?.toUpperCase(),
                config.url,
                "✓ JWT ATTACHED",
                "Token preview:",
                token.substring(0, 20) + "..."
            );
        } else {
            console.log(
                "[API REQUEST]",
                config.method?.toUpperCase(),
                config.url,
                isAuthRoute ? "✓ Auth route (no JWT)" : "✗ No token found",
                "Token in storage:",
                token ? "YES" : "NO"
            );
        }

        return config;
    },
    (error) => Promise.reject(error)
);

// ===============================
// RESPONSE INTERCEPTOR
// Handle 401 errors by clearing token and redirecting to login
// ===============================
API.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            const status = error.response.status;
            const msg = error.response.data?.error || "";
            const url = error.config?.url || "";

            console.warn(
                "[API ERROR]",
                error.config?.method?.toUpperCase(),
                url,
                "STATUS:",
                status,
                "MESSAGE:",
                msg
            );

            // Handle 401 Unauthorized errors (invalid/expired token)
            // Don't clear token on auth routes (login/signup failures are expected)
            const isAuthRoute = url.startsWith("/auth");
            const timeSinceLogin = Date.now() - lastLoginTime;
            const isWithinGracePeriod = timeSinceLogin < LOGIN_GRACE_PERIOD;
            
            if (status === 401 && !isAuthRoute) {
                if (isWithinGracePeriod) {
                    console.warn(`[AUTH] 401 error within ${timeSinceLogin}ms of login, might be race condition. Not clearing token yet.`);
                    console.warn("[AUTH] URL:", url, "Time since login:", timeSinceLogin, "ms");
                } else {
                    console.warn("[AUTH] Invalid token detected on protected route, clearing token");
                    console.warn("[AUTH] URL:", url, "isAuthRoute:", isAuthRoute);
                    localStorage.removeItem("token");
                    
                    // Dispatch custom event to notify App component to update auth state
                    window.dispatchEvent(new CustomEvent("auth:logout", { 
                        detail: { reason: msg || "Invalid token" } 
                    }));
                }
            } else if (status === 401 && isAuthRoute) {
                console.log("[AUTH] 401 on auth route (expected for invalid credentials), not clearing token");
            }
        }

        // Let callers (components) decide how to handle other errors
        return Promise.reject(error);
    }
);

// ===============================
// AUTH
// ===============================
export const signup = (username, password, emergencyName, emergencyPhone) =>
    API.post("/auth/signup", { 
        username, 
        password, 
        emergency_contact_name: emergencyName, 
        emergency_contact_phone: emergencyPhone 
    });

export const login = (username, password) => {
    lastLoginTime = Date.now();
    return API.post("/auth/login", { username, password });
};

// ===============================
// JOURNAL APIs (JWT REQUIRED)
// ===============================
export const submitJournal = (text) =>
    API.post("/journal", { text });

export const fetchJournals = () =>
    API.get("/journal");

export const fetchWeeklyTrends = () =>
    API.get("/journal/weekly");

export const fetchWeeklyMeanEmotion = () =>
    API.get("/journal/weekly/mean");

export const fetchJournalByDate = (date) =>
    API.get(`/journal/by-date?date=${date}`);

export const fetchReflectMetrics = () =>
    API.get("/journal/metrics");

export const triggerEmergencySMS = () =>
    API.post("/journal/trigger_sms_alert");

export default API;
