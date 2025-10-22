import { useEffect, useState } from 'react'
import { TrendingUp, Users, MessageSquare, Share2, Clock } from 'lucide-react'
import axios from 'axios'

interface Stats {
  total_posts: number
  total_reach: number
  total_engagement: number
  avg_engagement_rate: number
  best_post: any
  recent_posts: any[]
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardStats()
  }, [])

  const fetchDashboardStats = async () => {
    try {
      const response = await axios.get('/api/analytics/dashboard?days=7')
      setStats(response.data)
    } catch (error) {
      console.error('Error fetching dashboard stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">Đang tải dữ liệu...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Tổng quan hoạt động 7 ngày qua</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Tổng Bài Đăng"
          value={stats?.total_posts || 0}
          icon={<Clock className="text-blue-500" />}
          color="blue"
        />
        <StatCard
          title="Tổng Reach"
          value={formatNumber(stats?.total_reach || 0)}
          icon={<Users className="text-green-500" />}
          color="green"
        />
        <StatCard
          title="Tương Tác"
          value={formatNumber(stats?.total_engagement || 0)}
          icon={<MessageSquare className="text-purple-500" />}
          color="purple"
        />
        <StatCard
          title="Engagement Rate"
          value={`${stats?.avg_engagement_rate.toFixed(2) || 0}%`}
          icon={<TrendingUp className="text-orange-500" />}
          color="orange"
        />
      </div>

      {/* Best Post */}
      {stats?.best_post && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Share2 className="text-yellow-500" />
            Bài Đăng Hiệu Quả Nhất
          </h2>
          <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg p-6">
            <h3 className="font-semibold text-lg mb-3">{stats.best_post.title}</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-gray-600">Reach</p>
                <p className="text-xl font-bold">{formatNumber(stats.best_post.reach)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Likes</p>
                <p className="text-xl font-bold">{formatNumber(stats.best_post.likes)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Comments</p>
                <p className="text-xl font-bold">{formatNumber(stats.best_post.comments)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Engagement Rate</p>
                <p className="text-xl font-bold">{stats.best_post.engagement_rate.toFixed(2)}%</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Recent Posts */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold mb-4">Bài Đăng Gần Đây</h2>
        <div className="space-y-3">
          {stats?.recent_posts.map((post) => (
            <div
              key={post.id}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div>
                <h3 className="font-medium">{post.title || 'Untitled'}</h3>
                <p className="text-sm text-gray-600">
                  {post.posted_time ? new Date(post.posted_time).toLocaleString('vi-VN') : 'N/A'}
                </p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600">Reach: {formatNumber(post.reach)}</p>
                <p className="text-sm font-semibold text-primary">
                  {post.engagement_rate.toFixed(2)}% engagement
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold mb-4">Hành Động Nhanh</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <QuickActionButton
            label="Tạo Meme Mới"
            onClick={() => window.location.href = '/create'}
            color="blue"
          />
          <QuickActionButton
            label="Xem Tin Tức"
            onClick={() => window.location.href = '/news'}
            color="green"
          />
          <QuickActionButton
            label="Lên Lịch Đăng"
            onClick={() => window.location.href = '/calendar'}
            color="purple"
          />
        </div>
      </div>
    </div>
  )
}

function StatCard({ title, value, icon, color }: any) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-gray-600 text-sm font-medium">{title}</h3>
        {icon}
      </div>
      <p className="text-3xl font-bold text-gray-900">{value}</p>
    </div>
  )
}

function QuickActionButton({ label, onClick, color }: any) {
  return (
    <button
      onClick={onClick}
      className={`w-full py-3 px-4 bg-${color}-500 hover:bg-${color}-600 text-white font-medium rounded-lg transition-colors`}
    >
      {label}
    </button>
  )
}

function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}
