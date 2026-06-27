import React from "react";
import { useParams, Link } from "react-router-dom";
import API from "../api";

const SNAKES = { 99:54, 70:55, 52:42, 25:5, 87:24, 64:18, 45:7 };
const LADDERS = { 4:14, 9:31, 20:38, 28:84, 40:59, 51:67, 63:81, 71:91 };
const COLORS = ["#6366f1","#f59e0b","#10b981","#ef4444"];
const DICE_FACES = ["⚀","⚁","⚂","⚃","⚄","⚅"];

// get email from JWT without any library
const getMyEmail = () => {
  try {
    const t = localStorage.getItem("token");
    const payload = t.split(".")[1];
    const pad = payload.length % 4 ? "=".repeat(4 - payload.length % 4) : "";
    return JSON.parse(atob(payload + pad)).sub;
  } catch { return null; }
};

const Board = ({ positions, playerCount }) => {
  const rows = [];
  for (let r = 9; r >= 0; r--) {
    const going = (9 - r) % 2 === 0 ? "left" : "right";
    const nums = going === "left"
      ? Array.from({length:10}, (_,c) => r*10+c+1)
      : Array.from({length:10}, (_,c) => r*10+(9-c)+1);
    rows.push(nums);
  }

  const occupants = {};
  positions.slice(0, playerCount).forEach((pos, i) => {
    if (!occupants[pos]) occupants[pos] = [];
    occupants[pos].push(i);
  });

  return (
    <div style={{display:"grid", gridTemplateColumns:"repeat(10,1fr)", gap:2, background:"#0f172a", padding:6, borderRadius:12}}>
      {rows.flat().map(num => {
        const isSnakeHead = SNAKES[num] !== undefined;
        const isLadderFoot = LADDERS[num] !== undefined;
        const here = occupants[num] || [];
        return (
          <div key={num} style={{
            aspectRatio:"1",
            background: isSnakeHead ? "#7f1d1d" : isLadderFoot ? "#14532d" : num%2===0 ? "#1e293b" : "#0f172a",
            borderRadius:3,
            display:"flex", flexDirection:"column",
            alignItems:"center", justifyContent:"center",
            fontSize:"clamp(6px,1.1vw,9px)",
            border: here.length ? "1.5px solid #f59e0b" : "1px solid #1e293b",
            position:"relative", overflow:"hidden"
          }}>
            <span style={{color:"#475569", fontSize:"clamp(5px,0.9vw,8px)"}}>{num}</span>
            {isSnakeHead && <span style={{fontSize:"clamp(8px,1.3vw,11px)"}}>🐍</span>}
            {isLadderFoot && <span style={{fontSize:"clamp(8px,1.3vw,11px)"}}>🪜</span>}
            {here.map(i => (
              <div key={i} style={{
                width:8, height:8, borderRadius:"50%",
                background:COLORS[i], position:"absolute",
                bottom:1+Math.floor(i/2)*9, right:1+(i%2)*9,
                border:"1px solid #000"
              }}/>
            ))}
          </div>
        );
      })}
    </div>
  );
};

