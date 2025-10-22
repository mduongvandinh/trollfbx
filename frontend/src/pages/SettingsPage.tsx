import { useState, useEffect } from 'react';
import axios from 'axios';
import { Settings, Save, RefreshCw, AlertCircle, CheckCircle, Database, Cpu, Facebook, Rss, Plus, Trash2 } from 'lucide-react';

const API_URL = 'http://localhost:8000';

interface AppSettings {
  ollama_model: string;
  auto_refresh_interval: number;
  manual_mode: boolean;
  facebook_connected: boolean;
  news_sources: string[];
}

export default function SettingsPage() {
  const [settings, setSettings] = useState<AppSettings>({
    ollama_model: 'qwen2.5:7b-instruct-q4_K_M',
    auto_refresh_interval: 30,
    manual_mode: true,
    facebook_connected: false,
    news_sources: []
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const [ollamaModels, setOllamaModels] = useState<string[]>([]);
  const [testingOllama, setTestingOllama] = useState(false);
  const [ollamaStatus, setOllamaStatus] = useState<'unknown' | 'connected' | 'error'>('unknown');

  const [showAddSourceModal, setShowAddSourceModal] = useState(false);
  const [newSourceUrl, setNewSourceUrl] = useState('');
  const [newSourceType, setNewSourceType] = useState<'rss' | 'reddit'>('rss');

  useEffect(() => {
    fetchSettings();
    testOllamaConnection();
  }, []);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/settings`);
      setSettings(response.data);
    } catch (error) {
      console.error('Error fetching settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const testOllamaConnection = async () => {
    try {
      setTestingOllama(true);
      const response = await axios.get('http://localhost:11434/api/tags');

      if (response.data && response.data.models) {
        setOllamaModels(response.data.models.map((m: any) => m.name));
        setOllamaStatus('connected');
      }
    } catch (error) {
      console.error('Error connecting to Ollama:', error);
      setOllamaStatus('error');
    } finally {
      setTestingOllama(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      await axios.put(`${API_URL}/api/settings`, settings);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (error) {
      console.error('Error saving settings:', error);
      alert('Lỗi khi lưu cài đặt');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Đang tải...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <Settings className="w-8 h-8 text-gray-700" />
            Cài Đặt
          </h1>
          <p className="text-gray-600 mt-2">Cấu hình ứng dụng và tích hợp</p>
        </div>

        <button
          onClick={handleSave}
          disabled={saving}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-300 flex items-center gap-2"
        >
          {saved ? (
            <>
              <CheckCircle className="w-5 h-5" />
              Đã lưu
            </>
          ) : (
            <>
              <Save className="w-5 h-5" />
              {saving ? 'Đang lưu...' : 'Lưu cài đặt'}
            </>
          )}
        </button>
      </div>

      {/* Ollama Settings */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Cpu className="w-6 h-6 text-purple-600" />
          <h2 className="text-xl font-semibold">Ollama AI Configuration</h2>
        </div>

        <div className="space-y-4">
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-sm font-medium text-gray-700">Ollama Status</label>
              <button
                onClick={testOllamaConnection}
                disabled={testingOllama}
                className="px-3 py-1 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-1"
              >
                <RefreshCw className={`w-4 h-4 ${testingOllama ? 'animate-spin' : ''}`} />
                Test
              </button>
            </div>

            {ollamaStatus === 'connected' ? (
              <div className="flex items-center gap-2 text-sm text-green-700 bg-green-50 px-3 py-2 rounded">
                <CheckCircle className="w-4 h-4" />
                Đã kết nối với Ollama ({ollamaModels.length} models)
              </div>
            ) : ollamaStatus === 'error' ? (
              <div className="flex items-center gap-2 text-sm text-red-700 bg-red-50 px-3 py-2 rounded">
                <AlertCircle className="w-4 h-4" />
                Không kết nối được Ollama. Chạy: ollama serve
              </div>
            ) : (
              <div className="flex items-center gap-2 text-sm text-gray-700 bg-gray-50 px-3 py-2 rounded">
                <AlertCircle className="w-4 h-4" />
                Chưa kiểm tra
              </div>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Ollama Model</label>
            {ollamaModels.length > 0 ? (
              <select
                value={settings.ollama_model}
                onChange={(e) => setSettings({ ...settings, ollama_model: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {ollamaModels.map(model => (
                  <option key={model} value={model}>{model}</option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                value={settings.ollama_model}
                onChange={(e) => setSettings({ ...settings, ollama_model: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="qwen2.5:7b-instruct-q4_K_M"
              />
            )}
            <p className="text-xs text-gray-500 mt-1">
              Model được sử dụng để tạo caption và nội dung
            </p>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              <strong>Ollama Base URL:</strong> http://localhost:11434<br />
              Để thay đổi, cập nhật file .env trong backend
            </p>
          </div>
        </div>
      </div>

      {/* News Settings */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Rss className="w-6 h-6 text-orange-600" />
          <h2 className="text-xl font-semibold">News & Content Settings</h2>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Auto-refresh Interval (phút)
            </label>
            <input
              type="number"
              min="5"
              max="180"
              value={settings.auto_refresh_interval}
              onChange={(e) => setSettings({ ...settings, auto_refresh_interval: parseInt(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <p className="text-xs text-gray-500 mt-1">
              Tần suất tự động lấy tin tức mới (5-180 phút)
            </p>
          </div>

          <div className="border border-gray-200 rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-gray-700">News Sources ({settings.news_sources.length})</h3>
              <button
                onClick={() => setShowAddSourceModal(true)}
                className="px-3 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors flex items-center gap-1"
              >
                <Plus className="w-3 h-3" />
                Thêm nguồn
              </button>
            </div>

            {settings.news_sources.length === 0 ? (
              <div className="text-center py-6 bg-gray-50 rounded">
                <Rss className="w-8 h-8 text-gray-300 mx-auto mb-2" />
                <p className="text-sm text-gray-500">Chưa có nguồn tin nào</p>
                <button
                  onClick={() => setShowAddSourceModal(true)}
                  className="mt-2 text-xs text-blue-600 hover:text-blue-700"
                >
                  Thêm nguồn tin đầu tiên
                </button>
              </div>
            ) : (
              <ul className="space-y-2">
                {settings.news_sources.map((source, index) => (
                  <li key={index} className="flex items-center gap-3 bg-gray-50 px-3 py-2 rounded hover:bg-gray-100 transition-colors">
                    <Rss className="w-4 h-4 text-orange-500 flex-shrink-0" />
                    <span className="text-sm text-gray-700 flex-1 truncate font-mono text-xs">{source}</span>
                    <button
                      onClick={() => {
                        if (confirm('Xóa nguồn tin này?')) {
                          const newSources = settings.news_sources.filter((_, i) => i !== index);
                          setSettings({ ...settings, news_sources: newSources });
                        }
                      }}
                      className="ml-2 text-red-600 hover:text-red-700 transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </li>
                ))}
              </ul>
            )}

            <div className="mt-3 bg-blue-50 border border-blue-200 rounded p-3">
              <p className="text-xs text-blue-800">
                <strong>Hỗ trợ:</strong> RSS feeds (XML), Reddit subreddit URLs<br />
                <strong>Ví dụ RSS:</strong> https://www.skysports.com/rss/12040<br />
                <strong>Ví dụ Reddit:</strong> https://www.reddit.com/r/soccer
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Facebook Settings */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Facebook className="w-6 h-6 text-blue-600" />
          <h2 className="text-xl font-semibold">Facebook Integration</h2>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="font-medium text-gray-900">Manual Mode</div>
              <div className="text-sm text-gray-600">Đăng bài thủ công thay vì tự động theo lịch</div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.manual_mode}
                onChange={(e) => setSettings({ ...settings, manual_mode: e.target.checked })}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-sm text-yellow-800">
              <strong>Facebook API Configuration:</strong><br />
              1. Tạo Facebook App tại developers.facebook.com<br />
              2. Lấy Page Access Token<br />
              3. Thêm vào backend/.env: FACEBOOK_PAGE_ACCESS_TOKEN=your_token<br />
              4. Khởi động lại backend
            </p>
          </div>
        </div>
      </div>

      {/* Database Info */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Database className="w-6 h-6 text-gray-600" />
          <h2 className="text-xl font-semibold">Database Information</h2>
        </div>

        <div className="space-y-4">
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-gray-700 mb-2">Database Location</h3>
            <p className="text-sm text-gray-600 font-mono">
              backend/database/football_meme.db
            </p>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              <strong>Lưu ý:</strong> Database tự động lưu tất cả dữ liệu.
              Để backup, copy file football_meme.db sang vị trí an toàn.
            </p>
          </div>
        </div>
      </div>

      {/* System Info */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold mb-4">System Information</h2>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <div className="text-gray-600">Backend URL</div>
            <div className="font-mono text-gray-900">{API_URL}</div>
          </div>

          <div>
            <div className="text-gray-600">Ollama URL</div>
            <div className="font-mono text-gray-900">http://localhost:11434</div>
          </div>

          <div>
            <div className="text-gray-600">Database Type</div>
            <div className="font-mono text-gray-900">SQLite</div>
          </div>

          <div>
            <div className="text-gray-600">Mode</div>
            <div className="font-mono text-gray-900">{settings.manual_mode ? 'Manual' : 'Auto'}</div>
          </div>
        </div>
      </div>

      {/* Save Button (Bottom) */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          disabled={saving}
          className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-300 flex items-center gap-2 font-semibold"
        >
          {saved ? (
            <>
              <CheckCircle className="w-5 h-5" />
              Đã lưu thành công
            </>
          ) : (
            <>
              <Save className="w-5 h-5" />
              {saving ? 'Đang lưu...' : 'Lưu tất cả cài đặt'}
            </>
          )}
        </button>
      </div>

      {/* Add News Source Modal */}
      {showAddSourceModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-lg w-full p-6">
            <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Rss className="w-6 h-6 text-orange-600" />
              Thêm Nguồn Tin Mới
            </h3>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Loại nguồn tin</label>
                <div className="flex gap-3">
                  <button
                    onClick={() => setNewSourceType('rss')}
                    className={`flex-1 px-4 py-3 rounded-lg border-2 transition-all ${
                      newSourceType === 'rss'
                        ? 'border-blue-500 bg-blue-50 text-blue-700'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="font-semibold">RSS Feed</div>
                    <div className="text-xs text-gray-600 mt-1">Sky Sports, BBC, Guardian...</div>
                  </button>
                  <button
                    onClick={() => setNewSourceType('reddit')}
                    className={`flex-1 px-4 py-3 rounded-lg border-2 transition-all ${
                      newSourceType === 'reddit'
                        ? 'border-blue-500 bg-blue-50 text-blue-700'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="font-semibold">Reddit</div>
                    <div className="text-xs text-gray-600 mt-1">r/soccer, r/football...</div>
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">URL nguồn tin</label>
                <input
                  type="url"
                  value={newSourceUrl}
                  onChange={(e) => setNewSourceUrl(e.target.value)}
                  placeholder={
                    newSourceType === 'rss'
                      ? 'https://www.skysports.com/rss/12040'
                      : 'https://www.reddit.com/r/soccer'
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
                <p className="text-xs text-gray-700">
                  <strong>Gợi ý nguồn tin RSS:</strong><br />
                  • Sky Sports: https://www.skysports.com/rss/12040<br />
                  • The Guardian: https://www.theguardian.com/football/rss<br />
                  • BBC Sport: https://www.bbc.co.uk/sport/football/rss.xml<br />
                  <br />
                  <strong>Reddit:</strong><br />
                  • r/soccer: https://www.reddit.com/r/soccer<br />
                  • r/football: https://www.reddit.com/r/football
                </p>
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => {
                    setShowAddSourceModal(false);
                    setNewSourceUrl('');
                    setNewSourceType('rss');
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Hủy
                </button>
                <button
                  onClick={() => {
                    if (newSourceUrl.trim()) {
                      setSettings({ ...settings, news_sources: [...settings.news_sources, newSourceUrl.trim()] });
                      setShowAddSourceModal(false);
                      setNewSourceUrl('');
                      setNewSourceType('rss');
                    } else {
                      alert('Vui lòng nhập URL nguồn tin');
                    }
                  }}
                  className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                >
                  Thêm nguồn
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
