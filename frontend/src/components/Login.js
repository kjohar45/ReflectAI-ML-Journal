import { useState } from "react";
import { login } from "../services/api";

function Login({ onLogin, onSwitchToSignup }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e) => {
        e?.preventDefault(); // Prevent form submission if called from form
        setError("");
        
        if (!username.trim() || !password.trim()) {
            setError("Please enter both username and password");
            return;
        }

        try {
            // 🔥 CLEAR any stale token first
            localStorage.removeItem("token");

            console.log("Attempting login for user:", username);
            const res = await login(username, password);
            console.log("Login response:", res);
            
            const token = res.data?.access_token;
            
            if (!token) {
                console.error("No token in response:", res.data);
                setError("No token received from server");
                return;
            }
            
            console.log("Login successful, storing token:", token.substring(0, 20) + "...");
            localStorage.setItem("token", token);
            
            // Verify token was stored
            const storedToken = localStorage.getItem("token");
            if (!storedToken || storedToken !== token) {
                console.error("Token storage failed! Expected:", token.substring(0, 20), "Got:", storedToken?.substring(0, 20));
                setError("Failed to store authentication token");
                return;
            }
            
            console.log("Token stored successfully, calling onLogin callback");
            // Call the callback to update parent state
            onLogin();
        } catch (err) {
            console.error("Login error:", err);
            console.error("Error response:", err.response?.data);
            const errorMsg = err.response?.data?.error || err.message || "Invalid username or password";
            setError(errorMsg);
        }
    };


    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <input
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />

                <br />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <br />

                <button type="submit">Login</button>
            </form>

            {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}

            <p>
                New user?{" "}
                <button type="button" onClick={onSwitchToSignup}>
                    Signup
                </button>
            </p>
        </div>
    );
}

export default Login;
