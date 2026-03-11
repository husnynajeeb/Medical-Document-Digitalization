import { Link, useLocation, useNavigate } from "react-router-dom";
import { Home, FileText, BarChart3, Activity, LogOut } from "lucide-react";

export default function Sidebar() {
  const { pathname } = useLocation();
  const navigate = useNavigate();

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

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <aside className="w-72 bg-blue-50 border border-gray-200 rounded-r-2xl shadow-lg flex flex-col min-h-screen">
      {/* TOP SECTION */}
      <div>
        {/* LOGO */}
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

        {/* NAVIGATION */}
        <nav className="p-4 mt-4 flex flex-col">
          <Link to="/" className={linkStyle("/")}>
            <Home size={20} className={iconStyle("/")} />
            <span>Dashboard</span>
          </Link>

          <Link to="/enhancement" className={linkStyle("/enhancement")}>
            <FileText size={20} className={iconStyle("/enhancement")} />
            <span>AI Powered Image Enhancement</span>
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

          {/* ✅ Added: Prediction */}
          <Link to="/prediction" className={linkStyle("/prediction")}>
            <FileText size={20} className={iconStyle("/prediction")} />
            <span>Diabetes Prediction</span>
          </Link>
          <Link to="/risk" className={linkStyle("/risk")}>
            <BarChart3 size={20} className={iconStyle("/risk")} />
            <span>Risks and Recommendations</span></Link>
          <Link to="/translator" className={linkStyle("/translator")}>
            <FileText size={18} className={iconStyle("/translator")} />
            <span>Translation & Summarization</span>
          </Link>
        </nav>
      </div>

      {/* BOTTOM SECTION */}
      <div className="mt-auto p-4 border-t border-gray-200">
        <button
          onClick={logout}
          className="w-full flex items-center justify-center space-x-2 bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-xl transition"
        >
          <LogOut size={18} />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}
