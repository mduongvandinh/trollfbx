import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { Sparkles, Image as ImageIcon, Send, Save, RefreshCw, Newspaper, Wand2, Eye } from 'lucide-react';

interface NewsArticle {
  id: number;
  title: string;
  description: string;
  url: string;
  source: string;
  category: string;
  published_at: string;
  image_url?: string;
}

interface MemeTemplate {
  id: string;
  name: string;
  style: 'top-bottom' | 'quote' | 'comparison';
}

interface CaptionStyle {
  id: string;
  name: string;
  description: string;
  emoji: string;
}

const MEME_TEMPLATES: MemeTemplate[] = [
  { id: 'classic', name: 'Classic Meme (Top/Bottom Text)', style: 'top-bottom' },
  { id: 'quote', name: 'Quote Style', style: 'quote' },
  { id: 'comparison', name: 'Comparison/Drake Style', style: 'comparison' },
];

const CAPTION_STYLES: CaptionStyle[] = [
  { id: 'funny', name: 'Hài hước', description: 'Vui nhộn, troll nhẹ, Gen Z', emoji: '😂' },
  { id: 'sarcastic', name: 'Châm biếm', description: 'Mỉa mai tinh tế, ironic', emoji: '😏' },
  { id: 'dramatic', name: 'Kịch tính', description: 'Phóng đại, hào hứng!!!', emoji: '🔥' },
  { id: 'emotional', name: 'Cảm động', description: 'Nghiêm túc, tôn vinh', emoji: '💙' },
  { id: 'savage', name: 'Thẳng thắn', description: 'Troll mạnh, roast', emoji: '💀' },
];

interface GeneratedImage {
  variant_id: number;
  filename: string;
  url: string;
  style: string;
}