const GameDetailPage = () => {
  const { id } = useParams();
  const [game, setGame] = React.useState(null);
  const [players, setPlayers] = React.useState([]);
  const [moves, setMoves] = React.useState([]);
  const [rolling, setRolling] = React.useState(false);
  const [lastDice, setLastDice] = React.useState(null);
  const [error, setError] = React.useState("");
  const [myPlayer, setMyPlayer] = React.useState(null);

  const myEmail = getMyEmail();

  // compute positions from moves
  const positions = React.useMemo(() => {
    const pos = players.map(() => 1);
    moves.forEach(mv => {
      const pi = players.findIndex(p => p.id === mv.player_id);
      if (pi >= 0 && mv.to_position != null) pos[pi] = mv.to_position;
    });
    return pos;
  }, [players, moves]);

  const load = React.useCallback(async () => {
    try {
      const [gRes, pRes, mRes] = await Promise.all([
        API.get(`/games/${id}`),
        API.get(`/players?game_id=${id}&limit=20`),
        API.get(`/moves?game_id=${id}&limit=200`),
      ]);
      setGame(gRes.data);
      const pList = pRes.data?.items || pRes.data || [];
      setPlayers(pList);
      const mList = mRes.data?.items || mRes.data || [];
      setMoves(mList);
      // find which player is "me" by stored id in sessionStorage
      const storedId = sessionStorage.getItem(`player_id_game_${id}`);
      if (storedId) {
        const found = pList.find(p => p.id === Number(storedId));
        if (found) setMyPlayer(found);
      }
    } catch(e) { setError("Failed to load game"); }
  }, [id]);

  React.useEffect(() => {
    load();
    const t = setInterval(load, 3000);
    return () => clearInterval(t);
  }, [load]);

  const joinGame = async () => {
    setError("");
    try {
      // get my display_name from user list
      const usersRes = await API.get("/users").catch(() => ({data:{items:[]}}));
      const userList = usersRes.data?.items || usersRes.data || [];
      const me = userList.find(u => u.email === myEmail);
      const displayName = me?.display_name || myEmail?.split("@")[0] || "Player";

      const res = await API.post("/players", { game_id: Number(id), display_name: displayName });
      setMyPlayer(res.data);
      sessionStorage.setItem(`player_id_game_${id}`, res.data.id);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not join game");
    }
  };

  const rollDice = async () => {
    if (!myPlayer) return;
    setRolling(true);
    setError("");
    const dice = Math.floor(Math.random() * 6) + 1;
    setLastDice(dice);
    const pi = players.findIndex(p => p.id === myPlayer.id);
    const from = pi >= 0 ? positions[pi] : 1;
    let to = Math.min(from + dice, 100);
    if (SNAKES[to]) { to = SNAKES[to]; }
    else if (LADDERS[to]) { to = LADDERS[to]; }
    try {
      await API.post("/moves", {
        player_id: myPlayer.id,
        game_id: Number(id),
        dice_value: dice,
        from_position: from,
        to_position: to,
      });
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Move failed");
    }
    setRolling(false);
  };

  const startGame = async () => {
    await API.put(`/games/${id}`, { status: "active" });
    await load();
  };

  if (!game) return (
    <div className="flex items-center justify-center h-64">
      <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"/>
    </div>
  );

  const isWaiting = game.status === "waiting";
  const isActive = ["active","in_progress"].includes(game.status);
  const isDone = ["completed","finished"].includes(game.status);
  const canJoin = isWaiting && !myPlayer && players.length < game.max_players;
  const winner = players.find((_,i) => positions[i] >= 100);

  return (
    <div>
      <div className="flex items-center gap-3 mb-6">
        <Link to="/games" className="text-indigo-400 hover:text-indigo-300 text-sm">← All Games</Link>
        <span className="text-slate-600">/</span>
        <h2 className="text-xl font-semibold text-white">Game <span className="font-mono text-indigo-400">#{game.lobby_code}</span></h2>
        <span className={`ml-1 text-xs px-2 py-1 rounded-full font-medium ${
          isActive ? "bg-green-900 text-green-300" :
          isWaiting ? "bg-yellow-900 text-yellow-300" :
          "bg-slate-700 text-slate-400"
        }`}>{game.status}</span>
      </div>

      {winner && (
        <div className="bg-yellow-900/40 border border-yellow-600 rounded-xl px-5 py-4 mb-6 text-center">
          <div className="text-4xl mb-1">🏆</div>
          <p className="text-yellow-300 font-bold text-lg">{winner.display_name} wins!</p>
        </div>
      )}

      {error && (
        <div className="bg-red-900/30 border border-red-700 text-red-300 rounded-lg px-4 py-3 text-sm mb-4">{error}</div>
      )}

      <div className="grid lg:grid-cols-5 gap-6">
        {/* Board takes 3 cols */}
        <div className="lg:col-span-3">
          <Board positions={positions} playerCount={players.length} />
          <div className="mt-3 flex gap-4 text-xs text-slate-500">
            <span>🐍 Snake = go back &nbsp; 🪜 Ladder = go forward</span>
          </div>
        </div>

        {/* Side panel 2 cols */}
        <div className="lg:col-span-2 space-y-4">
          {/* Players card */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-4">
            <div className="flex justify-between items-center mb-3">
              <h3 className="font-semibold text-white text-sm">Players {players.length}/{game.max_players}</h3>
              {canJoin && (
                <button onClick={joinGame} className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs px-3 py-1 rounded-lg font-medium">
                  Join
                </button>
              )}
            </div>
            {players.length === 0 ? (
              <p className="text-slate-400 text-sm">No players yet. Be the first to join!</p>
            ) : (
              <div className="space-y-2">
                {players.map((p, i) => (
                  <div key={p.id} className={`flex items-center gap-2 p-2 rounded-lg ${myPlayer?.id === p.id ? "bg-slate-700" : ""}`}>
                    <div style={{width:10, height:10, borderRadius:"50%", background:COLORS[i], flexShrink:0}}/>
                    <span className="text-slate-200 text-sm flex-1 truncate">{p.display_name}</span>
                    <span className="text-slate-400 text-xs font-mono">sq {positions[i] || 1}</span>
                    {positions[i] >= 100 && <span className="text-sm">🏆</span>}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Action card */}
          {isWaiting && players.length >= 2 && myPlayer && (
            <button onClick={startGame}
              className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-xl transition-colors">
              Start Game ▶
            </button>
          )}

          {isActive && myPlayer && (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 flex flex-col items-center gap-3">
              <div style={{fontSize:72, lineHeight:1}}>{lastDice ? DICE_FACES[lastDice-1] : "🎲"}</div>
              {lastDice && (
                <p className="text-slate-300 text-sm">
                  Rolled <b className="text-white">{lastDice}</b>
                  {(() => {
                    const pi = players.findIndex(p => p.id === myPlayer.id);
                    const from = pi >= 0 ? (positions[pi] - lastDice) : 1;
                    const raw = Math.min((from < 1 ? 1 : from) + lastDice, 100);
                    if (SNAKES[raw]) return ` → 🐍 ${raw}→${SNAKES[raw]}`;
                    if (LADDERS[raw]) return ` → 🪜 ${raw}→${LADDERS[raw]}`;
                    return ` → sq ${positions[players.findIndex(p=>p.id===myPlayer.id)] || 1}`;
                  })()}
                </p>
              )}
              <button onClick={rollDice} disabled={rolling}
                className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-bold py-3 rounded-xl text-lg transition-colors">
                {rolling ? "Rolling…" : "Roll Dice"}
              </button>
            </div>
          )}

          {isActive && !myPlayer && (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 text-center text-slate-400 text-sm">
              Game in progress — spectating
            </div>
          )}

          {/* Move log */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-4">
            <h3 className="font-semibold text-white text-sm mb-3">Move Log</h3>
            {moves.length === 0 ? (
              <p className="text-slate-400 text-sm">No moves yet.</p>
            ) : (
              <div className="space-y-1 max-h-40 overflow-y-auto pr-1">
                {[...moves].reverse().map(m => {
                  const pi = players.findIndex(p => p.id === m.player_id);
                  const name = players[pi]?.display_name || `P${pi+1}`;
                  return (
                    <div key={m.id} className="flex items-start gap-2 text-xs">
                      <div style={{width:7, height:7, borderRadius:"50%", background:COLORS[pi]||"#64748b", marginTop:3, flexShrink:0}}/>
                      <span className="text-slate-300">
                        <span className="font-medium">{name}</span> rolled {m.dice_value} · {m.from_position}→{m.to_position}
                        {SNAKES[m.from_position + m.dice_value] ? " 🐍" : LADDERS[m.from_position + m.dice_value] ? " 🪜" : ""}
                      </span>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GameDetailPage;