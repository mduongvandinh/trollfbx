import { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { TrendingUp, Activity, Zap, AlertCircle, Clock, ThumbsUp, Loader2, CheckCircle, Sparkles } from 'lucide-react';
import ContentSuggestionsModalSimple from '../components/ContentSuggestionsModalSimple';

interface Trend {
  id: number;
  keyword: string;
  viral_score: number;
  status: string;
  priority: string;
  twitter_mentions: number;
  twitter_velocity: number;
  sentiment_score: number;
  detected_at: string;
}

interface TrendStats {
  total_trends: number;
  active_trends: number;
  high_priority_trends: number;
  average_viral_score: number;
  unread_alerts: number;
}

export default function TrendsPage() {
  const [trends, setTrends] = useState<Trend[]>([]);
  const [stats, setStats] = useState<TrendStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [detecting, setDetecting] = useState(false);
  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [selectedTrend, setSelectedTrend] = useState<Trend | null>(null);

  useEffect(() => {
    loadTrends();
    loadStats();

    // Auto-refresh every 30 seconds
    const interval = setInterval(() => {
      if (!detecting) {
        loadTrends();
        loadStats();
      }
    }, 30000);

    return () => clearInterval(interval);
  }, [detecting]);

  const loadTrends = async (silent = false) => {
    try {
      if (!silent) setLoading(true);
      setError(null);
      const response = await axios.get('http://localhost:8000/api/trends/trending?limit=20');
      setTrends(response.data);
      setLastUpdate(new Date());
    } catch (err: any) {
      console.error('Error loading trends:', err);
      if (!silent) {
        setError('Không thể tải trends. Vui lòng thử lại.');
        toast.error('Không thể tải trends');
      }
    } finally {
      if (!silent) setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/trends/stats');
      setStats(response.data);
    } catch (err: any) {
      console.error('Error loading stats:', err);
    }
  };

  const triggerDetection = async () => {
    setDetecting(true);
    setProgress(0);
    setError(null);

    // Show loading toast
    const toastId = toast.loading('Đang phát hiện trends...');

    try {
      // Step 1: Start detection
      setProgressMessage('🔍 Đang quét Twitter & Reddit...');
      setProgress(20);

      await axios.post('http://localhost:8000/api/trends/detect');

      // Step 2: Wait for processing
      setProgressMessage('🧠 Đang phân tích dữ liệu...');
      setProgress(40);
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Step 3: Calculate scores
      setProgressMessage('🎯 Đang tính viral scores...');
      setProgress(60);
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Step 4: Save to database
      setProgressMessage('💾 Đang lưu kết quả...');
      setProgress(80);
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Step 5: Load results
      setProgressMessage('✅ Hoàn tất! Đang tải kết quả...');
      setProgress(90);
      await loadTrends(true);
      await loadStats();

      setProgress(100);
      setProgressMessage('🎉 Phát hiện trends thành công!');

      // Success notification
      toast.success(
        `Tìm thấy ${trends.length} trending topics!`,
        { id: toastId, duration: 3000 }
      );

      // Auto-hide progress after 2 seconds
      setTimeout(() => {
        setDetecting(false);
        setProgress(0);
        setProgressMessage('');
      }, 2000);

    } catch (err: any) {
      console.error('Error detecting trends:', err);
      setError('Không thể phát hiện trends. Vui lòng thử lại.');
      toast.error('Phát hiện trends thất bại', { id: toastId });
      setDetecting(false);
      setProgress(0);
      setProgressMessage('');
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-red-600';
    if (score >= 60) return 'text-orange-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-gray-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-red-100 border-red-300';
    if (score >= 60) return 'bg-orange-100 border-orange-300';
    if (score >= 40) return 'bg-yellow-100 border-yellow-300';
    return 'bg-gray-100 border-gray-300';
  };

  const getPriorityBadge = (priority: string) => {
    const badges: { [key: string]: { color: string; label: string } } = {
      urgent: { color: 'bg-red-600 text-white', label: '🔥 Urgent' },
      high: { color: 'bg-orange-600 text-white', label: '⚠️ High' },
      normal: { color: 'bg-blue-600 text-white', label: 'Normal' },
      low: { color: 'bg-gray-600 text-white', label: 'Low' }
    };
    return badges[priority] || badges.normal;
  };

  const getStatusBadge = (status: string) => {
    const badges: { [key: string]: { color: string; label: string } } = {
      rising: { color: 'bg-green-100 text-green-800', label: '📈 Rising' },
      peak: { color: 'bg-red-100 text-red-800', label: '🔥 Peak' },
      declining: { color: 'bg-yellow-100 text-yellow-800', label: '📉 Declining' },
      low: { color: 'bg-gray-100 text-gray-800', label: 'Low' }
    };
    return badges[status] || badges.low;
  };

  const formatTimeAgo = (date: Date) => {
    const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);
    if (seconds < 60) return `${seconds} giây trước`;
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes} phút trước`;
    const hours = Math.floor(minutes / 60);
    return `${hours} giờ trước`;
  };

  return (
    <div>
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <TrendingUp className="w-8 h-8 text-blue-600" />
            AI Trend Detector
          </h1>
          <p className="text-gray-600 mt-1 flex items-center gap-2">
            Real-time viral trend monitoring & prediction
            {lastUpdate && (
              <span className="text-sm text-gray-500">
                • Cập nhật {formatTimeAgo(lastUpdate)}
              </span>
            )}
          </p>
        </div>
        <button
          onClick={triggerDetection}
          disabled={detecting || loading}
          className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl"
        >
          {detecting ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Đang phát hiện...
            </>
          ) : (
            <>
              <Activity className="w-5 h-5" />
              Detect Trends
            </>
          )}
        </button>
      </div>

      {/* Progress Bar (when detecting) */}
      {detecting && (
        <div className="bg-white border border-blue-200 rounded-lg p-6 mb-6 shadow-lg">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-medium text-gray-700">{progressMessage}</span>
            <span className="text-sm font-bold text-blue-600">{progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div
              className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-500 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
          {progress === 100 && (
            <div className="mt-3 flex items-center gap-2 text-green-600">
              <CheckCircle className="w-5 h-5" />
              <span className="text-sm font-medium">Hoàn tất!</span>
            </div>
          )}
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4 flex items-center gap-2">
          <AlertCircle className="w-5 h-5" />
          {error}
        </div>
      )}

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
          <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Trends</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total_trends}</p>
              </div>
              <TrendingUp className="w-8 h-8 text-blue-600" />
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Active</p>
                <p className="text-2xl font-bold text-green-600">{stats.active_trends}</p>
              </div>
              <Activity className="w-8 h-8 text-green-600" />
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">High Priority</p>
                <p className="text-2xl font-bold text-orange-600">{stats.high_priority_trends}</p>
              </div>
              <Zap className="w-8 h-8 text-orange-600" />
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Avg Score</p>
                <p className="text-2xl font-bold text-purple-600">{stats.average_viral_score.toFixed(1)}</p>
              </div>
              <ThumbsUp className="w-8 h-8 text-purple-600" />
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Alerts</p>
                <p className="text-2xl font-bold text-red-600">{stats.unread_alerts}</p>
              </div>
              <AlertCircle className="w-8 h-8 text-red-600" />
            </div>
          </div>
        </div>
      )}

      {/* Trends List */}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-lg">
        <div className="px-6 py-4 bg-gradient-to-r from-blue-50 to-purple-50 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            Trending Keywords
          </h2>
        </div>

        {loading && trends.length === 0 ? (
          <div className="text-center py-16">
            <Loader2 className="w-12 h-12 animate-spin mx-auto text-blue-600 mb-4" />
            <p className="text-gray-600 font-medium">Đang tải trends...</p>
            <p className="text-sm text-gray-500 mt-1">Vui lòng đợi...</p>
          </div>
        ) : trends.length === 0 ? (
          <div className="text-center py-16">
            <TrendingUp className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <p className="text-gray-600 font-medium mb-2">Chưa có trends nào được phát hiện</p>
            <p className="text-sm text-gray-500 mb-4">Click "Detect Trends" để bắt đầu quét</p>
            <button
              onClick={triggerDetection}
              disabled={detecting}
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              <Activity className="w-4 h-4" />
              Detect Trends Ngay
            </button>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {trends.map((trend, index) => (
              <div
                key={trend.id}
                className="px-6 py-4 hover:bg-blue-50 transition-colors cursor-pointer group"
                onClick={() => setSelectedTrend(trend)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4 flex-1">
                    {/* Rank */}
                    <div className="flex-shrink-0 w-10 text-center">
                      <span className={`text-2xl font-bold ${
                        index === 0 ? 'text-yellow-500' :
                        index === 1 ? 'text-gray-400' :
                        index === 2 ? 'text-orange-400' :
                        'text-gray-400'
                      }`}>
                        #{index + 1}
                      </span>
                    </div>

                    {/* Keyword */}
                    <div className="flex-1 min-w-0">
                      <h3 className="text-xl font-bold text-gray-900 mb-1">{trend.keyword}</h3>
                      <div className="flex items-center gap-3 flex-wrap">
                        <span className={`text-sm px-3 py-1 rounded-full font-medium ${getStatusBadge(trend.status).color}`}>
                          {getStatusBadge(trend.status).label}
                        </span>
                        <span className={`text-sm px-3 py-1 rounded-full font-medium ${getPriorityBadge(trend.priority).color}`}>
                          {getPriorityBadge(trend.priority).label}
                        </span>
                      </div>
                    </div>

                    {/* Metrics */}
                    <div className="hidden md:flex items-center gap-8 text-sm">
                      <div className="text-center">
                        <p className="font-bold text-lg text-gray-900">{trend.twitter_mentions.toLocaleString()}</p>
                        <p className="text-xs text-gray-500">Mentions</p>
                      </div>
                      <div className="text-center">
                        <p className="font-bold text-lg text-gray-900">{trend.twitter_velocity.toFixed(1)}</p>
                        <p className="text-xs text-gray-500">per min</p>
                      </div>
                    </div>

                    {/* Viral Score */}
                    <div className={`flex-shrink-0 w-28 h-28 rounded-full border-4 ${getScoreBgColor(trend.viral_score)} flex items-center justify-center shadow-lg`}>
                      <div className="text-center">
                        <p className={`text-3xl font-bold ${getScoreColor(trend.viral_score)}`}>
                          {trend.viral_score.toFixed(0)}
                        </p>
                        <p className="text-xs text-gray-600 font-medium">Score</p>
                      </div>
                    </div>

                    {/* AI Content Button */}
                    <div className="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">
                      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-2">
                        <Sparkles className="w-5 h-5" />
                        <span className="font-medium">Tạo Content AI</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Info Box */}
      <div className="mt-6 bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-5 shadow-md">
        <div className="flex items-start gap-3">
          <Sparkles className="w-6 h-6 text-purple-600 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-blue-900 mb-2 text-lg">✨ NEW: AI Content Suggestions</h3>
            <p className="text-sm text-blue-800 leading-relaxed">
              <strong>Click vào bất kỳ trend nào</strong> để AI tự động tạo <strong>5-10 nội dung bài viết</strong> thông minh!
              <br />
              AI sẽ tạo đa dạng định dạng: <strong>Tin tức</strong>, <strong>Meme</strong>, <strong>Hot Take</strong>, <strong>Phân tích</strong>, <strong>Ý kiến fan</strong>, và <strong>Caption ảnh</strong>.
              <br />
              <br />
              💡 <strong>One-click publish</strong> hoặc <strong>lên lịch tự động</strong> vào thời điểm tốt nhất!
            </p>
          </div>
        </div>
      </div>

      {/* Content Suggestions Modal */}
      {selectedTrend && (
        <ContentSuggestionsModalSimple
          trendId={selectedTrend.id}
          trendKeyword={selectedTrend.keyword}
          viralScore={selectedTrend.viral_score}
          onClose={() => setSelectedTrend(null)}
        />
      )}
    </div>
  );
}