export default function ContentCreator() {
  const location = useLocation();
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [selectedNews, setSelectedNews] = useState<NewsArticle | null>(null);
  const [caption, setCaption] = useState('');
  const [hashtags, setHashtags] = useState<string[]>([]);
  const [generatingCaption, setGeneratingCaption] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<MemeTemplate>(MEME_TEMPLATES[0]);
  const [selectedStyle, setSelectedStyle] = useState<CaptionStyle>(CAPTION_STYLES[0]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showPreview, setShowPreview] = useState(false);
  const [generatedImages, setGeneratedImages] = useState<GeneratedImage[]>([]);
  const [selectedImage, setSelectedImage] = useState<GeneratedImage | null>(null);

  // Meme text inputs
  const [topText, setTopText] = useState('');
  const [bottomText, setBottomText] = useState('');

  // Track if content is from AI (for saving without news_id)
  const [isFromAI, setIsFromAI] = useState(false);
  const [aiContentTitle, setAiContentTitle] = useState<string>('');
  const [aiContentId, setAiContentId] = useState<number | null>(null);
  const [regeneratingImages, setRegeneratingImages] = useState(false);

  useEffect(() => {
    loadNews();
  }, []);

  // Check if we have a pre-selected news from navigation
  useEffect(() => {
    if (location.state?.selectedNews) {
      const preSelectedNews = location.state.selectedNews as NewsArticle;
      setSelectedNews(preSelectedNews);
      // Scroll to the generation section
      setTimeout(() => {
        document.getElementById('generation-section')?.scrollIntoView({ behavior: 'smooth' });
      }, 500);
    }
  }, [location.state]);

  // Check if we have AI-generated content from Content Suggestions
  useEffect(() => {
    if (location.state?.fromAI) {
      const { contentId, title, content, hashtags: aiHashtags, trendKeyword, generatedImages: images } = location.state;

      // Mark as AI-generated content
      setIsFromAI(true);
      setAiContentTitle(title);
      setAiContentId(contentId);

      // Pre-fill caption with title + content
      const fullCaption = `${title}\n\n${content}`;
      setCaption(fullCaption);

      // Pre-fill hashtags
      if (aiHashtags && Array.isArray(aiHashtags)) {
        setHashtags(aiHashtags);
      }

      // Load generated images if available
      if (images && Array.isArray(images) && images.length > 0) {
        setGeneratedImages(images);
        setSelectedImage(images[0]); // Auto-select first image
        setSuccess(`✨ Nội dung từ AI Trend "${trendKeyword}" đã được tải với ${images.length} ảnh!`);
      } else {
        setSuccess(`✨ Nội dung từ AI Trend "${trendKeyword}" đã được tải!`);
      }

      // Scroll to caption section
      setTimeout(() => {
        document.getElementById('caption-section')?.scrollIntoView({ behavior: 'smooth' });
      }, 300);

      // Clear success message after 5 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 5000);
    }
  }, [location.state]);

  const loadNews = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:8000/api/news/latest?limit=20');
      setNews(response.data);
    } catch (err) {
      console.error('Error loading news:', err);
      setError('Không thể tải tin tức');
    } finally {
      setLoading(false);
    }
  };

  const generateCaption = async () => {
    if (!selectedNews) {
      setError('Vui lòng chọn tin tức trước');
      return;
    }

    try {
      setGeneratingCaption(true);
      setError(null);

      const response = await axios.post('http://localhost:8000/api/content/generate-caption', {
        news_id: selectedNews.id,
        news_title: selectedNews.title,
        news_description: selectedNews.description,
        style: selectedStyle.id,
      });

      setCaption(response.data.caption);
      // Set top/bottom text for classic meme
      if (response.data.top_text) setTopText(response.data.top_text);
      if (response.data.bottom_text) setBottomText(response.data.bottom_text);
      // Set hashtags
      if (response.data.hashtags) setHashtags(response.data.hashtags);

      setSuccess(`✨ Caption ${selectedStyle.name} đã được tạo bằng AI!`);
      setTimeout(() => setSuccess(null), 3000);
    } catch (err: any) {
      console.error('Error generating caption:', err);
      setError(err.response?.data?.detail || 'Không thể tạo caption. Kiểm tra Ollama đang chạy.');
    } finally {
      setGeneratingCaption(false);
    }
  };

  const createMeme = async () => {
    if (!selectedNews) {
      setError('Vui lòng chọn tin tức');
      return;
    }

    if (!caption && !topText && !bottomText) {
      setError('Vui lòng nhập caption hoặc tạo caption tự động');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await axios.post('http://localhost:8000/api/content/create-meme', {
        news_id: selectedNews.id,
        caption: caption,
        top_text: topText,
        bottom_text: bottomText,
        template_style: selectedTemplate.style,
        image_url: selectedNews.image_url,
      });

      setSuccess('✅ Meme đã được tạo thành công!');
      setTimeout(() => setSuccess(null), 3000);
    } catch (err: any) {
      console.error('Error creating meme:', err);
      setError(err.response?.data?.detail || 'Không thể tạo meme');
    } finally {
      setLoading(false);
    }
  };

  const saveContent = async () => {
    // Validate: need caption and either news or AI content
    if (!caption || (!selectedNews && !isFromAI)) {
      setError('Vui lòng chọn tin hoặc tạo nội dung AI và tạo caption');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const payload: any = {
        caption: caption,
        top_text: topText,
        bottom_text: bottomText,
        status: 'draft',
      };

      // Add news_id only if content is from news, not AI
      if (selectedNews) {
        payload.news_id = selectedNews.id;
      }

      // Add title if from AI-generated content
      if (isFromAI && aiContentTitle) {
        payload.title = aiContentTitle;
      }

      await axios.post('http://localhost:8000/api/content/save', payload);

      setSuccess('💾 Đã lưu nội dung!');
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      console.error('Error saving content:', err);
      setError('Không thể lưu nội dung');
    } finally {
      setLoading(false);
    }
  };

  const regenerateImages = async () => {
    if (!aiContentId) {
      setError('Không tìm thấy ID nội dung để tạo lại ảnh');
      return;
    }

    try {
      setRegeneratingImages(true);
      setError(null);
      setSuccess('Đang tạo lại 4 ảnh meme mới...');

      const response = await axios.post('http://localhost:8000/api/comfyui/generate', {
        content_id: aiContentId,
        num_variants: 4
      });

      if (response.data.success && response.data.images) {
        setGeneratedImages(response.data.images);
        setSelectedImage(response.data.images[0]); // Auto-select first image
        setSuccess(`Đã tạo lại ${response.data.images.length} ảnh meme mới!`);
        setTimeout(() => setSuccess(null), 3000);
      }
    } catch (err: any) {
      console.error('Error regenerating images:', err);
      setError(err.response?.data?.detail || 'Không thể tạo lại ảnh. Vui lòng kiểm tra ComfyUI.');
    } finally {
      setRegeneratingImages(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Tạo Nội Dung Meme</h1>

      {/* Pre-selected News Notification */}
      {location.state?.selectedNews && (
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-4 mb-4 flex items-center gap-3">
          <Sparkles className="w-5 h-5 text-purple-600" />
          <div className="flex-1">
            <p className="text-purple-900 font-medium">Tin tức đã được chọn sẵn!</p>
            <p className="text-purple-700 text-sm">Bạn có thể bắt đầu tạo nội dung ngay bên dưới.</p>
          </div>
        </div>
      )}

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
        {/* Left Column - News Selection */}
        <div>
          <div className="bg-white rounded-lg border border-gray-200 p-4 mb-4">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Newspaper className="w-5 h-5" />
              Chọn Tin Tức
            </h2>

            {loading && news.length === 0 ? (
              <div className="text-center py-8">
                <RefreshCw className="w-8 h-8 animate-spin mx-auto text-gray-400 mb-2" />
                <p className="text-gray-600">Đang tải tin tức...</p>
              </div>
            ) : (
              <div className="space-y-2 max-h-96 overflow-y-auto">
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
                    <div className="flex gap-3">
                      {article.image_url && (
                        <img
                          src={article.image_url}
                          alt={article.title}
                          className="w-16 h-16 object-cover rounded flex-shrink-0"
                        />
                      )}
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-sm line-clamp-2">{article.title}</h3>
                        <p className="text-xs text-gray-500 mt-1">{article.source}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Selected News Preview */}
          {selectedNews && (
            <div id="generation-section" className="bg-white rounded-lg border border-gray-200 p-4">
              <h3 className="font-semibold mb-2">Tin đã chọn:</h3>
              {selectedNews.image_url && (
                <img
                  src={selectedNews.image_url}
                  alt={selectedNews.title}
                  className="w-full h-48 object-cover rounded-lg mb-3"
                />
              )}
              <h4 className="font-medium mb-2">{selectedNews.title}</h4>
              <p className="text-sm text-gray-600 line-clamp-3">{selectedNews.description}</p>
            </div>
          )}
        </div>

        {/* Right Column - Caption & Meme Creation */}
        <div>
          {/* Caption Style Selector */}
          <div className="bg-white rounded-lg border border-gray-200 p-4 mb-4">
            <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <Wand2 className="w-5 h-5" />
              Chọn Phong Cách
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {CAPTION_STYLES.map((style) => (
                <button
                  key={style.id}
                  onClick={() => setSelectedStyle(style)}
                  className={`p-3 rounded-lg border-2 transition-all text-left ${
                    selectedStyle.id === style.id
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="text-2xl mb-1">{style.emoji}</div>
                  <div className="font-medium text-sm">{style.name}</div>
                  <div className="text-xs text-gray-500">{style.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* AI Caption Generation */}
          <div className="bg-white rounded-lg border border-gray-200 p-4 mb-4">
            <button
              onClick={generateCaption}
              disabled={!selectedNews || generatingCaption}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed mb-4"
            >
              {generatingCaption ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  AI đang tạo {selectedStyle.emoji}...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Tạo Caption "{selectedStyle.name}" với AI
                </>
              )}
            </button>

            <div id="caption-section" className="mb-4">
              <label className="block text-sm font-medium mb-2">Caption cho bài viết:</label>
              <textarea
                value={caption}
                onChange={(e) => setCaption(e.target.value)}
                placeholder="Caption sẽ được AI tạo tự động..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={8}
              />
            </div>

            {/* Hashtags Display */}
            {hashtags.length > 0 && (
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Hashtags tự động:</label>
                <div className="flex flex-wrap gap-2">
                  {hashtags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Generated Images from AI */}
            {generatedImages.length > 0 && (
              <div className="mb-6 p-4 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border-2 border-purple-200">
                <div className="flex items-center justify-between mb-3">
                  <label className="text-sm font-bold text-purple-900 flex items-center gap-2">
                    <Sparkles className="w-5 h-5" />
                    🎨 Ảnh meme AI đã tạo ({generatedImages.length})
                  </label>
                  <button
                    onClick={regenerateImages}
                    disabled={regeneratingImages || !aiContentId}
                    className="flex items-center gap-2 px-3 py-1.5 bg-orange-600 text-white text-sm rounded-lg hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  >
                    <RefreshCw className={`w-4 h-4 ${regeneratingImages ? 'animate-spin' : ''}`} />
                    {regeneratingImages ? 'Đang tạo...' : 'Tạo lại ảnh'}
                  </button>
                </div>
                <div className="grid grid-cols-4 gap-3 mb-3">
                  {generatedImages.map((img) => (
                    <div
                      key={img.variant_id}
                      onClick={() => setSelectedImage(img)}
                      className={`relative cursor-pointer rounded-lg overflow-hidden border-3 transition-all ${
                        selectedImage?.variant_id === img.variant_id
                          ? 'border-blue-500 ring-4 ring-blue-300 scale-105'
                          : 'border-gray-300 hover:border-blue-400'
                      }`}
                    >
                      <img
                        src={`http://localhost:8000${img.url}`}
                        alt={img.style}
                        className="w-full h-32 object-cover"
                      />
                      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-2">
                        <span className="text-white text-xs font-bold">{img.style}</span>
                      </div>
                      {selectedImage?.variant_id === img.variant_id && (
                        <div className="absolute top-2 right-2 bg-blue-500 text-white rounded-full p-1">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
                {selectedImage && (
                  <div className="text-sm text-purple-800 bg-white/60 p-2 rounded">
                    ✅ Đã chọn ảnh: <span className="font-bold">{selectedImage.style}</span>
                    <span className="ml-2 text-gray-600">({selectedImage.filename})</span>
                  </div>
                )}
              </div>
            )}

            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Template Meme:</label>
              <select
                value={selectedTemplate.id}
                onChange={(e) => {
                  const template = MEME_TEMPLATES.find((t) => t.id === e.target.value);
                  if (template) setSelectedTemplate(template);
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {MEME_TEMPLATES.map((template) => (
                  <option key={template.id} value={template.id}>
                    {template.name}
                  </option>
                ))}
              </select>
            </div>

            {selectedTemplate.style === 'top-bottom' && (
              <>
                <div className="mb-4">
                  <label className="block text-sm font-medium mb-2">Text phía trên:</label>
                  <input
                    type="text"
                    value={topText}
                    onChange={(e) => setTopText(e.target.value)}
                    placeholder="TOP TEXT"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-bold uppercase"
                  />
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-medium mb-2">Text phía dưới:</label>
                  <input
                    type="text"
                    value={bottomText}
                    onChange={(e) => setBottomText(e.target.value)}
                    placeholder="BOTTOM TEXT"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-bold uppercase"
                  />
                </div>
              </>
            )}
          </div>

          {/* Meme Preview */}
          {selectedNews?.image_url && (topText || bottomText) && (
            <div className="bg-white rounded-lg border border-gray-200 p-4 mb-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold flex items-center gap-2">
                  <Eye className="w-4 h-4" />
                  Preview Meme
                </h3>
                <button
                  onClick={() => setShowPreview(!showPreview)}
                  className="text-sm text-blue-600 hover:text-blue-700"
                >
                  {showPreview ? 'Ẩn' : 'Hiện'}
                </button>
              </div>
              {showPreview && (
                <div className="relative">
                  <img
                    src={selectedNews.image_url}
                    alt="Meme preview"
                    className="w-full rounded-lg"
                  />
                  {topText && (
                    <div className="absolute top-4 left-0 right-0 text-center">
                      <div className="inline-block px-4 py-2 bg-black bg-opacity-70">
                        <p className="text-white font-bold text-xl uppercase tracking-wide" style={{
                          textShadow: '2px 2px 4px rgba(0,0,0,0.8), -2px -2px 4px rgba(0,0,0,0.8)'
                        }}>
                          {topText}
                        </p>
                      </div>
                    </div>
                  )}
                  {bottomText && (
                    <div className="absolute bottom-4 left-0 right-0 text-center">
                      <div className="inline-block px-4 py-2 bg-black bg-opacity-70">
                        <p className="text-white font-bold text-xl uppercase tracking-wide" style={{
                          textShadow: '2px 2px 4px rgba(0,0,0,0.8), -2px -2px 4px rgba(0,0,0,0.8)'
                        }}>
                          {bottomText}
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Action Buttons */}
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h3 className="font-semibold mb-4">Hành động:</h3>
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={createMeme}
                disabled={loading || !selectedNews}
                className="flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ImageIcon className="w-4 h-4" />
                Tạo Meme
              </button>
              <button
                onClick={saveContent}
                disabled={loading || !caption}
                className="flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Save className="w-4 h-4" />
                Lưu Nháp
              </button>
            </div>

            <button
              disabled={true}
              className="w-full mt-3 flex items-center justify-center gap-2 px-4 py-2 bg-gray-400 text-white rounded-lg cursor-not-allowed"
              title="Cần cấu hình Facebook API"
            >
              <Send className="w-4 h-4" />
              Đăng lên Facebook (Chưa cấu hình)
            </button>

            <p className="text-xs text-gray-500 mt-3 text-center">
              💡 Tip: Thử các phong cách khác nhau để tìm caption hay nhất!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
