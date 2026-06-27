import React from 'react';
import API from '../api';
import StatCard from '../components/StatCard';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import ListItemCard from '../components/ListItemCard';
import Toast from '../components/Toast';

const Dashboard = () => {
  const [stats, setStats] = React.useState(null);
  const [recentGames, setRecentGames] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [toast, setToast] = React.useState(null);

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await API.get('/stats/summary');
        setStats(res.data);
        const gamesRes = await API.get('/games', { params: { limit: 5 } });
        setRecentGames(gamesRes.data.items || []);
      } catch (err) {
        setToast({ msg: 'Failed to load dashboard', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const chartData = [
    { month: 'Jan', total: 840 },
    { month: 'Feb', total: 720 },
    { month: 'Mar', total: 1100 },
    { month: 'Apr', total: 890 },
    { month: 'May', total: 1240 },
    { month: 'Jun', total: 980 },
  ];

  return (
    <div>
      {toast && <Toast toast={toast} />}
      <h2 className="text-2xl font-semibold text-slate-900 dark:text-white mb-6">Dashboard</h2>
      {loading ? (
        <div className="animate-pulse space-y-4">
          <div className="h-24 bg-slate-200 dark:bg-slate-700 rounded-xl" />
          <div className="h-64 bg-slate-200 dark:bg-slate-700 rounded-xl" />
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <StatCard label="Total Users" value={stats?.total_users ?? 0} change="+5% this week" />
            <StatCard label="Active Games" value={stats?.active_games ?? 0} change="+2% today" />
            <StatCard label="Moves Today" value={stats?.moves_today ?? 0} change="+12% vs yesterday" />
            <StatCard label="Avg Rating" value={stats?.average_rating?.toFixed(1) ?? '0.0'} change="+0.3" />
          </div>
          <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 p-5 mb-6">
            <h3 className="font-semibold text-slate-900 dark:text-white mb-4">Monthly Overview</h3>
            <ResponsiveContainer width="100%" height={240}>
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.15} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#1e293b', border: 'none', borderRadius: '8px', color: '#f1f5f9' }} />
                <Area type="monotone" dataKey="total" stroke="#6366f1" strokeWidth={2} fill="url(#colorTotal)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div>
            <h3 className="font-semibold text-slate-900 dark:text-white mb-4">Recent Games</h3>
            {recentGames.length === 0 ? (
              <p className="text-slate-500 dark:text-slate-400">No recent games.</p>
            ) : (
              <div className="space-y-3">
                {recentGames.map(game => (
                  <ListItemCard
                    key={game.id}
                    title={`Game ${game.lobby_code}`}
                    subtitle={`Status: ${game.status}`}
                    trailing={game.winner_player_id ? '🏆' : ''}
                  />
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
