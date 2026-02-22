import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {
  const { pathname } = useLocation();

  const linkStyle = (path) =>
    `flex items-center space-x-3 px-4 py-3 rounded-lg mb-2 font-semibold ${
      pathname === path
        ? "bg-blue-50 text-blue-600"
        : "text-gray-600 hover:bg-gray-100"
    }`;

  return (
    <div className="w-64 bg-white shadow-lg">
      <div className="p-6 border-b">
        <h1 className="text-lg font-bold text-gray-800">Medical Analyzer</h1>
      </div>

      <nav className="p-4">
        <Link to="/" className={linkStyle("/")}>Home</Link>
        <Link to="/upload" className={linkStyle("/upload")}>Upload</Link>
        <Link to="/results" className={linkStyle("/results")}>Results</Link>
      </nav>
    </div>
  );
}