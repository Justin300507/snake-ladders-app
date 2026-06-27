import React from 'react';
import { Moon, Sun } from 'lucide-react';

const Header = () => {
  const [dark, setDark] = React.useState(document.documentElement.classList.contains('dark'));

  React.useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);

  const today = new Date().toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' });

  return (
    <header className="flex justify-between items-center px-4 py-2 border-b border-slate-100 dark:border-slate-700">
      <h1 className="text-xl font-semibold text-slate-900 dark:text-white">Hello, {localStorage.getItem('display_name') || 'User'}</h1>
      <div className="flex items-center gap-2">
        <span className="text-slate-500 dark:text-slate-400 text-sm">{today}</span>
        <button
          onClick={() => setDark(d => !d)}
          className="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
        >
          {dark ? <Sun size={18} /> : <Moon size={18} />}
        </button>
      </div>
    </header>
  );
};

export default Header;
