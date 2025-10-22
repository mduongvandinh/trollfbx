import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Newspaper, RefreshCw, Clock, Tag, Settings, Grid, List, LayoutList, ExternalLink, Sparkles, Globe, Flag } from 'lucide-react';

interface NewsArticle {
  id: number;
  title: string;
  description: string;
  url: string;
  source: string;
  category: string;
  published_at: string;
  image_url?: string;
  created_at: string;
  content_category?: string;  // vietnamese | international | mixed | general
  vn_angle?: string;
  hashtags?: string;
}

type ViewMode = 'list' | 'grid' | 'compact';
type LanguageFilter = 'all' | 'vietnamese' | 'international';

export default function NewsPage() {
  const navigate = useNavigate();
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>('all');
  const [languageFilter, setLanguageFilter] = useState<LanguageFilter>('all');

  // View mode settings
  const [viewMode, setViewMode] = useState<ViewMode>(() => {
    const saved = localStorage.getItem('newsViewMode');
    return (saved as ViewMode) || 'list';
  });

  // Auto-refresh settings
  const [autoRefreshEnabled, setAutoRefreshEnabled] = useState(() => {
    const saved = localStorage.getItem('autoRefreshEnabled');
    return saved ? JSON.parse(saved) : false;
  });
  const [refreshInterval, setRefreshInterval] = useState(() => {
    const saved = localStorage.getItem('refreshInterval');
    return saved ? parseInt(saved) : 60;
  });
  const [showSettings, setShowSettings] = useState(false);
  const [nextRefreshIn, setNextRefreshIn] = useState<number>(0);

  useEffect(() => {
    loadNews();
  }, []);

  useEffect(() => {
    if (!autoRefreshEnabled) {
      setNextRefreshIn(0);
      return;
    }

    setNextRefreshIn(refreshInterval * 60);
    fetchNews();

    const fetchIntervalId = setInterval(() => {
      fetchNews();
      setNextRefreshIn(refreshInterval * 60);
    }, refreshInterval * 60 * 1000);

    const countdownId = setInterval(() => {
      setNextRefreshIn((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);

    return () => {
      clearInterval(fetchIntervalId);
      clearInterval(countdownId);
    };
  }, [autoRefreshEnabled, refreshInterval]);

  useEffect(() => {
    localStorage.setItem('autoRefreshEnabled', JSON.stringify(autoRefreshEnabled));
    localStorage.setItem('refreshInterval', refreshInterval.toString());
  }, [autoRefreshEnabled, refreshInterval]);

  useEffect(() => {
    localStorage.setItem('newsViewMode', viewMode);
  }, [viewMode]);

  const loadNews = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get('http://localhost:8000/api/news/latest?limit=50');
      setNews(response.data);
    } catch (err: any) {
      console.error('Error loading news:', err);
      setError('Không thể tải tin tức. Vui lòng thử lại.');
    } finally {
      setLoading(false);
    }
  };

  const fetchNews = async () => {
    try {
      setLoading(true);
      setError(null);
      await axios.post('http://localhost:8000/api/news/fetch');
      const response = await axios.get('http://localhost:8000/api/news/latest?limit=50');
      setNews(response.data);
    } catch (err: any) {
      console.error('Error fetching news:', err);
      setError('Không thể lấy tin mới. Vui lòng kiểm tra kết nối internet.');
    } finally {
      setLoading(false);
    }
  };

  const getCategoryBadgeColor = (category: string) => {
    const colors: { [key: string]: string } = {
      transfer: 'bg-blue-100 text-blue-800',
      match_result: 'bg-green-100 text-green-800',
      injury: 'bg-red-100 text-red-800',
      drama: 'bg-purple-100 text-purple-800',
      other: 'bg-gray-100 text-gray-800',
    };
    return colors[category] || colors.other;
  };

  const getCategoryLabel = (category: string) => {
    const labels: { [key: string]: string } = {
      transfer: 'Chuyển nhượng',
      match_result: 'Kết quả',
      injury: 'Chấn thương',
      drama: 'Drama',
      other: 'Khác',
    };
    return labels[category] || category;
  };

  // Helper function to check if source is Vietnamese
  const isVietnameseSource = (source: string) => {
    const vietnameseSources = [
      'Bóng đá',
      'thethao247',
      'vnexpress',
      'bongda24h',
      'VnExpress',
      'Thể Thao 247'
    ];
    return vietnameseSources.some(vn => source.toLowerCase().includes(vn.toLowerCase()));
  };

  const getSourceBadge = (source: string) => {
    const isVN = isVietnameseSource(source);

    if (isVN) {
      return {
        label: '🇻🇳 Nguồn VN',
        color: 'bg-red-100 text-red-700 border border-red-200',
        icon: Flag
      };
    } else {
      return {
        label: '🌍 Quốc tế',
        color: 'bg-blue-100 text-blue-700 border border-blue-200',
        icon: Globe
      };
    }
  };

  // Apply both category and source filters
  const filteredNews = news.filter(article => {
    // Category filter
    const categoryMatch = filter === 'all' || article.category === filter;

    // Source filter (Vietnamese vs International)
    let sourceMatch = true;
    if (languageFilter === 'vietnamese') {
      // Only show Vietnamese sources
      sourceMatch = isVietnameseSource(article.source);
    } else if (languageFilter === 'international') {
      // Only show International sources
      sourceMatch = !isVietnameseSource(article.source);
    }

    return categoryMatch && sourceMatch;
  });

  // Get source stats
  const languageStats = {
    vietnamese: news.filter(a => isVietnameseSource(a.source)).length,
    international: news.filter(a => !isVietnameseSource(a.source)).length,
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('vi-VN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatCountdown = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  // Render news based on view mode
  const handleCreateContent = (article: NewsArticle) => {
    // Navigate to content creator with pre-selected news
    navigate('/create', {
      state: {
        selectedNews: {
          id: article.id,
          title: article.title,
          description: article.description,
          image_url: article.image_url,
          url: article.url,
          source: article.source,
          vn_angle: article.vn_angle,
        }
      }
    });
  };

  const renderNewsItem = (article: NewsArticle) => {
    const sourceBadge = getSourceBadge(article.source);

    if (viewMode === 'grid') {
      // Grid View - Card layout with large image
      return (
        <div key={article.id} className="bg-white border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
          {article.image_url && (
            <img
              src={article.image_url}
              alt={article.title}
              className="w-full h-48 object-cover"
            />
          )}
          <div className="p-4">
            <div className="flex gap-2 mb-2 flex-wrap">
              <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${getCategoryBadgeColor(article.category)}`}>
                {getCategoryLabel(article.category)}
              </span>
              <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${sourceBadge.color}`}>
                {sourceBadge.label}
              </span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
              {article.title}
            </h3>
            <p className="text-gray-600 text-sm mb-3 line-clamp-3">
              {article.description}
            </p>
            {article.vn_angle && (
              <div className="bg-blue-50 border-l-4 border-blue-400 p-2 mb-3">
                <p className="text-xs text-blue-800 italic line-clamp-2">
                  💬 {article.vn_angle}
                </p>
              </div>
            )}
            <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
              <span className="flex items-center gap-1">
                <Newspaper className="w-3 h-3" />
                {article.source}
              </span>
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {formatDate(article.published_at)}
              </span>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => handleCreateContent(article)}
                className="flex-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-3 py-2 rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all text-sm font-medium flex items-center justify-center gap-1"
              >
                <Sparkles className="w-4 h-4" />
                Tạo Nội Dung
              </button>
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-1 text-sm"
                title="Xem bài gốc"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>
      );
    } else if (viewMode === 'compact') {
      // Compact View - Minimal with small thumbnail
      return (
        <div key={article.id} className="bg-white border-b border-gray-200 p-3 hover:bg-gray-50">
          <div className="flex gap-3">
            {article.image_url && (
              <img
                src={article.image_url}
                alt={article.title}
                className="w-20 h-20 object-cover rounded flex-shrink-0"
              />
            )}
            <div className="flex-1 min-w-0">
              <div className="flex items-start gap-2 mb-1">
                <h3 className="text-sm font-semibold text-gray-900 flex-1 line-clamp-2">
                  {article.title}
                </h3>
                <div className="flex gap-1 flex-shrink-0">
                  <span className={`px-1.5 py-0.5 rounded text-xs font-medium ${getCategoryBadgeColor(article.category)}`}>
                    {getCategoryLabel(article.category)}
                  </span>
                  <span className={`px-1.5 py-0.5 rounded text-xs font-medium ${sourceBadge.color}`}>
                    {sourceBadge.label.split(' ')[0]}
                  </span>
                </div>
              </div>
              {article.vn_angle && (
                <p className="text-xs text-blue-600 italic mb-1 line-clamp-1">
                  💬 {article.vn_angle}
                </p>
              )}
              <div className="flex items-center gap-2 text-xs text-gray-500 mb-2">
                <span>{article.source}</span>
                <span>•</span>
                <span>{formatDate(article.published_at)}</span>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => handleCreateContent(article)}
                  className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-3 py-1 rounded text-xs font-medium flex items-center gap-1 hover:from-purple-600 hover:to-pink-600 transition-all"
                >
                  <Sparkles className="w-3 h-3" />
                  Tạo Nội Dung
                </button>
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-700 flex items-center gap-1 text-xs"
                >
                  Xem <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          </div>
        </div>
      );
    } else {
      // List View - Default with medium image
      return (
        <div key={article.id} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
          <div className="flex gap-4">
            {article.image_url && (
              <img
                src={article.image_url}
                alt={article.title}
                className="w-40 h-40 object-cover rounded-lg flex-shrink-0"
              />
            )}
            <div className="flex-1">
              <div className="flex items-start justify-between gap-2 mb-2">
                <h3 className="text-lg font-semibold text-gray-900 flex-1">
                  {article.title}
                </h3>
                <div className="flex gap-2 flex-shrink-0">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${getCategoryBadgeColor(article.category)}`}>
                    <Tag className="w-3 h-3 inline mr-1" />
                    {getCategoryLabel(article.category)}
                  </span>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${sourceBadge.color}`}>
                    {sourceBadge.label}
                  </span>
                </div>
              </div>
              <p className="text-gray-600 mb-3 line-clamp-2">
                {article.description}
              </p>
              {article.vn_angle && (
                <div className="bg-blue-50 border-l-4 border-blue-400 p-3 mb-3">
                  <p className="text-sm text-blue-800 italic">
                    💬 <strong>Góc nhìn VN:</strong> {article.vn_angle}
                  </p>
                </div>
              )}
              <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
                <span className="flex items-center gap-1">
                  <Newspaper className="w-4 h-4" />
                  {article.source}
                </span>
                <span className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  {formatDate(article.published_at)}
                </span>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => handleCreateContent(article)}
                  className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all text-sm font-medium flex items-center gap-2"
                >
                  <Sparkles className="w-4 h-4" />
                  Tạo Nội Dung
                </button>
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium flex items-center gap-1"
                >
                  Xem chi tiết <ExternalLink className="w-4 h-4" />
                </a>
              </div>
            </div>
          </div>
        </div>
      );
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Tin Tức Bóng Đá</h1>
        <div className="flex items-center gap-3">
          {autoRefreshEnabled && nextRefreshIn > 0 && (
            <div className="text-sm text-gray-600 flex items-center gap-2">
              <Clock className="w-4 h-4" />
              Tự động lấy tin sau: {formatCountdown(nextRefreshIn)}
            </div>
          )}

          {/* View Mode Buttons */}
          <div className="flex items-center gap-1 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded ${viewMode === 'list' ? 'bg-white shadow' : 'hover:bg-gray-200'}`}
              title="Xem dạng danh sách"
            >
              <List className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded ${viewMode === 'grid' ? 'bg-white shadow' : 'hover:bg-gray-200'}`}
              title="Xem dạng lưới"
            >
              <Grid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('compact')}
              className={`p-2 rounded ${viewMode === 'compact' ? 'bg-white shadow' : 'hover:bg-gray-200'}`}
              title="Xem dạng thu gọn"
            >
              <LayoutList className="w-4 h-4" />
            </button>
          </div>

          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
            title="Cài đặt tự động làm mới"
          >
            <Settings className="w-5 h-5" />
          </button>
          <button
            onClick={fetchNews}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            {loading ? 'Đang tải...' : 'Lấy tin mới'}
          </button>
        </div>
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold mb-4">Cài đặt tự động làm mới</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={autoRefreshEnabled}
                  onChange={(e) => setAutoRefreshEnabled(e.target.checked)}
                  className="w-4 h-4 text-blue-600 rounded"
                />
                <span className="text-sm font-medium">Bật tự động lấy tin</span>
              </label>
            </div>
            {autoRefreshEnabled && (
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Khoảng thời gian (phút):
                </label>
                <select
                  value={refreshInterval}
                  onChange={(e) => setRefreshInterval(parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value={5}>5 phút</option>
                  <option value={10}>10 phút</option>
                  <option value={15}>15 phút</option>
                  <option value={30}>30 phút</option>
                  <option value={60}>60 phút (1 giờ)</option>
                  <option value={120}>120 phút (2 giờ)</option>
                  <option value={180}>180 phút (3 giờ)</option>
                </select>
                <p className="text-xs text-gray-500 mt-1">
                  Tin tức sẽ được tự động lấy mỗi {refreshInterval} phút
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          {error}
        </div>
      )}

      {/* Source Filter - Filter by Vietnamese vs International sources */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4 mb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Globe className="w-5 h-5 text-blue-600" />
            <h3 className="font-semibold text-gray-900">Lọc theo nguồn tin</h3>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setLanguageFilter('all')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                languageFilter === 'all'
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
              }`}
            >
              🌐 Tất cả nguồn ({news.length})
            </button>
            <button
              onClick={() => setLanguageFilter('vietnamese')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                languageFilter === 'vietnamese'
                  ? 'bg-red-600 text-white shadow-md'
                  : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
              }`}
            >
              🇻🇳 Nguồn Việt Nam ({languageStats.vietnamese})
            </button>
            <button
              onClick={() => setLanguageFilter('international')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                languageFilter === 'international'
                  ? 'bg-blue-600 text-white shadow-md'
                  : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
              }`}
            >
              🌍 Nguồn Quốc Tế ({languageStats.international})
            </button>
          </div>
        </div>
      </div>

      {/* Category filters */}
      <div className="flex gap-2 mb-6 flex-wrap">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg ${
            filter === 'all'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Tất cả
        </button>
        <button
          onClick={() => setFilter('transfer')}
          className={`px-4 py-2 rounded-lg ${
            filter === 'transfer'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Chuyển nhượng
        </button>
        <button
          onClick={() => setFilter('match_result')}
          className={`px-4 py-2 rounded-lg ${
            filter === 'match_result'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Kết quả
        </button>
        <button
          onClick={() => setFilter('injury')}
          className={`px-4 py-2 rounded-lg ${
            filter === 'injury'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Chấn thương
        </button>
        <button
          onClick={() => setFilter('drama')}
          className={`px-4 py-2 rounded-lg ${
            filter === 'drama'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Drama
        </button>
      </div>

      {/* News list */}
      {loading && news.length === 0 ? (
        <div className="text-center py-12">
          <RefreshCw className="w-12 h-12 animate-spin mx-auto text-gray-400 mb-4" />
          <p className="text-gray-600">Đang tải tin tức...</p>
        </div>
      ) : filteredNews.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <Newspaper className="w-12 h-12 mx-auto text-gray-400 mb-4" />
          <p className="text-gray-600 mb-2">Chưa có tin tức nào</p>
          <p className="text-sm text-gray-500">Click "Lấy tin mới" để tải tin tức từ các nguồn</p>
        </div>
      ) : (
        <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' : viewMode === 'compact' ? 'bg-white rounded-lg border border-gray-200 overflow-hidden' : 'grid gap-4'}>
          {filteredNews.map(renderNewsItem)}
        </div>
      )}

      {/* Stats */}
      {news.length > 0 && (
        <div className="mt-6 text-center text-sm text-gray-500">
          Hiển thị {filteredNews.length} / {news.length} tin tức
        </div>
      )}
    </div>
  );
}
