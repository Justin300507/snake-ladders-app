import React from "react";
import { Link } from "react-router-dom";
import API from "../api";

const STATUS_COLOR = {
  waiting: "bg-yellow-900 text-yellow-300",
  active: "bg-green-900 text-green-300",
  in_progress: "bg-green-900 text-green-300",
  completed: "bg-slate-700 text-slate-300",
  finished: "bg-slate-700 text-slate-300",
};

const GamesListPage = () => {
  const [games, setGames] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  const load = async () => {
    try {
      const res = await API.get("/games?limit=50");
      setGames(res.data?.items || res.data || []);
    } catch {}
    setLoading(false);
  };

  React.useEffect(() => { load(); const t = setInterval(load, 5000); return () => clearInterval(t); }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-semibold text-white">Games</h2>
        <Link to="/games/create"
          className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-4 py-2 rounded-xl">
          + New Game
        </Link>
      </div>
      {loading ? (
        <div className="space-y-3">{[1,2,3].map(i=><div key={i} className="h-16 bg-slate-700 rounded-xl animate-pulse"/>)}</div>
      ) : games.length === 0 ? (
        <div className="text-center py-16 text-slate-400">
          <div className="text-5xl mb-4">🎲</div>
          <p className="text-lg font-medium mb-2">No games yet</p>
          <Link to="/games/create" className="text-indigo-400 hover:underline">Create the first one</Link>
        </div>
      ) : (
        <div className="space-y-3">
          {games.map(g => (
            <Link key={g.id} to={`/games/${g.id}`}
              className="flex items-center gap-4 bg-slate-800 border border-slate-700 hover:border-indigo-500 rounded-xl px-5 py-4 transition-colors block">
              <div className="text-2xl">🎲</div>
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-white">Game #{g.lobby_code}</p>
                <p className="text-sm text-slate-400">{g.board_theme || "Classic"} · max {g.max_players} players</p>
              </div>
              <span className={`text-xs px-2 py-1 rounded-full font-medium ${STATUS_COLOR[g.status] || "bg-slate-700 text-slate-300"}`}>
                {g.status}
              </span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default GamesListPage;