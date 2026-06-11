import { useState, useEffect } from "react";
import JournalForm from "./components/JournalForm";
import MoodChart from "./components/MoodChart";
import WeeklyMean from "./components/WeeklyMean";
import CalendarView from "./components/CalendarView";
import Login from "./components/Login";
import Signup from "./components/Signup";
import Header from "./components/Header";
import ReflectMetrics from "./components/ReflectMetrics";

function App() {
    // ✅ AUTH STATE MUST COME FROM TOKEN
    const [isAuthenticated, setIsAuthenticated] = useState(
        !!localStorage.getItem("token")
    );

    const [showSignup, setShowSignup] = useState(false);

    // ✅ KEEP AUTH STATE IN SYNC WITH TOKEN
    useEffect(() => {
        const checkAuth = () => {
            const token = localStorage.getItem("token");
            const isAuth = !!token;
            console.log("Checking auth state, token exists:", isAuth);
            setIsAuthenticated(isAuth);
        };
        
        checkAuth();
        
        // Listen for storage changes (in case token is set in another tab)
        window.addEventListener("storage", checkAuth);
        
        // Listen for auth logout events (when token is invalid/cleared)
        const handleAuthLogout = (event) => {
            console.log("Auth logout event received, updating auth state", event.detail);
            // Double-check token is actually gone before logging out
            const token = localStorage.getItem("token");
            if (!token) {
                setIsAuthenticated(false);
            } else {
                console.warn("Auth logout event received but token still exists, ignoring");
            }
        };
        window.addEventListener("auth:logout", handleAuthLogout);
        
        return () => {
            window.removeEventListener("storage", checkAuth);
            window.removeEventListener("auth:logout", handleAuthLogout);
        };
    }, []);

    const logout = () => {
        localStorage.removeItem("token");
        setIsAuthenticated(false);
    };

    if (!isAuthenticated) {
        return (
            <div className="app-container">
                <h1>🧠 ReflectAI</h1>
                <div className="card">
                    {showSignup ? (
                        <Signup 
                            onSignup={() => setShowSignup(false)} 
                            onSwitchToLogin={() => setShowSignup(false)}
                        />
                    ) : (
                        <Login
                            onLogin={() => {
                                // ✅ GUARANTEED TOKEN EXISTS HERE
                                const token = localStorage.getItem("token");
                                console.log("onLogin callback called, token exists:", !!token);
                                if (token) {
                                    setIsAuthenticated(true);
                                } else {
                                    console.error("Token missing in onLogin callback!");
                                }
                            }}
                            onSwitchToSignup={() => setShowSignup(true)}
                        />
                    )}
                </div>
            </div>
        );
    }

    return (
        <div className="app-container">
            <Header onLogout={logout} />

            <div className="card">
                <JournalForm />
            </div>

            <div className="card reflect-card">
                <ReflectMetrics />
            </div>

            <div className="card">
                <MoodChart />
            </div>

            <div className="card">
                <WeeklyMean />
            </div>

            <div className="card">
                <CalendarView />
            </div>
        </div>
    );
}

export default App;
