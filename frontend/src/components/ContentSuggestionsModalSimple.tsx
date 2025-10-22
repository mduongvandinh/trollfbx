import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';
import { X, Loader2, Save, Edit, Copy, FileText, Image as ImageIcon, Sparkles } from 'lucide-react';

interface ContentSuggestion {
  id: number;
  trend_id: number;
  title: string;
  content: string;
  content_type: string;
  viral_prediction_score: number;
  hashtags: string[];
  status: string;
  generated_images?: ImageVariant[];  // Images from database
}

interface ImageVariant {
  variant_id: number;
  filename: string;
  url: string;
  style: string;
}

interface StyleInfo {
  id: string;
  name: string;
  emoji: string;
  description: string;
  preview_color?: string;
}

interface Props {
  trendId: number;
  trendKeyword: string;
  viralScore: number;
  onClose: () => void;
}

export default function ContentSuggestionsModalSimple({
  trendId,
  trendKeyword,
  viralScore,
  onClose
}: Props) {
  const navigate = useNavigate();
  const [suggestions, setSuggestions] = useState<ContentSuggestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [generatingImages, setGeneratingImages] = useState<{[key: number]: boolean}>({});
  const [generatedImages, setGeneratedImages] = useState<{[key: number]: ImageVariant[]}>({});
  const [availableStyles, setAvailableStyles] = useState<StyleInfo[]>([]);
  const [selectedStyles, setSelectedStyles] = useState<string[]>([]);
  const [showStyleSelector, setShowStyleSelector] = useState(false);

  useEffect(() => {
    generateContent();
    loadStyles();
  }, [trendId]);

  // Load existing images from API response
  useEffect(() => {
    const existingImages: {[key: number]: ImageVariant[]} = {};
    suggestions.forEach(suggestion => {
      if (suggestion.generated_images && suggestion.generated_images.length > 0) {
        existingImages[suggestion.id] = suggestion.generated_images;
      }
    });
    if (Object.keys(existingImages).length > 0) {
      setGeneratedImages(prev => ({ ...prev, ...existingImages }));
    }
  }, [suggestions]);

  const loadStyles = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/comfyui/styles');
      setAvailableStyles(response.data);
      // Default: select first 4 styles
      const defaultStyles = response.data.slice(0, 4).map((s: StyleInfo) => s.id);
      setSelectedStyles(defaultStyles);
    } catch (err) {
      console.error('Error loading styles:', err);
    }
  };

  const toggleStyle = (styleId: string) => {
    setSelectedStyles(prev => {
      if (prev.includes(styleId)) {
        // Remove if already selected
        return prev.filter(s => s !== styleId);
      } else {
        // Add if not selected
        return [...prev, styleId];
      }
    });
  };

  const generateContent = async () => {
    setLoading(true);
    const toastId = toast.loading('Đang tạo content...');

    try {
      const response = await axios.post('http://localhost:8000/api/content/generate', {
        trend_id: trendId,
        num_suggestions: 5
      });

      setSuggestions(response.data.suggestions);
      toast.success(`Tạo thành công ${response.data.suggestions.length} nội dung!`, {
        id: toastId
      });
    } catch (err: any) {
      console.error('Error:', err);
      toast.error('Không thể tạo content', { id: toastId });
    } finally {
      setLoading(false);
    }
  };

  const saveDraft = async (contentId: number) => {
    const toastId = toast.loading('💾 Đang lưu draft...');

    try {
      // Update status to "approved" (ready for manual publishing later)
      await axios.post(`http://localhost:8000/api/content/approve/${contentId}`);

      // Update status locally
      setSuggestions(prev => prev.map(s =>
        s.id === contentId ? { ...s, status: 'approved' } : s
      ));

      toast.success('✅ Đã lưu draft! Có thể post lên Facebook sau.', {
        id: toastId,
        duration: 3000
      });
    } catch (err) {
      toast.error('❌ Lưu draft thất bại', { id: toastId });
    }
  };

  const navigateToEdit = (suggestion: ContentSuggestion) => {
    // Navigate to content creator page with pre-filled data + generated images
    const images = generatedImages[suggestion.id] || [];

    navigate('/create', {
      state: {
        contentId: suggestion.id,
        title: suggestion.title,
        content: suggestion.content,
        hashtags: suggestion.hashtags,
        fromAI: true,
        trendKeyword: trendKeyword,
        generatedImages: images  // Pass generated images
      }
    });
    onClose(); // Close modal
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success('📋 Đã copy!');
  };

  const generateImages = async (contentId: number) => {
    if (selectedStyles.length === 0) {
      toast.error('Vui lòng chọn ít nhất 1 style!');
      return;
    }

    const toastId = toast.loading('🎨 Đang tạo ảnh meme...');
    setGeneratingImages(prev => ({ ...prev, [contentId]: true }));

    try {
      const response = await axios.post('http://localhost:8000/api/comfyui/generate', {
        content_id: contentId,
        num_variants: selectedStyles.length,
        selected_styles: selectedStyles
      });

      setGeneratedImages(prev => ({
        ...prev,
        [contentId]: response.data.images
      }));

      toast.success(`✅ Đã tạo ${response.data.images.length} ảnh meme!`, {
        id: toastId,
        duration: 4000
      });
    } catch (err: any) {
      console.error('Error generating images:', err);
      const errorMsg = err.response?.data?.detail || 'Không thể tạo ảnh';
      toast.error(`❌ ${errorMsg}`, { id: toastId });
    } finally {
      setGeneratingImages(prev => ({ ...prev, [contentId]: false }));
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-blue-600 text-white p-6 rounded-t-lg flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold">AI Content Suggestions</h2>
            <p className="text-sm">Trend: {trendKeyword} • Score: {viralScore}/100</p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-white/20 p-2 rounded-lg"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Style Selector */}
        <div className="px-6 pt-4 pb-2 bg-gray-50 border-b">
          <button
            onClick={() => setShowStyleSelector(!showStyleSelector)}
            className="flex items-center gap-2 text-sm font-medium text-gray-700 hover:text-gray-900"
          >
            <Sparkles className="w-4 h-4" />
            Chọn Style Ảnh ({selectedStyles.length} đã chọn)
            <span className={`transition-transform ${showStyleSelector ? 'rotate-180' : ''}`}>▼</span>
          </button>

          {showStyleSelector && (
            <div className="mt-3 grid grid-cols-4 gap-3 pb-3">
              {availableStyles.map((style) => (
                <button
                  key={style.id}
                  onClick={() => toggleStyle(style.id)}
                  className={`relative rounded-lg border-2 transition-all overflow-hidden ${
                    selectedStyles.includes(style.id)
                      ? 'border-blue-500 ring-2 ring-blue-200'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  {/* Preview with gradient background */}
                  <div
                    className="h-24 flex items-center justify-center"
                    style={{
                      background: style.preview_color
                        ? `linear-gradient(135deg, ${style.preview_color}40, ${style.preview_color})`
                        : 'linear-gradient(135deg, #f0f0f0, #e0e0e0)'
                    }}
                  >
                    <span className="text-5xl drop-shadow-lg">{style.emoji}</span>
                  </div>

                  {/* Style info */}
                  <div className="p-2 bg-white">
                    <div className="font-medium text-sm text-gray-900 mb-1">{style.name}</div>
                    <p className="text-xs text-gray-600 line-clamp-2">{style.description}</p>
                  </div>

                  {/* Selected checkmark */}
                  {selectedStyles.includes(style.id) && (
                    <div className="absolute top-2 right-2 bg-blue-500 text-white rounded-full w-6 h-6 flex items-center justify-center">
                      <span className="text-xs">✓</span>
                    </div>
                  )}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-6">
          {loading ? (
            <div className="text-center py-12">
              <Loader2 className="w-12 h-12 animate-spin mx-auto text-blue-600 mb-4" />
              <p className="text-gray-600">Đang tạo content...</p>
            </div>
          ) : suggestions.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600">Không có suggestions</p>
            </div>
          ) : (
            <div className="space-y-4">
              {suggestions.map((suggestion, index) => (
                <div key={suggestion.id} className="border-2 rounded-lg p-5 hover:border-blue-300 transition-colors">
                  <>
                      <div className="flex justify-between items-start mb-3">
                        <h3 className="text-lg font-bold flex-1 pr-4">{suggestion.title}</h3>
                        <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                          {suggestion.content_type}
                        </span>
                      </div>

                      <p className="text-gray-700 whitespace-pre-wrap mb-4 leading-relaxed">
                        {suggestion.content}
                      </p>

                      {/* Hashtags */}
                      {suggestion.hashtags && suggestion.hashtags.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-4">
                          {suggestion.hashtags.slice(0, 5).map((tag, i) => (
                            <span
                              key={i}
                              className="text-xs px-2 py-1 bg-blue-50 text-blue-600 rounded-full cursor-pointer hover:bg-blue-100"
                              onClick={() => copyToClipboard(`#${tag}`)}
                            >
                              #{tag}
                            </span>
                          ))}
                        </div>
                      )}

                      {/* Generated Images */}
                      {generatedImages[suggestion.id] && generatedImages[suggestion.id].length > 0 && (
                        <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                          <p className="text-sm font-medium text-gray-700 mb-2">🎨 Ảnh meme đã tạo:</p>
                          <div className="grid grid-cols-4 gap-2">
                            {generatedImages[suggestion.id].map((img) => (
                              <div key={img.variant_id} className="relative group">
                                <img
                                  src={`http://localhost:8000${img.url}`}
                                  alt={img.style}
                                  className="w-full h-32 object-cover rounded border-2 border-gray-200 hover:border-blue-400 cursor-pointer transition-all"
                                  onClick={() => window.open(`http://localhost:8000${img.url}`, '_blank')}
                                />
                                <span className="absolute bottom-1 left-1 bg-black/70 text-white text-xs px-2 py-0.5 rounded">
                                  {img.style}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      <div className="flex items-center justify-between pt-3 border-t">
                        <div className="flex items-center gap-4 text-sm">
                          <span className="font-medium text-red-600">
                            🔥 Viral: {suggestion.viral_prediction_score.toFixed(0)}/100
                          </span>
                          {suggestion.status === 'approved' && (
                            <span className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded-full">
                              ✅ Đã lưu Draft
                            </span>
                          )}
                        </div>

                        <div className="flex gap-2">
                          {/* Show "Tạo Ảnh" if no images, "Tạo lại" if images exist */}
                          <button
                            onClick={() => generateImages(suggestion.id)}
                            disabled={generatingImages[suggestion.id]}
                            className={`px-3 py-1.5 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1 text-sm font-medium ${
                              generatedImages[suggestion.id]?.length > 0
                                ? 'bg-orange-600 hover:bg-orange-700'
                                : 'bg-purple-600 hover:bg-purple-700'
                            }`}
                            title={generatedImages[suggestion.id]?.length > 0 ? 'Tạo lại ảnh meme mới' : 'Tạo ảnh meme với AI'}
                          >
                            {generatingImages[suggestion.id] ? (
                              <Loader2 className="w-4 h-4 animate-spin" />
                            ) : (
                              <Sparkles className="w-4 h-4" />
                            )}
                            {generatingImages[suggestion.id]
                              ? 'Đang tạo...'
                              : generatedImages[suggestion.id]?.length > 0
                                ? 'Tạo lại'
                                : 'Tạo Ảnh'
                            }
                          </button>

                          <button
                            onClick={() => copyToClipboard(`${suggestion.title}\n\n${suggestion.content}`)}
                            className="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 flex items-center gap-1 text-sm"
                            title="Copy toàn bộ"
                          >
                            <Copy className="w-4 h-4" />
                            Copy
                          </button>

                          <button
                            onClick={() => navigateToEdit(suggestion)}
                            className="px-3 py-1.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-1 text-sm font-medium"
                            title="Chỉnh sửa với đầy đủ công cụ"
                          >
                            <Edit className="w-4 h-4" />
                            Chỉnh sửa
                          </button>

                          <button
                            onClick={() => saveDraft(suggestion.id)}
                            disabled={suggestion.status === 'approved'}
                            className="px-4 py-1.5 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg hover:from-green-600 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1 text-sm font-medium shadow-md"
                            title="Lưu draft để post Facebook sau"
                          >
                            <Save className="w-4 h-4" />
                            {suggestion.status === 'approved' ? 'Đã lưu' : 'Lưu Draft'}
                          </button>
                        </div>
                      </div>
                    </>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
