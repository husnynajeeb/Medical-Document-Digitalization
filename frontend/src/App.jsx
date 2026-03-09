import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/layout/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import "./styles/app.css";

import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Results from "./pages/Results";
import History from "./pages/History";
import Login from "./pages/Login";
import Register from "./pages/Register";
import TranslatorPage from "./pages/TranslatorPage"

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout><Dashboard /></Layout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/upload"
          element={
            <ProtectedRoute>
              <Layout><Upload /></Layout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/results"
          element={
            <ProtectedRoute>
              <Layout><Results /></Layout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/history"
          element={
            <ProtectedRoute>
              <Layout><History /></Layout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/translator"
          element={
            <ProtectedRoute>
              <Layout><TranslatorPage /></Layout>
            </ProtectedRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}