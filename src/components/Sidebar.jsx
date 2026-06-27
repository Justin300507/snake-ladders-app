import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Users, Plus } from 'lucide-react';

const Sidebar = () => {
  return (
    <aside className="w-56 bg-white dark:bg-slate-800 border-r border-slate-100 dark:border-slate-700 flex flex-col px-3 py-4 fixed h-full">
      <div className="flex items-center gap-2 px-2 mb-6">
        <div className="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center">
          <span className="text-white text-sm font-bold">A</span>
        </div>
        <span className="font-bold text-slate-900 dark:text-white text-sm">AppName</span>
      </div>
      <nav className="flex-1 space-y-0.5">
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              isActive
                ? 'bg-indigo-50 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-300'
                : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700'
            }`
          }
        >
          <LayoutDashboard size={16} />
          Dashboard
        </NavLink>
        <NavLink
          to="/users"
          className={({ isActive }) =>
            `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              isActive
                ? 'bg-indigo-50 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-300'
                : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700'
            }`
          }
        >
          <Users size={16} />
          Users
        </NavLink>
        <NavLink
          to="/games/create"
          className={({ isActive }) =>
            `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              isActive
                ? 'bg-indigo-50 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-300'
                : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700'
            }`
          }
        >
          <Plus size={16} />
          New Game
        </NavLink>
      </nav>
    </aside>
  );
};

export default Sidebar;
