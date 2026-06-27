import React from 'react';
import API from '../api';
import ListItemCard from '../components/ListItemCard';
import Toast from '../components/Toast';
import { Users, Search } from 'lucide-react';

const UsersPage = () => {
  const [items, setItems] = React.useState([
    { id: 1, display_name: 'Alex Chen', email: 'alex@example.com', role: 'Player' },
    { id: 2, display_name: 'Maria Garcia', email: 'maria@example.com', role: 'Admin' },
    { id: 3, display_name: 'Liam Patel', email: 'liam@example.com', role: 'Player' },
    { id: 4, display_name: 'Sofia Rossi', email: 'sofia@example.com', role: 'Moderator' },
    { id: 5, display_name: 'Noah Kim', email: 'noah@example.com', role: 'Player' },
  ]);
  const [loading, setLoading] = React.useState(false);
  const [search, setSearch] = React.useState('');
  const [filterRole, setFilterRole] = React.useState('All');
  const [toast, setToast] = React.useState(null);

  React.useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true);
      try {
        const res = await API.get('/users');
        setItems(res.data.items || []);
      } catch (err) {
        setToast({ msg: 'Failed to load users', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchUsers();
  }, []);

  const filtered = items.filter(u => {
    const matchesSearch = u.display_name.toLowerCase().includes(search.toLowerCase()) || u.email.toLowerCase().includes(search.toLowerCase());
    const matchesRole = filterRole === 'All' || u.role === filterRole;
    return matchesSearch && matchesRole;
  });

  const roles = ['All', 'Admin', 'Player', 'Moderator'];

  return (
    <div>
      {toast && <Toast toast={toast} />}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Users</h2>
        <button className="btn-primary flex items-center gap-1.5">
          <Search size={16} /> Add User
        </button>
      </div>
      <div className="flex gap-4 mb-4">
        <div className="flex-1">
          <input
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search by name or email"
            className="input w-full"
          />
        </div>
        <select
          value={filterRole}
          onChange={e => setFilterRole(e.target.value)}
          className="input"
        >
          {roles.map(r => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
      </div>
      {loading ? (
        <div className="animate-pulse space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-16 bg-slate-200 dark:bg-slate-700 rounded-xl" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-10 text-slate-500 dark:text-slate-400">
          <Users size={48} className="mx-auto mb-4 text-slate-400 dark:text-slate-600" />
          <p>No results found</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map(user => (
            <ListItemCard
              key={user.id}
              title={user.display_name}
              subtitle={user.email}
              trailing={user.role}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default UsersPage;
