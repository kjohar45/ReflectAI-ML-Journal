import { useEffect, useState } from "react";
import { fetchWeeklyMeanEmotion } from "../services/api";

function WeeklyMean() {
    const [data, setData] = useState(null);
    const [error, setError] = useState("");

    useEffect(() => {
        fetchWeeklyMeanEmotion()
            .then((res) => setData(res.data))
            .catch((err) => {
                console.error("Error fetching weekly mean:", err);
                // Don't show error for 401 - interceptor will handle logout
                if (err.response?.status === 401) {
                    return;
                }
                setError("Failed to load weekly summary");
                setData({ mean_label: "No data" });
            });
    }, []);

    if (!data) return <p>Loading weekly mood summary...</p>;

    if (error) {
        return (
            <div style={{ marginTop: "20px" }}>
                <h2>Weekly Emotional Summary</h2>
                <p style={{ color: "red" }}>{error}</p>
            </div>
        );
    }

    return (
        <div style={{ marginTop: "20px" }}>
            <h2>Weekly Emotional Summary</h2>
            <p><strong>Overall Mood:</strong> {data.mean_label}</p>
        </div>
    );
}


export default WeeklyMean;
