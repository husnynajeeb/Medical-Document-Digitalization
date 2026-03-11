import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Grid,
  FormControl,
  Select,
  MenuItem,
  FormControlLabel,
  Switch,
  Typography,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Slider,
  Paper,
  Chip,
  Tooltip,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import InfoIcon from "@mui/icons-material/Info";
import axios from "axios";

/**
 * ✅ This version matches your REFERENCE IMAGE layout.
 *
 * IMPORTANT:
 * Your reference image is a "centered card page".
 * This file includes the wrapper (Paper + maxWidth) so it looks the same
 * even inside your sidebar Layout.
 *
 * Layout exactly:
 * Row1: Age(6) + Gender(6)
 * Row2: BMI(6) + HbA1c(6)
 * Row3: Blood Glucose(6) + Hypertension(3) + Heart Disease(3)
 * Row4: Smoking History(12)
 * Row5: Buttons(12)
 *
 * Backend:
 * - Health: GET "/"
 * - Predict: POST "/diabetes/predict"
 * - Auth: Authorization Bearer localStorage("token")
 * - Navigate: "/risk"
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const initialFormData = {
  age: 45,
  gender: "Male",
  bmi: 25,
  HbA1c_level: 5.5,
  blood_glucose_level: 120,
  hypertension: false,
  heart_disease: false,
  smoking_history: "never",
};

// Health status indicators
const getHealthStatus = (value, type) => {
  if (type === "bmi") {
    if (value < 18.5) return { label: "Underweight", color: "#2196f3", emoji: "⚖️" };
    if (value < 25) return { label: "Normal", color: "#4caf50", emoji: "✅" };
    if (value < 30) return { label: "Overweight", color: "#ff9800", emoji: "⚠️" };
    return { label: "Obese", color: "#f44336", emoji: "🔴" };
  }
  if (type === "hba1c") {
    if (value < 5.7) return { label: "Normal", color: "#4caf50", emoji: "✅" };
    if (value < 6.5) return { label: "Prediabetes", color: "#ff9800", emoji: "⚠️" };
    return { label: "Diabetes", color: "#f44336", emoji: "🔴" };
  }
  if (type === "glucose") {
    if (value < 100) return { label: "Normal", color: "#4caf50", emoji: "✅" };
    if (value < 126) return { label: "Prediabetes", color: "#ff9800", emoji: "⚠️" };
    return { label: "Diabetes", color: "#f44336", emoji: "🔴" };
  }
  return null;
};

const ValueLabelComponent = ({ children, open, value }) => {
  return (
    <Tooltip open={open} enterTouchDelay={0} placement="top" title={value}>
      {children}
    </Tooltip>
  );
};

export default function PredictionForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState(initialFormData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState(null);

  // Check API health on mount
  useEffect(() => {
    const checkApiHealth = async () => {
      try {
        await axios.get(`${API_BASE_URL}/`, { timeout: 3000 });
        setApiStatus("connected");
      } catch (err) {
        setApiStatus("disconnected");
      }
    };
    checkApiHealth();
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSliderChange = (name) => (event, newValue) => {
    setFormData((prev) => ({
      ...prev,
      [name]: newValue,
    }));
  };

  const handleReset = () => {
    setFormData(initialFormData);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/login");
        return;
      }

      const apiData = {
        age: formData.age,
        gender: formData.gender,
        bmi: formData.bmi,
        HbA1c_level: formData.HbA1c_level,
        blood_glucose_level: formData.blood_glucose_level,
        hypertension: formData.hypertension ? 1 : 0,
        heart_disease: formData.heart_disease ? 1 : 0,
        smoking_history: formData.smoking_history,
      };

      const response = await axios.post(`${API_BASE_URL}/diabetes/predict`, apiData, {
        timeout: 10000,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      sessionStorage.setItem(
        "predictionResults",
        JSON.stringify({
          ...response.data,
          patientData: apiData,
        })
      );

      navigate("/risk");
    } catch (err) {
      console.error("Submission error:", err);

      if (err?.response?.status === 401) {
        localStorage.removeItem("token");
        navigate("/login");
        return;
      }

      if (err.code === "ERR_NETWORK") {
        setError("Cannot connect to the server. Please check if the backend is running.");
      } else if (err.response) {
        setError(err.response.data?.detail || `Server error: ${err.response.status}`);
      } else {
        setError(err.message || "An unexpected error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    // ✅ centered page wrapper like the reference screenshot
    <Box sx={{ width: "100%", display: "flex", justifyContent: "center", py: 2 }}>
      <Paper
        elevation={0}
        sx={{
          width: "100%",
          borderRadius: 4,
          border: "1px solid #e5e7eb",
          p: { xs: 2, sm: 3 },
          bgcolor: "white",
          boxShadow: "0 8px 24px rgba(0,0,0,0.06)",
        }}
      >
        {/* Header */}
        <Box sx={{ textAlign: "center", mb: 4 }}>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: "bold", color: "primary.main" }}>
            🩺 Diabetes Risk Assessment
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 600, mx: "auto" }}>
            Adjust the sliders to input patient information for comprehensive XGBoost-based diabetes risk analysis
          </Typography>
        </Box>

        {/* API Status Alert */}
        {apiStatus === "disconnected" && (
          <Alert severity="warning" sx={{ mb: 3, borderRadius: 2 }}>
            ⚠️ Backend server is not connected. Please ensure the server is running at http://localhost:8000
          </Alert>
        )}
        {apiStatus === "connected" && (
          <Alert severity="success" sx={{ mb: 3, borderRadius: 2 }}>
            ✅ Connected to backend server
          </Alert>
        )}

        {/* Error Alert */}
        {error && (
          <Alert severity="error" sx={{ mb: 3, borderRadius: 2 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            {/* Row 1: Age + Gender */}
            <Grid item xs={12} sm={6}>
              <Card
                variant="outlined"
                sx={{
                  height: "100%",
                  borderRadius: 3,
                  border: "1px solid #e5e7eb",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
                }}
              >
                <CardContent>
                  <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 2 }}>
                    <Typography variant="h6" color="primary">
                      Age (years)
                    </Typography>
                    <Chip label={`${formData.age} years`} color="primary" variant="outlined" size="small" />
                  </Box>

                  <Box sx={{ px: 1 }}>
                    <Slider
                      value={formData.age}
                      onChange={handleSliderChange("age")}
                      min={0}
                      max={100}
                      step={1}
                      valueLabelDisplay="auto"
                      marks={[
                        { value: 0, label: "0" },
                        { value: 25, label: "25" },
                        { value: 50, label: "50" },
                        { value: 75, label: "75" },
                        { value: 100, label: "100" },
                      ]}
                      sx={{ mt: 2 }}
                    />
                  </Box>

                  <Box sx={{ display: "flex", justifyContent: "space-between", mt: 1, px: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      Young
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Elderly
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Card
                variant="outlined"
                sx={{
                  height: "100%",
                  borderRadius: 3,
                  border: "1px solid #e5e7eb",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
                }}
              >
                <CardContent>
                  <Typography variant="h6" color="primary" gutterBottom>
                    Gender
                  </Typography>

                  <FormControl fullWidth sx={{ mt: 2 }}>
                    <Select name="gender" value={formData.gender} onChange={handleChange} variant="outlined" size="medium">
                      <MenuItem value="Male">Male</MenuItem>
                      <MenuItem value="Female">Female</MenuItem>
                      <MenuItem value="Other">Other</MenuItem>
                    </Select>
                  </FormControl>
                </CardContent>
              </Card>
            </Grid>

            {/* Row 2: BMI + HbA1c */}
            <Grid item xs={12} sm={6}>
              <Card
                variant="outlined"
                sx={{
                  height: "100%",
                  borderRadius: 3,
                  border: "1px solid #e5e7eb",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
                }}
              >
                <CardContent>
                  <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 2 }}>
                    <Typography variant="h6" color="primary">
                      Body Mass Index (BMI)
                    </Typography>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      <Chip
                        label={getHealthStatus(formData.bmi, "bmi")?.label}
                        size="small"
                        sx={{ bgcolor: getHealthStatus(formData.bmi, "bmi")?.color, color: "white" }}
                      />
                      <Chip label={`${formData.bmi}`} color="primary" variant="outlined" size="small" />
                    </Box>
                  </Box>

                  <Box sx={{ px: 1 }}>
                    <Slider
                      value={formData.bmi}
                      onChange={handleSliderChange("bmi")}
                      min={10}
                      max={50}
                      step={0.1}
                      valueLabelDisplay="auto"
                      marks={[
                        { value: 10, label: "10" },
                        { value: 20, label: "20" },
                        { value: 30, label: "30" },
                        { value: 40, label: "40" },
                        { value: 50, label: "50" },
                      ]}
                      sx={{
                        mt: 2,
                        "& .MuiSlider-markLabel": { fontSize: "0.75rem" },
                      }}
                    />
                  </Box>

                  <Box sx={{ display: "flex", justifyContent: "space-between", mt: 2 }}>
                    <Chip label="Normal" size="small" sx={{ bgcolor: "#4caf50", color: "white", fontSize: "0.7rem" }} />
                    <Chip label="Prediabetes" size="small" sx={{ bgcolor: "#ff9800", color: "white", fontSize: "0.7rem" }} />
                    <Chip label="Overweight" size="small" sx={{ bgcolor: "#f44336", color: "white", fontSize: "0.7rem" }} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Card
                variant="outlined"
                sx={{
                  height: "100%",
                  borderRadius: 3,
                  border: "1px solid #e5e7eb",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
                }}
              >
                <CardContent>
                  <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 2 }}>
                    <Typography variant="h6" color="primary">
                      HbA1c Level (%)
                    </Typography>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      <Chip
                        label={getHealthStatus(formData.HbA1c_level, "hba1c")?.label}
                        size="small"
                        sx={{ bgcolor: getHealthStatus(formData.HbA1c_level, "hba1c")?.color, color: "white" }}
                      />
                      <Chip label={`${formData.HbA1c_level}%`} color="primary" variant="outlined" size="small" />
                    </Box>
                  </Box>

                  <Box sx={{ px: 1 }}>
                    <Slider
                      value={formData.HbA1c_level}
                      onChange={handleSliderChange("HbA1c_level")}
                      min={3.0}
                      max={15.0}
                      step={0.1}
                      valueLabelDisplay="auto"
                      marks={[
                        { value: 3.0, label: "3.0" },
                        { value: 5.5, label: "5.5" },
                        { value: 8.5, label: "8.5" },
                        { value: 13.9, label: "13.9" },
                        { value: 15.0, label: "15.0" },
                      ]}
                      sx={{ mt: 2 }}
                    />
                  </Box>

                  <Box sx={{ display: "flex", justifyContent: "space-between", mt: 2 }}>
                    <Chip label="Normal" size="small" sx={{ bgcolor: "#4caf50", color: "white", fontSize: "0.7rem" }} />
                    <Chip label="Prediabetes" size="small" sx={{ bgcolor: "#ff9800", color: "white", fontSize: "0.7rem" }} />
                    <Chip label="Diabetes" size="small" sx={{ bgcolor: "#f44336", color: "white", fontSize: "0.7rem" }} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Row 3: Glucose (6) + Hypertension (3) + Heart Disease (3) */}
            <Grid item xs={12} sm={6}>
              <Card
                variant="outlined"
                sx={{
                  height: "100%",
                  borderRadius: 3,
                  border: "1px solid #e5e7eb",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
                }}
              >
                <CardContent>
                  <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 2 }}>
                    <Typography variant="h6" color="primary">
                      Blood Glucose (mg/dL)
                    </Typography>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      <Chip
                        label={getHealthStatus(formData.blood_glucose_level, "glucose")?.label}
                        size="small"
                        sx={{ bgcolor: getHealthStatus(formData.blood_glucose_level, "glucose")?.color, color: "white" }}
                      />
                      <Chip label={`${formData.blood_glucose_level}`} color="primary" variant="outlined" size="small" />
                    </Box>
                  </Box>

                  <Box sx={{ px: 1 }}>
                    <Slider
                      value={formData.blood_glucose_level}
                      onChange={handleSliderChange("blood_glucose_level")}
                      min={50}
                      max={400}
                      step={1}
                      valueLabelDisplay="auto"
                      marks={[
                        { value: 120, label: "120" },
                        { value: 150, label: "150" },
                        { value: 250, label: "250" },
                        { value: 350, label: "350" },
                        { value: 400, label: "400" },
                      ]}
                      sx={{ mt: 2 }}
                    />
                  </Box>

                  <Box sx={{ display: "flex", justifyContent: "space-between", mt: 2 }}>
                    <Chip label="Normal" size="small" sx={{ bgcolor: "#4caf50", color: "white", fontSize: "0.7rem" }} />
                    <Chip label="Prediabetes" size="small" sx={{ bgcolor: "#ff9800", color: "white", fontSize: "0.7rem" }} />
                    <Chip label="Diabetes" size="small" sx={{ bgcolor: "#f44336", color: "white", fontSize: "0.7rem" }} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={3}>
              <Card
                variant="outlined"
                sx={{
                  height: "100%",
                  borderRadius: 3,
                  border: "1px solid #e5e7eb",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
                }}
              >
                <CardContent>
                  <Typography variant="h6" color="primary" gutterBottom>
                    Hypertension
                  </Typography>

                  <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
                    <FormControlLabel
                      control={<Switch name="hypertension" checked={formData.hypertension} onChange={handleChange} color="primary" size="medium" />}
                      label={formData.hypertension ? "Yes" : "No"}
                      labelPlacement="bottom"
                    />
                  </Box>

                  <Box sx={{ display: "flex", justifyContent: "space-between", mt: 2 }}>
                    <Chip label="No" size="small" variant={!formData.hypertension ? "filled" : "outlined"} color={!formData.hypertension ? "success" : "default"} />
                    <Chip label="Yes" size="small" variant={formData.hypertension ? "filled" : "outlined"} color={formData.hypertension ? "error" : "default"} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={3}>
              <Card
                variant="outlined"
                sx={{
                  height: "100%",
                  borderRadius: 3,
                  border: "1px solid #e5e7eb",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
                }}
              >
                <CardContent>
                  <Typography variant="h6" color="primary" gutterBottom>
                    Heart Disease
                  </Typography>

                  <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
                    <FormControlLabel
                      control={<Switch name="heart_disease" checked={formData.heart_disease} onChange={handleChange} color="primary" size="medium" />}
                      label={formData.heart_disease ? "Yes" : "No"}
                      labelPlacement="bottom"
                    />
                  </Box>

                  <Box sx={{ display: "flex", justifyContent: "space-between", mt: 2 }}>
                    <Chip label="No" size="small" variant={!formData.heart_disease ? "filled" : "outlined"} color={!formData.heart_disease ? "success" : "default"} />
                    <Chip label="Yes" size="small" variant={formData.heart_disease ? "filled" : "outlined"} color={formData.heart_disease ? "error" : "default"} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Row 4: Smoking full width */}
            <Grid item xs={12}>
              <Card
                variant="outlined"
                sx={{
                  height: "100%",
                  borderRadius: 3,
                  border: "1px solid #e5e7eb",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
                }}
              >
                <CardContent>
                  <Typography variant="h6" color="primary" gutterBottom>
                    Smoking History
                  </Typography>

                  <FormControl fullWidth sx={{ mt: 1 }}>
                    <Select name="smoking_history" value={formData.smoking_history} onChange={handleChange} variant="outlined">
                      <MenuItem value="never">🚭 Never Smoked</MenuItem>
                      <MenuItem value="former">🚬 Former Smoker</MenuItem>
                      <MenuItem value="current">🔥 Current Smoker</MenuItem>
                    </Select>
                  </FormControl>

                  <Box sx={{ display: "flex", justifyContent: "space-between", mt: 2 }}>
                    <Chip label="No" size="small" variant={formData.smoking_history === "never" ? "filled" : "outlined"} color={formData.smoking_history === "never" ? "success" : "default"} />
                    <Chip label="Yes" size="small" variant={formData.smoking_history !== "never" ? "filled" : "outlined"} color={formData.smoking_history !== "never" ? "error" : "default"} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Buttons */}
            <Grid item xs={12}>
              <Box sx={{ display: "flex", gap: 2, justifyContent: "center", mt: 2, flexWrap: "wrap" }}>
                <Button
                  type="submit"
                  variant="contained"
                  size="large"
                  disabled={loading || apiStatus !== "connected"}
                  startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
                  sx={{ minWidth: 200 }}
                >
                  {loading ? "Processing..." : "Assess Risk"}
                </Button>

                <Button type="button" variant="outlined" size="large" onClick={handleReset} startIcon={<RestartAltIcon />} sx={{ minWidth: 200 }}>
                  Reset Form
                </Button>
              </Box>
            </Grid>
          </Grid>
        </form>

        {/* Info Card */}
        <Card
          sx={{
            mt: 3,
            bgcolor: "#f5f5f5",
            borderRadius: 3,
            border: "1px solid #e5e7eb",
            boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
          }}
        >
          <CardContent>
            <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 1 }}>
              <InfoIcon color="info" />
              <Typography variant="h6">About This Assessment</Typography>
            </Box>
            <Typography variant="body2" color="text.secondary">
              This tool uses an XGBoost machine learning model trained on 100,000+ patient records to provide accurate diabetes risk predictions. The analysis considers 10 different risk categories including cardiovascular, kidney, eye, and nerve health.
            </Typography>
          </CardContent>
        </Card>
      </Paper>
    </Box>
  );
}