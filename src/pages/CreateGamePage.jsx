import React from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";

const CreateGamePage = () => {
  const navigate = useNavigate();
  const [maxPlayers, setMaxPlayers] = React.useState("4");
  const [boardTheme, setBoardTheme] = React.useState("Classic");
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true); setError("");
    try {
      const res = await API.post("/games", { max_players: Number(maxPlayers), board_theme: boardTheme });
      navigate(`/games/${res.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create game");
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <h2 className="text-2xl font-semibold text-slate-900 dark:text-white mb-6">New Game</h2>
      {error && <div className="bg-red-50 text-red-600 rounded-lg px-4 py-3 text-sm mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 p-6 space-y-5">
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Max Players</label>
          <div className="flex gap-3">
            {["2","3","4"].map(n => (
              <button key={n} type="button" onClick={() => setMaxPlayers(n)}
                className={`flex-1 py-2 rounded-lg border-2 font-semibold text-sm transition-all ${
                  maxPlayers === n
                    ? "border-indigo-500 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400"
                    : "border-slate-200 dark:border-slate-600 text-slate-600 dark:text-slate-300"
                }`}>{n} Players</button>
            ))}
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Board Theme</label>
          <div className="grid grid-cols-3 gap-2">
            {["Classic","Desert","Space","Ocean","Forest","Neon"].map(t => (
              <button key={t} type="button" onClick={() => setBoardTheme(t)}
                className={`py-2 rounded-lg border-2 text-sm font-medium transition-all ${
                  boardTheme === t
                    ? "border-indigo-500 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400"
                    : "border-slate-200 dark:border-slate-600 text-slate-600 dark:text-slate-300"
                }`}>{t}</button>
            ))}
          </div>
        </div>
        <button type="submit" disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold py-3 rounded-xl transition-colors">
          {loading ? "Creating…" : "Create Game"}
        </button>
      </form>
    </div>
  );
};

export default CreateGamePage;