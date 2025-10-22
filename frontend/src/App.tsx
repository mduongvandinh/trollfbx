import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import {
  Home,
  Newspaper,
  Image,
  Video,
  Calendar,
  BarChart3,
  Facebook,
  DollarSign,
  Settings,
  TrendingUp,
  Sparkles
} from 'lucide-react'

// Pages
import Dashboard from './pages/Dashboard'
import NewsPage from './pages/NewsPage'
import ContentCreator from './pages/ContentCreator'
import VideoMemeCreator from './pages/VideoMemeCreator'
import ContentCalendar from './pages/ContentCalendar'
import Analytics from './pages/Analytics'
import SocialMedia from './pages/SocialMedia'
import Monetization from './pages/Monetization'
import SettingsPage from './pages/SettingsPage'
import TrendsPage from './pages/TrendsPage'
import MemeLibrary from './pages/MemeLibrary'

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        <Toaster position="top-right" />

        {/* Sidebar */}
        <aside className="w-64 bg-white shadow-lg">
          <div className="p-6">
            <h1 className="text-2xl font-bold text-primary">⚽ Football Meme</h1>
            <p className="text-sm text-gray-500">Super App</p>
          </div>

          <nav className="mt-6">
            <NavItem to="/" icon={<Home size={20} />} label="Dashboard" />
            <NavItem to="/trends" icon={<TrendingUp size={20} />} label="🔥 AI Trends" />
            <NavItem to="/meme-library" icon={<Sparkles size={20} />} label="🎨 Meme Library" />
            <NavItem to="/news" icon={<Newspaper size={20} />} label="Tin Tức" />
            <NavItem to="/create" icon={<Image size={20} />} label="Tạo Nội Dung" />
            <NavItem to="/video-meme" icon={<Video size={20} />} label="Video Meme" />
            <NavItem to="/calendar" icon={<Calendar size={20} />} label="Lịch Đăng Bài" />
            <NavItem to="/analytics" icon={<BarChart3 size={20} />} label="Thống Kê" />
            <NavItem to="/social" icon={<Facebook size={20} />} label="Facebook" />
            <NavItem to="/monetization" icon={<DollarSign size={20} />} label="Kiếm Tiền" />
            <NavItem to="/settings" icon={<Settings size={20} />} label="Cài Đặt" />
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/trends" element={<TrendsPage />} />
            <Route path="/meme-library" element={<MemeLibrary />} />
            <Route path="/news" element={<NewsPage />} />
            <Route path="/create" element={<ContentCreator />} />
            <Route path="/video-meme" element={<VideoMemeCreator />} />
            <Route path="/calendar" element={<ContentCalendar />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/social" element={<SocialMedia />} />
            <Route path="/monetization" element={<Monetization />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function NavItem({ to, icon, label }: { to: string; icon: React.ReactNode; label: string }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `flex items-center gap-3 px-6 py-3 text-gray-700 hover:bg-blue-50 hover:text-primary transition-colors ${
          isActive ? 'bg-blue-50 text-primary border-r-4 border-primary' : ''
        }`
      }
    >
      {icon}
      <span className="font-medium">{label}</span>
    </NavLink>
  )
}

export default App
