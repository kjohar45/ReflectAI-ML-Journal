import { useState } from "react";
import { fetchJournalByDate } from "../services/api";

function CalendarView() {
    const [date, setDate] = useState("");
    const [entries, setEntries] = useState([]);
    const [overallEmotion, setOverallEmotion] = useState("");
    const [loading, setLoading] = useState(false);

    const handleDateChange = async (e) => {
        const selectedDate = e.target.value;
        setDate(selectedDate);

        if (!selectedDate) return;

        setLoading(true);
        try {
            const res = await fetchJournalByDate(selectedDate);
            setEntries(res.data.entries);
            setOverallEmotion(res.data.overall_emotion);
        } catch (err) {
            console.error(err);
            // Don't clear data for 401 - interceptor will handle logout
            if (err.response?.status === 401) {
                return;
            }
            setEntries([]);
            setOverallEmotion("");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>📅 View Journal by Date</h2>

            <input
                type="date"
                value={date}
                onChange={handleDateChange}
            />

            {loading && <p>Loading journal...</p>}

            {!loading && date && entries.length === 0 && (
                <p>No journal entry for this day.</p>
            )}

            {!loading && entries.length > 0 && (
                <div style={{ marginTop: "15px" }}>
                    <p style={{ marginTop: "12px" }}>
                        <strong>Overall Emotion:</strong> {overallEmotion}
                    </p>
                    <p><strong>Written:</strong></p>

                    {entries.map((entry, index) => (
                        <p key={index} style={{ marginLeft: "10px" }}>
                            • {entry.text}
                        </p>
                    ))}


                </div>
            )}
        </div>
    );
}

export default CalendarView;
