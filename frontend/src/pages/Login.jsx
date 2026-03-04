import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const login = async () => {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const res = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Login failed");
      return;
    }

    // Store token and username separately
    localStorage.setItem("token", data.access_token);
    if (data.name) {
      localStorage.setItem("username", data.name);
    } else {
      // If backend does not return name, decode from JWT as fallback
      const payload = JSON.parse(atob(data.access_token.split(".")[1]));
      if (payload.name) localStorage.setItem("username", payload.name);
    }

    navigate("/");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-10 rounded-2xl shadow-xl w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>

        <input
          className="w-full mb-4 p-3 border rounded-lg"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          className="w-full mb-6 p-3 border rounded-lg"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={login}
          className="w-full bg-blue-600 text-white py-3 rounded-lg"
        >
          Login
        </button>

        <p className="mt-4 text-sm text-center">
          No account? <Link to="/register" className="text-blue-600">Register</Link>
        </p>
      </div>
    </div>
  );
}