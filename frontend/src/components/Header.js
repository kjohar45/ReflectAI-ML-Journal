import "./Header.css";

function Header({ onLogout }) {
    return (
        <header className="app-header">
            <h1>🧠 AI Journal Companion</h1>
            <button onClick={onLogout} className="logout-btn">
                Logout
            </button>
        </header>
    );
}

export default Header;



