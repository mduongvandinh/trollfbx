import { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, Eye, Heart, MessageCircle, Share2, Users, Calendar, Award } from 'lucide-react';

const API_URL = 'http://localhost:8000';

interface Analytics {
  total_posts: number;
  total_reach: number;
  total_engagement: number;
  avg_engagement_rate: number;
  top_posts: PostAnalytics[];
  recent_posts: PostAnalytics[];
  engagement_by_day: DayEngagement[];
}

interface PostAnalytics {
  id: number;
  caption: string;
  posted_time: string;
  reach: number;
  impressions: number;
  likes: number;
  comments: number;
  shares: number;
  engagement_rate: number;
}

interface DayEngagement {
  date: string;
  posts: number;
  total_engagement: number;
}

interface ContentStats {
  total_drafts: number;
  total_scheduled: number;
  total_posted: number;
  total_failed: number;
}

export default function Analytics() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [contentStats, setContentStats] = useState<ContentStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState<'7days' | '30days' | '90days'>('30days');

  useEffect(() => {
    fetchAnalytics();
    fetchContentStats();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/analytics/overview?days=${parseInt(timeRange)}`);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchContentStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/analytics/content-stats`);
      setContentStats(response.data);
    } catch (error) {
      console.error('Error fetching content stats:', error);
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Đang tải dữ liệu...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Thống Kê</h1>

        <div className="flex items-center gap-2 bg-white rounded-lg border border-gray-200 p-1">
          <button
            onClick={() => setTimeRange('7days')}
            className={`px-4 py-2 rounded text-sm ${timeRange === '7days' ? 'bg-blue-500 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            7 ngày
          </button>
          <button
            onClick={() => setTimeRange('30days')}
            className={`px-4 py-2 rounded text-sm ${timeRange === '30days' ? 'bg-blue-500 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            30 ngày
          </button>
          <button
            onClick={() => setTimeRange('90days')}
            className={`px-4 py-2 rounded text-sm ${timeRange === '90days' ? 'bg-blue-500 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            90 ngày
          </button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <div className="text-gray-600 text-sm font-medium">Tổng Bài Đăng</div>
            <Calendar className="w-5 h-5 text-blue-500" />
          </div>
          <div className="text-3xl font-bold text-gray-900">{analytics?.total_posts || 0}</div>
          <div className="text-sm text-gray-500 mt-1">Trong {timeRange === '7days' ? '7' : timeRange === '30days' ? '30' : '90'} ngày</div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <div className="text-gray-600 text-sm font-medium">Tổng Tiếp Cận</div>
            <Eye className="w-5 h-5 text-green-500" />
          </div>
          <div className="text-3xl font-bold text-gray-900">{formatNumber(analytics?.total_reach || 0)}</div>
          <div className="text-sm text-gray-500 mt-1">Người dùng đã xem</div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <div className="text-gray-600 text-sm font-medium">Tương Tác</div>
            <Heart className="w-5 h-5 text-red-500" />
          </div>
          <div className="text-3xl font-bold text-gray-900">{formatNumber(analytics?.total_engagement || 0)}</div>
          <div className="text-sm text-gray-500 mt-1">Likes, comments, shares</div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <div className="text-gray-600 text-sm font-medium">Tỷ Lệ Tương Tác</div>
            <TrendingUp className="w-5 h-5 text-purple-500" />
          </div>
          <div className="text-3xl font-bold text-gray-900">{(analytics?.avg_engagement_rate || 0).toFixed(1)}%</div>
          <div className="text-sm text-gray-500 mt-1">Trung bình</div>
        </div>
      </div>

      {/* Content Status */}
      {contentStats && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-semibold mb-4">Trạng Thái Nội Dung</h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-3xl font-bold text-gray-700">{contentStats.total_drafts}</div>
              <div className="text-sm text-gray-600 mt-1">Bài Nháp</div>
            </div>

            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-3xl font-bold text-blue-700">{contentStats.total_scheduled}</div>
              <div className="text-sm text-blue-600 mt-1">Đã Lên Lịch</div>
            </div>

            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-3xl font-bold text-green-700">{contentStats.total_posted}</div>
              <div className="text-sm text-green-600 mt-1">Đã Đăng</div>
            </div>

            <div className="text-center p-4 bg-red-50 rounded-lg">
              <div className="text-3xl font-bold text-red-700">{contentStats.total_failed}</div>
              <div className="text-sm text-red-600 mt-1">Thất Bại</div>
            </div>
          </div>
        </div>
      )}

      {/* Top Performing Posts */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Award className="w-5 h-5 text-yellow-500" />
          Bài Đăng Hiệu Quả Nhất
        </h2>

        {!analytics || analytics.top_posts.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Chưa có dữ liệu analytics từ Facebook</p>
        ) : (
          <div className="space-y-4">
            {analytics.top_posts.slice(0, 5).map((post, index) => (
              <div
                key={post.id}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold">
                    #{index + 1}
                  </div>

                  <div className="flex-1">
                    <p className="text-sm text-gray-700 mb-3 line-clamp-2">{post.caption}</p>

                    <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-sm">
                      <div className="flex items-center gap-1 text-gray-600">
                        <Eye className="w-4 h-4" />
                        <span>{formatNumber(post.reach)}</span>
                      </div>

                      <div className="flex items-center gap-1 text-red-600">
                        <Heart className="w-4 h-4" />
                        <span>{formatNumber(post.likes)}</span>
                      </div>

                      <div className="flex items-center gap-1 text-blue-600">
                        <MessageCircle className="w-4 h-4" />
                        <span>{formatNumber(post.comments)}</span>
                      </div>

                      <div className="flex items-center gap-1 text-green-600">
                        <Share2 className="w-4 h-4" />
                        <span>{formatNumber(post.shares)}</span>
                      </div>

                      <div className="flex items-center gap-1 text-purple-600 font-semibold">
                        <TrendingUp className="w-4 h-4" />
                        <span>{post.engagement_rate.toFixed(1)}%</span>
                      </div>
                    </div>

                    <div className="text-xs text-gray-500 mt-2">
                      Đăng lúc: {new Date(post.posted_time).toLocaleString('vi-VN')}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recent Posts */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold mb-4">Bài Đăng Gần Đây</h2>

        {!analytics || analytics.recent_posts.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Chưa có bài đăng nào được đăng</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Caption</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Tiếp cận</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Likes</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Comments</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Shares</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Tỷ lệ</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Thời gian</th>
                </tr>
              </thead>
              <tbody>
                {analytics.recent_posts.map(post => (
                  <tr key={post.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 text-sm text-gray-700 max-w-xs truncate">{post.caption}</td>
                    <td className="py-3 px-4 text-sm text-center text-gray-700">{formatNumber(post.reach)}</td>
                    <td className="py-3 px-4 text-sm text-center text-red-600">{formatNumber(post.likes)}</td>
                    <td className="py-3 px-4 text-sm text-center text-blue-600">{formatNumber(post.comments)}</td>
                    <td className="py-3 px-4 text-sm text-center text-green-600">{formatNumber(post.shares)}</td>
                    <td className="py-3 px-4 text-sm text-center text-purple-600 font-semibold">{post.engagement_rate.toFixed(1)}%</td>
                    <td className="py-3 px-4 text-sm text-gray-500">
                      {new Date(post.posted_time).toLocaleDateString('vi-VN')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Info Note */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <strong>Lưu ý:</strong> Dữ liệu analytics sẽ được cập nhật tự động từ Facebook khi bạn kích hoạt tích hợp Facebook và đăng bài.
          Hiện tại bạn đang ở chế độ thử nghiệm với dữ liệu mẫu.
        </p>
      </div>
    </div>
  );
}
