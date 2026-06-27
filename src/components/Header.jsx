import React from 'react';
import { Moon, Sun, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const getDisplayName = () => {
  try {
    const t = localStorage.getItem("token");
    const payload = t.split(".")[1];
    const pad = payload.length % 4 ? "=".repeat(4 - payload.length % 4) : "";
    const sub = JSON.parse(atob(payload + pad)).sub;
    return sub?.split("@")[0] || "User";
  } catch { return "User"; }
};

const Header = () => {
  const navigate = useNavigate();
  const [dark, setDark] = React.useState(document.documentElement.classList.contains('dark'));
  const name = localStorage.getItem("display_name") || getDisplayName();

  React.useEffect(() => {
    document.documentElement.classList.toggle('dark', dark);
  }, [dark]);

  const today = new Date().toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' });

  return (
    <header className="flex justify-between items-center px-4 py-2 border-b border-slate-100 dark:border-slate-700">
      <h1 className="text-base font-semibold text-slate-900 dark:text-white">Hello, {name} 👋</h1>
      <div className="flex items-center gap-2">
        <span className="text-slate-500 dark:text-slate-400 text-sm hidden sm:block">{today}</span>
        <button onClick={() => setDark(d => !d)}
          className="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors">
          {dark ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        <button onClick={() => { localStorage.removeItem("token"); navigate("/login"); }}
          className="p-2 rounded-lg text-slate-500 hover:bg-red-100 dark:hover:bg-red-900/30 hover:text-red-500 transition-colors">
          <LogOut size={18} />
        </button>
      </div>
    </header>
  );
};

export default Header;
