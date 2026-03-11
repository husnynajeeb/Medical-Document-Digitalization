import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Button,
  LinearProgress,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Tab,
  Tabs,
} from '@mui/material'
import {
  TrendingUp,
  Warning,
  CheckCircle,
  LocalHospital,
  Restaurant,
  FitnessCenter,
  Medication,
} from '@mui/icons-material'
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

const getRiskColor = (level) => {
  switch (level?.toLowerCase()) {
    case 'high':
    case 'very high':
      return '#f44336'
    case 'medium':
    case 'moderate':
      return '#ff9800'
    case 'low':
    case 'low to moderate':
      return '#4caf50'
    default:
      return '#9e9e9e'
  }
}

const getRiskIcon = (level) => {
  switch (level?.toLowerCase()) {
    case 'high':
    case 'very high':
      return <Warning sx={{ color: '#f44336' }} />
    case 'medium':
    case 'moderate':
      return <TrendingUp sx={{ color: '#ff9800' }} />
    case 'low':
    case 'low to moderate':
      return <CheckCircle sx={{ color: '#4caf50' }} />
    default:
      return null
  }
}

const TabPanel = ({ children, value, index }) => (
  <div hidden={value !== index}>
    {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
  </div>
)

const getRecommendationType = (rec = '') => {
  if (rec.startsWith('🔴')) return 'section-red'
  if (rec.startsWith('🟡')) return 'section-yellow'
  if (rec.startsWith('🟢')) return 'section-green'
  if (rec.startsWith('✅')) return 'boxed-header'
  if (rec.startsWith('📅')) return 'boxed-header'
  if (rec.startsWith('🌱')) return 'boxed-header'
  if (rec.startsWith('💡')) return 'boxed-header'
  if (rec.startsWith('🍽️')) return 'boxed-header'
  if (rec.startsWith('⚖️')) return 'section-plain'
  return 'item'
}

const renderRecommendationRow = (rec, index) => {
  const type = getRecommendationType(rec)

  if (type === 'section-red') {
    return (
      <Box key={index} sx={{ mt: index === 0 ? 0 : 3, mb: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
        <Box
          sx={{
            width: 18,
            height: 18,
            borderRadius: '50%',
            bgcolor: '#f44336',
            border: '1px solid #000',
            flexShrink: 0,
          }}
        />
        <Typography sx={{ color: '#1565c0', fontSize: '2rem', fontWeight: 500 }}>
          {rec.replace('🔴', '').trim()}
        </Typography>
      </Box>
    )
  }

  if (type === 'section-yellow') {
    return (
      <Box key={index} sx={{ mt: 3, mb: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
        <Box
          sx={{
            width: 18,
            height: 18,
            borderRadius: '50%',
            bgcolor: '#ffeb3b',
            border: '1px solid #000',
            flexShrink: 0,
          }}
        />
        <Typography sx={{ color: '#1565c0', fontSize: '2rem', fontWeight: 500 }}>
          {rec.replace('🟡', '').trim()}
        </Typography>
      </Box>
    )
  }

  if (type === 'section-green') {
    return (
      <Box key={index} sx={{ mt: 3, mb: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
        <Box
          sx={{
            width: 18,
            height: 18,
            borderRadius: '50%',
            bgcolor: '#4caf50',
            border: '1px solid #000',
            flexShrink: 0,
          }}
        />
        <Typography sx={{ color: '#1565c0', fontSize: '2rem', fontWeight: 500 }}>
          {rec.replace('🟢', '').trim()}
        </Typography>
      </Box>
    )
  }

  if (type === 'section-plain') {
    return (
      <Box key={index} sx={{ mt: 3, mb: 1 }}>
        <Typography sx={{ color: '#1565c0', fontSize: '2rem', fontWeight: 500 }}>
          {rec}
        </Typography>
      </Box>
    )
  }

  if (type === 'boxed-header') {
    return (
      <Paper
        key={index}
        variant="outlined"
        sx={{
          p: 1.5,
          mb: 2,
          borderRadius: 1,
          bgcolor: '#fff',
        }}
      >
        <Typography variant="body1">{rec}</Typography>
      </Paper>
    )
  }

  return (
    <Paper
      key={index}
      variant="outlined"
      sx={{
        p: 1.5,
        mb: 2,
        borderRadius: 1,
        bgcolor: '#fff',
      }}
    >
      <Typography variant="body1">{rec}</Typography>
    </Paper>
  )
}

const Results = () => {
  const navigate = useNavigate()
  const [results, setResults] = useState(null)
  const [tabValue, setTabValue] = useState(0)

  useEffect(() => {
    const storedResults = sessionStorage.getItem('predictionResults')
    if (storedResults) {
      setResults(JSON.parse(storedResults))
    } else {
      navigate('/predict')
    }
  }, [navigate])

  if (!results) {
    return <LinearProgress />
  }

  const {
    diabetes_probability,
    diabetes_prediction,
    risk_assessment,
    risk_breakdown,
    recommendations,
    patientData,
    processing_time,
    model_type,
  } = results

  const pieData =
    risk_breakdown?.map((risk) => ({
      name: risk.type,
      value: risk.score,
      level: risk.level,
    })) || []

  const COLORS = ['#f44336', '#ff9800', '#4caf50', '#2196f3', '#9c27b0']

  const riskCounts = risk_assessment?.risk_counts || {
    High: 0,
    Medium: 0,
    Low: 0,
    None: 0,
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom align="center">
        Risk Assessment Results
      </Typography>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card sx={{ bgcolor: getRiskColor(risk_assessment?.overall_risk), color: 'white' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                {getRiskIcon(risk_assessment?.overall_risk)}
                <Typography variant="h6">Overall Risk</Typography>
              </Box>
              <Typography variant="h3" gutterBottom>
                {risk_assessment?.overall_risk}
              </Typography>
              <Typography variant="body2">Score: {risk_assessment?.overall_score}/30</Typography>
              <Typography variant="body2">{risk_assessment?.urgency}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Diabetes Prediction
              </Typography>
              <Typography variant="h4" color={diabetes_probability > 0.5 ? '#f44336' : '#4caf50'}>
                {diabetes_prediction}
              </Typography>
              <Typography variant="body1">
                Probability: {(diabetes_probability * 100).toFixed(1)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={diabetes_probability * 100}
                sx={{ mt: 2, height: 10, borderRadius: 5 }}
                color={diabetes_probability > 0.5 ? 'error' : 'success'}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Risk Summary
              </Typography>
              <Grid container spacing={1}>
                {Object.entries(riskCounts).map(([level, count]) =>
                  count > 0 ? (
                    <Grid item xs={6} key={level}>
                      <Chip
                        label={`${level}: ${count}`}
                        sx={{
                          bgcolor: getRiskColor(level),
                          color: 'white',
                          width: '100%',
                        }}
                      />
                    </Grid>
                  ) : null
                )}
              </Grid>
              <Typography variant="caption" display="block" sx={{ mt: 2 }}>
                Model: {model_type} | Time: {processing_time}s
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
          <Tab label="Risk Breakdown" />
          <Tab label="Recommendations" />
          <Tab label="Patient Data" />
          <Tab label="Visualizations" />
        </Tabs>
      </Box>

      {/* Risk Breakdown Tab */}
      <TabPanel value={tabValue} index={0}>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow sx={{ bgcolor: 'primary.main' }}>
                <TableCell sx={{ color: 'white' }}>Risk Type</TableCell>
                <TableCell sx={{ color: 'white' }}>Level</TableCell>
                <TableCell sx={{ color: 'white' }} align="center">
                  Score
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {risk_breakdown?.map((risk, index) => (
                <TableRow key={index}>
                  <TableCell>{risk.type}</TableCell>
                  <TableCell>
                    <Chip
                      label={risk.level}
                      size="small"
                      sx={{
                        bgcolor: getRiskColor(risk.level),
                        color: 'white',
                        minWidth: 80,
                      }}
                    />
                  </TableCell>
                  <TableCell align="center">{risk.score}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      {/* Recommendations Tab */}
      <TabPanel value={tabValue} index={1}>
        <Box sx={{ bgcolor: '#f5f5f5', p: 2, borderRadius: 1 }}>
          {recommendations?.map((rec, index) => renderRecommendationRow(rec, index))}
        </Box>
      </TabPanel>

      {/* Patient Data Tab */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Patient Information
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <Table size="small">
                  <TableBody>
                    <TableRow>
                      <TableCell><strong>Age</strong></TableCell>
                      <TableCell>{patientData?.age} years</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Gender</strong></TableCell>
                      <TableCell>{patientData?.gender}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>BMI</strong></TableCell>
                      <TableCell>{patientData?.bmi}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>HbA1c</strong></TableCell>
                      <TableCell>{patientData?.HbA1c_level}%</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Blood Glucose</strong></TableCell>
                      <TableCell>{patientData?.blood_glucose_level} mg/dL</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Hypertension</strong></TableCell>
                      <TableCell>{patientData?.hypertension ? 'Yes' : 'No'}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Heart Disease</strong></TableCell>
                      <TableCell>{patientData?.heart_disease ? 'Yes' : 'No'}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Smoking History</strong></TableCell>
                      <TableCell>{patientData?.smoking_history}</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Quick Actions
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <Button
                    variant="contained"
                    startIcon={<LocalHospital />}
                    fullWidth
                    onClick={() => window.open('https://www.google.com/maps/search/endocrinologist+near+me', '_blank')}
                  >
                    Find Endocrinologist
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<Restaurant />}
                    fullWidth
                    onClick={() => window.open('https://www.diabetes.org/healthy-living/recipes-nutrition', '_blank')}
                  >
                    Healthy Recipes
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<FitnessCenter />}
                    fullWidth
                    onClick={() => window.open('https://www.diabetes.org/healthy-living/fitness', '_blank')}
                  >
                    Exercise Guidelines
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<Medication />}
                    fullWidth
                    onClick={() => window.open('https://www.diabetes.org/diabetes/medication-management', '_blank')}
                  >
                    Medication Info
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Visualizations Tab */}
      <TabPanel value={tabValue} index={3}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom align="center">
                  Risk Distribution
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom align="center">
                  Risk Levels by Category
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={pieData}>
                    <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="value" fill="#1976d2" name="Risk Score" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mt: 4 }}>
        <Button variant="contained" size="large" onClick={() => navigate('/predict')}>
          New Assessment
        </Button>
        <Button variant="outlined" size="large" onClick={() => window.print()}>
          Print Report
        </Button>
      </Box>
    </Box>
  )
}

export default Results