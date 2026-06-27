import React from 'react';
import API from '../api';
import Toast from '../components/Toast';
import { Plus, CheckSquare } from 'lucide-react';

const CreateGamePage = () => {
  const [maxPlayers, setMaxPlayers] = React.useState('');
  const [boardTheme, setBoardTheme] = React.useState('');
  const [loading, setLoading] = React.useState(false);
  const [toast, setToast] = React.useState(null);

  const handleSubmit = async e => {
    e.preventDefault();
    if (!maxPlayers) return;
    setLoading(true);
    try {
      await API.post('/games', { max_players: Number(maxPlayers), board_theme: boardTheme });
      setToast({ msg: 'Game created', type: 'success' });
    } catch (err) {
      setToast({ msg: 'Failed to create game', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {toast && <Toast toast={toast} />}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Create Game</h2>
        <button className="btn-primary flex items-center gap-1.5">
          <Plus size={16} /> Save
        </button>
      </div>
      <form className="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 p-6 space-y-4" onSubmit={handleSubmit}>
        <div className="space-y-1">
          <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Max Players</label>
          <input
            type="number"
            min="2"
            value={maxPlayers}
            onChange={e => setMaxPlayers(e.target.value)}
            placeholder="e.g. 4"
            className="input"
          />
        </div>
        <div className="space-y-1">
          <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Board Theme (optional)</label>
          <input
            type="text"
            value={boardTheme}
            onChange={e => setBoardTheme(e.target.value)}
            placeholder="e.g. Desert"
            className="input"
          />
        </div>
        <div className="flex gap-2">
          <button
            type="submit"
            disabled={loading || !maxPlayers}
            className="btn-primary flex-1 flex items-center justify-center gap-2"
          >
            {loading && <CheckSquare size={16} className="animate-spin" />}
            Create
          </button>
          <button
            type="button"
            onClick={() => {
              setMaxPlayers('');
              setBoardTheme('');
            }}
            className="bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-white rounded-lg px-4 py-2"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateGamePage;
