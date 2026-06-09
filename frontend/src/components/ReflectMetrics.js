import { useEffect, useState } from "react";
import { fetchReflectMetrics } from "../services/api";

function ReflectMetrics() {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const loadMetrics = () => {
        setLoading(true);
        fetchReflectMetrics()
            .then((res) => {
                setMetrics(res.data);
                setError("");
            })
            .catch((err) => {
                console.error("Error loading metrics:", err);
                if (err.response?.status === 401) {
                    return;
                }
                setError("Failed to load ReflectAI metrics");
            })
            .finally(() => {
                setLoading(false);
            });
    };

    useEffect(() => {
        loadMetrics();
        window.addEventListener("refreshMetrics", loadMetrics);
        return () => {
            window.removeEventListener("refreshMetrics", loadMetrics);
        };
    }, []);

    if (loading) return <p>Loading ReflectAI metrics...</p>;
    if (error) return <p style={{ color: "red" }}>{error}</p>;
    if (!metrics) return <p>No metrics available.</p>;

    const getStatusColor = (val, thresholds) => {
        if (val > thresholds.high) return "#b91c1c"; // Red
        if (val > thresholds.med) return "#d97706"; // Amber
        return "#15803d"; // Green
    };

    return (
        <div>
            <h2>🧠 ReflectAI Adaptive Analytics</h2>
            
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "16px", marginTop: "15px" }}>
                
                <div style={{ padding: "16px", border: "1px solid #e5e7eb", borderRadius: "8px", background: "#f9fafb" }}>
                    <h3 style={{ fontSize: "0.9rem", color: "#6b7280", textTransform: "uppercase", marginBottom: "4px" }}>Emotional Risk Index (ERI)</h3>
                    <p style={{ fontSize: "1.8rem", fontWeight: "700", margin: "0", color: getStatusColor(metrics.eri, { high: 0.7, med: 0.4 }) }}>
                        {(metrics.eri * 100).toFixed(1)}%
                    </p>
                    <span style={{ fontSize: "0.75rem", color: "#9ca3af" }}>w1*F_neg + w2*D_avg + w3*K_risk</span>
                </div>

                <div style={{ padding: "16px", border: "1px solid #e5e7eb", borderRadius: "8px", background: "#f9fafb" }}>
                    <h3 style={{ fontSize: "0.9rem", color: "#6b7280", textTransform: "uppercase", marginBottom: "4px" }}>Emotional Volatility (EVI)</h3>
                    <p style={{ fontSize: "1.8rem", fontWeight: "700", margin: "0", color: getStatusColor(metrics.evi, { high: 0.6, med: 0.3 }) }}>
                        {(metrics.evi * 100).toFixed(1)}%
                    </p>
                    <span style={{ fontSize: "0.75rem", color: "#9ca3af" }}>State transition volatility</span>
                </div>

                <div style={{ padding: "16px", border: "1px solid #e5e7eb", borderRadius: "8px", background: "#f9fafb" }}>
                    <h3 style={{ fontSize: "0.9rem", color: "#6b7280", textTransform: "uppercase", marginBottom: "4px" }}>Latest Emotional Drift (EDS)</h3>
                    <p style={{ fontSize: "1.8rem", fontWeight: "700", margin: "0", color: getStatusColor(metrics.eds_latest, { high: 1.5, med: 0.8 }) }}>
                        {metrics.eds_latest ? metrics.eds_latest.toFixed(2) : "0.00"}
                    </p>
                    <span style={{ fontSize: "0.75rem", color: "#9ca3af" }}>|s_t - µ| / σ (std devs)</span>
                </div>

            </div>

            <div style={{ marginTop: "20px", padding: "16px", border: "1px solid #e5e7eb", borderRadius: "8px", background: "#fcfdff" }}>
                <h3>Adaptive Sentiment Personalization (ASP)</h3>
                <div style={{ display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: "12px", fontSize: "0.9rem" }}>
                    <div>
                        <strong>Baseline Mean Score (µ):</strong> {metrics.mean ? metrics.mean.toFixed(3) : "0.000"}
                    </div>
                    <div>
                        <strong>Standard Deviation (σ):</strong> {metrics.std_dev ? metrics.std_dev.toFixed(3) : "0.000"}
                    </div>
                    <div>
                        <strong>Happy Threshold (T_pos):</strong> {metrics.T_pos ? metrics.T_pos.toFixed(3) : "0.500"}
                    </div>
                    <div>
                        <strong>Sad Threshold (T_neg):</strong> {metrics.T_neg ? metrics.T_neg.toFixed(3) : "-0.500"}
                    </div>
                </div>
            </div>

            {metrics.distortions && metrics.distortions.length > 0 && (
                <div style={{ marginTop: "16px", padding: "12px 16px", background: "#fffbeb", borderLeft: "4px solid #f59e0b", borderRadius: "0 8px 8px 0" }}>
                    <strong>Detected Cognitive Distortions:</strong>
                    <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginTop: "8px" }}>
                        {metrics.distortions.map((dist, idx) => (
                            <span key={idx} style={{ background: "#fef3c7", color: "#92400e", padding: "2px 8px", borderRadius: "4px", fontSize: "0.8rem", fontWeight: "500" }}>
                                {dist}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            {metrics.ml_emotion && (
                <div style={{ marginTop: "20px", padding: "16px", border: "1px solid #e5e7eb", borderRadius: "8px", background: "#f9fafb" }}>
                    <h3>Latest ML Emotion Classification</h3>
                    <p>
                        <strong>Predicted Emotion: </strong> 
                        <span style={{ textTransform: "capitalize", fontWeight: "600", color: "#6366f1" }}>{metrics.ml_emotion}</span>
                        {" "}({(metrics.ml_confidence * 100).toFixed(1)}% confidence)
                    </p>
                    
                    {metrics.ml_probabilities && (
                        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: "12px", marginTop: "12px" }}>
                            {Object.entries(metrics.ml_probabilities).map(([emotion, prob]) => (
                                <div key={emotion} style={{ padding: "8px", background: "#ffffff", border: "1px solid #e5e7eb", borderRadius: "6px" }}>
                                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.8rem", marginBottom: "4px" }}>
                                        <span style={{ textTransform: "capitalize", fontWeight: "500" }}>{emotion}</span>
                                        <span>{(prob * 100).toFixed(0)}%</span>
                                    </div>
                                    <div style={{ background: "#e5e7eb", borderRadius: "3px", height: "4px", overflow: "hidden" }}>
                                        <div style={{ background: "#6366f1", height: "100%", width: `${(prob * 100).toFixed(0)}%` }} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default ReflectMetrics;
