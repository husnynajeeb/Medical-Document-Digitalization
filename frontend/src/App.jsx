import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/layout/Layout";
import ProtectedRoute from "./components/ProtectedRoute";

// pages
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Results from "./pages/Results";
import History from "./pages/History";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Prediction from "./pages/PredictionForm";
import Risk from "./pages/Risk_Results";
import Enhancement from "./pages/EnhancementPage/index";
import TranslatorPage from "./pages/TranslatorPage";

// 🌍 LANGUAGE SYSTEM
import { LanguageProvider } from "./services/useLanguage.jsx";

export default function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <Routes>

          {/* AUTH */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* DASHBOARD */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout>
                  <Dashboard />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* UPLOAD */}
          <Route
            path="/upload"
            element={
              <ProtectedRoute>
                <Layout>
                  <Upload />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* RESULTS */}
          <Route
            path="/results"
            element={
              <ProtectedRoute>
                <Layout>
                  <Results />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* HISTORY */}
          <Route
            path="/history"
            element={
              <ProtectedRoute>
                <Layout>
                  <History />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* ENHANCEMENT */}
          <Route
            path="/enhancement"
            element={
              <ProtectedRoute>
                <Layout>
                  <Enhancement />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* TRANSLATOR */}
          <Route
            path="/translator"
            element={
              <ProtectedRoute>
                <Layout>
                  <TranslatorPage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* PREDICTION */}
          <Route
            path="/prediction"
            element={
              <ProtectedRoute>
                <Layout>
                  <Prediction />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* RISK */}
          <Route
            path="/risk"
            element={
              <ProtectedRoute>
                <Layout>
                  <Risk />
                </Layout>
              </ProtectedRoute>
            }
          />

        </Routes>
      </BrowserRouter>
    </LanguageProvider>
  );
}