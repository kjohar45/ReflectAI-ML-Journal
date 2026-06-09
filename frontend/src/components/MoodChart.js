import { useEffect, useState } from "react";
import { fetchWeeklyTrends } from "../services/api";

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend
);

function MoodChart() {
    const [data, setData] = useState(null);
    const [error, setError] = useState("");

    useEffect(() => {
        const load = () => {
            fetchWeeklyTrends()
                .then((response) => {
                    setData(response.data || { Happy: 0, Sad: 0, Neutral: 0, Anxious: 0 });
                })
                .catch((error) => {
                    console.error("Error fetching weekly trends:", error);
                    if (error.response?.status === 401) {
                        return;
                    }
                    setError("Failed to load weekly trends");
                    setData({ Happy: 0, Sad: 0, Neutral: 0, Anxious: 0 });
                });
        };
        load();
        window.addEventListener("refreshMetrics", load);
        return () => window.removeEventListener("refreshMetrics", load);
    }, []);

    if (!data) {
        return <p>Loading weekly mood trends...</p>;
    }

    if (error) {
        return <p style={{ color: "red" }}>{error}</p>;
    }

    const chartData = {
        labels: ["Happy", "Sad", "Anxious", "Neutral"],
        datasets: [
            {
                label: "Entries (Last 7 Days)",
                data: [
                    data.Happy,
                    data.Sad,
                    data.Anxious,
                    data.Neutral
                ]
            }
        ]
    };

    return (
        <div>
            <h2>Weekly Mood Trends</h2>
            <Bar data={chartData} />
        </div>
    );
}

export default MoodChart;
