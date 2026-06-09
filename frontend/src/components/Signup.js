import { useState } from "react";
import { signup } from "../services/api";

function Signup({ onSignup, onSwitchToLogin }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [emergencyName, setEmergencyName] = useState("");
    const [emergencyPhone, setEmergencyPhone] = useState("");
    const [message, setMessage] = useState("");

    const handleSignup = async (e) => {
        e?.preventDefault();
        setMessage("");
        
        if (!username.trim() || !password.trim()) {
            setMessage("Please enter both username and password");
            return;
        }

        try {
            console.log("Attempting signup for user:", username);
            await signup(username, password, emergencyName, emergencyPhone);
            setMessage("Signup successful. Please login.");
            // Switch to login view after successful signup
            setTimeout(() => {
                onSignup();
            }, 1000);
        } catch (err) {
            console.error("Signup error:", err);
            const errorMsg = err.response?.data?.error || "Signup failed";
            setMessage(errorMsg);
        }
    };

    return (
        <div>
            <h2>Signup</h2>
            <form onSubmit={handleSignup}>
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

                <input
                    type="text"
                    placeholder="Emergency Contact Name"
                    value={emergencyName}
                    onChange={(e) => setEmergencyName(e.target.value)}
                    required
                />

                <br />

                <input
                    type="tel"
                    placeholder="Emergency Contact Phone Number"
                    value={emergencyPhone}
                    onChange={(e) => setEmergencyPhone(e.target.value)}
                    required
                />

                <br />

                <button type="submit">Signup</button>
            </form>

            {message && (
                <p style={{ 
                    color: message.includes("successful") ? "green" : "red",
                    marginTop: "10px" 
                }}>
                    {message}
                </p>
            )}

            <p>
                Already have an account?{" "}
                <button type="button" onClick={onSwitchToLogin}>
                    Login
                </button>
            </p>
        </div>
    );
}

export default Signup;
