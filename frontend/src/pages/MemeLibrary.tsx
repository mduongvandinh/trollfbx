import { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { Upload, Sparkles, Copy, Search, RefreshCw, Loader2 } from 'lucide-react';

interface MemeTemplate {
  id: number;
  title: string;
  category: string;
  image_url: string;
  analysis: any;
  times_used: number;
  created_at: string;
}

interface CategoryInfo {
  category: string;
  count: number;
}

export default function MemeLibrary() {
  const [templates, setTemplates] = useState<MemeTemplate[]>([]);
  const [categories, setCategories] = useState<CategoryInfo[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<MemeTemplate | null>(null);
  const [loading, setLoading] = useState(true);

  // Upload form state
  const [showUploadForm, setShowUploadForm] = useState(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadPreview, setUploadPreview] = useState<string | null>(null);
  const [caption, setCaption] = useState('');
  const [context, setContext] = useState('');
  const [uploading, setUploading] = useState(false);

  // Variation generator state
  const [playerName, setPlayerName] = useState('');
  const [varContext, setVarContext] = useState('');
  const [numVariations, setNumVariations] = useState(10);
  const [variations, setVariations] = useState<string[]>([]);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    loadTemplates();
    loadCategories();
  }, [selectedCategory]);

  const loadTemplates = async () => {
    try {
      setLoading(true);
      const params = selectedCategory ? { category: selectedCategory } : {};
      const response = await axios.get('http://localhost:8000/api/meme/templates', { params });
      setTemplates(response.data);
    } catch (err) {
      console.error('Error loading templates:', err);
      toast.error('Không thể tải meme templates');
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/meme/categories');
      setCategories(response.data.categories || []);
    } catch (err) {
      console.error('Error loading categories:', err);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setUploadFile(file);
      const reader = new FileReader();
      reader.onloadend = () => setUploadPreview(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile || !caption) {
      toast.error('Vui lòng chọn ảnh và nhập caption!');
      return;
    }

    const formData = new FormData();
    formData.append('file', uploadFile);
    formData.append('caption', caption);
    if (context) formData.append('context', context);

    try {
      setUploading(true);
      const response = await axios.post('http://localhost:8000/api/meme/upload', formData);
      toast.success(`✅ Upload thành công! Template ID: ${response.data.template_id}`);

      // Reset form
      setShowUploadForm(false);
      setUploadFile(null);
      setUploadPreview(null);
      setCaption('');
      setContext('');

      // Reload templates
      loadTemplates();
      loadCategories();
    } catch (err: any) {
      console.error('Upload error:', err);
      toast.error(err.response?.data?.detail || 'Upload thất bại!');
    } finally {
      setUploading(false);
    }
  };

  const handleGenerateVariations = async () => {
    if (!selectedTemplate) return;

    try {
      setGenerating(true);
      const response = await axios.post(
        `http://localhost:8000/api/meme/generate-variations/${selectedTemplate.id}`,
        {
          player_name: playerName || undefined,
          context: varContext || undefined,
          num_variations: numVariations
        }
      );
      setVariations(response.data.variations);
      toast.success(`✅ Đã tạo ${response.data.variations.length} variations!`);
    } catch (err: any) {
      console.error('Generate error:', err);
      toast.error(err.response?.data?.detail || 'Tạo variations thất bại!');
    } finally {
      setGenerating(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success('📋 Đã copy!');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">🎨 Meme Library</h1>
              <p className="text-gray-600 mt-1">Upload ảnh meme để AI học và tạo variations</p>
            </div>
            <button
              onClick={() => setShowUploadForm(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <Upload className="w-5 h-5" />
              Upload Meme
            </button>
          </div>

          {/* Category Filter */}
          <div className="mt-4 flex items-center gap-2 overflow-x-auto pb-2">
            <button
              onClick={() => setSelectedCategory(null)}
              className={`px-4 py-2 rounded-full whitespace-nowrap transition ${
                !selectedCategory ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Tất cả ({templates.length})
            </button>
            {categories.map((cat) => (
              <button
                key={cat.category}
                onClick={() => setSelectedCategory(cat.category)}
                className={`px-4 py-2 rounded-full whitespace-nowrap transition ${
                  selectedCategory === cat.category ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {cat.category} ({cat.count})
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        {loading ? (
          <div className="text-center py-12">
            <Loader2 className="w-12 h-12 animate-spin mx-auto text-blue-600" />
            <p className="mt-4 text-gray-600">Đang tải...</p>
          </div>
        ) : templates.length === 0 ? (
          <div className="text-center py-12">
            <Upload className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">Chưa có meme templates</h3>
            <p className="text-gray-600 mb-4">Upload ảnh meme đầu tiên để bắt đầu!</p>
            <button
              onClick={() => setShowUploadForm(true)}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Upload Meme Ngay
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {templates.map((template) => (
              <div
                key={template.id}
                className="bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer"
                onClick={() => setSelectedTemplate(template)}
              >
                <img
                  src={`http://localhost:8000${template.image_url}`}
                  alt={template.title}
                  className="w-full h-48 object-cover rounded-t-lg"
                />
                <div className="p-4">
                  <h3 className="font-semibold text-gray-900 mb-1 line-clamp-2">{template.title}</h3>
                  <div className="flex items-center justify-between text-sm text-gray-600">
                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">{template.category}</span>
                    <span>Đã dùng: {template.times_used}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Upload Modal */}
      {showUploadForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between p-6 border-b">
              <h2 className="text-2xl font-bold">Upload Meme</h2>
              <button onClick={() => setShowUploadForm(false)} className="text-gray-500 hover:text-gray-700">
                ✕
              </button>
            </div>

            <form onSubmit={handleUpload} className="p-6 space-y-4">
              {/* File Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Ảnh Meme</label>
                {uploadPreview ? (
                  <div className="relative">
                    <img src={uploadPreview} alt="Preview" className="w-full rounded-lg" />
                    <button
                      type="button"
                      onClick={() => { setUploadFile(null); setUploadPreview(null); }}
                      className="absolute top-2 right-2 p-2 bg-red-600 text-white rounded-full hover:bg-red-700"
                    >
                      ✕
                    </button>
                  </div>
                ) : (
                  <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50">
                    <Upload className="w-12 h-12 text-gray-400 mb-2" />
                    <span className="text-sm text-gray-600">Click để chọn ảnh</span>
                    <input type="file" accept="image/*" onChange={handleFileChange} className="hidden" />
                  </label>
                )}
              </div>

              {/* Caption */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Caption Meme *</label>
                <textarea
                  value={caption}
                  onChange={(e) => setCaption(e.target.value)}
                  placeholder='Ví dụ: Elanga: "It was my childhood dream to play for Adidas."'
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  rows={3}
                  required
                />
              </div>

              {/* Context */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Context (Optional)</label>
                <input
                  type="text"
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                  placeholder="Ví dụ: Nottingham Forest, sponsor troll"
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              {/* Submit */}
              <button
                type="submit"
                disabled={uploading || !uploadFile || !caption}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
              >
                {uploading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Upload className="w-5 h-5" />}
                {uploading ? 'Đang upload...' : 'Upload & Analyze'}
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Variation Generator Modal */}
      {selectedTemplate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between p-6 border-b">
              <h2 className="text-2xl font-bold">Generate Variations</h2>
              <button onClick={() => setSelectedTemplate(null)} className="text-gray-500 hover:text-gray-700">
                ✕
              </button>
            </div>

            <div className="p-6">
              {/* Template Info */}
              <div className="mb-6">
                <img
                  src={`http://localhost:8000${selectedTemplate.image_url}`}
                  alt={selectedTemplate.title}
                  className="w-full max-h-64 object-contain rounded-lg mb-4"
                />
                <h3 className="font-semibold text-lg mb-2">{selectedTemplate.title}</h3>
                <p className="text-sm text-gray-600 bg-gray-100 p-3 rounded">
                  Template type: <strong>{selectedTemplate.analysis?.template_type || 'unknown'}</strong>
                </p>
              </div>

              {/* Generate Form */}
              <div className="space-y-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Player Name</label>
                  <input
                    type="text"
                    value={playerName}
                    onChange={(e) => setPlayerName(e.target.value)}
                    placeholder="Ví dụ: Maguire, Sancho, Antony..."
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Context</label>
                  <input
                    type="text"
                    value={varContext}
                    onChange={(e) => setVarContext(e.target.value)}
                    placeholder="Ví dụ: Man United poor form, transfer saga..."
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Số lượng variations: {numVariations}
                  </label>
                  <input
                    type="range"
                    min="5"
                    max="30"
                    value={numVariations}
                    onChange={(e) => setNumVariations(parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>

                <button
                  onClick={handleGenerateVariations}
                  disabled={generating}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400"
                >
                  {generating ? <Loader2 className="w-5 h-5 animate-spin" /> : <Sparkles className="w-5 h-5" />}
                  {generating ? 'Đang tạo...' : 'Generate Variations'}
                </button>
              </div>

              {/* Variations List */}
              {variations.length > 0 && (
                <div>
                  <h4 className="font-semibold mb-3">📝 {variations.length} Variations:</h4>
                  <div className="space-y-2 max-h-96 overflow-y-auto">
                    {variations.map((variation, idx) => (
                      <div
                        key={idx}
                        className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100"
                      >
                        <span className="text-sm font-semibold text-gray-500 mt-1">{idx + 1}.</span>
                        <p className="flex-1 text-sm">{variation}</p>
                        <button
                          onClick={() => copyToClipboard(variation)}
                          className="text-blue-600 hover:text-blue-700"
                        >
                          <Copy className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
