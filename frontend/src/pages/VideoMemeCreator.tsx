import { useState, useEffect } from 'react';
import axios from 'axios';
import { Video, Play, Sparkles, Users, MessageSquare, Settings, Film, Download, RefreshCw } from 'lucide-react';

const API_URL = 'http://localhost:8000';

interface Template {
  id: string;
  name: string;
  description: string;
  duration: number;
  characters: number | string;
  difficulty: string;
}

interface Expression {
  id: string;
  name: string;
  emoji: string;
}

interface Pose {
  id: string;
  name: string;
}

interface NewsArticle {
  id: number;
  title: string;
  description: string;
  source: string;
  image_url?: string;
}

export default function VideoMemeCreator() {
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [selectedNews, setSelectedNews] = useState<NewsArticle | null>(null);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [expressions, setExpressions] = useState<Expression[]>([]);
  const [poses, setPoses] = useState<Pose[]>([]);
  const [teams, setTeams] = useState<string[]>([]);

  // Simple mode
  const [team1, setTeam1] = useState('');
  const [team2, setTeam2] = useState('');
  const [score, setScore] = useState('');

  // Advanced mode
  const [advancedMode, setAdvancedMode] = useState(false);

  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    loadNews();
    loadTemplates();
    loadCharacterOptions();
  }, []);

  const loadNews = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/news/latest?limit=20`);
      setNews(response.data);
    } catch (err) {
      console.error('Error loading news:', err);
    }
  };

  const loadTemplates = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/video-meme/templates`);
      setTemplates(response.data.templates);
      if (response.data.templates.length > 0) {
        setSelectedTemplate(response.data.templates[0]);
      }
    } catch (err) {
      console.error('Error loading templates:', err);
    }
  };

  const loadCharacterOptions = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/video-meme/characters`);
      setExpressions(response.data.expressions);
      setPoses(response.data.poses);
      setTeams(response.data.teams);
    } catch (err) {
      console.error('Error loading character options:', err);
    }
  };

  const createSimpleVideoMeme = async () => {
    if (!selectedNews || !team1 || !team2 || !score) {
      setError('Vui lòng điền đầy đủ thông tin');
      return;
    }

    try {
      setGenerating(true);
      setError(null);

      const response = await axios.post(`${API_URL}/api/video-meme/create-simple`, {
        news_id: selectedNews.id,
        team1: team1,
        team2: team2,
        score: score,
        template: selectedTemplate?.id || 'match_result'
      });

      setSuccess(response.data.message);
      setTimeout(() => setSuccess(null), 5000);
    } catch (err: any) {
      console.error('Error creating video meme:', err);
      setError(err.response?.data?.detail || 'Không thể tạo video meme');
    } finally {
      setGenerating(false);
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-700';
      case 'medium': return 'bg-yellow-100 text-yellow-700';
      case 'advanced': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getDifficultyLabel = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'Dễ';
      case 'medium': return 'Trung bình';
      case 'advanced': return 'Nâng cao';
      default: return difficulty;
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Tạo Video Meme Bóng Đá</h1>
        <p className="text-gray-600">Tạo video meme hoạt hình phong cách 442oons với AI</p>
      </div>

      {/* Feature Info Banner */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-6 mb-6">
        <div className="flex items-start gap-4">
          <Film className="w-8 h-8 text-purple-600 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-lg font-semibold text-purple-900 mb-2">
              🎬 Tính năng Video Meme AI - Phong cách 442oons
            </h3>
            <div className="text-sm text-purple-800 space-y-2">
              <p>• <strong>Nhân vật hoạt hình 3D</strong>: Tạo caricature cầu thủ với phong cách chibi, đầu to, thân nhỏ</p>
              <p>• <strong>Animation tự động</strong>: Sử dụng ComfyUI + AnimateDiff để tạo animation mượt mà</p>
              <p>• <strong>Voice-over AI</strong>: Tạo giọng nói tự động cho nhân vật</p>
              <p>• <strong>Templates có sẵn</strong>: Chọn từ nhiều mẫu có sẵn hoặc tự tạo</p>
            </div>
            <div className="mt-4 bg-white bg-opacity-50 rounded p-3">
              <p className="text-xs text-purple-700">
                <strong>⚙️ Yêu cầu:</strong> ComfyUI cần được cài đặt và chạy tại http://127.0.0.1:8188
                <br />
                <strong>📦 Models cần thiết:</strong> Stable Diffusion, AnimateDiff, ControlNet
              </p>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-4">
          {success}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column - News & Templates */}
        <div className="space-y-6">
          {/* News Selection */}
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Video className="w-5 h-5" />
              Chọn Tin Tức
            </h2>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {news.map((article) => (
                <div
                  key={article.id}
                  onClick={() => setSelectedNews(article)}
                  className={`p-3 rounded-lg border-2 cursor-pointer transition-all ${
                    selectedNews?.id === article.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <h3 className="font-medium text-sm line-clamp-2">{article.title}</h3>
                  <p className="text-xs text-gray-500 mt-1">{article.source}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Template Selection */}
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Film className="w-5 h-5" />
              Chọn Template
            </h2>
            <div className="space-y-2">
              {templates.map((template) => (
                <div
                  key={template.id}
                  onClick={() => setSelectedTemplate(template)}
                  className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                    selectedTemplate?.id === template.id
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-sm">{template.name}</h3>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${getDifficultyColor(template.difficulty)}`}>
                      {getDifficultyLabel(template.difficulty)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 mb-2">{template.description}</p>
                  <div className="flex items-center gap-3 text-xs text-gray-500">
                    <span className="flex items-center gap-1">
                      <Users className="w-3 h-3" />
                      {template.characters} nhân vật
                    </span>
                    {template.duration && (
                      <span>⏱️ {template.duration}s</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column - Configuration */}
        <div className="space-y-6">
          {/* Mode Toggle */}
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Chế độ tạo</h2>
              <button
                onClick={() => setAdvancedMode(!advancedMode)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  advancedMode
                    ? 'bg-purple-500 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {advancedMode ? '🔧 Nâng cao' : '⚡ Đơn giản'}
              </button>
            </div>

            {!advancedMode ? (
              /* Simple Mode */
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Đội 1:</label>
                  <select
                    value={team1}
                    onChange={(e) => setTeam1(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Chọn đội...</option>
                    {teams.map((team) => (
                      <option key={team} value={team}>{team}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Đội 2:</label>
                  <select
                    value={team2}
                    onChange={(e) => setTeam2(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Chọn đội...</option>
                    {teams.map((team) => (
                      <option key={team} value={team}>{team}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Tỷ số:</label>
                  <input
                    type="text"
                    value={score}
                    onChange={(e) => setScore(e.target.value)}
                    placeholder="Ví dụ: 3-1"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">Nhập tỷ số theo định dạng: 3-1, 2-0, v.v.</p>
                </div>
              </div>
            ) : (
              /* Advanced Mode */
              <div className="space-y-4">
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <p className="text-sm text-yellow-800">
                    🚧 Chế độ nâng cao đang trong quá trình phát triển.
                    <br />
                    Sẽ cho phép tùy chỉnh nhân vật, dialogue, và animation chi tiết.
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Preview Section */}
          {selectedNews && (
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <h3 className="font-semibold mb-3">Preview Tin Tức:</h3>
              {selectedNews.image_url && (
                <img
                  src={selectedNews.image_url}
                  alt={selectedNews.title}
                  className="w-full h-32 object-cover rounded-lg mb-3"
                />
              )}
              <h4 className="font-medium text-sm mb-2">{selectedNews.title}</h4>
              <p className="text-xs text-gray-600 line-clamp-3">{selectedNews.description}</p>
            </div>
          )}

          {/* Create Button */}
          <button
            onClick={createSimpleVideoMeme}
            disabled={generating || !selectedNews || !team1 || !team2 || !score}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-4 rounded-lg hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold text-lg flex items-center justify-center gap-3 shadow-lg"
          >
            {generating ? (
              <>
                <RefreshCw className="w-6 h-6 animate-spin" />
                Đang tạo video...
              </>
            ) : (
              <>
                <Sparkles className="w-6 h-6" />
                Tạo Video Meme
              </>
            )}
          </button>

          <p className="text-xs text-gray-500 text-center">
            ⚠️ Video meme sẽ mất 3-5 phút để tạo. Bạn có thể tiếp tục làm việc khác trong lúc chờ.
          </p>
        </div>
      </div>

      {/* Info Section */}
      <div className="mt-8 bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold mb-4">💡 Hướng dẫn sử dụng</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700">
          <div>
            <h4 className="font-semibold mb-2">1. Chuẩn bị ComfyUI</h4>
            <ul className="list-disc list-inside space-y-1 text-xs">
              <li>Cài đặt ComfyUI từ GitHub</li>
              <li>Download models: Stable Diffusion, AnimateDiff</li>
              <li>Chạy ComfyUI tại port 8188</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-2">2. Tạo Video Meme</h4>
            <ul className="list-disc list-inside space-y-1 text-xs">
              <li>Chọn tin tức làm chủ đề</li>
              <li>Chọn template phù hợp</li>
              <li>Điền thông tin đội bóng và tỷ số</li>
              <li>Click "Tạo Video Meme" và chờ kết quả</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
