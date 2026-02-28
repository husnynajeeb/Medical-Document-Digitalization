import { Link, useLocation } from "react-router-dom";
import { Home, FileText, BarChart3, Activity } from "lucide-react";

export default function Sidebar() {
  const { pathname } = useLocation();

  const linkStyle = (path) =>
    `flex items-center space-x-3 px-4 py-3 rounded-xl mb-2 font-medium transition-all duration-200 group ${
      pathname === path
        ? "bg-gradient-to-r from-blue-100 to-teal-100 text-blue-600 shadow-md"
        : "text-gray-700 hover:bg-gradient-to-r hover:from-blue-50 hover:to-teal-50 hover:text-blue-600 hover:shadow-sm"
    }`;

  const iconStyle = (path) =>
    pathname === path
      ? "text-blue-600"
      : "text-gray-400 group-hover:text-blue-500";

  return (
    <div className="w-72 bg-blue-50 border border-gray-200 rounded-r-2xl shadow-lg flex flex-col">

      {/* ===== LOGO ===== */}
      <div>
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-md ring-2 ring-blue-100">
              <Activity className="text-white" size={24} />
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-800">
                Medical Analyzer
              </h1>
              <p className="text-xs text-gray-600">
                AI-Powered Document Insights
              </p>
            </div>
          </div>
        </div>

        {/* ===== NAVIGATION ===== */}
        <nav className="p-4 mt-4">
          <Link to="/" className={linkStyle("/")}>
            <Home size={20} className={iconStyle("/")} />
            <span>Dashboard</span>
          </Link>

          <Link to="/upload" className={linkStyle("/upload")}>
            <FileText size={20} className={iconStyle("/upload")} />
            <span>AI Powered Interpretation</span>
          </Link>

          <Link to="/results" className={linkStyle("/results")}>
            <BarChart3 size={20} className={iconStyle("/results")} />
            <span>Interpretation Results</span>
          </Link>

          <Link to="/history" className={linkStyle("/history")}>
            <FileText size={18} className={iconStyle("/history")} />
            <span>Interpretation History</span>
          </Link>
        </nav>
      </div>
    </div>
  );
}