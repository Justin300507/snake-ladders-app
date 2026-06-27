import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Users, Plus, Gamepad2, Trophy } from 'lucide-react';

const Sidebar = () => {
  return (
    <aside className="w-56 bg-white dark:bg-slate-800 border-r border-slate-100 dark:border-slate-700 flex flex-col px-3 py-4 fixed h-full">
      <div className="flex items-center gap-2 px-2 mb-6">
        <div className="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center">
          <span className="text-white text-sm">🎲</span>
        </div>
        <span className="font-bold text-slate-900 dark:text-white text-sm">Snake & Ladders</span>
      </div>
      <nav className="flex-1 space-y-0.5">
        {[
          { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
          { to: "/games",     icon: Gamepad2,         label: "Games" },
          { to: "/users",     icon: Users,             label: "Players" },
        ].map(({ to, icon: Icon, label }) => (
          <NavLink key={to} to={to}
            className={({ isActive }) =>
              `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? "bg-indigo-50 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-300"
                  : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700"
              }`
            }
          >
            <Icon size={16} />{label}
          </NavLink>
        ))}
      </nav>
      <div className="mt-auto pt-3 border-t border-slate-200 dark:border-slate-700">
        <NavLink to="/games/create"
          className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium bg-indigo-600 text-white hover:bg-indigo-700 transition-colors justify-center">
          <Plus size={16} /> New Game
        </NavLink>
      </div>
    </aside>
  );
};

export default Sidebar;
