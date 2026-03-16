import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import EmployeeDetail from './pages/EmployeeDetail'
import MyScore from './pages/MyScore'

function PrivateRoute({ children, requiredRole }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" />
  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to={user.role === 'admin' ? '/dashboard' : '/my-score'} />
  }
  return children
}

function AppRoutes() {
  const { user } = useAuth()
  return (
    <Routes>
      <Route
        path="/login"
        element={
          user
            ? <Navigate to={user.role === 'admin' ? '/dashboard' : '/my-score'} />
            : <Login />
        }
      />
      <Route
        path="/dashboard"
        element={
          <PrivateRoute requiredRole="admin"><Dashboard /></PrivateRoute>
        }
      />
      <Route
        path="/employee/:id"
        element={
          <PrivateRoute requiredRole="admin"><EmployeeDetail /></PrivateRoute>
        }
      />
      <Route
        path="/my-score"
        element={
          <PrivateRoute requiredRole="employee"><MyScore /></PrivateRoute>
        }
      />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}
