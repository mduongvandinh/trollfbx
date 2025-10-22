import { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import {
  X, Sparkles, Copy, Send, Clock, TrendingUp, Heart, Share2,
  MessageCircle, Hash, Image as ImageIcon, Calendar, Loader2,
  CheckCircle, Edit, Trash2, AlertCircle
} from 'lucide-react';

interface ContentSuggestion {
  id: number;
  trend_id: number;
  title: string;
  content: string;
  content_type: string;
  tone: string;
  hashtags: string[];
  suggested_image_keywords: string[];
  viral_prediction_score: number;
  engagement_prediction: number;
  best_time_to_post: string;
  priority: string;
  status: string;
  created_at: string;
}

interface ContentSuggestionsModalProps {
  trendId: number;
  trendKeyword: string;
  viralScore: number;
  onClose: () => void;
}

export default function ContentSuggestionsModal({
  trendId,
  trendKeyword,
  viralScore,
  onClose
}: ContentSuggestionsModalProps) {
  const [suggestions, setSuggestions] = useState<ContentSuggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);

  useEffect(() => {
    loadSuggestions();
  }, [trendId]);

  const loadSuggestions = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:8000/api/content/trend/${trendId}`);

      if (response.data.length === 0) {
        // No suggestions yet, generate them
        await generateContent();
      } else {
        setSuggestions(response.data);
      }
    } catch (err) {
      console.error('Error loading suggestions:', err);
    } finally {
      setLoading(false);
    }
  };

  const generateContent = async () => {
    setGenerating(true);
    const toastId = toast.loading('🎨 Đang tạo content suggestions...');

    try {
      const response = await axios.post('http://localhost:8000/api/content/generate', {
        trend_id: trendId,
        num_suggestions: 8
      });

      setSuggestions(response.data.suggestions);
      toast.success(`✅ Tạo thành công ${response.data.suggestions.length} nội dung!`, {
        id: toastId,
        duration: 3000
      });
    } catch (err: any) {
      console.error('Error generating content:', err);
      toast.error('❌ Không thể tạo content', { id: toastId });
    } finally {
      setGenerating(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success('📋 Đã copy vào clipboard!');
  };

  const publishNow = async (contentId: number) => {
    const toastId = toast.loading('📤 Đang xuất bản...');

    try {
      await axios.post(`http://localhost:8000/api/content/publish/${contentId}`, null, {
        params: { platforms: ['facebook'] }
      });

      toast.success('✅ Xuất bản thành công!', { id: toastId });
      loadSuggestions(); // Reload to update status
    } catch (err) {
      toast.error('❌ Xuất bản thất bại', { id: toastId });
    }
  };

  const scheduleContent = async (contentId: number) => {
    const suggestion = suggestions.find(s => s.id === contentId);
    if (!suggestion) return;

    const toastId = toast.loading('📅 Đang lên lịch...');

    try {
      await axios.post('http://localhost:8000/api/content/schedule', {
        content_id: contentId,
        platform: 'facebook',
        scheduled_time: suggestion.best_time_to_post
      });

      toast.success('✅ Đã lên lịch xuất bản!', { id: toastId });
      loadSuggestions();
    } catch (err) {
      toast.error('❌ Lên lịch thất bại', { id: toastId });
    }
  };

  const getContentTypeInfo = (type: string) => {
    const types: { [key: string]: { label: string; color: string; emoji: string } } = {
      news: { label: 'Tin tức', color: 'bg-blue-100 text-blue-800', emoji: '📰' },
      meme: { label: 'Meme', color: 'bg-pink-100 text-pink-800', emoji: '😂' },
      hot_take: { label: 'Hot Take', color: 'bg-orange-100 text-orange-800', emoji: '🔥' },
      analysis: { label: 'Phân tích', color: 'bg-purple-100 text-purple-800', emoji: '📊' },
      fan_opinion: { label: 'Ý kiến fan', color: 'bg-green-100 text-green-800', emoji: '💬' },
      image_caption: { label: 'Caption ảnh', color: 'bg-yellow-100 text-yellow-800', emoji: '📸' }
    };
    return types[type] || types.news;
  };

  const getPriorityColor = (priority: string) => {
    const colors: { [key: string]: string } = {
      urgent: 'bg-red-500',
      high: 'bg-orange-500',
      normal: 'bg-blue-500',
      low: 'bg-gray-500'
    };
    return colors[priority] || colors.normal;
  };

  if (loading || generating) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg p-8 max-w-md w-full text-center">
          <Loader2 className="w-16 h-16 animate-spin mx-auto text-blue-600 mb-4" />
          <h3 className="text-xl font-bold mb-2">
            {generating ? '🎨 Đang tạo content...' : 'Đang tải...'}
          </h3>
          <p className="text-gray-600">
            {generating
              ? 'AI đang phân tích trend và tạo nội dung thông minh...'
              : 'Vui lòng đợi...'
            }
          </p>
        </div>
      </div>
    );
  }

  if (suggestions.length === 0) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg p-8 max-w-md w-full text-center">
          <AlertCircle className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-xl font-bold mb-2">Chưa có content suggestions</h3>
          <p className="text-gray-600 mb-6">Nhấn nút bên dưới để tạo nội dung</p>
          <button
            onClick={generateContent}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Sparkles className="w-5 h-5 inline mr-2" />
            Tạo Content Ngay
          </button>
          <button
            onClick={onClose}
            className="ml-4 px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
          >
            Đóng
          </button>
        </div>
      </div>
    );
  }

  const currentSuggestion = suggestions[selectedIndex];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-lg max-w-6xl w-full my-8 shadow-2xl">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-t-lg">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
                <Sparkles className="w-6 h-6" />
                AI Content Suggestions
              </h2>
              <p className="text-blue-100 text-sm">
                Trend: <span className="font-bold">{trendKeyword}</span> • Viral Score: {viralScore}/100
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-white/20 p-2 rounded-lg transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Content Type Tabs */}
          <div className="flex gap-2 mt-4 overflow-x-auto pb-2">
            {suggestions.map((suggestion, index) => {
              const typeInfo = getContentTypeInfo(suggestion.content_type);
              return (
                <button
                  key={suggestion.id}
                  onClick={() => setSelectedIndex(index)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all whitespace-nowrap ${
                    selectedIndex === index
                      ? 'bg-white text-blue-600 shadow-lg scale-105'
                      : 'bg-white/20 text-white hover:bg-white/30'
                  }`}
                >
                  <span>{typeInfo.emoji}</span>
                  <span className="font-medium">{typeInfo.label}</span>
                  {selectedIndex === index && (
                    <span className="bg-blue-600 text-white text-xs px-2 py-0.5 rounded-full">
                      {suggestion.viral_prediction_score.toFixed(0)}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Main Content (Left 2/3) */}
            <div className="lg:col-span-2 space-y-4">
              {/* Metrics */}
              <div className="flex items-center gap-4 flex-wrap">
                <div className={`flex items-center gap-2 px-4 py-2 rounded-lg ${getContentTypeInfo(currentSuggestion.content_type).color}`}>
                  <span className="text-2xl">{getContentTypeInfo(currentSuggestion.content_type).emoji}</span>
                  <span className="font-bold">{getContentTypeInfo(currentSuggestion.content_type).label}</span>
                </div>

                <div className={`px-3 py-1 rounded-full text-white text-sm font-medium ${getPriorityColor(currentSuggestion.priority)}`}>
                  {currentSuggestion.priority.toUpperCase()}
                </div>

                <div className="flex items-center gap-1 text-sm">
                  <TrendingUp className="w-4 h-4 text-red-500" />
                  <span className="font-bold text-red-600">{currentSuggestion.viral_prediction_score.toFixed(0)}</span>
                  <span className="text-gray-500">/100</span>
                </div>

                <div className="flex items-center gap-1 text-sm text-purple-600">
                  <Heart className="w-4 h-4" />
                  <span className="font-medium">{currentSuggestion.engagement_prediction.toFixed(1)}%</span>
                </div>
              </div>

              {/* Title */}
              <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-bold text-gray-900 flex-1">{currentSuggestion.title}</h3>
                  <button
                    onClick={() => copyToClipboard(currentSuggestion.title)}
                    className="text-gray-500 hover:text-blue-600 p-1"
                  >
                    <Copy className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Content */}
              <div className="bg-white border-2 border-gray-200 rounded-lg p-6">
                <div className="flex justify-between items-start mb-4">
                  <h4 className="font-semibold text-gray-700">📝 Nội dung:</h4>
                  <button
                    onClick={() => copyToClipboard(currentSuggestion.content)}
                    className="text-gray-500 hover:text-blue-600 flex items-center gap-1 text-sm"
                  >
                    <Copy className="w-4 h-4" />
                    Copy
                  </button>
                </div>
                <div className="text-gray-800 whitespace-pre-wrap leading-relaxed">
                  {currentSuggestion.content}
                </div>
              </div>

              {/* Hashtags */}
              <div className="flex flex-wrap gap-2">
                {currentSuggestion.hashtags.map((tag, i) => (
                  <span
                    key={i}
                    className="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-sm font-medium cursor-pointer hover:bg-blue-100 transition-colors"
                    onClick={() => copyToClipboard(`#${tag}`)}
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </div>

            {/* Sidebar (Right 1/3) */}
            <div className="space-y-4">
              {/* Best Time */}
              <div className="bg-gradient-to-br from-orange-50 to-red-50 border border-orange-200 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Clock className="w-5 h-5 text-orange-600" />
                  <h4 className="font-semibold text-gray-900">Thời gian tốt nhất</h4>
                </div>
                <p className="text-2xl font-bold text-orange-600">
                  {new Date(currentSuggestion.best_time_to_post).toLocaleString('vi-VN', {
                    hour: '2-digit',
                    minute: '2-digit',
                    day: '2-digit',
                    month: '2-digit'
                  })}
                </p>
              </div>

              {/* Actions */}
              <div className="space-y-3">
                <button
                  onClick={() => publishNow(currentSuggestion.id)}
                  disabled={currentSuggestion.status === 'published'}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg hover:from-green-600 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl"
                >
                  <Send className="w-5 h-5" />
                  {currentSuggestion.status === 'published' ? 'Đã xuất bản' : 'Xuất bản ngay'}
                </button>

                <button
                  onClick={() => scheduleContent(currentSuggestion.id)}
                  disabled={currentSuggestion.status === 'scheduled' || currentSuggestion.status === 'published'}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                >
                  <Calendar className="w-5 h-5" />
                  {currentSuggestion.status === 'scheduled' ? 'Đã lên lịch' : 'Lên lịch tự động'}
                </button>

                <button
                  onClick={() => copyToClipboard(`${currentSuggestion.title}\n\n${currentSuggestion.content}\n\n${currentSuggestion.hashtags.map(t => `#${t}`).join(' ')}`)}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                >
                  <Copy className="w-5 h-5" />
                  Copy toàn bộ
                </button>
              </div>

              {/* Image Keywords */}
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <ImageIcon className="w-5 h-5 text-purple-600" />
                  <h4 className="font-semibold text-gray-900">Từ khóa tìm ảnh</h4>
                </div>
                <div className="flex flex-wrap gap-2">
                  {currentSuggestion.suggested_image_keywords.map((keyword, i) => (
                    <span key={i} className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs">
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>

              {/* Stats */}
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Tone:</span>
                  <span className="text-sm font-medium">{currentSuggestion.tone}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Status:</span>
                  <span className="text-sm font-medium capitalize">{currentSuggestion.status}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <div className="flex justify-between items-center mt-6 pt-6 border-t">
            <button
              onClick={() => setSelectedIndex(Math.max(0, selectedIndex - 1))}
              disabled={selectedIndex === 0}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              ← Trước
            </button>

            <span className="text-sm text-gray-600">
              {selectedIndex + 1} / {suggestions.length}
            </span>

            <button
              onClick={() => setSelectedIndex(Math.min(suggestions.length - 1, selectedIndex + 1))}
              disabled={selectedIndex === suggestions.length - 1}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Sau →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
